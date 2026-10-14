(function(){
  var $=function(s){return document.querySelector(s)},$$=function(s){return document.querySelectorAll(s)},B=document.body;
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function set(k,v){try{v===null?localStorage.removeItem(k):localStorage.setItem(k,v)}catch(e){}}

  /* Ichki sahifalar: kirmagan bo'lsa bosh sahifaga qaytaradi */
  if(B.hasAttribute('data-private')){
    if(!get('access'))location.replace(B.dataset.home);
    var u=$('#userName');if(u)u.textContent=get('phone')||'';
    $('#logout').addEventListener('click',function(){['access','refresh','phone'].forEach(function(k){set(k,null)});location.href=B.dataset.home});
  }

  /* Vazifalar filtri */
  $$('[data-filter]').forEach(function(b){b.addEventListener('click',function(){
    $$('[data-filter]').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
    $$('[data-st]').forEach(function(r){r.hidden=b.dataset.filter!=='all'&&r.dataset.st!==b.dataset.filter});
  })});

  /* To'ygacha hisoblagich */
  var di=$('#weddingDate');
  if(di){var n=$('#days');
    var r=function(v){if(!v){n.textContent='—';return}var t=new Date();t.setHours(0,0,0,0);n.textContent=Math.max(0,Math.round((new Date(v+'T00:00:00')-t)/864e5))};
    var s=get('weddingDate');if(s){di.value=s;r(s)}
    di.addEventListener('change',function(){set('weddingDate',di.value);r(di.value)});
  }

  /* Kirish / ro'yxatdan o'tish oynasi (landing) */
  var dlg=$('#auth');if(!dlg)return;
  var mode='login',API='/api/v1/';
  function setMode(m){mode=m;$$('.dtabs button').forEach(function(b){b.setAttribute('aria-selected',b.dataset.mode===m)});
    $('#submitBtn').textContent=m==='login'?'Kirish':"Ro'yxatdan o'tish"}
  function open(m){if(get('access')){location.href=B.dataset.next;return}setMode(m);$('#err').textContent='';dlg.showModal();$('#phone').focus()}
  function post(u,b){return fetch(API+u,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)})
    .then(function(r){return r.json().catch(function(){return null}).then(function(d){return{ok:r.ok,d:d}})})}
  function msg(d){if(!d)return"Xatolik yuz berdi. Qayta urinib ko'ring.";if(d.detail)return d.detail;var v=d[Object.keys(d)[0]];return(Array.isArray(v)?v[0]:v)||"Xatolik yuz berdi."}
  $$('[data-open]').forEach(function(b){b.addEventListener('click',function(){open(b.dataset.open)})});
  $$('.dtabs button').forEach(function(b){b.addEventListener('click',function(){setMode(b.dataset.mode);$('#err').textContent=''})});
  $('#closeAuth').addEventListener('click',function(){dlg.close()});
  $('#authForm').addEventListener('submit',function(e){
    e.preventDefault();var body={phone_number:$('#phone').value.trim(),password:$('#pass').value};
    (mode==='register'?post('register/',body):Promise.resolve({ok:true})).then(function(r){
      if(!r.ok)throw r.d;return post('login/',body)}).then(function(r){
      if(!r.ok)throw r.d;set('access',r.d.access);set('refresh',r.d.refresh);set('phone',body.phone_number);location.href=B.dataset.next
    }).catch(function(d){$('#err').textContent=msg(d)});
  });
})();