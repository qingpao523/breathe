function draw(){
  var m=E.m; if(!m) return;
  g.clearRect(0,0,W,W); g.lineCap="round";
  var SH={dia:0,nose:0,coh:4,sigh:3,box:4,temp:6,co2:3};
  var S=SH[m.id]; if(S===undefined) S=0;
  var n=E.tl.length, R=250, cur=E.tl[E.idx], i, t;
  var pp=cur?Math.min(1,E.t/cur.sec):0;
  if(!S){
    var tot=2*Math.PI*R, pr=(E.idx+pp)/n;
    g.beginPath(); g.arc(C,C,R,0,6.2832);
    g.lineWidth=6; g.strokeStyle="rgba(255,255,255,.10)"; g.stroke();
    g.save(); g.setLineDash([tot*pr,tot*2]);
    g.lineWidth=8; g.strokeStyle="#8fd0ff"; g.stroke(); g.restore();
    return;
  }
  var v=[];
  for(i=0;i<S;i++){ t=-1.5708+i*2*Math.PI/S; v.push([C+R*Math.cos(t),C+R*Math.sin(t)]); }
  g.beginPath(); g.moveTo(v[0][0],v[0][1]);
  for(i=1;i<S;i++) g.lineTo(v[i][0],v[i][1]);
  g.closePath(); g.lineWidth=6; g.strokeStyle="rgba(255,255,255,.10)"; g.stroke();
  var did=(E.cyc-1)*n + E.idx;
  var base=Math.floor(did/S)*S, k;
  for(k=base;k<did;k++){
    var A=v[k%S], B=v[(k+1)%S];
    g.beginPath(); g.moveTo(A[0],A[1]); g.lineTo(B[0],B[1]);
    g.lineWidth=8; g.strokeStyle="#5ee0ff"; g.stroke();
  }
  var ci=did%S, A2=v[ci], B2=v[(ci+1)%S];
  var hd=(cur&&(cur.k==="hold"||cur.k==="hold2"));
  g.setLineDash(hd?[7,13]:[]);
  g.beginPath(); g.moveTo(A2[0],A2[1]);
  g.lineTo(A2[0]+(B2[0]-A2[0])*pp, A2[1]+(B2[1]-A2[1])*pp);
  g.lineWidth=8; g.strokeStyle=hd?"rgba(255,158,203,.85)":"#8fd0ff"; g.stroke();
  g.setLineDash([]);
}
