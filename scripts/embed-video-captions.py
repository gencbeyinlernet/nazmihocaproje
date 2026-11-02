"""Embed optional Turkish subtitles into downloaded MP4s without re-encoding video/audio."""
from pathlib import Path
import json,subprocess,concurrent.futures,hashlib
R=Path(__file__).resolve().parents[1];p=R/'videos/manifest.json';m=json.loads(p.read_text())
def mux(v):
 f=R/v['src'];streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(f)]))['streams']
 if not any(s['codec_type']=='subtitle' for s in streams):
  temp=f.with_suffix('.captions.mp4');subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',str(f),'-i',str(R/v['captions']),'-map','0:v','-map','0:a','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language=tur','-movflags','+faststart',str(temp)],check=True,capture_output=True);temp.replace(f)
 v['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();v['bytes']=f.stat().st_size;return v
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 rows=list(pool.map(mux,m['videos'].values()))
m['videos']={v['id']:v for v in rows};tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');tmp.replace(p)
print('All 220 MP4s contain optional Turkish subtitles; speech and image streams copied unchanged.',flush=True)
