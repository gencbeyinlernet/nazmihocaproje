"""Batch render all active stories, reusing encoded camera-motion backgrounds.
Video: Full HD H.264, original synthetic voice + subtle effects, optional Turkish captions.
Resume-safe: only completed, validated outputs enter the public manifest.
"""
import argparse,json,math,subprocess,tempfile,textwrap,hashlib,concurrent.futures,threading,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=3);p.add_argument('--limit',type=int);args=p.parse_args()
job=json.loads(subprocess.check_output(['node','scripts/export-video-jobs.cjs'],cwd=R));CACHE=Path('/tmp/merak-video-cache');CACHE.mkdir(exist_ok=True);OUT=R/'videos';(OUT/'files').mkdir(parents=True,exist_ok=True);(OUT/'captions').mkdir(exist_ok=True);(OUT/'posters').mkdir(exist_ok=True);font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def run(cmd):subprocess.run(['ffmpeg','-nostdin','-v','error','-y',*cmd],check=True,capture_output=True)
def stamp(t,comma=False):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02}'+(',' if comma else '.')+f'{ms:03}'
background_lengths={k:max([math.ceil(max(8,s['record']['duration']+.86)*2)/2 for story in job['stories'] for s in story['scenes'] if s['photo']==k],default=8)+.5 for k in job['photos']}
def background(key):
 dest=CACHE/(key+'.mp4');photo=job['photos'][key]
 if dest.exists():return
 x,y,w,h=photo['rect'];label=CACHE/(key+'.txt');label.write_text('Merak Bahçesi',encoding='utf-8')
 vf=f"[0:v]crop={w}:{h}:{x}:{y},scale=2304:1296:force_original_aspect_ratio=increase,crop=2304:1296,zoompan=z='1.015+on*0.000035':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,setsar=1,fade=t=in:st=0:d=0.16,drawbox=x=0:y=ih-88:w=iw:h=88:color=0x082f32@0.86:t=fill,drawtext=fontfile={font}:textfile={label}:fontcolor=white:fontsize=33:x=52:y=h-60[frame];[1:v]scale=96:96[logo];[frame][logo]overlay=W-w-40:36,format=yuv420p[v]"
 temp=dest.with_suffix('.pending.mp4');run(['-loop','1','-framerate','30','-i',str(R/photo['src']),'-i',str(R/'logo.jpg'),'-filter_complex_threads','1','-filter_complex',vf,'-map','[v]','-an','-t',str(background_lengths[key]),'-c:v','libx264','-preset','fast','-crf','26','-maxrate','300k','-bufsize','600k','-bf','0','-g','240','-threads','1',str(temp)]);temp.replace(dest)
 run(['-ss','2','-i',str(dest),'-frames:v','1',str(OUT/'posters'/f'{key}.jpg')]);print('BACKGROUND',key,flush=True)
