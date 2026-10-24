"""Generate replaceable Turkish demo narration from a reviewed local job list.
Requires piper-tts, ffmpeg and the two voice models listed in assets/audio/CREDITS.md.
Never truncates speech or squeezes it into the storyboard's target duration.
"""
import argparse,hashlib,json,subprocess,tempfile,wave
from pathlib import Path
from piper import PiperVoice,SynthesisConfig
parser=argparse.ArgumentParser();parser.add_argument('jobs');parser.add_argument('--models',required=True);args=parser.parse_args()
root=Path(__file__).resolve().parents[1];models=Path(args.models);jobs=json.loads(Path(args.jobs).read_text());voices={};entries={}
for name in ['dfki','fettah']:
 voices[name]=PiperVoice.load(str(models/f'vits-piper-tr_TR-{name}-medium'/f'tr_TR-{name}-medium.onnx'))
profiles={'Zehra':('dfki',1.02,1.06),'Elif':('dfki',1.02,1.06),'Ömer':('fettah',1.02,1.04),'Deniz':('fettah',1.02,1.04),'Öğretmen':('dfki',1.10,1.0),'Derya Öğretmen':('dfki',1.10,1.0),'Anlatıcı':('fettah',1.08,1.0)}
for n,job in enumerate(jobs,1):
 name,pace,pitch=profiles.get(job['speaker'],profiles['Anlatıcı']);dest=root/'assets/audio/anlatim'/job['group']/(job['id']+'.mp3');dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():
  with tempfile.TemporaryDirectory(prefix='merak-narration-') as d:
   raw=Path(d)/'raw.wav'
   with wave.open(str(raw),'wb') as f:voices[name].synthesize_wav(job['text'],f,SynthesisConfig(length_scale=pace,noise_scale=.45,noise_w_scale=.55))
   # A small character tone difference, not a claim of a real child or female actor.
   filters=(f'asetrate=22050*{pitch},aresample=22050,atempo={1/pitch},' if pitch!=1 else '')+'loudnorm=I=-18:TP=-2:LRA=7,adelay=100,apad=pad_dur=0.25'
   subprocess.run(['ffmpeg','-nostdin','-y','-hide_banner','-loglevel','error','-i',str(raw),'-af',filters,'-ar','24000','-ac','1','-c:a','libmp3lame','-b:a','64k',str(dest)],check=True)
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(dest)]).decode().strip());assert duration>1
 entries[job['id']]={'url':dest.relative_to(root).as_posix(),'duration':round(duration,3),'speaker':job['speaker'],'voice':name,'kind':'synthetic-demo','textSha256':hashlib.sha256(job['text'].encode()).hexdigest(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
 if n%10==0 or n==len(jobs):print(f'{n}/{len(jobs)} recordings ready',flush=True)
manifest={'locale':'tr-TR','status':'replaceable-demo','engine':'Piper TTS 1.8.0','notes':'Yeni Türkçe örnek kayıtlar; gerçek çocuk veya karakter oyuncusu kaydı değildir. Doğal konuşma süresi korunur. Kullanıcının kayıtlarıyla değiştirilebilir.','scenes':entries}
(root/'assets/audio/narration-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(root/'assets/narration-data.js').write_text("'use strict';\nwindow.MERAK_NARRATION = "+json.dumps(manifest,ensure_ascii=False,indent=2)+';\n')
