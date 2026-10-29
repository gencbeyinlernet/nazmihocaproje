/* Regenerates every story-to-photo association. Run from the repository root. */
const fs=require('fs'),vm=require('vm');const c={window:{}};
for(const file of ['catalog','productions','story-library-data','common-story-data','visual-story-data','university'])vm.runInNewContext(fs.readFileSync(`assets/${file}.js`,'utf8'),c);
const norm=s=>String(s||'').toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ı/g,'i');
const atlases={
 observation:[1536,1024,768,512,['garden','bee','seedling','stars'],['Bahçede bitkileri gözlemleyen öğrenciler ve öğretmen','Bir çiçeğin üzerinde nektar toplayan arı','Nemli topraktan çıkan yeşil filiz','Dağların üzerinde yıldızlı gece gökyüzü']],
 school:[1536,1024,768,486,['classroom','library-study','notes','seminar'],['Sınıfta öğretmenleriyle konuşan öğrenciler','Kütüphanede kaynak araştıran öğrenciler','Bir bitkinin yanında gözlem defterine not alan eller','Üniversite öğrencilerinin katıldığı bir seminer']],
 worship:[1672,941,836,470,['mosque-interior','ablution','iftar','prayer'],['Gün ışığıyla aydınlanan cami iç mekânı','Abdest hazırlığında ellerini yıkayan kişi','İftar sofrasında bir araya gelen aile','Dua için açılmış eller']],
 values:[1448,1086,724,543,['help-neighbour','reconcile','share','return-notebook'],['Yaşlı komşusuna alışveriş poşetleri taşıyan gençler','Anlaşmazlığını konuşarak çözen öğrenciler','Elma dilimlerini eşit paylaşan eller','Bulduğu defteri öğretmenine teslim eden öğrenci']],
 culture:[1672,941,836,470,['mosque-exterior','madrasa','books','ney'],['Tarihî mimariyi temsil eden bir cami dış görünümü','Revaklı tarihî bir medrese avlusu','Kütüphane rafındaki ciltli eski kitaplar','Ney çalan bir müzisyenin elleri']],
 nature:[1448,1086,724,543,['rain','harvest','plant-tree','clean-stream'],['Yağmurla ıslanan yapraklar ve toprak','Tarlada meyve ve sebzelerle dolu bir sepet','Öğretmenleriyle birlikte fidan diken öğrenciler','Dere kenarında çöpleri toplayan gençler']],
 palace:[1672,941,836,470,['palace-gate','palace-hall','palace-table','palace-guide'],['Bir sarayın bahçeye açılan kapısı','Bir sarayın geniş ve aydınlık salonu','Sarayda yiyeceklerle hazırlanmış bir sofra','Saray avlusunda rehberini dinleyen öğrenciler']],
 reason:[1672,941,836,470,['needle','carpenter','train','robot'],['İğne ve iplikle çalışan terzinin elleri','Ahşap bir masa yapan marangoz','Vagonları çeken bir lokomotif','Masanın üzerinde tekerlekli robot yapan öğrenciler']],
 heritage:[1672,941,836,470,['desert-town','desert-path','kaaba','quran'],['Eski bir çöl yerleşimini temsil eden taş evler','Dağların arasından geçen tarihî bir çöl yolu','Kâbe ve çevresini temsil eden uzak görünüm','Ahşap rahle üzerinde kapalı Kur’an-ı Kerim']],
 reflection:[1672,941,836,470,['sunrise','cemetery','reflect','discussion'],['Denizin üzerinde yükselen güneş','Ağaçlar arasındaki sakin bir mezarlık','Yağmurlu pencerenin yanında düşünen bir genç','Kütüphanede saygıyla görüş alışverişi yapan yetişkinler']],
 worldfaith:[1672,941,836,470,['church','synagogue','hindu-temple','stupa'],['Hristiyanlık konusuna eşlik eden temsili kilise','Yahudilik konusuna eşlik eden temsili sinagog','Hinduizm konusuna eşlik eden temsili tapınak','Budizm konusuna eşlik eden temsili stupa']],
 daily:[1672,941,836,444,['planning','health','family','sport'],['Masa başında zamanını planlayan bir öğrenci','Doktoruyla görüşen bir genç ve ebeveyni','Büyüklerini dinleyen aile üyeleri','Okul bahçesinde birlikte basketbol oynayan öğrenciler']]
};
const photos={};for(const [name,[w,h,sx,sy,keys,alts]]of Object.entries(atlases))keys.forEach((key,i)=>{const x=i%2?sx:0,y=i>1?sy:0;photos[key]={src:`assets/photos/${name}.webp`,width:w,height:h,rect:[x+2,y+2,(i%2?w-sx:sx)-4,(i>1?h-sy:sy)-4],alt:alts[i]};});
const themes=[
 [/yahud/,'synagogue books discussion'],[/hristiyan/,'church books discussion'],[/hindu/,'hindu-temple books discussion'],[/budiz/,'stupa books discussion'],[/konfuc|taoizm/,'books discussion seminar'],
 [/dogdugu cevre|cocuklugu|genclik yillari/,'desert-town desert-path books'],[/peygamber|hz\.|kissa|vahiy|elcileri/,'quran books desert-path'],
 [/namaz|tahiyyat/,'mosque-interior ablution prayer'],[/hazirlik sart/,'ablution mosque-interior prayer'],[/ramazan|oruc|iftar/,'iftar prayer share'],[/dua/,'prayer quran mosque-interior'],[/sure|ayet|kur.an|ilahi kitap/,'quran books library-study'],
 [/cami|mimari/,'mosque-exterior mosque-interior madrasa'],[/musiki/,'ney books mosque-exterior'],[/sanat/,'ney mosque-exterior books'],[/medeniyet|egitim kurum/,'madrasa books library-study'],[/tasavvuf|gelenek|kultur/,'books ney mosque-exterior'],
 [/saglik|tipla/,'health planning family'],[/gida|bagimlilik/,'harvest health sport'],[/paylas|zekat|sadaka|yardim|iktisadi/,'help-neighbour share harvest'],[/merhamet|rahman|rahim/,'help-neighbour plant-tree share'],[/adalet|esitlik|hakki/,'share reconcile return-notebook'],[/dogru soz|guvenilir/,'return-notebook classroom reconcile'],[/baris|affedi|istisar|deger verme|nezaket/,'reconcile family classroom'],
 [/cevre/,'clean-stream plant-tree garden'],[/teknoloji/,'robot library-study notes'],[/bilim|bilgi/,'library-study notes seminar'],[/ahlak|sorumlu|irade|kader|kaza/,'planning reconcile notes'],[/duzen|yaratil|kozmolojik|teleolojik|alem/,'stars seedling garden'],[/felsef|ontolojik|yorum|istismar|kotuluk/,'discussion books reflect'],[/inanc|iman|tevhit|allah/,'stars garden quran']
];
const specific=[
 [/lokomotif|vagon|tren/,'train'],[/igne|iplik/,'needle'],[/marangoz|masa yap/,'carpenter'],[/robot/,'robot'],[/polen|nektar|arilar|bir ari\b/,'bee'],[/yagmur/,'rain'],[/filiz|tohum/,'seedling'],[/yildiz|gece ve gunduz|gokyuzu/,'stars'],[/cop|atik|dereyi|dere kenar/,'clean-stream'],[/fidan|agac dik/,'plant-tree'],[/meyve|sebze|hasat|elma|nar agac/,'harvest'],
 [/abdest/,'ablution'],[/iftar|oruc|ramazan/,'iftar'],[/namaz/,'mosque-interior'],[/dua ed|dua et|dua icin/,'prayer'],[/kabe|hac ibadet/,'kaaba'],[/saray.*sofra|saray.*yiyecek/,'palace-table'],[/saray.*kapi/,'palace-gate'],[/saray/,'palace-hall'],[/ney|musiki/,'ney'],[/medrese/,'madrasa'],[/doktor|hastane/,'health'],[/basketbol|spor/,'sport'],[/komsu.*yardim|yardim.*komsu/,'help-neighbour'],[/buldugu.*defter|kayip.*defter/,'return-notebook'],[/paylas|esit/,'share'],[/baris|anlasmazlik|uzlas|ozur/,'reconcile'],[/buyukanne|buyukbaba|dede|aile.*sohbet/,'family'],[/zaman.*plan|plan.*zaman|calisma plan/,'planning'],[/kutuphane|kaynak arastir/,'library-study'],[/gozlem defter|defter.*not|not.*defter/,'notes'],[/bahce.*gozlem|gozlem.*bahce/,'garden']
];
const scenePhotos={},storyPhotos={},audit=[];
function choose(topic,scene,i){const t=norm(topic),body=norm(scene.text);const pool=(themes.find(([r])=>r.test(t))?.[1]||'classroom library-study notes').split(' ');return specific.find(([r])=>r.test(body))?.[1]||pool[i%pool.length];}
function assign(id,topic,scenes){const keys=scenes.map((s,i)=>{const key=choose(topic,s,i);if(!scenePhotos[s.id])scenePhotos[s.id]=key;return scenePhotos[s.id];});storyPhotos[id]=keys[0];audit.push({id,topic,scenes:scenes.map((s,i)=>({id:s.id,photo:keys[i]}))});}
for(const s of c.window.MERAK_STORY_LIBRARY.stories)assign(s.id,s.topic,s.scenes);
for(const g of c.window.MERAK_CATALOG)for(const u of g.units)for(const l of u.lessons)assign(l.id,l.topic,[l.info,...l.story,l.question].map((text,i)=>({id:l.id+'-audio-'+i,text})));
for(const p of c.window.MERAK_PRODUCTIONS)assign(p.id,p.topic,p.scenes);
for(const p of c.window.MERAK_COMMON_STORY.chapters)assign('ortak-'+p.id,p.title,p.scenes);
for(const p of c.window.MERAK_VISUAL_STORY.chapters)assign('ikinci-'+p.id,p.title,p.scenes);
for(const p of c.window.MERAK_UNIVERSITY)assign('universite-'+p.id,p.category,[...p.reading,...p.questions,p.task].map((text,i)=>({id:p.id+'-audio-'+i,text})));
const explicit={
 'gozlem-kulubu':['garden','bee','bee','stars','rain','garden','notes'],
 'birligin-anlami':['classroom','garden','quran','stars','sunrise','notes','library-study'],
 'guzel-isimler':['library-study','quran','books','help-neighbour','garden','notes','classroom'],
 'ortak-01':['library-study','stars','palace-gate','quran','reflect','quran','palace-gate'],
 'ortak-02':['palace-table','palace-table','palace-guide','share','palace-hall','palace-guide','ablution'],
 'ortak-03':['palace-gate','garden','reflect','classroom','share','reconcile','notes'],
 'ortak-04':['palace-guide','palace-guide','classroom','books','quran','palace-guide','stars'],
 'ortak-05':['harvest','harvest','stars','sunrise','harvest','share','clean-stream'],
 'ortak-06':['rain','seedling','help-neighbour','planning','clean-stream','classroom','robot'],
 'ortak-07':['robot','robot','robot','robot','discussion','quran','notes'],
 'ortak-08':['notes','library-study','palace-hall','quran','share','discussion','classroom']
};
for(const [prefix,keys]of Object.entries(explicit))keys.forEach((k,i)=>scenePhotos[`${prefix}-${String(i+1).padStart(2,'0')}`]=k);
for(const row of audit){for(const s of row.scenes)s.photo=scenePhotos[s.id];storyPhotos[row.id]=row.scenes[0].photo;}
const data={version:'2026-10-28-photos',kind:'AI-generated-photorealistic-illustrations',photos,scenes:scenePhotos,stories:storyPhotos};
fs.writeFileSync('assets/photo-data.js',"'use strict';\n// Photorealistic illustrations, not documentary photographs. See PHOTOREAL-GORSELLER.md.\nwindow.MERAK_PHOTOS = "+JSON.stringify(data,null,2)+';\n');
fs.writeFileSync('assets/photos/scene-map.json',JSON.stringify(audit,null,2)+'\n');
console.log(`${Object.keys(photos).length} photos; ${Object.keys(scenePhotos).length} mapped scenes; ${c.window.MERAK_STORY_LIBRARY.stories.length} library stories.`);
