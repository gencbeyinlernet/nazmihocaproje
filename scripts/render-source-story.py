"""Render a source-preserving, explicitly adapted voiced reflection video."""
import argparse,json,hashlib,subprocess,tempfile,wave,math,re,textwrap
from pathlib import Path
from piper import PiperVoice,SynthesisConfig
p=argparse.ArgumentParser();p.add_argument('story');p.add_argument('--model',required=True);p.add_argument('--atlas',required=True);a=p.parse_args();R=Path(__file__).resolve().parents[1];O=R/'video-ornekleri'/a.story;plan=json.loads((O/'senaryo.json').read_text());AUD=R/'assets/audio'/a.story;AUD.mkdir(exist_ok=True);font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
subprocess.run(['ffmpeg','-v','error','-y','-i',a.atlas,'-c:v','libwebp','-quality','85',str(O/'sahne-gorselleri.webp')],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',a.atlas]));W=probe['streams'][0]['width'];H=probe['streams'][0]['height'];voice=PiperVoice.load(a.model);caps=[];timeline=[];cursor=0
with tempfile.TemporaryDirectory(prefix=a.story+'-') as td:
 td=Path(td);pieces=[]
 for i,scene in enumerate(plan['scenes'],1):
  sid=scene['id'];text=scene['text'];speaker=scene['speaker'];mp3=AUD/(sid+'.mp3');wav=td/(sid+'.wav')
  with wave.open(str(wav),'wb') as out:voice.synthesize_wav(text,out,SynthesisConfig(length_scale=1.04 if speaker=='Öğrenci' else 1.09,noise_scale=.4,noise_w_scale=.5))
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-af','highpass=f=70,loudnorm=I=-18:TP=-2:LRA=7,adelay=140,apad=pad_dur=0.25,asetpts=N/SR/TB','-ar','24000','-ac','1','-c:a','libmp3lame','-b:a','80k',str(mp3)],check=True)
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(mp3)]));length=math.ceil((duration+(.8 if '?' in text else .6))*30)/30
  panel=scene['panel'];x=(W//2 if panel%2 else 0)+6;y=(H//2 if panel>1 else 0)+6;w=W//2-12;h=H//2-12
  label=td/f'label{i}.txt';label.write_text(speaker+' · '+scene['title']);badge=td/f'badge{i}.txt';badge.write_text(scene['badge'])
  vf=f"[0:v]crop={w}:{h}:{x}:{y},scale=2304:1296:force_original_aspect_ratio=increase,crop=2304:1296,zoompan=z='1.015+on*0.00005':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,setsar=1,fade=t=in:d=0.18,fade=t=out:st={length-.18}:d=0.18,drawbox=x=0:y=ih-104:w=iw:h=104:color=0x082f32@0.9:t=fill,drawtext=fontfile={font}:textfile={label}:fontcolor=white:fontsize=31:x=48:y=h-72,drawbox=x=26:y=26:w=1150:h=66:color=0x082f32@0.88:t=fill,drawtext=fontfile={font}:textfile={badge}:fontcolor=white:fontsize=28:x=46:y=43[frame];[2:v]scale=96:96[logo];[frame][logo]overlay=W-w-36:30,format=yuv420p[v]"
  piece=td/(sid+'.mp4');subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-loop','1','-framerate','30','-i',str(O/'sahne-gorselleri.webp'),'-i',str(mp3),'-i',str(R/'logo.jpg'),'-filter_complex_threads','1','-filter_complex',vf,'-map','[v]','-map','1:a','-af',f'apad,atrim=duration={length}','-t',str(length),'-c:v','libx264','-preset','veryfast','-crf','25','-maxrate','600k','-bufsize','1200k','-threads','1','-c:a','aac','-b:a','96k','-ar','48000','-ac','1',str(piece)],check=True);pieces.append(piece)
  sentences=re.split(r'(?<=[.!?])\s+',text);total=sum(map(len,sentences));elapsed=cursor
  for sentence in sentences:
   end=elapsed+duration*len(sentence)/total;caps.append((elapsed,end,speaker+': '+sentence));elapsed=end
  timeline.append({**scene,'start':round(cursor,3),'end':round(cursor+length,3),'audioDuration':round(duration,3),'audio':mp3.relative_to(R).as_posix(),'audioSha256':hashlib.sha256(mp3.read_bytes()).hexdigest()});cursor+=length;print(f'{a.story} {i}/{len(plan["scenes"])} · {cursor:.1f}s',flush=True)
 def stamp(t,comma=False):
  ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02}'+(',' if comma else '.')+f'{ms:03}'
 (O/'altyazi.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(stamp(s)+' --> '+stamp(e)+'\n'+'\n'.join(textwrap.wrap(t,80)) for s,e,t in caps)+'\n')
 (O/'altyazi.srt').write_text('\n\n'.join(str(i+1)+'\n'+stamp(s,True)+' --> '+stamp(e,True)+'\n'+'\n'.join(textwrap.wrap(t,80)) for i,(s,e,t) in enumerate(caps))+'\n')
 listing=td/'concat.txt';listing.write_text(''.join(f"file '{f}'\n" for f in pieces));dest=O/(a.story+'.mp4');subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(O/'altyazi.srt'),'-map','0:v','-map','0:a','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language=tur','-metadata','title='+plan['title'],'-movflags','+faststart',str(dest)],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-ss','2','-i',str(dest),'-frames:v','1',str(O/'kapak.jpg')],check=True)
 (O/'kurgu.json').write_text(json.dumps({'title':plan['title'],'order':plan['order'],'adaptation':plan['adaptation'],'realHumanFootage':False,'engine':'Piper TTS 1.8.0 / Fettah','sourceSha256':hashlib.sha256((O/'ozgun-metin.txt').read_bytes()).hexdigest(),'duration':round(cursor,3),'scenes':timeline},ensure_ascii=False,indent=2)+'\n');print('READY',a.story,round(cursor,2),'seconds',round(dest.stat().st_size/1024**2,2),'MiB',flush=True)
