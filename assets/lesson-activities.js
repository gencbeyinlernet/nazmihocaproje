'use strict';
(()=>{
  const data=window.MERAK_LESSON_ACTIVITIES;if(!data)return;
  const base=new URL('../',document.currentScript.src),key='merak-lesson-activities-v1';
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const url=p=>new URL(p,base).href,has=id=>Object.hasOwn(data.lessons,id),valid=(a,n)=>Number.isInteger(a)&&a>=0&&a<n;
  let active=null,volatileStore=null;
  function fresh(){return {heard:[],game:{started:false,index:0,answers:[null,null,null],tries:[0,0,0]},quiz:{active:false,index:0,answers:[null,null,null,null,null]},latest:null,best:null,attemptCount:0};}
  function score(answers,lesson){return answers.reduce((n,a,i)=>n+(a===lesson.quiz[i].answer?20:0),0);}
  function gameDone(s,lesson){return lesson.game.every((g,i)=>s.game.answers[i]===g.answer||s.game.answers[i]!==null&&s.game.tries[i]>=3);}
  function read(id){
    const lesson=data.lessons[id],s=fresh();if(!lesson)return s;
    try{
      const store=volatileStore||JSON.parse(localStorage.getItem(key)),v=store?.version===data.version?store.lessons?.[id]:null;if(!v||typeof v!=='object')return s;
      if(Array.isArray(v.heard))s.heard=[...new Set(v.heard.filter(x=>lesson.sceneIds.includes(x)))];
      for(let i=0;i<lesson.game.length;i++){const a=v.game?.answers?.[i],t=v.game?.tries?.[i];s.game.answers[i]=valid(a,lesson.game[i].options.length)?a:null;s.game.tries[i]=Number.isInteger(t)?Math.min(3,Math.max(0,t)):0;if(a===null)s.game.tries[i]=Math.min(2,s.game.tries[i]);}
      s.game.started=v.game?.started===true;s.game.index=valid(v.game?.index,lesson.game.length)?v.game.index:0;
      let gap=false;for(let i=0;i<lesson.quiz.length;i++){const a=v.quiz?.answers?.[i];if(!gap&&valid(a,lesson.quiz[i].options.length))s.quiz.answers[i]=a;else gap=true;}
      s.quiz.active=v.quiz?.active===true;s.quiz.index=valid(v.quiz?.index,lesson.quiz.length)?v.quiz.index:0;
      const full=a=>Array.isArray(a)&&a.length===lesson.quiz.length&&a.every((v,i)=>valid(v,lesson.quiz[i].options.length));
      if(s.heard.length===lesson.sceneIds.length&&gameDone(s,lesson)){if(full(v.latest))s.latest=[...v.latest];if(full(v.best))s.best=[...v.best];if(s.latest&&(!s.best||score(s.latest,lesson)>score(s.best,lesson)))s.best=[...s.latest];}
      s.attemptCount=s.latest&&Number.isInteger(v.attemptCount)?Math.max(1,Math.min(999999,v.attemptCount)):0;
    }catch{}
    return s;
  }
  function save(id,s){
    let store=volatileStore;try{store=store||JSON.parse(localStorage.getItem(key));}catch{}
    if(store?.version!==data.version||!store.lessons||typeof store.lessons!=='object'||Array.isArray(store.lessons))store={version:data.version,lessons:{}};
    store.lessons[id]=JSON.parse(JSON.stringify(s));try{localStorage.setItem(key,JSON.stringify(store));volatileStore=null;return true;}catch{volatileStore=store;return false;}
  }
  function recordHeard(id,ids){if(!has(id))return;const s=read(id),lesson=data.lessons[id];s.heard=[...new Set([...s.heard,...ids.filter(x=>lesson.sceneIds.includes(x))])];save(id,s);}
  function summary(id){if(!has(id))return null;const lesson=data.lessons[id],s=read(id);return {heard:[...s.heard],listened:s.heard.length===lesson.sceneIds.length,gameComplete:gameDone(s,lesson),quizComplete:Boolean(s.latest),score:s.latest?score(s.latest,lesson):null,best:s.best?score(s.best,lesson):null,retaking:Boolean(s.quiz.active&&s.latest)};}
  class Activity{
    constructor(root,options){
      active?.destroy();window.MerakNarration?.destroy();active=this;this.root=root;this.options=options;this.lesson=data.lessons[options.id];this.id=options.id;this.audio=new Audio();this.audio.preload='none';this.token=0;this.audioId=null;this.dead=false;this.selected=null;this.reviewPlayer=null;
      if(options.heard)recordHeard(this.id,options.heard);this.state=read(this.id);
      this.click=e=>{const b=e.target.closest('[data-act]');if(!b)return;switch(b.dataset.act){
        case'listen':this.audio.paused?this.playClip(this.clipId):this.pause();break;
        case'start-game':this.state.game.started=true;this.persist();this.show('game',true);break;
        case'retry-game':this.state.game.answers[this.state.game.index]=null;this.selected=null;this.persist();this.show('game',true);break;
        case'next-game':if(this.roundDone()){if(this.state.game.index<this.lesson.game.length-1){this.state.game.index++;this.persist();this.show('game',true);}else this.show('quiz-intro');}break;
        case'start-quiz':case'retake':this.state.quiz={active:true,index:0,answers:[null,null,null,null,null]};this.persist();this.show('quiz',true);break;
        case'next-quiz':if(this.state.quiz.answers[this.state.quiz.index]!==null){if(this.state.quiz.index<this.lesson.quiz.length-1){this.state.quiz.index++;this.persist();this.show('quiz',true);}else this.finishQuiz();}break;
        case'review':this.review();break;
        case'return':this.show(this.beforeReview);break;
        case'exit':this.pause();options.onExit?.();break;
        case'continue':this.pause();(options.onContinue||options.onExit)?.();break;
        case'replay':this.pause();options.onReplay?.();break;
      }};
      this.change=e=>{if(e.target.name==='activity-choice'){this.selected=Number(e.target.value);const check=root.querySelector('[data-act=check]');if(check)check.disabled=false;}};
      this.submit=e=>{e.preventDefault();this.check();};root.addEventListener('click',this.click);root.addEventListener('change',this.change);root.addEventListener('submit',this.submit);
      this.audio.onended=()=>this.audioControls();this.audio.onerror=()=>{if(!this.dead&&this.audio.error&&this.audio.getAttribute('src')){this.message('Ses yüklenemedi. Dinle düğmesiyle yeniden deneyebilirsin.');this.audioControls();}};
      this.hidden=()=>{if(document.hidden)this.pause();};document.addEventListener('visibilitychange',this.hidden);window.addEventListener('merak-navigation-open',this.hiddenPause=()=>this.pause());
      this.dialogObserver=new MutationObserver(()=>{const dialogs=[...document.querySelectorAll('dialog[open]')],top=dialogs.at(-1),parent=root.closest('dialog');if(top&&!top.contains(root)||parent&&!parent.open)this.pause();});this.dialogObserver.observe(document.body,{subtree:true,attributes:true,attributeFilter:['open']});
      const s=this.state;if(s.heard.length!==this.lesson.sceneIds.length)this.show('blocked');else if(s.quiz.active&&gameDone(s,this.lesson))this.show('quiz');else if(s.latest)this.show('result');else if(gameDone(s,this.lesson))this.show('quiz-intro');else if(s.game.started)this.show('game');else this.show('intro');
    }
    persist(){this.storageFailed=!save(this.id,this.state);}
    message(t){const node=this.root.querySelector('.activity-audio-status');if(node)node.textContent=t;}
    stop(){this.token++;this.audioId=null;this.audio.pause();this.audio.removeAttribute('src');this.audio.load();}
    pause(){this.token++;this.audio.pause();this.reviewPlayer?.pause();this.audioControls();}
    audioControls(){if(this.dead)return;const button=this.root.querySelector('[data-act=listen]');if(button){button.textContent=this.audio.paused?'Dinle':'Duraklat';button.setAttribute('aria-pressed',String(!this.audio.paused));}}
    async playClip(id){if(this.dead||document.hidden)return;this.reviewPlayer?.pause();const clip=window.MERAK_ACTIVITY_AUDIO?.clips[id];if(!clip){this.message('Bu yönergenin ses kaydı henüz hazır değil.');return;}if(this.audioId!==id||this.audio.ended||this.audio.error||!this.audio.getAttribute('src')){this.stop();this.audioId=id;this.audio.src=url(clip.url);this.audio.load();}const token=this.token;this.message('');try{await this.audio.play();if(!this.dead&&token===this.token)this.audioControls();}catch{if(!this.dead&&token===this.token){this.message('Sesi açmak için Dinle düğmesine dokun.');this.audioControls();}}}
    steps(activeStep){return `<ol class="activity-steps" aria-label="Bu dersin adımları">${['Dinle','Oyna','Sınav','Sonuç'].map((label,i)=>`<li ${i===activeStep?'aria-current="step"':''} class="${i<activeStep?'is-done':''}"><span aria-hidden="true">${i<activeStep?'✓':i+1}</span>${label}</li>`).join('')}</ol>`;}
    chrome(body,step=1){return `<section class="lesson-activities">${this.steps(step)}${body}<p class="activity-audio-status" role="status"></p>${this.storageFailed?'<p class="activity-storage-note">Bu tarayıcı ilerlemeyi kaydedemiyor. Sayfa açıkken devam edebilirsin.</p>':''}<details class="activity-teacher-note"><summary>Öğretmen için ders ve kaynak bilgisi</summary><p>${esc(this.lesson.curriculum.program)} · <b>${esc(this.lesson.curriculum.code)}</b><br>${esc(this.lesson.curriculum.text)}</p><p>${esc(this.lesson.curriculum.evidence)}<br>${esc(this.lesson.curriculum.book)}</p><p>Özgün etkinlik ve soru taslağı; öğretmen içerik kontrolü içindir. Metin, görsel ve ses üretiminde yapay zekâ desteği kullanılmıştır. Yeni yönerge sesleri değiştirilebilir sentetik anlatıcı örnekleridir. <a href="${url('assets/audio/CREDITS.md')}">Seslerin kaynak ve lisans bilgisi</a></p></details></section>`;}
    roundDone(){const i=this.state.game.index;return this.state.game.answers[i]===this.lesson.game[i].answer||this.state.game.answers[i]!==null&&this.state.game.tries[i]>=3;}
    show(view,autoplay=false){
      this.stop();this.reviewPlayer?.destroy();this.reviewPlayer=null;this.view=view;this.selected=null;
      const l=this.lesson,s=this.state;let body='',step=view==='quiz'||view==='quiz-intro'?2:view==='result'?3:1;
      if(view==='blocked')body=`<div class="activity-entry"><span class="activity-kicker">ÖNCE HİKÂYE</span><h2 tabindex="-1">Önce birlikte izleyelim.</h2><p>Oyundaki bağlantıları hikâyede keşfedeceksin.</p><button type="button" class="activity-primary" data-act="replay">Hikâyeyi aç →</button></div>`;
      if(view==='intro'){
        this.clipId=this.id+'-intro';body=`<div class="activity-entry sound-finish"><span class="activity-kicker">DİNLEME TAMAMLANDI ✓</span><div class="activity-leaf" aria-hidden="true">✦</div><h2 tabindex="-1">Şimdi doğa dedektifi ol!</h2><p>Üç olayın bağlantısını bul. Sonra beş soruyla öğrendiklerini dene.</p><div class="activity-entry-tags"><span>3 bağlantı</span><span>5 soru</span><span>Kendi hızında</span></div><button type="button" class="activity-primary" data-act="start-game">Oyuna başla →</button><button type="button" class="activity-listen" data-act="listen" aria-pressed="false">Dinle</button></div>`;
      }
      if(view==='quiz-intro'){
        this.clipId=this.id+'-quiz-intro';body=`<div class="activity-entry"><span class="activity-kicker">OYUN TAMAMLANDI ✓</span><h2 tabindex="-1">Şimdi sıra sende.</h2><p>Beş soruda birer cevap seç. Her doğru cevap 20 puan; her cevabın bir açıklaması var.</p><span class="activity-mini-note">Sınav puanın, dinleme durumundan ayrı tutulur.</span><button type="button" class="activity-primary" data-act="start-quiz">5 soruluk sınava başla →</button><button type="button" class="activity-listen" data-act="listen" aria-pressed="false">Dinle</button></div>`;
      }
      if(view==='game'||view==='quiz')body=this.question(view);
      if(view==='result')body=this.result();
      this.root.innerHTML=this.chrome(body,step);this.root.querySelector('h2')?.focus({preventScroll:true});this.root.scrollIntoView({block:'start',behavior:'instant'});if(autoplay)this.playClip(this.clipId);
    }
    question(kind){
      const isGame=kind==='game',state=this.state[kind],index=state.index,row=this.lesson[kind][index],answer=state.answers[index],submitted=answer!==null,correct=answer===row.answer,revealed=isGame&&state.tries[index]>=3,locked=submitted&&(!isGame||correct||revealed);
      this.clipId=this.id+'-'+kind+'-'+row.id;
      const options=row.options.map((text,i)=>`<label class="activity-choice ${submitted&&i===answer?'is-selected':''} ${locked&&i===row.answer?'is-correct':''} ${locked&&!correct&&i===answer?'is-wrong':''}"><input type="radio" name="activity-choice" value="${i}" ${submitted&&i===answer?'checked':''} ${submitted?'disabled':''}><span class="activity-letter" aria-hidden="true">${String.fromCharCode(65+i)}</span><span>${esc(text)}${locked&&i===row.answer?`<small>✓ ${isGame?'Doğru bağlantı':'Doğru cevap'}</small>`:locked&&!correct&&i===answer?'<small>Senin seçimin</small>':''}</span></label>`).join('');
      const feedback=submitted?`<section class="activity-feedback ${correct?'is-positive':'is-explained'}" aria-labelledby="activity-feedback-title"><h3 id="activity-feedback-title" tabindex="-1">${isGame?(correct?'Bağlantıyı kurdun!':revealed?'Bağlantıyı birlikte görelim.':'Bir kez daha düşünelim.'):correct?'Doğru cevap ✓':'Cevabına birlikte bakalım.'}</h3><p>${esc(isGame&&!correct&&!revealed?row.hint:row.explanation)}</p><button type="button" class="activity-text" data-act="review">İlgili sahneyi yeniden dinle ↺</button></section>`:'';
      let action;
      if(!submitted)action='<button type="submit" class="activity-primary" data-act="check" disabled>Cevabımı kontrol et</button>';
      else if(isGame&&!locked)action='<button type="button" class="activity-primary" data-act="retry-game">Tekrar dene →</button>';
      else action=`<button type="button" class="activity-primary" data-act="${isGame?'next-game':'next-quiz'}">${isGame?(index===this.lesson.game.length-1?'Sınava geç →':'Sonraki bağlantı →'):(index===this.lesson.quiz.length-1?'Sonucumu gör →':'Sonraki soru →')}</button>`;
      if(submitted)this.clipId=this.id+'-'+kind+'-'+row.id+(isGame&&!correct&&!revealed?'-hint':'-explanation');
      return `<header class="activity-question-top"><span class="activity-kicker">${isGame?'DOĞA DEDEKTİFİ':'MİNİ SINAV'}</span><span class="activity-counter">${index+1} / ${this.lesson[kind].length}</span></header>${isGame?`<img class="activity-picture" src="${url(row.image)}" alt="${esc(row.title)}" width="1672" height="941">`:''}<form class="activity-form"><fieldset><legend><h2 tabindex="-1">${esc(isGame?row.title:'Soru '+(index+1))}</h2><p>${esc(row.prompt)}</p></legend><div class="activity-choices">${options}</div></fieldset>${feedback}<div class="activity-question-actions">${action}<button type="button" class="activity-listen" data-act="listen" aria-pressed="false">Dinle</button></div></form>`;
    }
    check(){
      if(!['game','quiz'].includes(this.view)||this.selected===null)return;
      const kind=this.view,s=this.state[kind],row=this.lesson[kind][s.index];if(s.answers[s.index]!==null||!valid(this.selected,row.options.length))return;
      s.answers[s.index]=this.selected;if(kind==='game')s.tries[s.index]=Math.min(3,s.tries[s.index]+1);this.persist();this.show(kind);const feedback=this.root.querySelector('#activity-feedback-title');feedback?.focus({preventScroll:true});feedback?.scrollIntoView({block:'center',behavior:'instant'});this.playClip(this.clipId);
    }
    finishQuiz(){
      const s=this.state;if(!s.quiz.active||s.quiz.answers.some(a=>a===null)||!gameDone(s,this.lesson)||s.heard.length!==this.lesson.sceneIds.length)return;
      s.latest=[...s.quiz.answers];if(!s.best||score(s.latest,this.lesson)>score(s.best,this.lesson))s.best=[...s.latest];s.attemptCount++;s.quiz.active=false;this.persist();this.options.onComplete?.(summary(this.id));this.show('result',true);
    }
    result(){
      const s=this.state;if(!s.latest)return '';const last=score(s.latest,this.lesson),best=score(s.best||s.latest,this.lesson);this.clipId=this.id+'-result-'+last;
      return `<div class="activity-result"><span class="activity-kicker">ÇALIŞMANI TAMAMLADIN</span><h2 tabindex="-1">${last===100?'Bağlantıları kurdun!':last>=60?'Keşfe devam ediyoruz!':'Birlikte pekiştirelim.'}</h2><div class="activity-score" style="--score:${last}%"><strong>${last}<small>/ 100</small></strong></div><p>Son denemende <b>${last/20} / 5</b> doğru cevap.</p><span class="activity-best">En iyi puanın: ${best} / 100</span><div class="activity-result-status"><span>✓ Hikâye dinlendi</span><span>✓ 3 bağlantı incelendi</span><span>✓ 5 soru cevaplandı</span></div><div class="activity-badge"><span aria-hidden="true">✦</span><span><b>${esc(this.lesson.badge)}</b><small>Etkinlik katılım rozeti</small></span></div><button type="button" class="activity-primary" data-act="continue">${esc(this.options.continueLabel||'Konulara dön')} →</button><button type="button" class="activity-secondary" data-act="retake">Soruları tekrar dene ↺</button><button type="button" class="activity-listen" data-act="listen" aria-pressed="false">▷ Sonucumu dinle</button><details class="activity-answer-review"><summary>Cevaplarımı ve açıklamaları gör</summary>${this.lesson.quiz.map((q,i)=>`<article><h3>${i+1}. ${esc(q.prompt)}</h3><p>Senin cevabın: ${esc(q.options[s.latest[i]])}</p><p><b>Doğru cevap:</b> ${esc(q.options[q.answer])}</p><p>${esc(q.explanation)}</p></article>`).join('')}</details><p class="activity-mini-note">İlerlemen ve puanların bu tarayıcıda saklanır.</p></div>`;
    }
    review(){
      if(!['game','quiz'].includes(this.view))return;this.beforeReview=this.view;const row=this.lesson[this.view][this.state[this.view].index],production=window.MERAK_PRODUCTIONS?.find(p=>p.id===this.lesson.productionId),scene=production?.scenes[row.scene];if(!scene)return;
      this.stop();this.root.innerHTML=`<section class="lesson-activities"><button type="button" class="activity-text" data-act="return">← Etkinliğe dön</button><div id="activity-review-player"></div></section>`;
      this.reviewPlayer=MerakNarration.mount(this.root.querySelector('#activity-review-player'),{title:'Hikâyeden hatırla',scenes:[scene],autoplay:true,onComplete:()=>this.show(this.beforeReview)});
    }
    destroy(){if(this.dead)return;this.stop();this.reviewPlayer?.destroy();this.reviewPlayer=null;this.dead=true;this.root.removeEventListener('click',this.click);this.root.removeEventListener('change',this.change);this.root.removeEventListener('submit',this.submit);document.removeEventListener('visibilitychange',this.hidden);window.removeEventListener('merak-navigation-open',this.hiddenPause);this.dialogObserver.disconnect();if(active===this)active=null;}
  }
  window.MerakLessonActivities={has,summary,recordHeard,mount:(root,options)=>has(options.id)?new Activity(root,options):null,pause:()=>active?.pause(),destroy:()=>active?.destroy(),get active(){return active;}};
  window.addEventListener('beforeunload',()=>active?.destroy());
})();
