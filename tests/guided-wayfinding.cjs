const assert=require('node:assert/strict');
require('./helpers/audio-harness.cjs')(async({page:p,base,errors,missing})=>{
 const ready=()=>p.waitForFunction(()=>MerakNarration.active&&!MerakNarration.active.loading&&MerakNarration.active.audio?.readyState>=2);
 await p.setViewportSize({width:390,height:844});
 // Existing bookmarks and links must reach the class picker, not the welcome screen.
 await p.goto(base+'#siniflar');
 assert.equal(await p.locator('[data-grade-choice]').count(),9);
 assert((await p.locator('.journey-stepper [aria-current=step]').innerText()).includes('Sınıfını seç'));
 await p.click('[data-grade-choice="5"]');
 assert((await p.locator('.journey-stepper [aria-current=step]').innerText()).includes('İzle ve dinle'));
 await p.click('#journey-watch');await ready();
 const progress=p.locator('.journey-scene-progress');
 assert.equal(await progress.getAttribute('aria-valuenow'),'0');
 assert.equal(await progress.locator('.is-listened').count(),0);
 assert.equal(await progress.locator('.is-current').count(),1);
 await p.evaluate(()=>{const a=MerakNarration.active.audio;a.currentTime=a.duration-.05;});
 await p.waitForFunction(()=>MerakNarration.active.ended);
 assert.equal(await progress.getAttribute('aria-valuenow'),'1');
 assert.equal(await progress.locator('.is-listened').count(),1);
 await p.click('[data-sound=next]');await ready();
 assert.equal(await p.locator('.journey-scene-position').innerText(),'2. sahne');
 assert.equal(await progress.locator('.is-listened').count(),1,'Opening a scene must not mark it listened');
 // The accessibility skip link is an anchor, not a request to leave playback.
 await p.locator('.journey-skip').focus();await p.keyboard.press('Enter');
 assert.equal(await p.evaluate(()=>MerakNarration.active.index),1);
 await p.goto(base+'#merak');assert(await p.locator('#journey-help').isVisible());
 assert(await p.evaluate(()=>MerakNarration.active.audio.paused));
 assert.equal(await p.locator('body').evaluate(e=>e.style.overflow),'hidden');
 await p.click('#journey-help-close');assert.equal(await p.locator('body').evaluate(e=>e.style.overflow),'');
 await p.click('#journey-menu-open');await p.click('[data-journey-nav="map"]');
 assert.equal(await p.locator('.journey-route-status').first().innerText(),'Devam ediyor');
 assert.equal(await p.locator('.journey-route-status').nth(1).innerText(),'Henüz tamamlanmadı');
 // Completed paths should offer a replay and completed replays must begin at scene one.
 await p.evaluate(()=>{
  const episodes=[...MERAK_COMMON_STORY.chapters.map(c=>({id:'ortak-'+c.id,scenes:c.scenes})),...MERAK_STORY_LIBRARY.stories.filter(s=>s.order===1&&s.grade==='5'),...MERAK_VISUAL_STORY.chapters.map(c=>({id:'ikinci-'+c.id,scenes:c.scenes}))];
  localStorage.setItem('merak-guided-journey-v1',JSON.stringify({grade:'5',completed:episodes.map(e=>e.id),heard:Object.fromEntries(episodes.map(e=>[e.id,e.scenes.map(s=>s.id)])),positions:Object.fromEntries(episodes.map(e=>[e.id,e.scenes.length-1])),last:''}));
 });
 await p.goto(base+'?test=completed');
 assert((await p.locator('h1').innerText()).includes('Bütün keşifleri tamamladın'));
 assert((await p.locator('.journey-current-copy .journey-primary').innerText()).includes('Yeniden izle'));
 assert.equal(await p.locator('.journey-route-status').first().innerText(),'Tamamlandı');
 await p.locator('.journey-current-copy .journey-primary').click();
 assert((await p.locator('#journey-watch').innerText()).includes('Yeniden izle'));
 await p.click('#journey-watch');await ready();
 assert.equal(await p.evaluate(()=>MerakNarration.active.index),0);
 assert.equal(await progress.getAttribute('aria-valuenow'),'7');
 // All compact guidance and progress labels fit without horizontal scrolling.
 for(const width of [320,390,768,1440]){
  await p.setViewportSize({width,height:900});
  assert(!await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'Player overflow '+width);
  await p.click('[data-journey="map"]');await p.click('[data-journey="class"]');
  assert(!await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'Steps overflow '+width);
  await p.click('[data-grade-choice="5"]');await p.click('#journey-watch');await ready();
 }
 await p.setViewportSize({width:390,height:844});
 await p.screenshot({path:'/tmp/guided-progress-mobile.png',fullPage:true});
 const explore=await p.request.get(base+'kesfet/');
 assert((await explore.text()).includes('href="../metin-atolyesi/"'));
 await p.goto(base+'#merak');assert(await p.locator('#journey-help').isVisible());
 assert(!await p.evaluate(()=>!!MerakNarration.active),'Opening a question bookmark must not autoplay');
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);
 console.log('PASS: visible step guidance, truthful scene progress, unfinished labels, legacy class and question links, accessibility skip link, completed journey replay from scene one, scroll cleanup and four responsive widths.');
}).catch(e=>{console.error(e);process.exitCode=1});
