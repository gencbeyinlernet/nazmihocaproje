"""Optional offline authoring tool; website visitors do not install this runtime.

Requires piper-tts==1.8.0, ffmpeg and the tr_TR-fettah-medium model.
The generated model card identifies the training dataset as CC0.
"""
import json,wave,subprocess,tempfile,hashlib
from pathlib import Path
from piper import PiperVoice,SynthesisConfig
import argparse
parser=argparse.ArgumentParser(description='Üç örneğin yedişer seslendirmesini üretir; mevcut örnek sesleri yeniler.')
parser.add_argument('--model',required=True,type=Path,help='Piper .onnx dosyası; .onnx.json aynı klasörde olmalı')
args=parser.parse_args()
if args.model.stem!="tr_TR-fettah-medium":parser.error("Bu örnek üretici tr_TR-fettah-medium modeli için ayarlanmıştır.")
root=Path(__file__).resolve().parents[1]
s=(root/'assets/productions.js').read_text();data=json.loads(s[s.index('['):].strip().rstrip(';'))
voice=PiperVoice.load(args.model)
manifest=[]
for p in data:
 (root/'assets/audio'/p['id']).mkdir(exist_ok=True)
 for scene in p['scenes']:
  out=root/'assets/audio'/p['id']/f"{scene['number']:02}.wav"
  with tempfile.TemporaryDirectory(prefix='merak-voice-') as d:
   raw=Path(d)/'raw.wav'
   with wave.open(str(raw),'wb') as w:voice.synthesize_wav(scene['text'],w,SynthesisConfig(length_scale=1.35,noise_scale=.5,noise_w_scale=.6))
   with wave.open(str(raw)) as r:duration=r.getnframes()/r.getframerate()
   speed=max(1,duration/7.6)
   filters=f'atempo={speed:.5f},loudnorm=I=-18:TP=-2:LRA=7'
   normalized=Path(d)/'normalized.wav'
   subprocess.run(['ffmpeg','-nostdin','-y','-hide_banner','-loglevel','error','-i',str(raw),'-af',filters,'-ar','22050','-ac','1','-c:a','pcm_s16le',str(normalized)],check=True)
   with wave.open(str(normalized)) as r:pcm=r.readframes(r.getnframes())
   pcm=b'\0'*(int(.12*22050)*2)+pcm
   assert len(pcm)<=176400*2, 'Speech would be truncated'
   pcm+=b'\0'*(176400*2-len(pcm))
   with wave.open(str(out),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(22050);w.writeframes(pcm)
  with wave.open(str(out)) as r:assert abs(r.getnframes()/r.getframerate()-8)<.001
  scene['audioUrl']=out.relative_to(root).as_posix();scene['audioDuration']=8;scene['audioKind']='synthetic-demo';scene['audioVoice']='Piper Türkçe · fettah (örnek anlatıcı)'
  manifest.append({'id':scene['id'],'speaker':scene['speaker'],'text':scene['text'],'audioUrl':scene['audioUrl'],'seconds':8,'rawSeconds':round(duration,3),'tempo':round(speed,5),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
  print(scene['id'],round(duration,2),'-> 8s',flush=True)
 p['audioStatus']='synthetic-demo'
(root/'assets/productions.js').write_text("'use strict';\n// Seven-scene image stories. Synthetic demo audio is replaceable; video URLs remain empty.\nwindow.MERAK_PRODUCTIONS = "+json.dumps(data,ensure_ascii=False,indent=2)+';\n')
(root/'assets/audio/manifest.json').write_text(json.dumps({'engine':'Piper TTS 1.8.0','voice':'tr_TR-fettah-medium','datasetLicense':'CC0 (model card)','voiceSource':'https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-fettah-medium.tar.bz2','notes':'Örnek yapay zekâ anlatıcı sesi. Her sahne 8 saniye; konuşma kesilmeden kısa sessizlik eklenir. OpenAI.fm veya gerçek karakter kaydı değildir.','scenes':manifest},ensure_ascii=False,indent=2)+'\n')
