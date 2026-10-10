(function(){
  var spd=document.getElementById("segSpd");
  if(spd&&spd.parentNode){
    var wrap=document.createElement("div");
    wrap.innerHTML='<div class="seg" id="segMode"><button data-m="cyc" class="on">按次数</button><button data-m="time">按时间</button><button data-m="free">自由</button></div><div class="seg" id="segVal" style="margin-top:8px"></div>';
    spd.parentNode.insertBefore(wrap, spd.nextSibling);
    var segMode=document.getElementById("segMode"), segVal=document.getElementById("segVal");
    var CY=[3,6,10,20], TI=[5,10,15,20];
    function renderVal(){
      var mo=window.__mode||"cyc";
      if(mo==="free"){ segVal.innerHTML='<button class="on">不限</button>'; return; }
      var arr=(mo==="cyc")?CY:TI, dft=(mo==="cyc")?6:10, v0=window.__val||dft;
      segVal.innerHTML=arr.map(function(v){return '<button data-v="'+v+'"'+(v===v0?' class="on"':'')+'>'+v+(mo==="cyc"?" 次":" 分")+'</button>';}).join("");
      segVal.querySelectorAll("button").forEach(function(b){
        b.onclick=function(){ segVal.querySelectorAll("button").forEach(function(x){x.classList.remove("on")}); b.classList.add("on"); window.__val=+b.dataset.v; };
      });
    }
    segMode.querySelectorAll("button").forEach(function(b){
      b.onclick=function(){ segMode.querySelectorAll("button").forEach(function(x){x.classList.remove("on")}); b.classList.add("on"); window.__mode=b.dataset.m; window.__val=null; renderVal(); };
    });
    window.__mode="cyc"; renderVal();
  }
  var _cyc=cycOf;
  cycOf=function(m,lv){
    if(window.__mode==="free"||window.__mode==="time") return 999999;
    if(window.__mode==="cyc") return window.__val||_cyc(m,lv);
    return _cyc(m,lv);
  };
  setInterval(function(){
    if(window.__mode!=="time"||!E||E.mode!=="run") return;
    if(E.elapsed>=(window.__val||10)*60){ E.mode="idle"; finish(); }
  },400);
  var st=document.querySelector("#g .stage");
  if(st){
    var box=document.createElement("div");
    box.style.cssText="position:absolute;top:10px;right:14px;font-size:13px;color:#9fb3cc;letter-spacing:.08em";
    st.appendChild(box);
    setInterval(function(){
      if(!E||!E.m) return;
      if(window.__mode==="time"){
        var left=Math.max(0,(window.__val||10)*60-E.elapsed);
        box.textContent=Math.floor(left/60)+":"+("0"+Math.floor(left%60)).slice(-2);
      } else if(window.__mode==="free"){
        box.textContent="自由 · "+E.switches+" 相位";
      } else {
        var t=cycOf(E.m,E.curLv||1);
        box.textContent="循环 "+Math.min(E.cyc,t)+" / "+t;
      }
    },200);
  }
  var skip=document.getElementById("gSkip");
  if(skip){ skip.textContent="完成"; skip.onclick=function(){ if(E.mode!=="idle"){ finish(); } }; }
})();
