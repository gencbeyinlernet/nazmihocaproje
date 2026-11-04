const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),dir=path.join(root,'flow-hazirlik/gunes-scuti');
const plan=JSON.parse(fs.readFileSync(path.join(dir,'sahneler.json'))),timeline=JSON.parse(fs.readFileSync(path.join(dir,'kurgu.json')));
assert.equal(plan.scenes.length,74);assert.equal(plan.scenes.filter(s=>s.audioFile).length,73);assert.equal(plan.coverage.length,21);assert(plan.coverage.every(c=>c.scenes.length));assert(timeline.scenes.every(s=>s.durationSeconds<=8));assert.equal(plan.scenes[73].audioFile,null);assert.equal(plan.scenes[73].text,'');
const localMedia=process.env.GUNES_TEST_MEDIA_DIR,publicMedia=process.env.GUNES_TEST_REAL_MEDIA==='1'||!localMedia;
require('./helpers/audio-harness.cjs')(async({page,base,errors,missing})=>{
 if(!publicMedia)await page.route('https://raw.githubusercontent.com/**/gunes-scuti/**',async route=>{const url=route.request().url(),name=url.split('/gunes-scuti/')[1];assert(name&&!name.includes('..'));const file=path.join(localMedia,name),types={'.jpg':'image/jpeg','.mp3':'audio/mpeg','.mp4':'video/mp4','.zip':'application/zip'};await route.fulfill({path:file,contentType:types[path.extname(file)]||'text/plain',headers:{'access-control-allow-origin':'*'}})});
 await page.goto(base);await page.waitForSelector('[data-opening-order="2"]');
 assert((await page.locator('#journey-intro-video source').getAttribute('src')).includes('igneden-kainata'));
 assert.equal(await page.locator('[data-opening-order]').count(),2);
 await page.locator('[data-opening-order="2"]').click();await page.waitForFunction(()=>document.querySelector('video')?.readyState>=2);
 assert(page.url().includes('/flow-hazirlik/gunes-scuti/video.html'));
 const duration=await page.locator('video').evaluate(v=>v.duration);assert(Math.abs(duration-timeline.durationSeconds)<.1);
 await page.locator('video').evaluate(v=>v.play());await page.waitForFunction(()=>document.querySelector('video').currentTime>.2);
 await page.locator('video').evaluate(v=>{v.pause();v.currentTime=350;v.textTracks[0].mode='showing'});await page.waitForFunction(()=>document.querySelector('video').textTracks[0].cues?.length===73);
 await page.getByRole('link',{name:'← Önceki video',exact:true}).click();assert(page.url().includes('/igneden-kainata/video.html'));
 await page.getByRole('link',{name:/Sonraki video/}).click();assert(page.url().includes('/gunes-scuti/video.html'));
 for(const width of [320,390,768,1440]){await page.setViewportSize({width,height:900});assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1));}
 await page.getByRole('link',{name:'Sahne sahne incele',exact:true}).click();await page.waitForFunction(()=>document.querySelector('#scene-image').naturalWidth>0);
 assert.equal(await page.locator('#scene-select option').count(),74);
 await page.locator('#scene-audio').evaluate(a=>a.play());await page.waitForFunction(()=>document.querySelector('#scene-audio').currentTime>.1);
 await page.locator('#next').click();assert.equal(await page.locator('#scene-audio').evaluate(a=>a.paused),true);assert((await page.locator('#scene-audio').getAttribute('src')).includes('02-ali.mp3'));
 await page.locator('#scene-select').selectOption('73');assert.equal(await page.locator('#scene-audio').getAttribute('src'),null);assert(await page.locator('#quiet').isVisible());assert(await page.locator('#next').isDisabled());
 for(let i=0;i<74;i++){await page.locator('#scene-select').selectOption(String(i));await page.waitForFunction(()=>document.querySelector('#scene-image').complete&&document.querySelector('#scene-image').naturalWidth>0);assert((await page.locator('#scene-image').getAttribute('src')).endsWith(plan.scenes[i].imageFile));}
 for(const width of [320,390,768,1440]){await page.setViewportSize({width,height:900});assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1));}
 await page.setViewportSize({width:390,height:844});await page.selectOption('#scene-select','0');await page.screenshot({path:'/tmp/gunes-scuti-mobile.png',fullPage:true});
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);console.log('PASS: two opening films, 74 images, 73 scene voices/captions, playback, seek, previous/next, silent ending, mobile 320–1440px.'+(publicMedia?' Public CDN verified.':' Local media fixture.'));
}).catch(e=>{console.error(e);process.exitCode=1});
