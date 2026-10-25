'use strict';
(()=>{
 const base=new URL('../',document.currentScript.src),url=p=>new URL(p,base).href;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)'),instances=new Map();
 function mount(root){
  for(const [el,dispose] of instances)if(!el.isConnected){dispose();instances.delete(el);}
  for(const el of root.querySelectorAll('.topic-carousel')){
   if(instances.has(el))continue;
   const slides=[...el.querySelectorAll('.spotlight-slide')],toggle=el.querySelector('[data-slide-auto]'),count=el.querySelector('[data-slide-count]');
   if(slides.length<2)continue;
   let index=0,automatic=!reduced.matches,hovered=false,timer=null,point=null,suppressClick=false;
   function cancel(){clearTimeout(timer);timer=null;}
   function schedule(){cancel();if(automatic&&!hovered&&!document.hidden&&window.ContentTerms?.accepted()&&!document.querySelector('dialog[open]'))timer=setTimeout(()=>show(index+1,false),7000);}
   function controls(){toggle.textContent=automatic?'Otomatik geçişi durdur':'Otomatik geçişi başlat';toggle.setAttribute('aria-pressed',String(automatic));el.dataset.autoplay=String(automatic);}
   function show(next,manual=true){const previous=index;index=(next+slides.length)%slides.length;slides.forEach((s,i)=>s.hidden=i!==index);if(index!==previous&&!reduced.matches)slides[index].animate([{opacity:.45,transform:'translateX(12px)'},{opacity:1,transform:'translateX(0)'}],{duration:280,easing:'ease-out'});for(const dot of el.querySelectorAll('[data-slide-to]')){if(Number(dot.dataset.slideTo)===index)dot.setAttribute('aria-current','true');else dot.removeAttribute('aria-current');}count.setAttribute('aria-live',manual?'polite':'off');count.textContent=(index+1)+' / '+slides.length;if(manual)automatic=false;controls();schedule();}
   el.addEventListener('click',e=>{if(suppressClick&&e.target.closest('.spotlight-track')){e.preventDefault();suppressClick=false;return;}suppressClick=false;const b=e.target.closest('button');if(!b)return;if(b.hasAttribute('data-slide-next'))show(index+1);if(b.hasAttribute('data-slide-prev'))show(index-1);if(b.dataset.slideTo!==undefined)show(Number(b.dataset.slideTo));if(b===toggle){automatic=!automatic;controls();schedule();}});
   el.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key)||e.target.matches('input,select,textarea'))return;e.preventDefault();show(index+(e.key==='ArrowRight'?1:-1));});
   el.addEventListener('mouseenter',()=>{hovered=true;cancel();});el.addEventListener('mouseleave',()=>{hovered=false;schedule();});
   el.addEventListener('focusin',()=>{automatic=false;cancel();controls();});
   const track=el.querySelector('.spotlight-track');
   track.addEventListener('pointerdown',e=>{suppressClick=false;if(e.isPrimary&&e.pointerType!=='mouse')point={x:e.clientX,y:e.clientY,id:e.pointerId};});
   track.addEventListener('pointerup',e=>{if(!point||e.pointerId!==point.id)return;const dx=e.clientX-point.x,dy=e.clientY-point.y;point=null;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.4){show(index+(dx<0?1:-1));suppressClick=true;}});
   track.addEventListener('pointercancel',()=>point=null);
   const onMotion=()=>{if(reduced.matches){automatic=false;controls();cancel();}},onVisibility=()=>{if(document.hidden)cancel();else schedule();};
   // Modal changes also pause the slideshow while a story, question or menu is open.
   const observer=new MutationObserver(schedule);observer.observe(document.body,{subtree:true,attributes:true,attributeFilter:['open']});
   reduced.addEventListener('change',onMotion);document.addEventListener('visibilitychange',onVisibility);window.addEventListener('merak-consent-change',schedule);
   instances.set(el,()=>{cancel();observer.disconnect();reduced.removeEventListener('change',onMotion);document.removeEventListener('visibilitychange',onVisibility);window.removeEventListener('merak-consent-change',schedule);});controls();schedule();
  }
 }
 window.MerakSpotlight={mount};
 document.addEventListener('DOMContentLoaded',()=>{
  const shell=document.querySelector('#app-shell');if(!shell)return;
  const rail=document.createElement('aside');rail.id='discovery-rail';rail.className='discovery-rail';rail.setAttribute('aria-label','Soru ve diğer menüler');
  const qa=document.querySelector('#merak'),configured=window.MerakQuestions?.configured();
  rail.innerHTML=`<section class="question-invite" aria-labelledby="question-invite-title"><span class="question-invite-icon" aria-hidden="true">?</span><span class="eyebrow">MERAK ETTİĞİN BİR ŞEY Mİ VAR?</span><h2 id="question-invite-title">Sor, birlikte cevap arayalım.</h2><p>Aklındaki soruyu veya görüşünü bizimle paylaş.</p>${qa?'<button type="button" id="open-question-area" class="button">Soru sor <span aria-hidden="true">→</span></button>':`<a class="button" href="${url('')}#merak">Soru sor <span aria-hidden="true">→</span></a>`}${qa&&!configured?'<small>Soru hizmeti hazırlık aşamasında.</small>':''}</section><details class="quick-menu"><summary>Diğer menüler <span aria-hidden="true">⌄</span></summary><nav aria-label="Diğer menüler"><a href="${url('ortak-hikaye/')}"><span aria-hidden="true">◇</span>Ortak ilk hikâye<span aria-hidden="true">→</span></a><a href="${url('igneden-kainata/')}"><span aria-hidden="true">◈</span>İğneden Kâinata<span aria-hidden="true">→</span></a><a href="${url('sahne-atolyesi/')}"><span aria-hidden="true">▧</span>Sesli hikâyeler<span aria-hidden="true">→</span></a><a href="${url('indir/')}"><span aria-hidden="true">↓</span>Yerel test paketi<span aria-hidden="true">→</span></a><button type="button" id="rail-terms"><span aria-hidden="true">◇</span>Paylaşım ve gizlilik</button></nav><details class="rail-help"><summary>Nasıl ilerlerim?</summary><ol><li>Sınıfını seç.</li><li>Bir konuyu veya hikâyeyi aç.</li><li>İzle ve dinle düğmesine bas.</li></ol></details></details>`;
  const anchor=document.querySelector('.site-header')||document.querySelector('.class-nav-toolbar');if(anchor)anchor.after(rail);else shell.prepend(rail);
  document.body.classList.add('has-discovery-rail');rail.querySelector('#rail-terms').onclick=()=>window.ContentTerms?.open();
  const wide=matchMedia('(min-width: 1280px)'),menus=rail.querySelector('.quick-menu');const layout=()=>menus.open=wide.matches;wide.addEventListener('change',layout);layout();
  if(!qa)return;
  let support=document.querySelector('#support-area');if(!support){support=document.createElement('div');support.id='support-area';qa.before(support);support.append(qa);}else support.open=true;
  const dialog=document.createElement('dialog');dialog.id='question-dialog';dialog.className='question-dialog';dialog.setAttribute('aria-labelledby','question-dialog-title');dialog.innerHTML='<header class="question-dialog-header"><h2 id="question-dialog-title">Soru ve cevap alanı</h2><button type="button" id="close-question-area" aria-label="Soru alanını kapat">×</button></header>';dialog.append(support);document.body.append(dialog);
  const trigger=rail.querySelector('#open-question-area');let previousOverflow='';
  function open(){if(!ContentTerms.require()||dialog.open)return;previousOverflow=document.body.style.overflow;document.body.style.overflow='hidden';dialog.showModal();document.querySelector('#close-question-area').focus();}
  trigger.onclick=open;document.querySelector('#close-question-area').onclick=()=>dialog.close();
  dialog.addEventListener('close',()=>{document.body.style.overflow=previousOverflow;trigger.focus({preventScroll:true});if(location.hash==='#merak')history.replaceState(null,'',location.pathname+location.search);});
  dialog.addEventListener('click',e=>{if(e.target!==dialog)return;const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();});
  dialog.addEventListener('keydown',e=>{if(e.key!=='Tab')return;const items=[...dialog.querySelectorAll('button:not(:disabled),a[href],input:not(:disabled),select:not(:disabled),textarea:not(:disabled)')].filter(x=>x.getClientRects().length),first=items[0],last=items.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}});
  const fromHash=()=>{if(location.hash==='#merak'&&ContentTerms.accepted())open();};window.addEventListener('hashchange',fromHash);window.addEventListener('merak-consent-change',fromHash);fromHash();
 });
})();
