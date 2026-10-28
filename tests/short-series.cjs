const assert=require('node:assert/strict');
require('./helpers/audio-harness.cjs')(async({page:p,base,errors,missing})=>{
 for(const grade of ['5','6','8','9','10','11','12']){
  await p.goto(base+'#siniflar');await p.click('[data-grade-choice="'+grade+'"]');await p.locator('#journey-root [data-journey=map]').first().click();
  assert.equal(await p.locator('[data-starter-stories] .journey-route-item').count(),10);
  const ids=await p.locator('[data-starter-stories] [data-open-preview]').evaluateAll(es=>es.map(e=>e.dataset.openPreview));assert.equal(new Set(ids).size,10);assert(ids.includes('g'+grade+'-1-1-ornek-3'));assert(ids.every(id=>id.startsWith('g'+grade+'-')));
 }
 for(const width of [320,390,768,1440]){await p.setViewportSize({width,height:900});assert(!await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'Overflow '+width);}
 await p.setViewportSize({width:390,height:844});await p.screenshot({path:'/tmp/short-series-mobile.png',fullPage:true});
 await p.click('[data-open-preview="g12-1-1-ornek-3"]');await p.click('#journey-watch');await p.waitForFunction(()=>MerakNarration.active?.audio?.readyState>=2);assert((await p.evaluate(()=>MerakNarration.active.audio.src)).includes('ek20261028-12-1.mp3'));await p.check('[data-sound-auto]');await p.evaluate(()=>{MerakNarration.active.audio.defaultPlaybackRate=16;MerakNarration.active.audio.playbackRate=16;});await p.waitForSelector('.journey-celebration');
 assert.equal(await p.locator('.lesson-activities').count(),0);assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);console.log('PASS: seven book-verified grades each show ten unique ordered starters; new story real audio and automatic completion; no student quiz; four responsive widths.');
}).catch(e=>{console.error(e);process.exitCode=1;});
