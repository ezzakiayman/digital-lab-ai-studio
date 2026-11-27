// Rasterize the portable, editable layer tracks independently of Remotion's lesson components.
// The resulting images test the handoff manifest. This is not an Adobe After Effects render.
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import path from 'node:path';
import {openBrowser} from '@remotion/renderer';

const [projectFile, planFile, output] = process.argv.slice(2);
if (!projectFile || !planFile || !output) throw Error('Use check-render.mjs <project.json> <frames.json> <output>');
const root = path.dirname(path.resolve(projectFile));
const project = JSON.parse(await readFile(projectFile, 'utf8'));
const frames = JSON.parse(await readFile(planFile, 'utf8'));
await mkdir(output,{recursive:true});
const images=new Map();

function interpolated(a,b,t){
 if(typeof a==='number'&&typeof b==='number') return a+(b-a)*t;
 if(Array.isArray(a)&&Array.isArray(b)&&a.length===b.length)return a.map((v,i)=>interpolated(v,b[i],t));
 if(a?.vertices&&b?.vertices&&a.vertices.length===b.vertices.length)
  return Object.fromEntries(Object.entries(a).map(([key,value])=>[key,interpolated(value,b[key],t)]));
 return t<1?a:b;
}
function prop(spec,frame,fallback){
 if(spec===undefined||spec===null)return fallback;
 if(!spec.keys||Array.isArray(spec)||typeof spec.keys!=='object')return spec;
 const keys=spec.keys;
 if(frame<=keys[0][0])return keys[0][1];
 for(let i=1;i<keys.length;i++){
  const [time,value]=keys[i];
  if(frame===time)return value;
  if(frame<time){
   const [start,prev,hold]=keys[i-1];
   return hold?prev:interpolated(prev,value,(frame-start)/(time-start));
  }
 }
 return keys.at(-1)[1];
}
function rgb(color){
 return color?'rgb('+color.slice(0,3).map(n=>Math.round(n*255)).join(',')+')':'none';
}
const xml=v=>String(v).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const xy=(v,i)=>String(v[i]);
function curve(shape){
 const {vertices:pts,inTangents:ins,outTangents:outs,closed}=shape;
 let d='M'+pts[0].join(' ');
 for(let i=1;i<pts.length+(closed?1:0);i++){
  const j=i%pts.length,k=i-1;
  const ctr1=[pts[k][0]+outs[k][0],pts[k][1]+outs[k][1]];
  const ctr2=[pts[j][0]+ins[j][0],pts[j][1]+ins[j][1]];
  d+='C'+ctr1+' '+ctr2+' '+pts[j];
 }
 return d+(closed?'Z':'');
}
function family(font){
 if(/Arial/i.test(font))return 'Arial';
 if(/CambriaMath/i.test(font))return 'Cambria Math';
 if(/Cambria/i.test(font))return 'Cambria';
 if(/TimesNewRoman/i.test(font))return 'Times New Roman';
 return font;
}
async function renderLayer(layer,local,idx){
 if(local<layer.start||local>=layer.end)return '';
 const v=(key,def)=>prop(layer[key],local,def);
 const p=v('position',[0,0]),s=v('scale',[100,100]),r=v('rotation',0),a=v('anchor',[0,0]);
 const opacity=v('opacity',100)/100;
 if(opacity<=0)return '';
 const transform='translate('+xy(p,0)+' '+xy(p,1)+') rotate('+r+') scale('+s[0]/100+' '+s[1]/100+') translate('+(-a[0])+' '+(-a[1])+')';
 const color=rgb(v('fill',null)),stroke=rgb(v('stroke',null));
 let child='';
 if(layer.type==='text'){
  const font=v('font','ArialMT');
  const justify=String(v('justify','left')).toLowerCase();
  child='<text x="0" y="0" text-anchor="'+(justify.includes('center')?'middle':justify.includes('right')?'end':'start')+
   '" xml:space="preserve" font-family="'+xml(family(font))+'" font-weight="'+(/bold|semibold|heavy/i.test(font)?'700':'400')+
   '" font-style="'+(/italic|oblique/i.test(font)?'italic':'normal')+'" font-size="'+v('size',60)+'" fill="'+color+'">'+xml(v('text',''))+'</text>';
 }else if(layer.type==='path'){
  const end=v('trimEnd',100);
  const dash=end<100?' pathLength="1" stroke-dasharray="1 2" stroke-dashoffset="'+(1-end/100)+'"':'';
  child='<path d="'+curve(v('path'))+'" fill="'+color+'" stroke="'+stroke+'" stroke-width="'+v('strokeWidth',0)+
   '" stroke-linecap="'+v('lineCap','butt')+'" stroke-linejoin="'+v('lineJoin','miter')+'"'+dash+'/>';
 }else if(layer.type==='image'){
  const asset=v('asset');
  if(!images.has(asset)){
   const bytes=await readFile(path.resolve(root,asset)); const png=bytes.subarray(1,4).toString()==='PNG';
   if(!png)throw Error('Unsupported image type for QA: '+asset);
   images.set(asset,{src:'data:image/png;base64,'+bytes.toString('base64'),width:bytes.readUInt32BE(16),height:bytes.readUInt32BE(20)});
  }
  const img=images.get(asset);
  child='<image x="0" y="0" width="'+v('width',img.width)+'" height="'+v('height',img.height)+'" href="'+img.src+'"/>';
 }
 let result='<g opacity="'+opacity+'" transform="'+transform+'">'+child+'</g>';
 const mask=v('maskRect',null);
 if(mask){
  result='<defs><clipPath id="clip'+idx+'"><rect x="'+mask[0]+'" y="'+mask[1]+'" width="'+Math.max(0,mask[2])+
   '" height="'+Math.max(0,mask[3])+'"/></clipPath></defs><g clip-path="url(#clip'+idx+')">'+result+'</g>';
 }
 return result;
}

const browser=await openBrowser('chrome');
try{
 const page=await browser.newPage({context:()=>null,logLevel:'error',indent:false,pageIndex:0,onBrowserLog:null,onLog:()=>{}});
 await page.setViewport({width:project.width,height:project.height,deviceScaleFactor:1});
 await page.goto({url:'about:blank',timeout:30000});
 for(const frame of frames){
  let offset=0;
  const scene=project.scenes.find(s=>{if(frame<offset+s.frames)return true;offset+=s.frames;return false;});
  if(!scene)throw Error('Bad frame '+frame);
  const nodes=[];
  for(const [i,layer] of scene.layers.entries())nodes.push(await renderLayer(layer,frame-offset,i));
  const markup='<svg xmlns="http://www.w3.org/2000/svg" width="'+project.width+'" height="'+project.height+
   '" viewBox="0 0 '+project.width+' '+project.height+'"><rect width="100%" height="100%" fill="white"/>'+nodes.join('')+'</svg>';
  await page.evaluate(async (svg)=>{
   document.body.style.cssText='margin:0;background:white;overflow:hidden';
   document.body.innerHTML=svg;
   await document.fonts.ready;
   await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  },markup);
  const {value:shot}=await page._client().send('Page.captureScreenshot',{format:'png',fromSurface:true, captureBeyondViewport:false});
  await writeFile(path.join(output,'f'+String(frame).padStart(6,'0')+'.png'),Buffer.from(shot.data,'base64'));
 }
}finally{await browser.close({silent:true});}
console.log('Rasterized '+frames.length+' independently reconstructed frames.');

