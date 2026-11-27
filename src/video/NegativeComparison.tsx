import React from 'react';
import {AbsoluteFill,Audio,staticFile,useCurrentFrame,interpolate} from 'remotion';
import {Timeline} from '../lib/timeline';
type Scene=Extract<Timeline['scenes'][number],{type:'negative-comparison'}>;
// Independent of source pixels: all mathematical marks are editable SVG nodes.
export const NegativeComparison:React.FC<{scene:Scene}>=({scene})=>{
 const f=useCurrentFrame();const [a,b]=scene.operands;
 const event=(target:string)=>scene.events.find(e=>e.target===target&&f>=e.from&&f<e.to);
 const active=(target:string)=>!!event(target);
 const opacity=(target:string)=>{const e=event(target);return e?interpolate(f,[e.from,e.from+10],[0,1],{extrapolateRight:'clamp'}):0;};
 const ink='#1D1D1D',turquoise='#0DBBA1',red='#E60012';
 const text=(x:number,y:number,value:string|number,target?:string,color=ink,size=60)=><text x={x} y={y} fontSize={size} fill={color} fontWeight="700" opacity={target?opacity(target):1}>{value}</text>;
 const arrow=(x:number,target:string)=><g opacity={opacity(target)} stroke={red} strokeWidth="3" fill="none"><path d={`M${x-32} 790 H${x+32} M${x} 790 V837 l-8 -8 M${x} 837 l8 -8`}/></g>;
 return <AbsoluteFill style={{background:'#fff',fontFamily:'Arial, sans-serif'}}>
 <svg width="1920" height="1080" viewBox="0 0 1920 1080">
  <rect x="194" y="111" width="427" height="90" rx="30" fill={turquoise}/>
  {text(233,175,scene.title,undefined,'#fff',64)}
  <rect x="169" y="279" width="1599" height="277" rx="21" fill="none" stroke={turquoise} strokeWidth="7"/>
  <g fill={ink} fontSize="64" letterSpacing="0.45"><text x="190" y="383">Si <tspan fontWeight="700">deux nombres sont négatifs</tspan>, alors <tspan fontWeight="700">le plus petit</tspan></text><text x="190" y="480">est celui qui a <tspan fontWeight="700">la plus grande valeur absolue.</tspan></text></g>
  <rect x="168" y="600" width="1600" height="466" rx="31" fill="none" stroke={turquoise} strokeWidth="6"/>
  {text(192,667,'Exemple 1 :',undefined,turquoise)}
  <g opacity={opacity('prompt')}>{text(656,773,'Comparer')}{text(975,773,`- ${Math.abs(a)}`)}{text(1070,773,'et')}{text(1155,773,`- ${Math.abs(b)}`)}</g>
  {active('signs')&&<g stroke={red} strokeWidth="3" fill="none"><rect x="967" y="737" width="37" height="37" rx="9"/><rect x="1150" y="737" width="37" height="37" rx="9"/></g>}
  {arrow(1024,'arrowA')}{arrow(1205,'arrowB')}
  {text(1008,895,Math.abs(a),'absoluteA',active('redA')?red:ink)}
  {text(1190,895,Math.abs(b),'absoluteB',active('redB')?red:ink)}
  {text(1100,895,'>','greater',red)}
  {active('focusA')&&<rect x="969" y="715" width="91" height="74" rx="15" stroke={red} strokeWidth="3" fill="none"/>}
  {text(657,891,'On a','given')}
  {text(657,1000,'Donc','therefore')}{text(975,1000,`- ${Math.abs(a)}`,'resultA')}{text(1100,1000,'<','less',red)}{text(1155,1000,`- ${Math.abs(b)}`,'resultB')}
 </svg>
 {scene.audio&&<Audio src={staticFile(scene.audio)}/>}
 </AbsoluteFill>;
};
