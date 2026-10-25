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
  const main=document.querySelector('main');if(main&&!document.querySelector('a.skip')){if(!main.id)main.id='main';const skip=document.createElement('a');skip.className='skip learning-skip';skip.href='#'+main.id;skip.textContent='İçeriğe geç';document.body.prepend(skip);}if(main&&!main.hasAttribute('tabindex'))main.tabIndex=-1;
  const institution=document.querySelector('.institution>div>div');if(institution&&!institution.querySelector('.public-access-badge')){const badge=document.createElement('span');badge.className='public-access-badge';badge.textContent='Herkese açık · Paylaşılabilir';institution.append(badge);}
  const brand=document.querySelector('.brand>span');if(brand)brand.innerHTML='<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M5 8h9c2 0 3 2 3 3v16c-2-3-5-4-12-4V8Zm22 0h-7c-2 0-3 2-3 3v16c2-3 5-4 10-4V8Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="m16 2 1.2 2.8L20 6l-2.8 1.2L16 10l-1.2-2.8L12 6l2.8-1.2L16 2Z" fill="currentColor"/></svg>';
  for(const button of document.querySelectorAll('#privacy-btn'))button.textContent='Paylaşım ve gizlilik';
  const rail=document.querySelector('#discovery-rail');if(rail){const tools=rail.querySelector('.quick-menu nav');if(tools){const a=document.createElement('a');a.className='teacher-quick-link';a.href=url('ders-hazirla/');a.innerHTML='<span aria-hidden="true">▣</span>Derse hazırlan<span aria-hidden="true">→</span>';tools.prepend(a);const share=document.createElement('button');share.type='button';share.id='share-public-content';share.innerHTML='<span aria-hidden="true">↗</span>İçeriği paylaş';share.onclick=()=>MerakShare(share);tools.append(share);}const terms=rail.querySelector('#rail-terms');if(terms)terms.innerHTML='<span aria-hidden="true">◇</span>Paylaşım ve gizlilik';}
  const icons={book:'M4 5h6c2 0 2 1 2 2v14c-2-2-5-2-8-2V5Zm16 0h-6c-2 0-2 1-2 2v14c2-2 5-2 8-2V5Z',lesson:'M4 5h16v14H4zM8 9h8M8 13h5',play:'M9 7l8 5-8 5V7ZM12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Z',download:'M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5',shield:'M12 2l8 3v6c0 5-8 11-8 11S4 16 4 11V5l8-3Zm-4 9 3 3 5-6',share:'M8 12l8-6m-8 6 8 6M5 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6Zm14-7a3 3 0 1 0 0 6 3 3 0 0 0 0-6Zm0 14a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z',spark:'m12 2 3 7 7 3-7 3-3 7-3-7-7-3 7-3 3-7Z'};
  const icon=name=>'<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="'+icons[name]+'" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  for(const item of document.querySelectorAll('.quick-menu nav>a,.quick-menu nav>button')){const slot=item.querySelector('span:first-child');if(!slot)continue;const href=item.getAttribute('href')||'';const key=item.id==='share-public-content'?'share':item.id==='rail-terms'?'shield':href.includes('ders-hazirla')?'lesson':href.includes('sahne-atolyesi')?'play':href.includes('igneden-kainata')?'spark':href.includes('indir')?'download':'book';slot.innerHTML=icon(key);}
  const teacherIcon=document.querySelector('.teacher-entry-link>span:first-child');if(teacherIcon)teacherIcon.innerHTML=icon('lesson');
  const status=document.createElement('p');status.id='public-share-status';status.className='public-share-status';status.setAttribute('role','status');if(rail)rail.append(status);else document.querySelector('.site-footer')?.append(status);
 });
})();
