"""Local ElevenLabs voice preview and dialogue batch. Keys stay in memory on this PC."""
import hashlib,json,queue,threading,time,urllib.request,urllib.error,zipfile,sys,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent;DATA=json.loads((ROOT/'senaryo.json').read_text(encoding='utf-8'));TURNS=[t for s in DATA['scenes'] for t in s['turns']]
API='https://api.elevenlabs.io';events=queue.Queue();voices={}
def request(key,path,body=None):
 raw=None if body is None else json.dumps(body).encode();req=urllib.request.Request(API+path,data=raw,headers={'xi-api-key':key,'Content-Type':'application/json','User-Agent':'Merak-Dialogue-Studio/1.0'})
 try:
  with urllib.request.urlopen(req,timeout=90) as r:return r.read()
 except urllib.error.HTTPError as e:
  msg=e.read(800).decode(errors='replace');raise RuntimeError(f'ElevenLabs {e.code}: {msg}') from None

def synthesize(key,voice,text,model):
 return request(key,'/v1/text-to-speech/'+voice+'?output_format=mp3_44100_128',{'text':text,'model_id':model,'voice_settings':{'stability':.4,'similarity_boost':.75,'style':.5,'use_speaker_boost':True,'speed':.97}})
def generate_batch(key,selected,model,notify,produce=synthesize):
 if len(set(selected.values()))<3:raise ValueError('Üç rol için birbirinden farklı üç ses seçin.')
 dest=ROOT/'kayitlar';dest.mkdir(exist_ok=True);entries=[]
 for i,turn in enumerate(TURNS,1):
  voice=selected[turn['speaker']];identity=hashlib.sha256((turn['text']+'|'+voice+'|'+model+'|dialogue-v1').encode()).hexdigest();mp3=dest/(turn['id']+'.mp3');meta=mp3.with_suffix('.json');cached=None
  if meta.exists() and mp3.exists():
   try:
    c=json.loads(meta.read_text(encoding='utf-8'))
    if c.get('inputHash')==identity and c['sha256']==hashlib.sha256(mp3.read_bytes()).hexdigest():cached=c
   except (ValueError,KeyError):pass
  if cached is None:
   audio=produce(key,voice,turn['text'],model)
   if len(audio)<3000:raise ValueError('Eksik ses kaydı: '+turn['id'])
   pending=mp3.with_suffix('.pending');pending.write_bytes(audio);pending.replace(mp3)
   cached={'id':turn['id'],'speaker':turn['speaker'],'textSha256':turn['textSha256'],'voiceId':voice,'model':model,'inputHash':identity,'sha256':hashlib.sha256(audio).hexdigest(),'file':mp3.name}
   meta.write_text(json.dumps(cached,ensure_ascii=False,indent=2),encoding='utf-8')
  entries.append(cached);notify(f'{i}/{len(TURNS)} hazır: {turn["speaker"]}')
 result=ROOT/'uzun-diyalog-sesleri.zip';tmp=result.with_suffix('.pending')
 with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('kayitlar.json',json.dumps({'storyId':DATA['id'],'engine':'ElevenLabs','status':'generated-awaiting-listening-review','scenes':entries},ensure_ascii=False,indent=2));z.write(ROOT/'senaryo.json','senaryo.json')
  for row in entries:z.write(dest/row['file'],row['file'])
 tmp.replace(result);return result

