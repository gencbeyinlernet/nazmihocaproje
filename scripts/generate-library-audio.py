"""Generate compact replaceable CC0-model narrator examples for the story library."""
import json,subprocess,tempfile,wave,hashlib
from pathlib import Path
from piper import PiperVoice,SynthesisConfig
r=Path(__file__).resolve().parents[1];model=Path('/tmp/merak-tts-models/vits-piper-tr_TR-fettah-medium/tr_TR-fettah-medium.onnx')
v=PiperVoice.load(str(model));jobs=json.loads((r/'ses-planlari/kutuphane-ses-metinleri.json').read_text());m={}
for n,j in enumerate(jobs,1):
 dest=r/'assets/audio/anlatim/kutuphane'/(j['id']+'.mp3');dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():
  with tempfile.TemporaryDirectory() as td:
   raw=Path(td)/'raw.wav'
   with wave.open(str(raw),'wb') as w:v.synthesize_wav(j['text'],w,SynthesisConfig(length_scale=1.08,noise_scale=.45,noise_w_scale=.55))
   subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(raw),'-af','loudnorm=I=-18:TP=-2:LRA=7,adelay=100,apad=pad_dur=0.25','-ar','22050','-ac','1','-c:a','libmp3lame','-b:a','24k',str(dest)],check=True,capture_output=True)
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(dest)]));assert duration>1
 m[j['id']]={'url':dest.relative_to(r).as_posix(),'duration':round(duration,3),'speaker':j['speaker'],'voice':'fettah','kind':'synthetic-demo','textSha256':hashlib.sha256(j['text'].encode()).hexdigest(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
 if n%50==0:print(n,'/',len(jobs),flush=True)
(r/'assets/audio/library-manifest.json').write_text(json.dumps({'engine':'Piper TTS','voice':'fettah','modelDatasetLicense':'CC0','status':'replaceable-demo','scenes':m},ensure_ascii=False,indent=2)+'\n')
(r/'assets/library-narration.js').write_text("'use strict';\nObject.assign(window.MERAK_NARRATION.scenes, "+json.dumps(m,ensure_ascii=False,indent=2)+');\n')
print('READY',len(m),flush=True)
