"""Generate all requested female-role replacements locally. Does not publish anything."""
import asyncio,hashlib,json,os,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def validate_jobs(data):
 jobs=data['jobs'];seen=set()
 if len(jobs)!=60:raise ValueError('60 replik bulunmalı.')
 for j in jobs:
  if j['id'] in seen or not all(c.isalnum() or c=='-' for c in j['id']):raise ValueError('Geçersiz sahne kimliği.')
  seen.add(j['id'])
  if hashlib.sha256(j['text'].encode()).hexdigest()!=j['textSha256']:raise ValueError('Replik değişmiş: '+j['id'])
 return jobs

async def generate(data,communicate):
 jobs=validate_jobs(data);entries=[]
 # Nothing is labelled ready until the entire batch succeeds. The live site is untouched.
 with tempfile.TemporaryDirectory(prefix='merak-ses-') as tmp:
  temp=Path(tmp)
  for i,j in enumerate(jobs,1):
   dest=temp/(j['id']+'.mp3')
   for attempt in range(3):
    try:
     rate='-3%' if j['speaker'] in ['Öğretmen','Derya Öğretmen'] else '+0%'
     await communicate(j['text'],voice=data['voice'],rate=rate,pitch='+0Hz',proxy=os.environ.get('HTTPS_PROXY'),connect_timeout=15,receive_timeout=45).save(str(dest))
     if not dest.exists() or dest.stat().st_size<3000:raise ValueError('Ses dosyası boş veya eksik.')
     break
    except Exception:
     if attempt==2:raise
     await asyncio.sleep(2*(attempt+1))
   entries.append({'id':j['id'],'speaker':j['speaker'],'textSha256':j['textSha256'],'previousAudioSha256':j['currentAudioSha256'],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'file':dest.name,'voice':data['voice'],'rate':rate})
   print(f'{i}/60 hazır: {j["speaker"]} — {j["id"]}',flush=True)
  (temp/'kayitlar.json').write_text(json.dumps({'engine':'Microsoft Edge online neural TTS','status':'generated-awaiting-review','scenes':entries},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  pending=ROOT/'yeni-kadin-sesleri.tmp'
  with zipfile.ZipFile(pending,'w',zipfile.ZIP_DEFLATED) as z:
   for f in sorted(temp.iterdir()):z.write(f,f.name)
  result=ROOT/'yeni-kadin-sesleri.zip';pending.replace(result)
  return result

if __name__=='__main__':
 try:
  import edge_tts
  data=json.loads((ROOT/'metinler.json').read_text(encoding='utf-8'))
  print('60 kadın rolü kaydı hazırlanıyor. İnternet bağlantısını açık tutun.\nBu işlem web sitesine dosya göndermez.',flush=True)
  result=asyncio.run(generate(data,edge_tts.Communicate))
  print('\nTAMAMLANDI: '+str(result)+'\nBu ZIP dosyasını sohbetimize yükleyebilirsiniz.')
 except KeyboardInterrupt:
  print('\nİşlem iptal edildi; yeni tamamlanmış paket oluşturulmadı.');sys.exit(1)
 except Exception as exc:
  print('\nİşlem tamamlanamadı. Yeni ses paketi hazır değil.\n'+str(exc));sys.exit(1)
