const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
require('./helpers/audio-harness.cjs')(async({page:p,base,root,errors,missing})=>{
 const ready=()=>p.waitForFunction(()=>MerakNarration.active&&!MerakNarration.active.loading&&MerakNarration.active.audio?.readyState>=2);
 const summary=()=>p.evaluate(()=>MerakLessonActivities.summary('g5-1-1'));
 const choose=async n=>{await p.check('input[name="activity-choice"][value="'+n+'"]');await p.click('[data-act=check]');};
 const answers=await p.request.get(base+'assets/lesson-activities-data.js');assert(answers.ok());
 await p.setViewportSize({width:390,height:844});await p.goto(base+'sahne-atolyesi/?ekran=ogretmen#icerik=gozlem-kulubu&etkinlik=1');
 assert((await p.locator('.lesson-activities h2').innerText()).includes('Önce birlikte'));assert.equal(await p.locator('[data-act=start-quiz]').count(),0);assert.equal((await summary()).quizComplete,false);
 await p.click('[data-act=replay]');await ready();await p.evaluate(()=>{const a=MerakNarration.active.audio;a.defaultPlaybackRate=16;a.playbackRate=16;});await p.check('[data-sound-auto]');await p.waitForSelector('[data-act=start-game]');
 assert.equal((await summary()).listened,true);assert.equal((await summary()).gameComplete,false);assert.equal((await summary()).score,null);assert.equal(await p.evaluate(()=>MerakNarration.active),null);
 await p.click('[data-act=start-game]');assert.equal(await p.locator('.activity-counter').innerText(),'1 / 3');assert(await p.locator('[data-act=check]').isDisabled());
 assert(await p.evaluate(()=>document.querySelector('.activity-steps').getBoundingClientRect().top>=document.querySelector('.site-header').getBoundingClientRect().bottom),'Sticky header must not cover the lesson steps');
 await choose(0);assert((await p.locator('.activity-feedback').innerText()).includes('Işığın'));assert.equal((await summary()).gameComplete,false);
 await p.click('[data-act=retry-game]');await choose(1);await p.click('[data-act=next-game]');
 await p.reload();assert.equal(await p.locator('.activity-counter').innerText(),'2 / 3');assert.equal((await summary()).score,null);
 // Review a scene without changing the recorded game answer or scoring a quiz.
 await choose(0);await p.click('[data-act=review]');await ready();assert((await p.evaluate(()=>MerakNarration.active.audio.src)).includes('gozlem-kulubu-03.mp3'));await p.click('[data-act=return]');
 await p.click('[data-act=retry-game]');await choose(0);await p.click('[data-act=retry-game]');await choose(0);assert((await p.locator('.activity-feedback h3').innerText()).includes('birlikte'));assert(await p.locator('.activity-choice.is-correct').isVisible());await p.click('[data-act=next-game]');await choose(0);await p.click('[data-act=next-game]');
 assert.equal((await summary()).gameComplete,true);assert.equal((await summary()).score,null);await p.click('[data-act=start-quiz]');assert.equal(await p.locator('.activity-counter').innerText(),'1 / 5');
 // First submitted answers are final for this attempt: 3 correct = 60, not an inflated retry score.
 const selected=[1,0,0,0,1];
 for(let i=0;i<5;i++){
  assert.equal(await p.locator('.activity-counter').innerText(),(i+1)+' / 5');await choose(selected[i]);assert.equal(await p.locator('.activity-feedback').count(),1);assert(await p.locator('input[name=activity-choice]').first().isDisabled());
  if(i===1){await p.reload();assert.equal(await p.locator('.activity-counter').innerText(),'2 / 5');assert(await p.locator('.activity-feedback').isVisible());}
  if(i<4)await p.click('[data-act=next-quiz]');
 }
 assert.equal((await summary()).score,null);await p.click('[data-act=next-quiz]');assert.equal((await summary()).score,60);assert.equal((await summary()).best,60);assert(await p.locator('.activity-score').isVisible());assert((await p.locator('.activity-result-status').innerText()).includes('5 soru cevaplandı'));
 await p.goto(base+'hikayeler/?sinif=5');assert(await p.locator('.library-example.is-complete').first().isVisible());assert((await p.locator('.lesson-activity-tag').first().innerText()).includes('60/100'));
 // The guided route and the teacher's studio share a result, without another account or exam.
 await p.goto(base+'sahne-atolyesi/?ekran=ogretmen#icerik=gozlem-kulubu&etkinlik=1');assert((await p.locator('.activity-score').innerText()).includes('60'));
 await p.click('[data-act=retake]');const correct=[1,3,0,2,1];for(let i=0;i<5;i++){await choose(correct[i]);await p.click('[data-act=next-quiz]');}assert.equal((await summary()).score,100);assert.equal((await summary()).best,100);
 await p.click('[data-act=retake]');for(let i=0;i<5;i++){await choose(0);await p.click('[data-act=next-quiz]');}assert.equal((await summary()).score,20);assert.equal((await summary()).best,100);
 await p.evaluate(()=>MerakLessonActivities.pause());await p.click('[data-act=listen]');await p.waitForFunction(()=>MerakLessonActivities.active.audio.currentTime>.6);await p.click('[data-act=listen]');assert(await p.evaluate(()=>MerakLessonActivities.active.audio.paused));const heldTime=await p.evaluate(()=>MerakLessonActivities.active.audio.currentTime);await p.click('[data-act=listen]');await p.waitForFunction(()=>!MerakLessonActivities.active.audio.paused);assert(await p.evaluate(t=>MerakLessonActivities.active.audio.currentTime>=t-.01,heldTime),'Resume must keep the same clip position');await p.evaluate(()=>window.dispatchEvent(new Event('merak-navigation-open')));assert(await p.evaluate(()=>MerakLessonActivities.active.audio.paused));await p.keyboard.press('Escape');
 for(const width of [320,390,768,1100,1440]){
  await p.setViewportSize({width,height:900});assert(!await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'Result overflow '+width);
  const previousScore=(await summary()).score;await p.click('[data-act=retake]');assert(!await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'Question overflow '+width);
  await choose(1);assert(!await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'Feedback overflow '+width);
  // A partial retake survives reload and cannot overwrite the last completed score.
  await p.reload();assert.equal((await summary()).score,previousScore);assert.equal(await p.locator('.activity-counter').innerText(),'1 / 5');
  await p.goto(base+'sahne-atolyesi/?ekran=ogretmen#icerik=gozlem-kulubu&etkinlik=1');
  // Finish the partial run so the next layout iteration can start another attempt.
  for(let i=0;i<5;i++){if(i)await choose(correct[i]);await p.click('[data-act=next-quiz]');}
 }
 await p.setViewportSize({width:390,height:844});await p.screenshot({path:'/tmp/pilot-result-mobile.png',fullPage:true});
 const audioManifest=JSON.parse(fs.readFileSync(path.join(root,'assets/audio/activity-manifest.json'))),jobs=JSON.parse(fs.readFileSync(path.join(root,'ses-planlari/etkinlik-ses-metinleri.json')));
 assert.equal(jobs.length,27);for(const j of jobs){const m=audioManifest.clips[j.id];assert(m);assert.equal(crypto.createHash('sha256').update(j.text).digest('hex'),m.textSha256);assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,m.url))).digest('hex'),m.sha256);assert(m.duration>1);}
 await p.evaluate(()=>ContentTerms.open());p.once('dialog',d=>d.accept());await p.click('#terms-reset');await p.waitForFunction(()=>window.MerakLessonActivities&&!MerakLessonActivities.summary('g5-1-1').listened);assert.equal(await p.evaluate(()=>localStorage.getItem('merak-lesson-activities-v1')),null);
 await p.evaluate(()=>localStorage.setItem('merak-lesson-activities-v1','{"version":"wrong","lessons":{"g5-1-1":{"latest":[1,3,0,2,1]}}}'));await p.goto(base+'sahne-atolyesi/?ekran=ogretmen#icerik=gozlem-kulubu&etkinlik=1');assert.equal((await summary()).quizComplete,false);assert((await p.locator('.lesson-activities h2').innerText()).includes('Önce birlikte'));
 // Denied device storage still allows this open page to complete the practice.
 await p.evaluate(()=>{Storage.prototype.getItem=()=>{throw new Error('Storage denied');};Storage.prototype.setItem=()=>{throw new Error('Storage denied');};const l=MERAK_LESSON_ACTIVITIES.lessons['g5-1-1'];MerakLessonActivities.recordHeard(l.id,l.sceneIds);MerakLessonActivities.mount(document.querySelector('#studio-activity'),{id:l.id});});
 await p.click('[data-act=start-game]');for(const n of [1,2,0]){await choose(n);await p.click('[data-act=next-game]');}await p.click('[data-act=start-quiz]');for(let i=0;i<5;i++){await choose(correct[i]);await p.click('[data-act=next-quiz]');}assert.equal((await summary()).score,100);assert(await p.locator('.activity-storage-note').isVisible());
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);console.log('PASS: listening gate; three-round game, hints and third-attempt explanation; five-question scoring, feedback/review; shared progress, resume and retake/best score; menu audio pause; 27 MP3 hashes; corrupt state and five responsive widths.');
}).catch(e=>{console.error(e);process.exitCode=1;});
