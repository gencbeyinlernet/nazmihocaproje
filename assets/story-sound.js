'use strict';
(()=>{
 const base=new URL('../',document.currentScript.src),setting='merak-scene-sounds-v1';
 const normalize=s=>String(s||'').toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ı/g,'i');
 const sounds={garden:{duration:10,loop:true},rain:{duration:10,loop:true},water:{duration:8,loop:true},bee:{duration:1.8},paper:{duration:1.1},pencil:{duration:1.5},train:{duration:8,loop:true},robot:{duration:1.3}};
 // Cues describe literal objects/actions in a scene, not a soundtrack for beliefs.
 function cue(scene){
  const text=normalize(scene?.text),photo=window.MerakPhotos?.keyFor(scene);
  if(/lokomotif|vagon|tren/.test(text)&&photo==='train')return 'train';
  if(/robot/.test(text)&&photo==='robot')return 'robot';
  if(/yagmur/.test(text)&&['rain','seedling','garden'].includes(photo))return 'rain';
  if(/ari\b|arilar|polen|nektar/.test(text)&&photo==='bee')return 'bee';
  if(/abdest|musluk|cesme|akan su|derenin|dere kenar/.test(text)&&['ablution','clean-stream','rain'].includes(photo))return 'water';
  if(/sayfa.*cevr|defter.*ac|kitab.*ac/.test(text))return 'paper';
  if(/defter.*yaz|not.*al|not.*yaz/.test(text)&&photo==='notes')return 'pencil';
  if(/bahce|gozlem|agac|cicek|fidan/.test(text)&&['garden','plant-tree','seedling'].includes(photo))return 'garden';
  return '';
 }
 function pauseAfter(scene,next){return /[?？]/.test(scene?.text||'')?700:!next?450:scene?.speaker!==next?.speaker?380:280;}
 class Soundscape{
  constructor(){this.media=new Audio();this.media.preload='none';this.media.volume=.75;this.enabled=true;this.key='';this.destroyed=false;this.token=0;try{this.enabled=localStorage.getItem(setting)!=='off';}catch{}}
  start(scene,elapsed=0){
   this.stop();if(!this.enabled||this.destroyed)return;const key=cue(scene),item=sounds[key];if(!item||!item.loop&&elapsed>=item.duration)return;
   const token=this.token;this.key=key;this.media.loop=Boolean(item.loop);this.media.src=new URL('assets/audio/ambience/'+key+'.mp3',base).href;
   try{this.media.currentTime=item.loop?elapsed%item.duration:elapsed;}catch{}
   // A decorative track failing or being blocked must never stop the spoken story.
   this.media.play().catch(()=>{if(token===this.token)this.stop();});
  }
  stop(){this.token++;this.media.pause();this.key='';}
  setEnabled(value){this.enabled=Boolean(value);try{localStorage.setItem(setting,this.enabled?'on':'off');}catch{}if(!this.enabled)this.stop();}
  destroy(){this.stop();this.destroyed=true;this.media.removeAttribute('src');this.media.load();}
 }
 window.MerakStorySound={create:()=>new Soundscape(),cue,pauseAfter};
})();
