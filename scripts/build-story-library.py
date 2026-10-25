"""Build book-ordered original story drafts; never modifies uploaded sources or book catalog."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def readjs(name,variable):
 s=(root/'assets'/name).read_text();return json.JSONDecoder().raw_decode(s.split('window.'+variable+' = ',1)[1])[0]
catalog=readjs('catalog.js','MERAK_CATALOG');productions=readjs('productions.js','MERAK_PRODUCTIONS')
def rows(name):return [line.split('|') for line in (root/'ses-planlari'/name).read_text().splitlines() if line and not line.startswith('#')]
names={'5':['Zehra','Ömer'],'6':['Asya','Kerem'],'8':['Elif','Deniz'],'9':['Eylül','Mert'],'10':['Defne','Arda'],'11':['Selin','Bora'],'12':['Duru','Can']}
seeds={v[0]:v for v in rows('mufredat-hikaye-tohumlari.txt')};alternates={v[0]:v for v in rows('unite-alternatifleri.txt')};stories=[];jobs=[]
for g in catalog:
 for u in g['units']:
  for l in u['lessons']:
   prod=next((p for p in productions if p['lessonId']==l['id']),None)
   base={'grade':g['id'],'lessonId':l['id'],'unit':u['number'],'unitTitle':u['title'],'code':l['code'],'topic':l['topic'],'page':l['page'],'sourceTitle':g['source']['title'],'reviewed':False}
   if l['story']:
    scenes=prod['scenes'] if prod else [{'id':l['id']+'-audio-'+str(i),'text':text,'speaker':'Anlatıcı'} for i,text in enumerate([l['info'],*l['story'],l['question']])]
    item={**base,'id':l['id']+'-ornek-1','title':l['storyTitle'],'order':1,'characters':l['characters'],'scenes':scenes,'external':('sahne-atolyesi/#icerik='+prod['id']) if prod else '', 'core':l['info']}
   else:
    _,title,event,fact,action,result,question=seeds[l['id']]
    texts=[event,'Bu durumun ne anlattığını anlamak için öğretmenlerinin rehberliğinde konu üzerine düşündüler.',fact,action,result,'Öğrendiklerini günlük hayattaki başka bir örnekle ilişkilendirmeyi denediler.',question]
    scenes=[{'id':'kutuphane-'+l['id']+'-1-'+str(i+1),'text':text,'speaker':'Anlatıcı','label':label} for i,(label,text) in enumerate(zip(['Olay','İlk soru','Konuyu öğrenelim','Seçim','Sonuç','Bağlantı','Birlikte düşünelim'],texts))]
    item={**base,'id':l['id']+'-ornek-1','title':title,'order':1,'characters':names[g['id']],'scenes':scenes,'external':'','core':fact}
    jobs.extend({'id':s['id'],'text':s['text'],'speaker':s['speaker'],'group':'kutuphane'} for s in scenes)
   stories.append(item)
   if l is u['lessons'][0]:
    _,title,event,action,result=alternates[g['id']+'-'+str(u['number'])]
    question=l['question'] or seeds[l['id']][-1]
    texts=[event,'Kahramanlar ilk düşündükleri cevapla yetinmeyip konuyu daha dikkatli ele almaya karar verdi.',item['core'],action,result,'Örneğin konuyu anlamaya nasıl yardımcı olduğunu ve nerede sınırlı kaldığını tartıştılar.',question]
    scenes=[{'id':'kutuphane-'+l['id']+'-2-'+str(i+1),'text':text,'speaker':'Anlatıcı','label':label} for i,(label,text) in enumerate(zip(['Yeni bir olay','İlk düşünce','Temel bilgi','Birlikte araştıralım','Sonuç','Değerlendirme','Sıra sende'],texts))]
    stories.append({**base,'id':l['id']+'-ornek-2','title':title,'order':2,'characters':names[g['id']],'scenes':scenes,'external':'','core':item['core']})
    jobs.extend({'id':s['id'],'text':s['text'],'speaker':s['speaker'],'group':'kutuphane'} for s in scenes)
assert len(stories)==198 and len(jobs)==1225
payload={'version':'2026-10-25','status':'original-teacher-review-drafts','stories':stories}
(root/'assets/story-library-data.js').write_text("'use strict';\n// Original narratives, book heading order; no reproduced book passages.\nwindow.MERAK_STORY_LIBRARY = "+json.dumps(payload,ensure_ascii=False,indent=2)+';\n')
(root/'ses-planlari/kutuphane-ses-metinleri.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2)+'\n')
print('Library:',len(stories),'stories;',len(jobs),'new voice jobs')
