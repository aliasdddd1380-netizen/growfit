/* GrowFit service worker v6 — network-first, offline fallback.
   Cache name bumped (growfit-v2) so the new files replace the old cache; old caches are deleted on activate. */
const V='growfit-v2';
const FILES=['./','index.html','coach.html','form.html','sport.html','manifest-student.json','manifest-coach.json','icon-192.png','icon-512.png','icon-maskable-512.png','apple-touch-icon.png','fonts/Vazirmatn-Regular.woff2','fonts/Vazirmatn-Bold.woff2'];
self.addEventListener('install',e=>{
  /* tolerant: a missing optional file (font, icon) must not break the whole install */
  e.waitUntil(caches.open(V).then(c=>Promise.allSettled(FILES.map(f=>c.add(f)))).then(()=>self.skipWaiting()));
});
self.addEventListener('activate',e=>{
  e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
self.addEventListener('fetch',e=>{
  const r=e.request;
  if(r.method!=='GET')return;
  let u;try{u=new URL(r.url)}catch(x){return}
  if(u.origin!==self.location.origin)return;
  e.respondWith(
    fetch(r).then(res=>{
      if(res&&res.ok&&res.type==='basic'){const cp=res.clone();caches.open(V).then(c=>c.put(r,cp)).catch(()=>{})}
      return res;
    }).catch(()=>caches.match(r,{ignoreSearch:true}).then(m=>m||(r.mode==='navigate'?caches.match('index.html'):undefined)||Response.error()))
  );
});