keys=sorted({s['photo'] for story in job['stories'] for s in story['scenes']})
with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:list(pool.map(background,keys))
lock=threading.Lock();manifest={};metaPath=OUT/'manifest.json'
if metaPath.exists():manifest=json.loads(metaPath.read_text())['videos']
def build(story):
 sid=story['id'];scenes=story['scenes'];identity=hashlib.sha256(json.dumps([(s['id'],s['record']['sha256'],s['photo'],s['text'],s['cue']) for s in scenes],ensure_ascii=False).encode()).hexdigest();dest=OUT/'files'/f'{sid}.mp4';timings=[];cursor=0;caps=[]
 for scene in scenes:
  d=scene['record']['duration'];length=math.ceil(max(8,.16+d+(.7 if '?' in scene['text'] else .45))*2)/2
  timings.append((cursor,length));caps.append((cursor+.16,cursor+.16+d,scene['text']));cursor+=length
 existing=manifest.get(sid)
 if existing and existing.get('inputHash')==identity and (R/existing['src']).exists():return existing
 if sid=='g5-1-1-ornek-1':
  row={'id':sid,'title':story['title'],'grade':story.get('grade',''),'topic':story.get('topic',''),'sceneCount':len(scenes),'src':'video-ornekleri/7-sahne-gozlem-kulubu/gozlem-kulubu-ilk-video.mp4','captions':'video-ornekleri/7-sahne-gozlem-kulubu/altyazi.vtt','poster':'video-ornekleri/7-sahne-gozlem-kulubu/kapak.jpg','duration':57.221,'inputHash':identity}
 else:
  with tempfile.TemporaryDirectory(prefix='merak-batch-') as td:
   td=Path(td);listing=td/'concat.txt';listing.write_text(''.join(f"file '{CACHE/ (scene['photo']+'.mp4')}'\ninpoint 0\noutpoint {length}\nduration {length}\n" for scene,(_,length) in zip(scenes,timings)))
   cmd=['-f','concat','-safe','0','-i',str(listing)];filters=[];streams=[];nextindex=1
   for i,(scene,(_,length)) in enumerate(zip(scenes,timings)):
    voiceIdx=nextindex;cmd+=['-i',str(R/scene['record']['url'])];nextindex+=1
    filters.append(f'[{voiceIdx}:a]loudnorm=I=-18:TP=-2:LRA=7,aresample=48000,adelay=160:all=1,apad,atrim=duration={length},asetpts=PTS-STARTPTS[v{i}]')
    if scene['cue']:
     fx=nextindex;nextindex+=1;cmd+=['-stream_loop','-1','-i',str(R/'assets/audio/ambience'/(scene['cue']+'.mp3'))]
     filters.append(f'[{fx}:a]volume=0.65,afade=t=in:d=0.35,afade=t=out:st={length-.5}:d=0.5,atrim=duration={length},aresample=48000,asetpts=PTS-STARTPTS[f{i}]');filters.append(f'[v{i}][f{i}]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.85:level=false[a{i}]')
    else:filters.append(f'[v{i}]anull[a{i}]')
    streams.append(f'[a{i}]')
   filters.append(''.join(streams)+f'concat=n={len(scenes)}:v=0:a=1[a]');temp=dest.with_suffix('.pending.mp4')
   run([*cmd,'-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','80k','-ac','1','-ar','48000','-t',str(cursor),'-movflags','+faststart','-metadata','title='+story['title'],str(temp)])
   probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(temp)]));actual=float(probe['format']['duration']);assert abs(actual-cursor)<.15,(sid,actual,cursor);assert probe['streams'][0]['codec_name']=='h264' and probe['streams'][0]['width']==1920;temp.replace(dest)
  cap=OUT/'captions'/f'{sid}.vtt';cap.write_text('WEBVTT\n\n'+'\n\n'.join(stamp(a)+' --> '+stamp(b)+'\n'+'\n'.join(textwrap.wrap(text,82)) for a,b,text in caps)+'\n',encoding='utf-8');row={'id':sid,'title':story['title'],'grade':story.get('grade',''),'topic':story.get('topic',''),'sceneCount':len(scenes),'src':dest.relative_to(R).as_posix(),'captions':cap.relative_to(R).as_posix(),'poster':f"videos/posters/{scenes[0]['photo']}.jpg",'duration':round(actual,3),'inputHash':identity}
 row['sha256']=hashlib.sha256((R/row['src']).read_bytes()).hexdigest();row['bytes']=(R/row['src']).stat().st_size
 with lock:
  manifest[sid]=row;payload={'version':'2026-11-02-batch','method':'edited-stills-and-existing-narration','expectedStories':len(job['stories']),'videos':manifest};temp=metaPath.with_suffix('.tmp');temp.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n');temp.replace(metaPath);print(f"VIDEO {len(manifest)}/{len(job['stories'])} {sid} {row['bytes']/1024**2:.2f}MiB",flush=True)
 return row
stories=job['stories'][:args.limit] if args.limit else job['stories']
with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:list(pool.map(build,stories))
if len(manifest)==len(job['stories']):
 subprocess.run(['python',str(R/'scripts/embed-video-captions.py')],check=True)
print('FINISHED',len(manifest),'videos;',round(sum(x['bytes'] for x in manifest.values())/1024**2,1),'MiB',flush=True)
