'use strict';
(()=>{
 const base=new URL('../',document.currentScript.src),data=window.MERAK_PHOTOS;
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function keyFor(scene){const id=typeof scene==='string'?scene:scene?.id||'';return data.scenes[id]||data.stories[id]||data.stories[id.replace(/-custom-(intro|question)$/,'')]||'';}
 function picture(key,options={}){
  const p=data.photos[key];if(!p)return '';const src=new URL(p.src,base).href;
  // The inline SVG viewport displays one photograph from the compressed sheet.
  // A real image probe lets the player wait for loading and handle connection errors.
  return `<div class="photo-frame" data-photo-key="${esc(key)}"><img class="photo-load-probe" ${options.probeId?`id="${esc(options.probeId)}"`:''} src="${esc(src)}" alt="" aria-hidden="true" width="1" height="1"><svg class="story-photo" role="img" aria-label="${esc(p.alt)}" viewBox="${p.rect.join(' ')}" preserveAspectRatio="xMidYMid slice"><image href="${esc(src)}" width="${p.width}" height="${p.height}"/></svg></div>`;
 }
 function render(scene,options){return picture(keyFor(scene),options);}
 window.MerakPhotos={picture,render,keyFor,source:scene=>{const p=data.photos[keyFor(scene)];return p?new URL(p.src,base).href:'';}};
})();
