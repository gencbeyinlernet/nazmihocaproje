'use strict';
(()=>{
 const base=new URL('../',document.currentScript.src),url=p=>new URL(p,base).href;
 window.MerakShare=async(button,address=location.href)=>{
  const status=document.querySelector('#public-share-status');
  try{const clean=new URL(address);clean.searchParams.delete('v');if(navigator.share){await navigator.share({title:document.title,url:clean.href});if(status)status.textContent='Paylaşım tamamlandı.';}else if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(clean.href);if(status)status.textContent='Bağlantı kopyalandı. Dilediğin yerde paylaşabilirsin.';}else throw Error('copy');}
  catch(e){if(e.name==='AbortError')return;if(status){status.textContent='Bu bağlantıyı kopyalayıp paylaşabilirsin: ';const a=document.createElement('a');a.href=address;a.textContent=address;status.append(a);}}
 };
 document.addEventListener('DOMContentLoaded',()=>{
  document.body.classList.add('public-learning');
  const institution=document.querySelector('.institution>div>div');if(institution&&!institution.querySelector('.public-access-badge')){const badge=document.createElement('span');badge.className='public-access-badge';badge.textContent='Herkese açık · Paylaşılabilir';institution.append(badge);}
  const brand=document.querySelector('.brand>span');if(brand)brand.innerHTML='<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M5 8h9c2 0 3 2 3 3v16c-2-3-5-4-12-4V8Zm22 0h-7c-2 0-3 2-3 3v16c2-3 5-4 10-4V8Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="m16 2 1.2 2.8L20 6l-2.8 1.2L16 10l-1.2-2.8L12 6l2.8-1.2L16 2Z" fill="currentColor"/></svg>';
  for(const button of document.querySelectorAll('#privacy-btn'))button.textContent='Paylaşım ve gizlilik';
  const rail=document.querySelector('#discovery-rail');if(rail){const tools=rail.querySelector('.quick-menu nav');if(tools){const a=document.createElement('a');a.className='teacher-quick-link';a.href=url('ders-hazirla/');a.innerHTML='<span aria-hidden="true">▣</span>Derse hazırlan<span aria-hidden="true">→</span>';tools.prepend(a);const share=document.createElement('button');share.type='button';share.id='share-public-content';share.innerHTML='<span aria-hidden="true">↗</span>İçeriği paylaş';share.onclick=()=>MerakShare(share);tools.append(share);}const terms=rail.querySelector('#rail-terms');if(terms)terms.innerHTML='<span aria-hidden="true">◇</span>Paylaşım ve gizlilik';}
  const status=document.createElement('p');status.id='public-share-status';status.className='public-share-status';status.setAttribute('role','status');if(rail)rail.append(status);else document.querySelector('.site-footer')?.append(status);
 });
})();
