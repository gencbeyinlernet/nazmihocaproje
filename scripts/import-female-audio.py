"""Validate and import a complete user-generated female-role recording ZIP.
No archive paths are trusted or extracted directly; narration text stays unchanged.
"""
import argparse,hashlib,json,subprocess,tempfile,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('archive');args=p.parse_args()
r=Path(__file__).resolve().parents[1];manifest_path=r/'assets/audio/narration-manifest.json';m=json.loads(manifest_path.read_text());jobs={j['id']:j for j in json.loads((r/'ses-planlari/kadin-sesi-yenileme/metinler.json').read_text())['jobs']};changes={}
with zipfile.ZipFile(args.archive) as z,tempfile.TemporaryDirectory(prefix='merak-emel-check-') as d:
 if sum(x.file_size for x in z.infolist())>32*1024*1024:raise ValueError('Archive exceeds expected recording size.')
 rows=json.loads(z.read('kayitlar.json'))['scenes'];assert len(rows)==60 and {x['id'] for x in rows}==set(jobs)
 assert len(z.namelist())==len(set(z.namelist()))==61
 assert set(z.namelist())=={'kayitlar.json',*(j+'.mp3' for j in jobs)}
 for row in rows:
  sid=row['id'];old=m['scenes'][sid];job=jobs[sid]
  assert row['file']==sid+'.mp3' and row['voice']=='tr-TR-EmelNeural'
  assert row['speaker']==job['speaker']==old['speaker']
  assert row['textSha256']==job['textSha256']==old['textSha256']==hashlib.sha256(job['text'].encode()).hexdigest()
  assert row['previousAudioSha256']==job['currentAudioSha256']
  assert old['sha256'] in [row['previousAudioSha256'],row['sha256']]
  audio=z.read(row['file']);assert hashlib.sha256(audio).hexdigest()==row['sha256'] and len(audio)>3000
  tmp=Path(d)/row['file'];tmp.write_bytes(audio)
  subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(tmp),'-f','null','-'],check=True,capture_output=True)
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(tmp)]));assert 1<duration<90
  dest=(r/old['url']).resolve();assert dest.is_relative_to(r/'assets/audio/anlatim')
  changes[sid]=(dest,audio,{**old,'duration':round(duration,3),'sha256':row['sha256'],'voice':row['voice'],'engine':'Microsoft Edge online neural TTS','kind':'synthetic-narration','revision':'20261029-emel','rate':row['rate'],'origin':'user-uploaded-generated-recording'})
 # Commit only after validating every file; untouched male recordings retain their hashes.
 for sid,(dest,audio,meta) in changes.items():dest.write_bytes(audio);m['scenes'][sid]=meta
m['engine']='Piper TTS 1.8.0 / Microsoft Edge online neural TTS'
m['notes']='Kadın rolleri kullanıcı tarafından üretilip yüklenen Türkçe Emel kayıtlarıdır. Diğer kayıtlar Piper örnekleridir. Sentetik seslerdir; gerçek çocuk oyuncu kaydı değildir. Metinler ve doğal konuşma süreleri korunur.'
manifest_path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(r/'assets/narration-data.js').write_text("'use strict';\nwindow.MERAK_NARRATION = "+json.dumps(m,ensure_ascii=False,indent=2)+';\n')
print('Imported 60 verified recordings; other audio unchanged.')
