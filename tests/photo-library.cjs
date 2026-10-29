const assert=require('node:assert/strict'),fs=require('fs'),vm=require('vm'),path=require('path');
const c={window:{}};for(const f of ['photo-data','story-library-data','common-story-data','visual-story-data','productions','university'])vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../assets/'+f+'.js'),'utf8'),c);
const w=c.window,data=w.MERAK_PHOTOS,stories=w.MERAK_STORY_LIBRARY.stories;
assert.equal(stories.length,205);assert.equal(Object.keys(data.photos).length,48);
for(const p of Object.values(data.photos)){assert(fs.statSync(path.join(__dirname,'..',p.src)).size>10000);const[x,y,width,height]=p.rect;assert(x>=0&&y>=0&&width>0&&height>0&&x+width<=p.width&&y+height<=p.height);assert(p.alt.length>15);}
for(const s of [...stories,...w.MERAK_PRODUCTIONS,...w.MERAK_COMMON_STORY.chapters,...w.MERAK_VISUAL_STORY.chapters])for(const scene of s.scenes)assert(data.photos[data.scenes[scene.id]],`Missing scene image: ${s.id}/${scene.id}`);
for(const p of w.MERAK_UNIVERSITY)for(let i=0;i<p.reading.length+p.questions.length+1;i++)assert(data.photos[data.scenes[p.id+'-audio-'+i]]);
assert.equal(data.scenes['gozlem-kulubu-03'],'bee');assert.equal(data.scenes['gozlem-kulubu-05'],'rain');assert.equal(data.scenes['ortak-07-01'],'robot');
require('./helpers/audio-harness.cjs')(async({page,base,errors,missing})=>{
 await page.goto(base);await page.waitForSelector('.journey-image-card .story-photo');
 // Each source decodes; each individual viewport has a visible, accessible image.
 await page.evaluate(async()=>{for(const [key,p]of Object.entries(MERAK_PHOTOS.photos)){const h=document.createElement('div');h.style.width='600px';h.innerHTML=MerakPhotos.picture(key);document.body.append(h);const img=h.querySelector('img');await img.decode();const svg=h.querySelector('svg');if(svg.getBoundingClientRect().height<100||!svg.getAttribute('aria-label'))throw Error(key);h.remove();}});
 for(const width of [320,390,768,1440]){await page.setViewportSize({width,height:900});assert(await page.locator('.journey-image-card .story-photo').isVisible());assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1));}
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'/tmp/photos-home-mobile.png'});
 await page.goto(base+'hikayeler/?sinif=6');await page.waitForSelector('[data-library-play]');await page.locator('[data-library-play]').first().click();await page.waitForFunction(()=>MerakNarration.active&&!MerakNarration.active.loading);assert(await page.locator('.sound-image .story-photo').isVisible());assert.equal(await page.locator('.sound-image .library-scene').count(),0);
 await page.evaluate(()=>MerakNarration.pause());await page.screenshot({path:'/tmp/photos-story-mobile.png'});await page.click('#close-library');
 // Every library scene renders an actual bitmap, including every previously symbolic story.
 const coverage=await page.evaluate(()=>{let count=0;for(const s of MERAK_STORY_LIBRARY.stories)for(let i=0;i<s.scenes.length;i++){const html=MerakStoryLibrary.renderScene(s,i);if(!html.includes('<image href=')||!html.includes('data-photo-key'))throw Error(s.scenes[i].id);count++;}return count;});assert(coverage>1200);
 await page.goto(base+'sahne-atolyesi/');await page.click('#start-story');await page.waitForFunction(()=>MerakNarration.active&&!MerakNarration.active.loading);await page.evaluate(()=>MerakNarration.pause());assert.equal(await page.locator('.sound-image .photo-frame').getAttribute('data-photo-key'),'garden');await page.click('[data-sound=next]');await page.waitForFunction(()=>MerakNarration.active.index===1&&!MerakNarration.active.loading);assert.equal(await page.locator('.sound-image .photo-frame').getAttribute('data-photo-key'),'bee');
 for(const width of [320,390,768,1440]){await page.setViewportSize({width,height:900});assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1));const box=await page.locator('.sound-image .story-photo').boundingBox();assert(box.width>200&&box.height>100);}
 await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:'/tmp/photos-player-desktop.png'});
 // Broken atlas must stop playback rather than allowing narration over a blank image.
 await page.route('**/assets/photos/observation.webp',r=>r.abort());await page.goto(base+'sahne-atolyesi/');await page.click('#start-story');await page.waitForFunction(()=>MerakNarration.active?.imageFailed);assert(!await page.evaluate(()=>MerakNarration.active.playing));await page.unroute('**/assets/photos/observation.webp');await page.click('[data-sound=play]');await page.waitForFunction(()=>MerakNarration.active.playing);await page.evaluate(()=>MerakNarration.pause());
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);console.log(`PASS: 205 stories, ${coverage} library scenes, 48 realistic image viewports; all files decode, mobile/desktop layout, scene changes and image-error stop/retry.`);
}).catch(e=>{console.error(e);process.exitCode=1});
