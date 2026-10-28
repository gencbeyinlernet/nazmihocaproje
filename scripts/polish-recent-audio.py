"""Re-render the 49 recent narrator samples; retain text and all other recordings."""
import json,subprocess,tempfile,wave,hashlib,argparse
from pathlib import Path
from piper import PiperVoice,SynthesisConfig
p=argparse.ArgumentParser();p.add_argument('--model',required=True);args=p.parse_args()
r=Path(__file__).resolve().parents[1];v=PiperVoice.load(args.model)
m=json.loads((r/'assets/audio/library-manifest.json').read_text())
jobs=[j for j in json.loads((r/'ses-planlari/kutuphane-ses-metinleri.json').read_text()) if j['id'].startswith('ek20261028-')]
assert len(jobs)==49
for i,j in enumerate(jobs,1):
 dest=r/m['scenes'][j['id']]['url']
 with tempfile.TemporaryDirectory() as d:
  raw=Path(d)/'voice.wav'
  with wave.open(str(raw),'wb') as out:v.synthesize_wav(j['text'],out,SynthesisConfig(length_scale=1.02,noise_scale=.45,noise_w_scale=.55))
  subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(raw),'-af','highpass=f=70,loudnorm=I=-18:TP=-2:LRA=7,afade=t=in:d=0.01,adelay=120,apad=pad_dur=0.35','-ar','22050','-ac','1','-c:a','libmp3lame','-b:a','48k',str(dest)],check=True)
 m['scenes'][j['id']].update(duration=round(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(dest)])),3),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),textSha256=hashlib.sha256(j['text'].encode()).hexdigest())
 print(i,'/',len(jobs),flush=True)
(r/'assets/audio/library-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(r/'assets/library-narration.js').write_text("'use strict';\nObject.assign(window.MERAK_NARRATION.scenes, "+json.dumps(m['scenes'],ensure_ascii=False,indent=2)+');\n')
