"""Render the first actual MP4 from the project's existing stills and recordings.
Requires Node.js, ffmpeg/ffprobe and DejaVu Sans.
Camera motion is editorial pan/zoom, not generative character animation.
"""
import json,math,subprocess,tempfile,hashlib,textwrap
from pathlib import Path
R=Path(__file__).resolve().parents[1];job=json.loads(subprocess.check_output(['node','-e',"const fs=require('fs'),vm=require('vm'),c={window:{}};for(const f of ['productions','photo-data','narration-data'])vm.runInNewContext(fs.readFileSync('assets/'+f+'.js','utf8'),c);const w=c.window;process.stdout.write(JSON.stringify({production:w.MERAK_PRODUCTIONS[0],photos:w.MERAK_PHOTOS,narration:w.MERAK_NARRATION}));"],cwd=R));p=job['production'];out=R/'video-ornekleri/7-sahne-gozlem-kulubu';out.mkdir(exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';timeline=[];cursor=0;captions=[]
def stamp(t,comma=False):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02}'+(',' if comma else '.')+f'{ms:03}'
with tempfile.TemporaryDirectory(prefix='merak-film-') as td:
 td=Path(td);parts=[]
 for i,s in enumerate(p['scenes']):
  n=job['narration']['scenes'][s['id']];photo=job['photos']['photos'][job['photos']['scenes'][s['id']]];x,y,w,h=photo['rect'];voice=R/n['url'];seconds=max(8,.16+n['duration']+(.7 if '?' in s['text'] else .45));seconds=math.ceil(seconds*30)/30
  cue={0:'garden',1:'bee',2:'bee',4:'rain',6:'pencil'}.get(i);piece=td/f'{i+1:02}.mp4'
  title=td/f'title-{i}.txt';title.write_text(f'{i+1:02} / 07   ·   '+s['speaker'],encoding='utf-8');short=td/f'heading-{i}.txt';short.write_text('Gökyüzü Kulübü' if i==0 else s['title'],encoding='utf-8')
  vf=f"[0:v]crop={w}:{h}:{x}:{y},scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='1.02+on*0.0001':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,setsar=1,fade=t=in:st=0:d=0.16,fade=t=out:st={seconds-.16}:d=0.16,drawbox=x=0:y=ih-124:w=iw:h=124:color=0x082f32@0.86:t=fill,drawtext=fontfile={font}:textfile={title}:fontcolor=0xd8ece7:fontsize=27:x=52:y=h-102,drawtext=fontfile={font}:textfile={short}:fontcolor=white:fontsize=35:x=52:y=h-62[frame];[2:v]scale=96:96[logo];[frame][logo]overlay=W-w-40:36,format=yuv420p[v];[1:a]loudnorm=I=-18:TP=-2:LRA=7,aresample=48000,adelay=160:all=1,apad,atrim=duration={seconds}[voice]"
  cmd=['ffmpeg','-nostdin','-v','error','-y','-loop','1','-framerate','30','-i',str(R/photo['src']),'-i',str(voice),'-i',str(R/'logo.jpg')]
  if cue:
   cmd+=['-stream_loop','-1','-i',str(R/'assets/audio/ambience'/f'{cue}.mp3')]
   vf+=f';[3:a]volume=0.65,afade=t=in:d=0.35,afade=t=out:st={seconds-.5}:d=0.5,atrim=duration={seconds}[fx];[voice][fx]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.85:level=false[a]'
  else:vf+=';[voice]anull[a]'
  cmd+=['-filter_complex_threads','1','-filter_complex',vf,'-map','[v]','-map','[a]','-t',str(seconds),'-r','30','-c:v','libx264','-preset','fast','-crf','21','-threads','2','-c:a','aac','-b:a','160k','-ac','2','-ar','48000',str(piece)]
  subprocess.run(cmd,check=True);parts.append(piece)
  start=cursor+.16;end=start+n['duration'];captions.append((start,end,s['text']));timeline.append({'scene':s['id'],'start':round(cursor,3),'end':round(cursor+seconds,3),'speechStart':round(start,3),'speechEnd':round(end,3),'speaker':s['speaker'],'text':s['text'],'photo':job['photos']['scenes'][s['id']],'audio':n['url'],'audioSha256':n['sha256'],'effect':cue,'motion':'gentle digital zoom','flowMotionBrief':s['motion']});cursor+=seconds;print(f'{i+1}/7 rendered · {cursor:.2f}s',flush=True)
 vtt='WEBVTT\n\n'+'\n\n'.join(stamp(a)+' --> '+stamp(b)+'\n'+'\n'.join(textwrap.wrap(t,82)) for a,b,t in captions)+'\n';(out/'altyazi.vtt').write_text(vtt,encoding='utf-8');srt='\n\n'.join(str(i+1)+'\n'+stamp(a,True)+' --> '+stamp(b,True)+'\n'+'\n'.join(textwrap.wrap(t,82)) for i,(a,b,t) in enumerate(captions))+'\n';(out/'altyazi.srt').write_text(srt,encoding='utf-8')
 listing=td/'concat.txt';listing.write_text(''.join(f"file '{part}'\n" for part in parts));dest=out/'gozlem-kulubu-ilk-video.mp4';subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(out/'altyazi.srt'),'-map','0:v','-map','0:a','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language=tur','-metadata','title=Gökyüzü Kulübünün İlk Buluşması','-metadata','comment=Photo-realistic AI stills with editorial camera motion; synthetic Turkish narration.','-movflags','+faststart',str(dest)],check=True)
 (out/'video-kurgusu.json').write_text(json.dumps({'status':'first-video-review','method':'edited-stills-and-existing-narration','generatedWithFlow':False,'newElevenLabsRecording':False,'targetSize':'1920x1080','timeline':timeline},ensure_ascii=False,indent=2)+'\n')
 subprocess.run(['ffmpeg','-v','error','-y','-ss','2','-i',str(dest),'-frames:v','1',str(out/'kapak.jpg')],check=True)
 print('READY',dest,round(cursor,3),round(dest.stat().st_size/1024**2,2),'MiB',flush=True)
