"""Generate replaceable Turkish narrator audio for the pilot practice. No student data."""
import json,subprocess,tempfile,wave,hashlib,argparse
from pathlib import Path
from piper import PiperVoice,SynthesisConfig
p=argparse.ArgumentParser();p.add_argument('--model',required=True);args=p.parse_args()
r=Path(__file__).resolve().parents[1]
script="const fs=require('fs'),vm=require('vm'),s={window:{}};vm.runInNewContext(fs.readFileSync('assets/lesson-activities-data.js','utf8'),s);process.stdout.write(JSON.stringify(s.window.MERAK_LESSON_ACTIVITIES));"
data=json.loads(subprocess.check_output(['node','-e',script],cwd=r))
jobs=[]
for lesson in data['lessons'].values():
 prefix=lesson['id']
 jobs += [{'id':prefix+'-intro','text':lesson['intro']},{'id':prefix+'-quiz-intro','text':lesson['quizIntro']}]
 for kind in ['game','quiz']:
  for i,row in enumerate(lesson[kind],1):
   stem=(f'{i}. soru. ' if kind=='quiz' else '')+row['prompt']+' '+ ' '.join(chr(65+n)+' seçeneği: '+text for n,text in enumerate(row['options']))
   jobs.append({'id':prefix+'-'+kind+'-'+row['id'],'text':stem})
   jobs.append({'id':prefix+'-'+kind+'-'+row['id']+'-explanation','text':row['explanation']})
   if kind=='game':jobs.append({'id':prefix+'-'+kind+'-'+row['id']+'-hint','text':row['hint']})
 for score in range(0,101,20):
  jobs.append({'id':prefix+'-result-'+str(score),'text':f'Çalışmayı tamamladın. Beş sorudan {score//20} tanesini doğru cevapladın. Son denemendeki puanın yüz üzerinden {score}. Açıklamaları yeniden inceleyebilir veya soruları tekrar deneyebilirsin.'})
voice=PiperVoice.load(args.model);entries={}
for i,job in enumerate(jobs,1):
 dest=r/'assets/audio/etkinlik'/f"{job['id']}.mp3";dest.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as d:
  raw=Path(d)/'voice.wav'
  with wave.open(str(raw),'wb') as out:voice.synthesize_wav(job['text'],out,SynthesisConfig(length_scale=1.06,noise_scale=.45,noise_w_scale=.55))
  subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(raw),'-af','loudnorm=I=-18:TP=-2:LRA=7,adelay=100,apad=pad_dur=0.25','-ar','22050','-ac','1','-c:a','libmp3lame','-b:a','40k',str(dest)],check=True)
 seconds=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(dest)]))
 entries[job['id']]={'url':dest.relative_to(r).as_posix(),'duration':round(seconds,3),'textSha256':hashlib.sha256(job['text'].encode()).hexdigest(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
 print(f'{i}/{len(jobs)}',flush=True)
manifest={'version':data['version'],'kind':'replaceable-synthetic-demo','voice':'fettah','modelDatasetLicense':'CC0','clips':entries}
(r/'assets/audio/activity-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(r/'assets/activity-narration.js').write_text("'use strict';\nwindow.MERAK_ACTIVITY_AUDIO = "+json.dumps(manifest,ensure_ascii=False,indent=2)+';\n')
(r/'ses-planlari/etkinlik-ses-metinleri.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2)+'\n')
