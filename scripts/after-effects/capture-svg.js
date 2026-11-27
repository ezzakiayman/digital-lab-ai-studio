// Read the actual Chromium SVG painting primitives at the current Remotion frame.
// All coordinates are flattened into the composition before entering the interchange.
const round=x=>Math.round(x*1000)/1000;
const n=(el,key)=>Number(el.getAttribute(key)||0);
const point=(m,x,y)=>[round(m.a*x+m.c*y+m.e),round(m.b*x+m.d*y+m.f)];
const vector=(m,x,y)=>[round(m.a*x+m.c*y),round(m.b*x+m.d*y)];
const matrixScale=m=>Math.hypot(m.a,m.b);
const identity=()=>({vertices:[],inTangents:[],outTangents:[],closed:false});
const append=(g,x,y,inn=[0,0],out=[0,0])=>{g.vertices.push([x,y]);g.inTangents.push(inn);g.outTangents.push(out);};
const k=0.5522847498307936;
function converted(g,m){
 return {vertices:g.vertices.map(p=>point(m,...p)),inTangents:g.inTangents.map(p=>vector(m,...p)),
  outTangents:g.outTangents.map(p=>vector(m,...p)),closed:g.closed};
}
function rectangle(e){
 const g=identity(),x=n(e,'x'),y=n(e,'y'),w=n(e,'width'),h=n(e,'height');
 const a=Math.min(w/2,n(e,'rx')||n(e,'ry')),b=Math.min(h/2,n(e,'ry')||a);
 if(!a&&!b){for(const v of [[x,y],[x+w,y],[x+w,y+h],[x,y+h]])append(g,...v);}
 else{
  append(g,x+a,y,[-a*k,0]);append(g,x+w-a,y,[0,0],[a*k,0]);append(g,x+w,y+b,[0,-b*k]);
  append(g,x+w,y+h-b,[0,0],[0,b*k]);append(g,x+w-a,y+h,[a*k,0]);append(g,x+a,y+h,[0,0],[-a*k,0]);
  append(g,x,y+h-b,[0,b*k]);append(g,x,y+b,[0,0],[0,-b*k]);
 }
 g.closed=true;return g;
}
function ellipse(e){
 const x=n(e,'cx'),y=n(e,'cy'),a=n(e,'rx')||n(e,'r'),b=n(e,'ry')||n(e,'r');
 const g=identity();
 append(g,x+a,y,[0,-k*b],[0,k*b]);append(g,x,y+b,[k*a,0],[-k*a,0]);
 append(g,x-a,y,[0,k*b],[0,-k*b]);append(g,x,y-b,[-k*a,0],[k*a,0]);
 g.closed=true;return g;
}
function paths(d){
 const items=d.match(/[MmLlHhVvQqCcZz]|[-+]?(?:\d*\.)?\d+(?:e[-+]?\d+)?/gi)||[];
 const result=[];let g=null,x=0,y=0,oldX=0,oldY=0,i=0,op=null;
 function xy(dx,dy,relative){return [relative?x+dx:dx,relative?y+dy:dy];}
 const next=()=>{if(i>=items.length||/^[a-z]$/i.test(items[i]))throw Error('Invalid path '+d);return Number(items[i++]);};
 while(i<items.length){
  if(/^[a-z]$/i.test(items[i]))op=items[i++];
  if(!op)throw Error('No path command: '+d);
  const relative=op===op.toLowerCase();
  switch(op.toUpperCase()){
   case 'M':{
    [x,y]=xy(next(),next(),relative);g=identity();result.push(g);append(g,x,y);oldX=x;oldY=y;op=relative?'l':'L';break;
   }
   case 'L': [x,y]=xy(next(),next(),relative);append(g,x,y);break;
   case 'H': x=(relative?x:0)+next();append(g,x,y);break;
   case 'V': y=(relative?y:0)+next();append(g,x,y);break;
   case 'C':{
    const c1=xy(next(),next(),relative),c2=xy(next(),next(),relative),end=xy(next(),next(),relative);
    g.outTangents[g.vertices.length-1]=[c1[0]-x,c1[1]-y];append(g,...end,[c2[0]-end[0],c2[1]-end[1]]);
    [x,y]=end;break;
   }
   case 'Q':{
    const q=xy(next(),next(),relative),end=xy(next(),next(),relative);
    g.outTangents[g.vertices.length-1]=[(q[0]-x)*2/3,(q[1]-y)*2/3];
    append(g,...end,[(q[0]-end[0])*2/3,(q[1]-end[1])*2/3]);[x,y]=end;break;
   }
   case 'Z': g.closed=true;x=oldX;y=oldY;op=null;break;
   default:throw Error('Unsupported command '+op);
  }
 }
 return result;
}
function paint(css){
 if(css==='none')return [null,1];
 const arr=css.match(/[\d.]+/g)?.map(Number);
 if(!arr||arr.length<3||!css.startsWith('rgb'))throw Error('Unsupported paint '+css);
 return [arr.slice(0,3).map(v=>round(v/255)),arr.length>3?arr[3]:1];
}
function opacity(el,root){
 let value=1;
 for(let node=el;node&&node!==root.parentElement;node=node.parentElement)value*=Number(getComputedStyle(node).opacity);
 return value;
}
function maskRect(el){
 for(let node=el;node?.namespaceURI==='http://www.w3.org/2000/svg';node=node.parentElement){
  const id=node.getAttribute('clip-path')?.match(/#([^)]*)/);
  if(!id)continue;
  const rect=document.getElementById(id[1])?.querySelector('rect');
  if(!rect)throw Error('Unsupported clip '+id[1]);
  const m=node.getCTM();return [...point(m,n(rect,'x'),n(rect,'y')),...vector(m,n(rect,'width'),n(rect,'height'))];
 }
 return null;
}
function font(css){
 const f=css.fontFamily.split(',')[0].trim().replace(/["']/g,'');
 const bold=Number(css.fontWeight)>=600, italic=css.fontStyle==='italic';
 if(f==='Cambria Math')return 'CambriaMath';
 if(f==='Cambria')return 'Cambria'+(bold?(italic?'-BoldItalic':'-Bold'):(italic?'-Italic':''));
 if(f==='Arial')return 'Arial'+(bold?(italic?'-BoldItalicMT':'-BoldMT'):(italic?'-ItalicMT':'MT'));
 throw Error('Unmapped native font '+css.fontFamily);
}
const baselineCache=new Map();
function alphabeticOffset(css){
 const baseline=css.dominantBaseline;
 if(baseline==='auto'||baseline==='alphabetic')return 0;
 const key=[baseline,css.fontFamily,css.fontWeight,css.fontSize,css.fontStyle].join('|');
 if(baselineCache.has(key))return baselineCache.get(key);
 // SVG exposes the active baseline from getStartPositionOfChar. AE point text
 // uses the alphabetic baseline. Measure the real font's offset in Chromium.
 const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg'),word=document.createElementNS(ns,'text');
 svg.style.cssText='position:absolute;left:-10000px;top:0;visibility:hidden';
 Object.assign(word.style,{fontFamily:css.fontFamily,fontWeight:css.fontWeight,fontStyle:css.fontStyle,fontSize:css.fontSize,dominantBaseline:baseline});
 word.textContent='H';svg.appendChild(word);document.body.appendChild(svg);
 const first=word.getBBox().y-word.getStartPositionOfChar(0).y;
 word.style.dominantBaseline='alphabetic';
 const delta=first-(word.getBBox().y-word.getStartPositionOfChar(0).y);
 svg.remove();baselineCache.set(key,delta);return delta;
}
function textRuns(el,root,order){
 const total=el.getNumberOfChars();if(total===0)return [];
 const walk=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
 const nodes=[];while(walk.nextNode())if(walk.currentNode.textContent.length)nodes.push(walk.currentNode);
 let fragments=nodes.map(node=>node.textContent);
 if(!el.closest('[xml\\:space="preserve"]')){
  fragments=fragments.map(t=>t.replace(/[ \n\t\r]+/g,' '));
  if(fragments.length){fragments[0]=fragments[0].replace(/^ /,'');fragments[fragments.length-1]=fragments.at(-1).replace(/ $/,'');}
 }
 if(fragments.join('').length!==total){
  const raw=nodes.map(node=>node.textContent);
  if(raw.join('').length===total)fragments=raw;
  else throw Error('SVG character indexing mismatch "'+fragments.join('')+'", '+total+' vs '+fragments.join('').length);
 }
 let offset=0;const layers=[];
 for(let i=0;i<nodes.length;i++){
  // The baseline origin of the first visible glyph also accounts for text-anchor,
  // XML space collapsing, measured word widths, optical alignment and nested tspans.
  const str=fragments[i],trimmed=str.trim();const start=offset+(str.length-str.trimStart().length);offset+=str.length;
  if(!trimmed)continue;
  const glyph=el.getStartPositionOfChar(start);
  const leaf=nodes[i].parentElement,css=getComputedStyle(leaf),m=el.getCTM();
  const [fill,alpha]=paint(css.fill),mask=maskRect(leaf);
  const props={text:trimmed,position:point(m,glyph.x,glyph.y+alphabeticOffset(css)),font:font(css),size:round(parseFloat(css.fontSize)*matrixScale(m)),
    fill,opacity:round(100*opacity(leaf,root)*alpha*Number(css.fillOpacity))};
  if(mask)props.maskRect=mask;
  const math=el.closest('[data-formula]')?.getAttribute('data-formula');
  const name=math?math+' · '+(el.dataset.mathRole==='power'?'exposant ':'')+trimmed:trimmed;
  const suffix='.'+String(i).padStart(3,'0');
  layers.push({id:order+suffix,order:order+suffix,kind:'text',name,props});
 }
 return layers;
}
export function captureSvg(root){
 const layers=[];
 function visit(el,address){
  const tag=el.localName,m=el.getCTM();
  if(tag==='defs'||tag==='title'||tag==='desc')return;
  if(tag==='svg'||tag==='g'){
   Array.from(el.children).forEach((child,i)=>visit(child,address+'.'+String(i).padStart(3,'0')));
   return;
  }
  if(tag==='text'){layers.push(...textRuns(el,root,address));return;}
  if(tag==='image'||tag==='foreignObject'){
   const url=tag==='image'?el.getAttribute('href'):el.querySelector('img')?.getAttribute('src');
   if(!url)throw Error('Unexpected embedded SVG object');
   const asset=url.split('/').at(-1),name=asset.includes('microphone')?'Microphone':'Cible de l’objectif';
   layers.push({kind:'image',id:address,order:address,name,props:{asset,position:point(m,n(el,'x'),n(el,'y')),
    size:vector(m,n(el,'width'),n(el,'height')),opacity:round(opacity(el,root)*100)}});return;
  }
  const geo=tag==='path'?paths(el.getAttribute('d')):tag==='rect'?[rectangle(el)]:tag==='ellipse'||tag==='circle'?[ellipse(el)]:null;
  if(!geo)throw Error('Unhandled SVG type '+tag);
  const css=getComputedStyle(el),[fill,fa]=paint(css.fill),[stroke,sa]=paint(css.stroke);
  if(fill&&stroke&&fa*Number(css.fillOpacity)!==sa*Number(css.strokeOpacity))throw Error('Unequal paint alpha');
  const dash=el.getAttribute('stroke-dasharray');
  if(dash&&!(dash==='1'&&el.getAttribute('pathLength')==='1'))throw Error('Unsupported dash');
  const base={fill,stroke,strokeWidth:round(parseFloat(css.strokeWidth)*matrixScale(m)),
   lineCap:css.strokeLinecap,lineJoin:css.strokeLinejoin,
   trimEnd:dash?round((1-Number(el.getAttribute('stroke-dashoffset')||0))*100):100,
   opacity:round(100*opacity(el,root)*(fill?fa*Number(css.fillOpacity):sa*Number(css.strokeOpacity)))};
  if(el.hasAttribute('filter')){
   if(el.getAttribute('filter')!=='url(#objective-shadow)')throw Error('Unhandled filter');
   base.shadow=[12,16,5,.55];
  }
  let name=tag==='rect'?'Cadre':tag==='ellipse'?'Repère':el.closest('[data-link-index]')?'Objectif · flèche':'Tracé';
  if(el.hasAttribute('data-objective-banner'))name='Bandeau de l’objectif';
  else if(tag==='rect'&&fill&&stroke===null)name='Cartouche';
  for(const [j,g] of geo.entries()){
   const id=address+'.'+String(j).padStart(3,'0');
   layers.push({id,order:id,kind:'path',name,props:{geometry:converted(g,m),...base}});
  }
 }
 visit(root,'000');return layers;
}

