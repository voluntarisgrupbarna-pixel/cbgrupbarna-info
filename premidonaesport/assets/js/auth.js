/* CB Grup Barna · Accés protegit · Codi: 1965 */
(function(){
  'use strict';
  var KEY='cbgb_access_v1';
  var CODE='1965';

  if(sessionStorage.getItem(KEY)==='1') return;

  /* Amaga el contingut immediatament per evitar flash */
  var hideStyle=document.createElement('style');
  hideStyle.textContent='body{visibility:hidden!important;background:#040404!important;overflow:hidden!important}';
  (document.head||document.documentElement).appendChild(hideStyle);

  function unlock(){
    sessionStorage.setItem(KEY,'1');
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
    gate.innerHTML='<style>'
      +'#cbgb-gate{position:fixed;inset:0;z-index:99999;background:#040404;display:flex;align-items:center;justify-content:center;padding:2rem;font-family:\'Inter\',system-ui,sans-serif}'
      +'#cbgb-gate *{box-sizing:border-box}'
      +'.cbgb-wrap{text-align:center;max-width:420px;width:100%;animation:cbgbIn .9s ease forwards}'
      +'@keyframes cbgbIn{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}'
      +'.cbgb-logo{height:72px;width:auto;filter:drop-shadow(0 0 18px rgba(226,6,19,.45));margin-bottom:1.75rem}'
      +'.cbgb-ey{font-size:.5rem;letter-spacing:.4em;text-transform:uppercase;color:#FF3B41;margin-bottom:1.1rem}'
      +'.cbgb-title{font-family:\'Anton\',\'Haettenschweiler\',\'Arial Narrow\',sans-serif;font-size:clamp(1.8rem,5vw,2.6rem);font-weight:700;color:#F4F1EC;line-height:1.1;margin-bottom:.4rem}'
      +'.cbgb-title .r{color:#E20613;font-style:italic}'
      +'.cbgb-sub{font-family:\'Anton\',\'Haettenschweiler\',\'Arial Narrow\',sans-serif;font-size:clamp(.85rem,2.5vw,1rem);color:rgba(244,241,236,.4);margin-bottom:2.25rem}'
      +'.cbgb-form{display:flex;flex-direction:column;gap:.75rem;align-items:center}'
      +'.cbgb-input{background:transparent;border:1px solid rgba(226,6,19,.35);color:#F4F1EC;padding:.85rem 1.25rem;font-family:\'Inter\',system-ui,sans-serif;font-size:1.1rem;letter-spacing:.35em;text-align:center;width:min(260px,85vw);outline:none;transition:border-color .25s ease}'
      +'.cbgb-input:focus{border-color:#FF3B41}'
      +'.cbgb-input::placeholder{color:rgba(244,241,236,.2);letter-spacing:.15em;font-size:.75rem}'
      +'.cbgb-btn{background:#E20613;border:none;color:#F4F1EC;padding:.85rem 2rem;font-family:\'Inter\',system-ui,sans-serif;font-size:.68rem;font-weight:500;letter-spacing:.25em;text-transform:uppercase;cursor:pointer;transition:all .25s ease;width:min(260px,85vw)}'
      +'.cbgb-btn:hover{background:#a50d26}'
      +'.cbgb-err{color:#ff4060;font-size:.65rem;letter-spacing:.1em;display:none;margin-top:.25rem}'
      +'.cbgb-foot{margin-top:2.5rem;font-size:.5rem;letter-spacing:.2em;text-transform:uppercase;color:rgba(244,241,236,.55)}'
      +'</style>'
      +'<div class="cbgb-wrap">'
        +'<img src="/premidonaesport/assets/img/logo-barna.webp" alt="CB Grup Barna" class="cbgb-logo">'
        +'<div class="cbgb-ey">CB Grup Barna · Àrea privada</div>'
        +'<h1 class="cbgb-title">Accés <span class="r">restringit</span></h1>'
        +'<p class="cbgb-sub">Introdueix el codi per continuar</p>'
        +'<form class="cbgb-form" id="cbgb-gate-form" autocomplete="off">'
          +'<input id="cbgb-gate-input" class="cbgb-input" type="text" inputmode="numeric" placeholder="Codi d\'accés" maxlength="20" autocomplete="off" spellcheck="false">'
          +'<button type="submit" class="cbgb-btn">Entrar →</button>'
          +'<span id="cbgb-gate-err" class="cbgb-err">Codi incorrecte. Torna-ho a intentar.</span>'
        +'</form>'
        +'<div class="cbgb-foot">CB Grup Barna · El Clot · Barcelona · 1965</div>'
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
