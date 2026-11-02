"""Create an immediately watchable long dialogue cut from three connected existing chapters.
No new speech is generated and no women's voice replacement is claimed.
"""
import json,subprocess,tempfile,re,textwrap
from pathlib import Path
R=Path(__file__).resolve().parents[1];OUT=R/'video-ornekleri/uzun-gozlem';OUT.mkdir(exist_ok=True)
m=json.loads((R/'videos/manifest.json').read_text())['videos'];ids=['g5-1-1-ornek-1','g5-1-2-ornek-1','g5-1-3-ornek-1'];names=['Bahçedeki keşif','Birliğin anlamı','Güzel isimler'];font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
productions=json.loads(subprocess.check_output(['node','-e',"const fs=require('fs'),vm=require('vm'),c={window:{}};vm.runInNewContext(fs.readFileSync('assets/productions.js','utf8'),c);process.stdout.write(JSON.stringify(c.window.MERAK_PRODUCTIONS))"],cwd=R));timeline=[];cursor=0;caps=[];durations=[]
def sec(s):
 h,mi,se=s.split(':');return int(h)*3600+int(mi)*60+float(se)
def stamp(t,comma=False):
 ms=round(t*1000);h,ms=divmod(ms,3600000);mi,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{mi:02}:{s:02}'+(',' if comma else '.')+f'{ms:03}'
for k,sid in enumerate(ids):
 row=m[sid];probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(R/row['src'])]));duration=float(probe['format']['duration']);durations.append(duration)
 blocks=(R/row['captions']).read_text().strip().split('\n\n')[1:];assert len(blocks)==7
 for i,block in enumerate(blocks):
  lines=block.splitlines();a,b=lines[0].split(' --> ');text=' '.join(lines[1:]);scene=productions[k]['scenes'][i];assert text==scene['text'];start=cursor+sec(a);end=cursor+sec(b);caps.append((start,end,scene['speaker']+': '+text));timeline.append({'id':scene['id'],'speaker':scene['speaker'],'text':scene['text'],'chapter':names[k],'start':round(start,3),'end':round(end,3)})
 cursor+=duration
(OUT/'altyazi.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(stamp(a)+' --> '+stamp(b)+'\n'+'\n'.join(textwrap.wrap(t,82)) for a,b,t in caps)+'\n')
(OUT/'altyazi.srt').write_text('\n\n'.join(str(i+1)+'\n'+stamp(a,True)+' --> '+stamp(b,True)+'\n'+'\n'.join(textwrap.wrap(t,82)) for i,(a,b,t) in enumerate(caps))+'\n')
with tempfile.TemporaryDirectory(prefix='merak-long-') as d:
 d=Path(d);cmd=['ffmpeg','-nostdin','-v','error','-y']
 for sid in ids:cmd+=['-i',str(R/m[sid]['src'])]
 cmd+=['-i',str(OUT/'altyazi.srt')]
 filters=[f'[{i}:v]setsar=1,setpts=PTS-STARTPTS[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[a{i}]' for i in range(3)];filters.append('[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]')
 overlay='[v]drawbox=x=0:y=ih-124:w=iw:h=124:color=0x082f32:t=fill'
 for i,turn in enumerate(timeline):
  label=d/(str(i)+'.txt');label.write_text(turn['speaker']+' · '+turn['chapter']);start=0 if i==0 else turn['start']-.16;end=timeline[i+1]['start']-.16 if i+1<len(timeline) else cursor
  overlay+=f",drawtext=fontfile={font}:textfile={label}:fontcolor=white:fontsize=34:x=52:y=h-78:enable='between(t,{start},{end})'"
 filters.append(overlay+'[out]');dest=OUT/'bahceden-gokyuzune-uzun-video.mp4'
 subprocess.run([*cmd,'-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','[out]','-map','[a]','-map','3:0','-c:v','libx264','-preset','veryfast','-crf','23','-maxrate','850k','-bufsize','1700k','-threads','2','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','160k','-c:s','mov_text','-metadata:s:s:0','language=tur','-movflags','+faststart',str(dest)],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-ss','2','-i',str(dest),'-frames:v','1',str(OUT/'kapak.jpg')],check=True)
(OUT/'kurgu.json').write_text(json.dumps({'title':'Bahçeden Gökyüzüne','method':'three-existing-connected-dialogue-chapters','voiceReplaced':False,'sources':ids,'duration':cursor,'turns':timeline},ensure_ascii=False,indent=2)+'\n');print('READY',cursor,'seconds',dest.stat().st_size/1024**2,'MiB',flush=True)
