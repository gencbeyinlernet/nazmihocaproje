"""Create an attributed faith-reflection video from the supplied aspirin text.
Photorealistic fictional stills + camera motion, local synthetic Turkish narration.
No real actors, generative character motion, or chemical experiment is claimed.
"""
import json,re,math,hashlib,subprocess,tempfile,wave,textwrap,argparse
from pathlib import Path
from piper import PiperVoice,SynthesisConfig
p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--atlas',required=True);a=p.parse_args()
R=Path(__file__).resolve().parents[1];OUT=R/'video-ornekleri/aspirin';AUD=R/'assets/audio/aspirin';OUT.mkdir(exist_ok=True);AUD.mkdir(exist_ok=True)
raw=(OUT/'ozgun-metin.txt').read_text();rawhash=hashlib.sha256(raw.encode()).hexdigest();normalized=raw
for broken,joined in {'bu-lunduğu':'bulunduğu','geçiyorsu-nuz':'geçiyorsunuz','me-toduydu':'metoduydu','nesil-ler':'nesiller','tesadü-fen':'tesadüfen','muhake-mesini':'muhakemesini','“in-sanın':'“insanın','çalışma-larının':'çalışmalarının','ol-maktaysa':'olmaktaysa'}.items():normalized=normalized.replace(broken,joined)
lines=normalized.splitlines();parts=[('Anlatıcı','Bir aspirinle başlayan soru',lines[0],0,False),('Anlatıcı','Laboratuvarda bir düşünce deneyi',lines[1],0,False),('Öğretmen','Öğretmenin varsayımı',lines[2].removeprefix('- ').removesuffix(' der.').replace('“','').replace('”',''),1,True),('Öğrenciler','Öğrencilerin itirazı',lines[4].removeprefix('- '),3,False),('Anlatıcı','Araştırma, gözlem ve deney',lines[5],2,False),('Öğretmen','Soru sormak ve sorgulamak',lines[7].removeprefix('- '),3,False),('Anlatıcı','Metnin tartıştığı iddia',lines[8],0,False),('Anlatıcı','Bilim insanlarının emeği',lines[9],2,False),('Anlatıcı','Yaratılış üzerine bir soru',lines[10],3,False)]
voice=PiperVoice.load(a.model);font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';timeline=[];caps=[];cursor=0
subprocess.run(['ffmpeg','-v','error','-y','-i',a.atlas,'-c:v','libwebp','-quality','85',str(OUT/'sahne-gorselleri.webp')],check=True)
with tempfile.TemporaryDirectory(prefix='aspirin-film-') as td:
 td=Path(td);pieces=[]
 for i,(speaker,title,text,panel,hypothetical) in enumerate(parts,1):
  sid=f'aspirin-{i:02}';mp3=AUD/(sid+'.mp3');wav=td/(sid+'.wav')
  speak=text.replace('vb.','ve benzeri').replace('Tabikî','Tabii ki')
  with wave.open(str(wav),'wb') as f:voice.synthesize_wav(speak,f,SynthesisConfig(length_scale=1.04 if speaker=='Öğrenciler' else 1.08,noise_scale=.4,noise_w_scale=.5))
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-af','highpass=f=70,loudnorm=I=-18:TP=-2:LRA=7,adelay=140,apad=pad_dur=0.25,asetpts=N/SR/TB','-ar','24000','-ac','1','-c:a','libmp3lame','-b:a','80k',str(mp3)],check=True)
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(mp3)]));length=math.ceil((duration+(.8 if '?' in text else .6))*30)/30
  # Atlas 1672x941; each panel is shown alone, with a tiny inset to avoid seams.
  x=2+(836 if panel%2 else 0);y=2+(470 if panel>1 else 0);w=832;h=467 if panel>1 else 466
  label=td/f'label-{i}.txt';label.write_text(speaker+' · '+title);tag=td/'hypothesis.txt';tag.write_text('DÜŞÜNCE DENEYİ · Öğretmenin varsayımı')
  vf=f"[0:v]crop={w}:{h}:{x}:{y},scale=2304:1296:force_original_aspect_ratio=increase,crop=2304:1296,zoompan=z='1.015+on*0.00005':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,setsar=1,fade=t=in:d=0.18,fade=t=out:st={length-.18}:d=0.18,drawbox=x=0:y=ih-104:w=iw:h=104:color=0x082f32@0.9:t=fill,drawtext=fontfile={font}:textfile={label}:fontcolor=white:fontsize=31:x=48:y=h-72"
  if hypothetical:vf+=f",drawbox=x=28:y=26:w=1000:h=70:color=0x082f32@0.9:t=fill,drawtext=fontfile={font}:textfile={tag}:fontcolor=white:fontsize=30:x=48:y=44"
  vf+='[frame];[2:v]scale=96:96[logo];[frame][logo]overlay=W-w-36:30,format=yuv420p[v]'
  piece=td/(sid+'.mp4');subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-loop','1','-framerate','30','-i',str(OUT/'sahne-gorselleri.webp'),'-i',str(mp3),'-i',str(R/'logo.jpg'),'-filter_complex_threads','1','-filter_complex',vf,'-map','[v]','-map','1:a','-af',f'apad,atrim=duration={length}','-t',str(length),'-c:v','libx264','-preset','veryfast','-crf','24','-maxrate','650k','-bufsize','1300k','-threads','2','-c:a','aac','-b:a','96k','-ar','48000','-ac','1',str(piece)],check=True);pieces.append(piece)
  # Caption chunks follow full sentences so users can optionally read at a comfortable size.
  sentences=re.split(r'(?<=[.!?])\s+',text);weights=[len(s) for s in sentences];elapsed=cursor
  for sentence,weight in zip(sentences,weights):
   end=elapsed+duration*weight/max(1,sum(weights));caps.append((elapsed,end,speaker+': '+sentence));elapsed=end
  timeline.append({'id':sid,'speaker':speaker,'text':text,'spokenText':speak,'start':round(cursor,3),'end':round(cursor+length,3),'audioDuration':round(duration,3),'panel':panel,'hypothetical':hypothetical,'audio':mp3.relative_to(R).as_posix(),'audioSha256':hashlib.sha256(mp3.read_bytes()).hexdigest()});cursor+=length;print(f'{i}/9 rendered; {cursor:.1f}s',flush=True)
 def stamp(t,comma=False):
  ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02}'+(',' if comma else '.')+f'{ms:03}'
 (OUT/'altyazi.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(stamp(s)+' --> '+stamp(e)+'\n'+'\n'.join(textwrap.wrap(t,80)) for s,e,t in caps)+'\n')
 (OUT/'altyazi.srt').write_text('\n\n'.join(str(i+1)+'\n'+stamp(s,True)+' --> '+stamp(e,True)+'\n'+'\n'.join(textwrap.wrap(t,80)) for i,(s,e,t) in enumerate(caps))+'\n')
 listing=td/'concat.txt';listing.write_text(''.join(f"file '{f}'\n" for f in pieces));dest=OUT/'aspirin-dusunce-deneyi.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(OUT/'altyazi.srt'),'-map','0:v','-map','0:a','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language=tur','-metadata','title=Aspirin: Bir Düşünce Deneyi','-movflags','+faststart',str(dest)],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-ss','2','-i',str(dest),'-frames:v','1',str(OUT/'kapak.jpg')],check=True)
 (OUT/'kurgu.json').write_text(json.dumps({'title':'Aspirin: Bir Düşünce Deneyi','method':'photorealistic-fictional-stills-with-editorial-camera-motion','realHumanFootage':False,'engine':'Piper TTS 1.8.0 / tr_TR-fettah-medium','sourceSha256':rawhash,'duration':round(cursor,3),'scenes':timeline},ensure_ascii=False,indent=2)+'\n');print('READY',round(cursor,2),'seconds',dest.stat().st_size/1024**2,'MiB',flush=True)
