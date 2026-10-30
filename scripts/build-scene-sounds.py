"""Create original, intentionally quiet synthetic scene cues; no speech or music.
Peak ceiling -27 dBFS keeps these below narration even on mobile volume APIs.
"""
import math,random,subprocess,tempfile,wave,array,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];RATE=22050;random.seed(2951)
def env(t,start,length):
 x=(t-start)/length
 return math.sin(math.pi*x)**2 if 0<x<1 else 0

def make(name,duration):
 values=[];low=0;prev=0
 for n in range(int(RATE*duration)):
  t=n/RATE;white=random.uniform(-1,1);low=.965*low+.035*white;high=white-prev;prev=white
  if name=='garden':
   v=.32*low
   for at in [1.1,1.48,5.2,5.65]:
    q=t-at;v+=.055*env(t,at,.23)*math.sin(2*math.pi*(2200*q+1700*q*q))
  elif name=='rain':v=.26*white+.3*low
  elif name=='water':v=(.35+.1*math.sin(t*1.8))*(.2*white+.5*low)
  elif name=='bee':v=.12*math.sin(2*math.pi*185*t+1.6*math.sin(2*math.pi*5*t))*env(t,.05,1.4)+.025*low
  elif name=='paper':v=high*(.7*env(t,.05,.32)+.45*env(t,.35,.25)+.2*env(t,.63,.2))
  elif name=='pencil':v=high*sum(.35*env(t,at,.17) for at in [.08,.3,.54,.83,1.07])
  elif name=='train':
   v=.65*low+.025*math.sin(2*math.pi*63*t)
   v+=white*sum(.35*env(t,at,.05) for at in [i*.46 for i in range(16)])
  elif name=='robot':v=sum(.1*env(t,at,.14)*math.sin(2*math.pi*(280+60*i)*t) for i,at in enumerate([.1,.42,.75]))+.08*low*env(t,.05,1)
  fade=min(1,t/.12,(duration-t)/.35);values.append(v*max(0,fade))
 peak=max(abs(v) for v in values);gain=10**(-27/20)/max(peak,1e-8)
 return array.array('h',(int(v*gain*32767) for v in values))
rows=[]
for name,duration,loop in [('garden',10,True),('rain',10,True),('water',8,True),('bee',1.8,False),('paper',1.1,False),('pencil',1.5,False),('train',8,True),('robot',1.3,False)]:
 dest=ROOT/'assets/audio/ambience'/f'{name}.mp3'
 with tempfile.TemporaryDirectory() as d:
  wav=Path(d)/'cue.wav'
  with wave.open(str(wav),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE);f.writeframes(make(name,duration).tobytes())
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-c:a','libmp3lame','-b:a','48k',str(dest)],check=True)
 rows.append({'id':name,'seconds':duration,'loop':loop,'peakCeilingDbfs':-27,'kind':'original-synthetic-scene-effect'})
(ROOT/'assets/audio/ambience/manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
print('8 quiet scene cues generated; no narration recordings changed.')
