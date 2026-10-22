'use strict';
// Public project settings only. Set these after the private question service is deployed.
window.MERAK_QUESTION_CONFIG=Object.freeze({supabaseUrl:'',publicKey:''});
window.MerakQuestions=(()=>{
 const cfg=window.MERAK_QUESTION_CONFIG;let session=null;
 try{const s=JSON.parse(sessionStorage.getItem('merak-qa-admin'));if(s?.expiresAt>Date.now())session=s;}catch{}
 const configured=()=>/^https:\/\/[a-z0-9.-]+\/?$/i.test(cfg.supabaseUrl)&&Boolean(cfg.publicKey);
 const isAdmin=()=>Boolean(session?.expiresAt>Date.now());
 async function call(path,body,admin=false){if(!configured())throw Error('Soru ve özel cevap hizmeti henüz bağlanmadı.');if(admin&&!isAdmin())throw Error('Eğitimci girişi gerekiyor.');const r=await fetch(cfg.supabaseUrl.replace(/\/$/,'')+path,{method:'POST',headers:{apikey:cfg.publicKey,'Content-Type':'application/json',...(session?.token?{Authorization:'Bearer '+session.token}:{})},body:JSON.stringify(body),cache:'no-store'});let data=null;try{data=await r.json();}catch{}
 if(!r.ok){if(admin&&(r.status===401||r.status===403)){session=null;try{sessionStorage.removeItem('merak-qa-admin');}catch{}}if(data?.code==='P0001')throw Error('Soru kutusu şu an yoğun. Daha sonra tekrar dene.');throw Error(r.status===401||r.status===403?'Giriş veya yetki doğrulanamadı.':'İşlem tamamlanamadı. Bilgileri ve bağlantını kontrol et.');}return data;}
 const rpc=(name,data,admin=false)=>call('/rest/v1/rpc/'+name,data,admin);
 const newCode=()=>Array.from(crypto.getRandomValues(new Uint8Array(32)),b=>b.toString(16).padStart(2,'0')).join('');
 async function submit(grade,topic,question,token){const result=await rpc('merak_question_create',{p_grade:grade,p_topic:topic,p_question:question,p_token:token});if(!result?.id)throw Error('Soru kaydı sunucu tarafından doğrulanamadı.');return result;}
 async function lookup(token){if(!/^[a-f0-9]{64}$/.test(token))throw Error('Takip kodu 64 karakter olmalı.');return rpc('merak_question_reply',{p_token:token});}
 async function login(email,password){const data=await call('/auth/v1/token?grant_type=password',{email,password});if(!data?.access_token)throw Error('Giriş doğrulanamadı.');session={token:data.access_token,expiresAt:Date.now()+(data.expires_in||3600)*1000};try{await list();try{sessionStorage.setItem('merak-qa-admin',JSON.stringify(session));}catch{}}catch(error){session=null;throw error;}}
 async function logout(){try{if(session)await call('/auth/v1/logout',{});}finally{session=null;try{sessionStorage.removeItem('merak-qa-admin');}catch{}}}
 async function list(){return rpc('merak_question_admin_list',{},true);}
 async function answer(id,text){return rpc('merak_question_answer',{p_id:id,p_answer:text},true);}
 return {configured,isAdmin,newCode,submit,lookup,login,logout,list,answer};
})();
