import React from 'react';
import {AbsoluteFill,Audio,staticFile,useCurrentFrame,interpolate} from 'remotion';
import {Timeline} from '../lib/timeline';
type Section=Extract<Timeline['scenes'][number],{type:'lesson-section'}>;
const teal='#0DBBA1',ink='#1D1D1D',red='#E60012',green='#53C96B';
export const LessonSection:React.FC<{scene:Section}>=({scene})=>{
 const f=useCurrentFrame();
 const on=(target:string)=>scene.events.some(e=>e.target===target&&f>=e.from&&f<e.to);
 const fade=(target:string)=>{const e=scene.events.find(e=>e.target===target&&f>=e.from&&f<e.to);return e?Math.min(1,(f-e.from)/10):0;};
 const text=(x:number,y:number,s:React.ReactNode,size=60,color=ink,bold=false)=> <text x={x} y={y} fill={color} fontSize={size} fontWeight={bold?700:400}>{s}</text>;
 const label=(title:string,width=455)=><g><path d={`M193 104 H${193+width-55} Q${193+width} 104 ${193+width} 160 Q${193+width} 216 ${193+width-55} 216 H193 Z`} fill={teal}/>{text(240,173,title,52,'white',true)}</g>;
 const frame=(x:number,y:number,w:number,h:number)=> <rect x={x} y={y} width={w} height={h} rx="30" fill="none" stroke={teal} strokeWidth="6"/>;
 const direction=(right:boolean,x:number,y:number)=> <g>{text(x,y-30,right?'Plus grand':'Plus petit',52)}<path d={right?`M${x} ${y} h220 v-23 l57 55 -57 55 v-23 h-220 Z`:`M${x+277} ${y} h-220 v-23 l-57 55 57 55 v-23 h220 Z`} fill={right?green:red}/></g>;
 let content:React.ReactNode;
 if(scene.section==='intro'){
  const y=interpolate(f,[120,165],[337,155],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  content=<><defs><filter id="shadow"><feDropShadow dx="12" dy="16" stdDeviation="5" floodOpacity="0.4"/></filter></defs><g transform={`translate(0,${y-155})`}><rect x="82" y="155" width="1755" height="230" rx="50" fill="white" stroke="#2D77CB" strokeWidth="8" filter="url(#shadow)"/><g stroke="#2D77CB" strokeWidth="18" fill="none"><circle cx="177" cy="265" r="65"/><circle cx="177" cy="265" r="36"/><circle cx="177" cy="265" r="5"/></g><path d="M177 265 L260 182 M241 205 L240 172 L258 150 L265 177 L289 180 L267 205 Z" stroke="#F47714" strokeWidth="12" fill="#F47714"/>{text(290,289,'Comparer et ranger des nombres',80,'#41476D',true)}</g>
  {on('compare')&&<g stroke={red} strokeWidth="5" fill="none"><path d="M294 325 H705 M503 325 V510 l-25 -30 M503 510 l25 -30"/></g>}
  {on('compare')&&text(445,572,'قارن',66)}
  {on('symbols')&&<>{text(415,700,<>... <tspan fill={red}>&gt;</tspan> ...</>,60)}{text(415,790,<>... <tspan fill={red}>&lt;</tspan> ...</>,60)}</>}
  {on('sort')&&<><path d="M825 325 H995 M910 325 V510 l-25 -30 M910 510 l25 -30" fill="none" stroke={teal} strokeWidth="5"/>{text(858,572,'رتب',66)}</>}
  {on('numbers')&&<><path d="M1275 325 H1620 M1460 325 V510 l-25 -30 M1460 510 l25 -30" fill="none" stroke="#655AAB" strokeWidth="5"/>{text(1150,590,'+4 ; −5 ; 2,3 …',80)}</>}
  </>;
 }else if(scene.section==='phonetics'){
  content=<>{text(590,267,'Comparer',150,teal,true)}{on('syllables')&&text(470,790,<><tspan fill="#087EB7">Com- </tspan><tspan fill={red}>pa- </tspan>{on('ending')&&<tspan fill="#E8A31B">rer</tspan>}</>,145,ink,true)}{on('whole')&&text(470,790,'Comparer',145,'#087EB7',true)}</>;
 }else if(scene.section==='property-lead'){
  content=<><rect x="194" y="111" width={on('expanded')?1543:427} height="90" rx="30" fill={teal}/>{text(233,175,on('expanded')?'Propriété 1 (comparer deux nombres négatifs):':'Propriété 1',64,'white',true)}</>;
 }else if(scene.section==='opposite-signs'){
  content=<>{label('Propriété 2',420)}{frame(173,277,1600,183)}{text(200,383,'Un nombre négatif est plus petit qu’un nombre positif.',57,ink,true)}
  {on('example')&&<g opacity={fade('example')}>{frame(179,553,1600,495)}{text(262,642,'Exemple :',58,teal,true)}
   {!on('result')&&<>{on('prompt')&&text(650,775,'je compare −5 et 1',58,ink,true)}{on('negative')&&<><path d="M995 800 L720 950 l32 -6 M720 950 l15 -30" fill="none" stroke={red} strokeWidth="6"/>{text(580,1000,'Négatif',58,red,true)}</>}{on('positive')&&<><path d="M1175 800 L1420 950 l-30 -7 M1420 950 l-15 -30" fill="none" stroke={red} strokeWidth="6"/>{text(1300,1000,'Positif',58,teal,true)}</>}</>}
   {on('result')&&<g opacity={fade('result')}>{text(800,805,<>donc −5 <tspan fill={red}>&lt;</tspan> 1</>,64,ink,true)}</g>}
  </g>}</>;
 }else{
  const summary=scene.section==='summary';
  content=<>{!summary&&<>{label('Remarque')}{frame(192,275,1544,232)}{text(237,360,<>Pour <tspan fontWeight="700">comparer deux nombres</tspan>, on peut les placer sur la droite</>,48)}{text(237,464,'numérique.',48)}</>}
   {on('line')&&<g><path d="M450 846 H1505 l-24 -18 v36 l24 -18" fill={ink} stroke={ink} strokeWidth="4"/>{Array.from({length:7},(_,i)=>i-3).map(n=><g key={n}><path d={`M${960+n*160} 830 V862`} stroke={ink} strokeWidth="3"/>{text(960+n*160-(n<0?25:15),916,n,52,n===0?'black':'#404040')}</g>)}</g>}
   {on('left')&&direction(false,530,670)}{on('right')&&direction(true,1140,670)}
   {on('comparison')&&text(750,1020,<>−3 <tspan fill={on('answer')?red:ink}>{on('answer')?' < ':' ………… '}</tspan> −2</>,60,ink,true)}
   {on('place')&&<g fill="none" strokeWidth="3"><rect x="447" y="864" width="67" height="79" rx="9" stroke={red}/><rect x="607" y="864" width="67" height="79" rx="9" stroke="#EF9E40"/></g>}
   {summary&&text(470,1060,'',40)}
  </>;
 }
 return <AbsoluteFill style={{background:'white',fontFamily:'Arial, sans-serif'}}><svg width="1920" height="1080" viewBox="0 0 1920 1080">{content}</svg>{scene.audio&&<Audio src={staticFile(scene.audio)}/>}</AbsoluteFill>;
};
