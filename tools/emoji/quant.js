const {chromium}=require('playwright');const fs=require('fs');
const cands=JSON.parse(fs.readFileSync('cands.json','utf8'));
const PAL={R:'#E53935',O:'#FB8C00',Y:'#FDD835',G:'#43A047',B:'#1E88E5',P:'#8E24AA',K:'#F06292',N:'#7B5136',W:'#F5F5F5',D:'#1E1E1E',C:'#26C6DA',
 M:'#A0182E',L:'#A5D63A',A:'#8FD3FF',V:'#B79CE6',T:'#00897B',E:'#F8BBD9',H:'#8EE3C3',I:'#FFCC99',J:'#FFF3A3',Q:'#757F8A',U:'#D7B98E'};
const G=40,S=160;
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.setContent('<canvas id=c width=160 height=160></canvas>');
await p.evaluate(PAL=>{const toLab=h=>{let r=parseInt(h.slice(1,3),16)/255,g=parseInt(h.slice(3,5),16)/255,b=parseInt(h.slice(5,7),16)/255;return lab(r,g,b)};
 window.lab=(r,g,b)=>{const f=c=>c>0.04045?Math.pow((c+0.055)/1.055,2.4):c/12.92;r=f(r);g=f(g);b=f(b);let x=(r*.4124+g*.3576+b*.1805)/.95047,y=r*.2126+g*.7152+b*.0722,z=(r*.0193+g*.1192+b*.9505)/1.08883;const q=t=>t>0.008856?Math.cbrt(t):7.787*t+16/116;x=q(x);y=q(y);z=q(z);return[116*y-16,500*(x-y),200*(y-z)]};
 window.PL=Object.entries(PAL).map(([k,h])=>[k,toLab(h)]);window.near=(r,g,b)=>{const L=lab(r/255,g/255,b/255);let bk=null,bd=1e9;for(const[k,l]of PL){const d=(L[0]-l[0])**2+(L[1]-l[1])**2+(L[2]-l[2])**2;if(d<bd){bd=d;bk=k}}return bk}},PAL);
const res=[];
for(const c of cands){const svg=fs.readFileSync(c.svg,'utf8');
 const r=await p.evaluate(async({svg,G,S})=>{const img=new Image();img.src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(svg)));await img.decode();const cv=document.getElementById('c'),x=cv.getContext('2d');x.clearRect(0,0,S,S);x.drawImage(img,0,0,S,S);
  const d=x.getImageData(0,0,S,S).data,bs=S/G,grid=[];const cache=new Map();
  for(let gy=0;gy<G;gy++){let row='';for(let gx=0;gx<G;gx++){const cnt={};let op=0;for(let yy=0;yy<bs;yy++)for(let xx=0;xx<bs;xx++){const i=((gy*bs+yy)*S+gx*bs+xx)*4;if(d[i+3]<128)continue;op++;const key=(d[i]>>3)<<10|(d[i+1]>>3)<<5|(d[i+2]>>3);let k=cache.get(key);if(!k){k=near(d[i],d[i+1],d[i+2]);cache.set(key,k)}cnt[k]=(cnt[k]||0)+1}
    if(op<bs*bs*0.5){row+='.';continue}let bk='.',bc=-1;for(const k in cnt)if(cnt[k]>bc){bc=cnt[k];bk=k}row+=bk}grid.push(row)}return grid},{svg,G,S});
 res.push({...c,grid:r})}
fs.writeFileSync('quant.json',JSON.stringify(res));console.log('done',res.length);await b.close()})();
