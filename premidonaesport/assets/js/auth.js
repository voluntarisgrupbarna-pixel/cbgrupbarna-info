/* CB Grup Barna · Accés protegit del dossier del Premi Dona i Esport
   ------------------------------------------------------------------
   Codi: 1965 (el mateix any de fundació que surt al peu de la pantalla).

   Tres coses que s'hi han arreglat:

   1. Hi havia DUES portes. Les tres portades (/premidonaesport/ i les seves
      versions /es/ i /en/) portaven, a més d'aquesta, una segona reixa amb
      quatre caselles de PIN escrita dins de l'HTML, amb el mateix codi i una
      clau de sessió diferent. Qui hi arribava havia de teclejar 1965 dues
      vegades. Ara la porta és aquesta i prou, i reconeix les dues claus
      antigues perquè ningú no hagi de tornar a entrar-hi.
   2. No hi havia sortida. Qui no té el codi es quedava en un carreró: ni un
      enllaç. Ara hi ha la pàgina pública de bàsquet femení, que és on hi ha
      aquest mateix contingut resumit i obert a tothom.
   3. Sortia sempre en català, també a /es/ i /en/.
*/
(function(){
  'use strict';
  var KEY='cbgb_access_v1';
  var KEY_ALT='cbgb_premi_ok';   // la de la reixa antiga de les portades
  var CODE='1965';

  function jaObert(){
    try{ return sessionStorage.getItem(KEY)==='1' || sessionStorage.getItem(KEY_ALT)==='1'; }
    catch(e){ return false; }
  }
  if(jaObert()) return;

  var LG=(document.documentElement.lang||'ca').slice(0,2).toLowerCase();
  var T={
    ca:{ area:'CB Grup Barna · Àrea privada', t1:'Accés', t2:'restringit',
         sub:'Introdueix el codi per continuar', ph:'Codi d\'accés', btn:'Entrar →',
         err:'Codi incorrecte. Torna-ho a intentar.',
         sortida:'No tens el codi? Mira el projecte femení del club →', url:'/femeni/',
         aria:'Accés restringit al dossier' },
    es:{ area:'CB Grup Barna · Área privada', t1:'Acceso', t2:'restringido',
         sub:'Introduce el código para continuar', ph:'Código de acceso', btn:'Entrar →',
         err:'Código incorrecto. Inténtalo de nuevo.',
         sortida:'¿No tienes el código? Mira el proyecto femenino del club →', url:'/es/baloncesto-femenino/',
         aria:'Acceso restringido al dosier' },
    en:{ area:'CB Grup Barna · Private area', t1:'Restricted', t2:'access',
         sub:'Enter the code to continue', ph:'Access code', btn:'Enter →',
         err:'Wrong code. Try again.',
         sortida:"Don't have the code? See the club's women's project →", url:'/en/womens-basketball/',
         aria:'Restricted access to the dossier' }
  }[LG] || null;
  if(!T) T={ area:'CB Grup Barna', t1:'Accés', t2:'restringit', sub:'Introdueix el codi per continuar',
             ph:'Codi', btn:'Entrar →', err:'Codi incorrecte.', sortida:'Bàsquet femení →',
             url:'/femeni/', aria:'Accés restringit' };

  /* Amaga el contingut immediatament per evitar flash */
  var hideStyle=document.createElement('style');
  hideStyle.textContent='body{visibility:hidden!important;background:#040404!important;overflow:hidden!important}';
  (document.head||document.documentElement).appendChild(hideStyle);

  function unlock(){
    try{ sessionStorage.setItem(KEY,'1'); sessionStorage.setItem(KEY_ALT,'1'); }catch(e){}
    var g=document.getElementById('cbgb-gate');
    if(g)g.remove();
    hideStyle.remove();
    document.body.style.visibility='';
    document.body.style.overflow='';
  }

  function showGate(){
    hideStyle.textContent='';
    document.body.style.visibility='visible';
    document.body.style.background='#040404';
    document.body.style.overflow='hidden';

    var gate=document.createElement('div');
    gate.id='cbgb-gate';
    gate.setAttribute('role','dialog');
    gate.setAttribute('aria-modal','true');
    gate.setAttribute('aria-label',T.aria);
    gate.innerHTML='<style>'
      +'#cbgb-gate{position:fixed;inset:0;z-index:99999;background:#040404;display:flex;align-items:center;justify-content:center;padding:2rem;font-family:\'Inter\',system-ui,sans-serif}'
      +'#cbgb-gate *{box-sizing:border-box}'
      +'.cbgb-wrap{text-align:center;max-width:420px;width:100%;animation:cbgbIn .9s ease forwards}'
      +'@keyframes cbgbIn{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}'
      +'.cbgb-logo{height:72px;width:auto;filter:drop-shadow(0 0 18px rgba(226,6,19,.45));margin-bottom:1.75rem}'
      +'.cbgb-ey{font-size:.5rem;letter-spacing:.4em;text-transform:uppercase;color:#FF3B41;margin-bottom:1.1rem}'
      +'.cbgb-title{font-family:\'Anton\',\'Haettenschweiler\',\'Arial Narrow\',sans-serif;font-size:clamp(1.8rem,5vw,2.6rem);font-weight:700;color:#F4F1EC;line-height:1.1;margin-bottom:.4rem}'
      +'.cbgb-title .r{color:#E20613;font-style:italic}'
      +'.cbgb-sub{font-family:\'Anton\',\'Haettenschweiler\',\'Arial Narrow\',sans-serif;font-size:clamp(.85rem,2.5vw,1rem);color:rgba(244,241,236,.78);margin-bottom:2.25rem}'
      +'.cbgb-form{display:flex;flex-direction:column;gap:.75rem;align-items:center}'
      +'.cbgb-input{background:transparent;border:1px solid rgba(226,6,19,.35);color:#F4F1EC;padding:.85rem 1.25rem;font-family:\'Inter\',system-ui,sans-serif;font-size:1.1rem;letter-spacing:.35em;text-align:center;width:min(260px,85vw);outline:none;transition:border-color .25s ease}'
      +'.cbgb-input:focus{border-color:#FF3B41}'
      +'.cbgb-input::placeholder{color:rgba(244,241,236,.78);letter-spacing:.15em;font-size:.75rem}'
      +'.cbgb-btn{background:#E20613;border:none;color:#fff;padding:.85rem 2rem;font-family:\'Inter\',system-ui,sans-serif;font-size:.68rem;font-weight:500;letter-spacing:.25em;text-transform:uppercase;cursor:pointer;transition:all .25s ease;width:min(260px,85vw)}'
      +'.cbgb-btn:hover{background:#a50d26}'
      +'.cbgb-err{color:#ff4060;font-size:.65rem;letter-spacing:.1em;display:none;margin-top:.25rem}'
      +'.cbgb-foot{margin-top:2.5rem;font-size:.5rem;letter-spacing:.2em;text-transform:uppercase;color:rgba(244,241,236,.78)}'
      +'.cbgb-out{display:inline-block;margin-top:1.6rem;font-size:.72rem;color:rgba(244,241,236,.72);border-bottom:1px solid rgba(226,6,19,.6);text-decoration:none;padding-bottom:2px}'
      +'.cbgb-out:hover,.cbgb-out:focus-visible{color:#F4F1EC;border-color:#FF3B41}'
      +'.cbgb-input:focus-visible,.cbgb-btn:focus-visible{outline:2px solid #FF3B41;outline-offset:2px}'
      +'</style>'
      +'<div class="cbgb-wrap">'
        +'<img src="/premidonaesport/assets/img/logo-barna.webp" alt="CB Grup Barna" class="cbgb-logo">'
        +'<div class="cbgb-ey">'+T.area+'</div>'
        +'<p class="cbgb-title">'+T.t1+' <span class="r">'+T.t2+'</span></p>'
        +'<p class="cbgb-sub">'+T.sub+'</p>'
        +'<form class="cbgb-form" id="cbgb-gate-form" autocomplete="off">'
          +'<input id="cbgb-gate-input" class="cbgb-input" type="text" inputmode="numeric" placeholder="'+T.ph+'" aria-label="'+T.ph+'" aria-describedby="cbgb-gate-err" maxlength="20" autocomplete="off" spellcheck="false">'
          +'<button type="submit" class="cbgb-btn">'+T.btn+'</button>'
          +'<span id="cbgb-gate-err" class="cbgb-err" role="alert">'+T.err+'</span>'
        +'</form>'
        +'<a class="cbgb-out" href="'+T.url+'">'+T.sortida+'</a>'
        +'<div class="cbgb-foot">CB Grup Barna · El Clot · Barcelona</div>'
      +'</div>';

    document.body.insertBefore(gate, document.body.firstChild);

    var inp=document.getElementById('cbgb-gate-input');
    var form=document.getElementById('cbgb-gate-form');
    var err=document.getElementById('cbgb-gate-err');

    setTimeout(function(){ if(inp) inp.focus(); }, 120);

    if(form) form.addEventListener('submit',function(e){
      e.preventDefault();
      var val=(inp?inp.value:'').trim();
      if(val===CODE){
        unlock();
      } else {
        if(err) err.style.display='block';
        if(inp){ inp.value=''; inp.focus(); }
      }
    });

    /* Tecla Enter des de qualsevol lloc */
    document.addEventListener('keydown',function kd(e){
      if(e.key==='Enter' && document.getElementById('cbgb-gate')){
        if(document.activeElement!==inp) form && form.dispatchEvent(new Event('submit'));
      }
    });
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',showGate);
  } else {
    showGate();
  }
})();
