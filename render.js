function draw(){
  var m=E.m; if(!m) return;
  g.clearRect(0,0,W,W); g.lineCap="round";
  var SH={dia:0,nose:0,coh:4,sigh:3,box:4,temp:6,co2:3};
  var S=SH[m.id]; if(S===undefined) S=0;
  var n=E.tl.length,i,v=[],t,R=250,cur=E.tl[E.idx];
  var pp=cur?Math.min(1,E.t/cur.sec):0, pr, tot;
  if(!S){
    tot=2*Math.PI*R; pr=(E.idx+pp)/n;
    g.beginPath(); g.arc(C,C,R,0,6.2832);
  } else {
    var done=((E.cyc-1)*n + E.idx + pp)/S;
    pr=done-Math.floor(done);
    for(i=0;i<S;i++){ t=-1.5708+i*2*Math.PI/S; v.push([C+R*Math.cos(t),C+R*Math.sin(t)]); }
    g.beginPath(); g.moveTo(v[0][0],v[0][1]);
    for(i=1;i<S;i++) g.lineTo(v[i][0],v[i][1]);
    g.closePath();
    tot=S*2*R*Math.sin(Math.PI/S);
  }
  g.lineWidth=6; g.strokeStyle="rgba(255,255,255,.12)"; g.stroke();
  g.save(); g.setLineDash([tot*pr,tot*2]); g.lineWidth=8; g.strokeStyle="#8fd0ff"; g.stroke(); g.restore();
}