if __name__=='__main__':
 import tkinter as tk
 from tkinter import ttk,messagebox
 app=tk.Tk();app.title('Merak Bahçesi · Diyalog Ses Atölyesi');app.geometry('760x660');app.minsize(620,570)
 frame=ttk.Frame(app,padding=22);frame.pack(fill='both',expand=True);ttk.Label(frame,text='Üç karakter, bir hikâye',font=('Segoe UI',19,'bold')).pack(anchor='w');ttk.Label(frame,text='Zehra · Ömer · Öğretmen | 7 sahne, 28 replik',wraplength=680).pack(anchor='w',pady=(6,16))
 ttk.Label(frame,text='ElevenLabs API anahtarı (kaydedilmez; yalnız ElevenLabs’a gönderilir)').pack(anchor='w');secret=ttk.Entry(frame,show='•');secret.pack(fill='x',pady=(5,10))
 roleboxes={}
 for role in DATA['roles']:
  ttk.Label(frame,text=role).pack(anchor='w');b=ttk.Combobox(frame,state='readonly');b.pack(fill='x',pady=(4,8));roleboxes[role]=b
 status=tk.StringVar(value='Önce sesleri listeleyin. Ardından her rol için farklı bir ses seçip kısa örneği dinleyin.');ttk.Label(frame,textvariable=status,wraplength=680).pack(anchor='w',pady=10)
 controls=ttk.Frame(frame);controls.pack(fill='x',pady=8);buttons=[]
 def busy(value):
  for b in buttons:b.configure(state='disabled' if value else 'normal')
 def worker(task):
  busy(True)
  def run():
   try:task()
   except Exception as e:events.put(('error',str(e)))
   finally:events.put(('busy',False))
  threading.Thread(target=run,daemon=True).start()
 def load():
  key=secret.get().strip()
  if not key:messagebox.showinfo('Anahtar gerekli','ElevenLabs API anahtarını bu bilgisayarda girin. Sohbete göndermeyin.');return
  def task():
   data=json.loads(request(key,'/v1/voices'))['voices'];listed={f'{v["name"]} · {v["voice_id"]}':v['voice_id'] for v in data};events.put(('voices',listed))
  worker(task)
 def selection():
  key=secret.get().strip();selected={r:voices.get(b.get(),'') for r,b in roleboxes.items()}
  if not key or not all(selected.values()):raise ValueError('Önce sesleri listeleyip üç rolü seçin.')
  return key,selected
 def preview():
  try:key,selected=selection()
  except ValueError as e:messagebox.showinfo('Ses seçimi',str(e));return
  def task():
   folder=ROOT/'ornekler';folder.mkdir(exist_ok=True)
   for role in DATA['roles']:
    sample={'Zehra':'Ömer, şu çiçeğe bak! Sence neden solmuş olabilir?','Ömer':'Bir tahminim var. Ama önce toprağı birlikte kontrol edelim mi?','Öğretmen':'Güzel bir soru! Önce dikkatle gözlemleyelim, sonra bulduklarımızı konuşalım.'}[role]
    audio=synthesize(key,selected[role],sample,'eleven_multilingual_v2');f=folder/(role+'.mp3');f.write_bytes(audio);events.put(('status',role+' örneği hazır.'))
   events.put(('preview',str(folder)))
  worker(task)
 def generate():
  try:key,selected=selection()
  except ValueError as e:messagebox.showinfo('Ses seçimi',str(e));return
  if len(set(selected.values()))<3:messagebox.showinfo('Farklı sesler','Her karakter için farklı bir ses seçin.');return
  chars=sum(len(t['text']) for t in TURNS)
  if not messagebox.askyesno('Kota kullanımı',f'{len(TURNS)} replik, yaklaşık {chars} karakter seslendirilecek. ElevenLabs kotanız kullanılır; ücret hesabınızın planına bağlıdır. Devam edilsin mi?'):return
  def task():
   result=generate_batch(key,selected,'eleven_multilingual_v2',lambda text:events.put(('status',text)));events.put(('done',str(result)))
  worker(task)
 for text,fn in [('1 · Sesleri listele',load),('2 · Kısa örnekler üret',preview),('3 · Hikâyeyi seslendir',generate)]:
  b=ttk.Button(controls,text=text,command=fn);b.pack(side='left',padx=(0,8));buttons.append(b)
 ttk.Label(frame,text='Örnekler ve tam üretim hesabınızın kotasını kullanır. Anahtar dosyaya veya ZIP’e yazılmaz.\nİnternet kesilirse hazır replikler korunur; yeniden çalıştırıldığında aynı seslerle devam eder.\nBu araç yalnız ses üretir; web sitesini otomatik değiştirmez.',wraplength=680).pack(anchor='w',pady=12)
 def poll():
  try:
   while True:
    kind,value=events.get_nowait()
    if kind=='voices':
     voices.clear();voices.update(value)
     for b in roleboxes.values():b['values']=list(voices)
     status.set(f'{len(voices)} ses bulundu. Kadın sesi için öğretmen örneğini dinleyerek seçin.')
    elif kind=='status':status.set(value)
    elif kind=='busy':busy(value)
    elif kind=='error':status.set('İşlem tamamlanmadı.');messagebox.showerror('Ses üretimi',value)
    elif kind=='preview':
     if os.name=='nt':os.startfile(value)
     messagebox.showinfo('Örnekler hazır','Açılan klasördeki üç MP3’ü dinleyin. Beğenmediğiniz sesi değiştirip örnekleri yeniden üretebilirsiniz.')
    elif kind=='done':status.set('Tamamlandı: uzun-diyalog-sesleri.zip');messagebox.showinfo('Tamamlandı','Oluşan uzun-diyalog-sesleri.zip dosyasını sohbetimize yükleyin.\n'+value)
  except queue.Empty:pass
  app.after(150,poll)
 poll();app.mainloop()
