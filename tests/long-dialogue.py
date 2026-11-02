"""Validate dialogue structure and local batch resume/export without contacting a voice service."""
import importlib.util,json,tempfile,hashlib,zipfile
from pathlib import Path
r=Path(__file__).resolve().parents[1];src=r/'ses-planlari/uzun-diyalog/SESLENDIR.py';spec=importlib.util.spec_from_file_location('long_dialogue',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
data=m.DATA;assert len(data['scenes'])==7;assert len(m.TURNS)==28;assert len({t['speaker'] for t in m.TURNS})==3
for scene in data['scenes']:
 assert len(scene['turns'])==4 and len({t['speaker'] for t in scene['turns']})==3
 for a,b in zip(scene['turns'],scene['turns'][1:]):assert a['speaker']!=b['speaker']
for t in m.TURNS:assert hashlib.sha256(t['text'].encode()).hexdigest()==t['textSha256']
selected={'Zehra':'female-young','Ömer':'male-young','Öğretmen':'female-teacher'};calls=[]
def fake(key,voice,text,model):calls.append((voice,text));return (voice+text).encode()*100
with tempfile.TemporaryDirectory() as d:
 m.ROOT=Path(d);(m.ROOT/'senaryo.json').write_text(json.dumps(data))
 p=m.generate_batch('DO-NOT-EXPORT-THIS',selected,'eleven_multilingual_v2',lambda _:None,produce=fake);assert len(calls)==28
 with zipfile.ZipFile(p) as z:
  assert len(z.namelist())==30
  assert all(b'DO-NOT-EXPORT-THIS' not in z.read(n) for n in z.namelist())
  rows=json.loads(z.read('kayitlar.json'))['scenes'];assert len({x['voiceId'] for x in rows})==3
  for row in rows:assert hashlib.sha256(z.read(row['file'])).hexdigest()==row['sha256']
 m.generate_batch('DO-NOT-EXPORT-THIS',selected,'eleven_multilingual_v2',lambda _:None,produce=fake);assert len(calls)==28
 selected['Öğretmen']='another-female';m.generate_batch('DO-NOT-EXPORT-THIS',selected,'eleven_multilingual_v2',lambda _:None,produce=fake);assert len(calls)==35
 try:m.generate_batch('unused',dict.fromkeys(selected,'same-voice'),'model',lambda _:None,produce=fake)
 except ValueError:pass
 else:raise AssertionError('Roles need distinct voices')
print('PASS: 7 scenes/28 alternating turns, 3 distinct roles, text hashes, export excludes key, cached resume, changing only teacher regenerates 7 replies. Voice service not called.')
