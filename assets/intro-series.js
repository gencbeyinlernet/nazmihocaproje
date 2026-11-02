'use strict';
(()=>{
 const base=new URL('../',document.currentScript.src),url=p=>new URL(p,base).href;
 const items=[{id:'aspirin',title:'Bir aspirinle başlayan soru',topic:'Bir düşünce deneyi'},{id:'gunes-scuti',title:'Güneş ve UY Scuti',topic:'Yıldızlar, enerji ve yaratılış',preview:true},{id:'igne',title:'Bir iğneden başlayan sorular',topic:'Atomlar, üretim ve benzetmeler',preview:true}];
 function cards(){return `<section class="intro-series" aria-label="İlk üç video"><h2>İlk üç video</h2><div class="intro-series-grid">${items.map((s,i)=>`<a class="intro-series-card" data-intro-order="${i+1}" href="${url('video-ornekleri/'+s.id+'/')}"><img src="${url('video-ornekleri/'+s.id+'/kapak.jpg')}" alt="${s.title}" loading="lazy" width="1920" height="1080"><span><small>${i+1}. VİDEO${s.preview?' · ÖNİZLEME':''}</small><strong>${s.title}</strong><em>${s.topic}</em><b>İzle ▶</b></span></a>`).join('')}</div></section>`;}
 window.MerakIntroSeries={items,cards};
 document.querySelectorAll('[data-intro-series]').forEach(node=>node.innerHTML=cards());
 document.querySelectorAll('[data-intro-current]').forEach(node=>{const i=items.findIndex(s=>s.id===node.dataset.introCurrent);if(i<0)return;node.innerHTML=`<div class="intro-series-links">${items.map((s,k)=>`<a href="${url('video-ornekleri/'+s.id+'/')}" ${i===k?'aria-current="page"':''}>${k+1}. ${s.title}</a>`).join('')}</div><div class="intro-series-next">${i>0?`<a href="${url('video-ornekleri/'+items[i-1].id+'/')}">← Önceki video</a>`:''}${i<items.length-1?`<a class="intro-next" href="${url('video-ornekleri/'+items[i+1].id+'/')}">Sonraki video → ${i+2}. ${items[i+1].title}</a>`:`<a href="${url('videos/')}">Diğer videolara geç →</a>`}</div>`;});
})();
