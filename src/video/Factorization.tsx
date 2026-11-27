import React from 'react';
import {AbsoluteFill,Audio,Easing,interpolate,staticFile,useCurrentFrame} from 'remotion';
import {Timeline} from '../lib/timeline';
import {charter} from '../lib/charter';
import {objectiveColor} from '../lib/objective';
import {objectiveEntrance} from '../lib/presentation';
import {primeFactorization,powerDigits} from '../lib/factorization';
import {ObjectiveBanner} from './ObjectiveDeclaration';
import {SectionHeader} from './SectionHeader';
import {LinkedObjective,TeachingEntrance} from './StoryboardVisuals';
import {PronunciationWord} from './PronunciationWord';
type Scene=Extract<Timeline['scenes'][number],{type:'factorization'}>;
const red='#E60012',purple='#7061AA',green='#00B050';
export const Factorization:React.FC<{scene:Scene}>=({scene})=>{
 const revised=scene.revision!==undefined;
 const reviewed=scene.revision==='2026-11-12';
 const f=useCurrentFrame(),at=(i:number)=>scene.beats[i]?.from??0,cue=(name:string,fallback:number)=>scene.cues[name]??fallback;
 const p=(s:number,d=18)=>interpolate(f,[s,s+d],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)});
 const show=(s:number,n:React.ReactNode)=><g opacity={p(revised?Math.max(13,s):s)} transform={`translate(0 ${8*(1-p(revised?Math.max(13,s):s))})`}>{n}</g>;
 const pop=(s:number,x:number,y:number,n:React.ReactNode)=>{const scale=interpolate(f,[s,s+8,s+20],[.94,1.025,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});return <g opacity={p(s,10)} transform={`translate(${x} ${y}) scale(${scale}) translate(${-x} ${-y})`}>{n}</g>;};
 const text=(x:number,y:number,n:React.ReactNode,size=62,color=charter.ink,bold=false)=><text x={x} y={y} fontSize={size} fill={color} fontWeight={bold?700:400}>{n}</text>;
 const centered=(x:number,y:number,n:React.ReactNode,size=64,color=charter.ink,bold=false)=><text x={x} y={y} textAnchor="middle" fontSize={size} fill={color} fontWeight={bold?700:400}>{n}</text>;
 const box=(height=735)=><rect data-content-box x="169" y="270" width="1599" height={height} rx="28" fill="white" stroke={charter.turquoise} strokeWidth="6"/>;
 const frame=(height=735)=>revised?null:box(height);
 const arrow=(x:number,y:number,end:number,start:number,color=purple)=><g stroke={color} strokeWidth="5" fill="none" opacity={f>=start?1:0}><path d={`M${x} ${y} V${end}`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(start,24)}/><path d={`M${x-18} ${end-22} L${x} ${end} L${x+18} ${end-22}`} opacity={p(start+18,8)}/></g>;
 const equation=(value:72|360,y:number,start:number)=>{
  const factors=primeFactorization(value),xs=value===360?[900,1160,1420]:[980,1240],valueX=value===360?500:610,equalsX=value===360?710:790;
  return <g data-prime-equation={value} fontFamily="Cambria Math, Times New Roman, serif">
   {centered(valueX,y,value,110)}{pop(cue('equals',start),equalsX,y-35,centered(equalsX,y,'=',104))}
   {factors.map((factor,i)=>{
    const x=xs[i],reveal=cue('factor'+i,start+i*30);
    const color=reviewed&&f>=cue('emphasis'+i,scene.durationInFrames)?red:charter.ink;
    const exponent=powerDigits(factor.exponent);
    const notation=reviewed?<><tspan data-factor-base={factor.prime} fill={color}>{factor.prime}</tspan>{exponent}</>:`${factor.prime}${exponent}`;
    return <g key={factor.prime} data-factor={factor.prime+'^'+factor.exponent}>
    {i>0&&show(cue('equals',start),centered(x-130,y,'×',94))}
    {f<reveal?show(cue('equals',start),<text data-pending-factor x={x} y={y} textAnchor="middle" fontSize="90" fill="#888888">…</text>):pop(reveal,x,y-35,centered(x,y,notation,110))}
   </g>;})}
  </g>;
 };
 let body:React.ReactNode;
 switch(scene.kind){
 case 'intro':{
  if(revised){
   body=<LinkedObjective frame={f} title="Décomposer un nombre en produit de nombres premiers" measure={1741} size={56} links={[
    {from:0,width:738,start:at(1),end:scene.cues.redEnd,content:x=>show(cue('writing',at(1)+20),<>{centered(x,692,'Écrire sous forme',58)}{centered(x,768,'de produit',58)}</>)},
    {from:849,width:220,start:at(2),end:scene.cues.greenEnd,content:x=>show(cue('multiplication',at(2)+20),centered(x,734,'… × …',98))},
    {from:1180,width:561,start:at(3),content:x=>[2,5,6].map((n,i)=>{
     const y=674+i*102;
     return <g key={n}>{pop(cue('prime'+i,at(3)+i*20),x,y-25,
      <>{centered(x-35,y,n,76)}{text(x+37,y,i===2?'✕':'✓',68,i===2?red:green,true)}</>)}</g>;
    })},
   ]}/>;
   break;
  }
  const motion=objectiveEntrance(f,at(1));
  const terms=[{text:'Décomposer un nombre',x:340,y:230,w:828,labelX:480,shaft:'M754 250 H320 V480 C320 540 480 540 480 610'},{text:'produit',x:444,y:350,w:248,labelX:960,shaft:'M568 370 V480 C568 540 960 540 960 610'},{text:'nombres premiers',x:816,y:350,w:628,labelX:1440,shaft:'M1130 370 V480 C1130 540 1440 540 1440 610'}];
  body=<g data-objective-entrance transform={`translate(0 ${motion.offsetY})`}><ObjectiveBanner>
   {text(340,350,'en',72,charter.navy,true)}{text(712,350,'de',72,charter.navy,true)}
   {terms.map((t,i)=>{const start=at(i+1),color=objectiveColor(i),active=f>=start&&(i===2||f<at(i+2));return <g key={t.text} data-link-index={i}>
    {active&&<rect x={t.x-8} y={t.y-70} width={t.w+16} height="88" rx="10" fill={color} opacity=".1"/>}
    <text data-objective-title x={t.x} y={t.y} fontSize="72" fontWeight="700" fill={active?color:charter.navy}>{t.text}</text>
    <g stroke={color} strokeWidth="4" fill="none" opacity={f>=start?1:0}><path d={`M${t.x} ${t.y+20} H${t.x+t.w}`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(start)}/><path data-objective-connector d={t.shaft} pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(start+8,24)}/><path d={`M${t.labelX-20} 586 L${t.labelX} 610 L${t.labelX+20} 586`} opacity={p(start+24,8)}/></g>
    {i===0&&show(cue('writing',start+20),<>{centered(480,725,'Écrire sous forme',56)}{centered(480,805,'de produit',56)}</>)}
    {i===1&&show(cue('multiplication',start+20),centered(960,765,'… × …',94))}
   </g>;})}
   {[2,5,6].map((n,i)=>{const start=cue('prime'+i,at(3)+i*20),y=715+i*95;return <g key={n}>{pop(start,1440,y-25,<>{centered(1390,y,n,78)}{text(1480,y,i===2?'✕':'✓',70,i===2?red:green,true)}</>)}</g>;})}
  </ObjectiveBanner></g>;break;
 }
 case 'theorem':body=<>{frame(330)}{show(at(1),<>
  {text(225,355,'Tout entier positif supérieur ou égal à 2',58)}
  {text(225,445,'peut s’écrire comme un produit de nombres premiers,',58)}
  {text(225,535,'de façon unique, à l’ordre des facteurs près.',58)}
 </>)}
  {show(at(2),<>{arrow(960,625,695,at(2))}{equation(360,835,at(2))}</>)}
  {f<at(4)?show(at(3),centered(960,980,'Décomposition en produit de facteurs premiers',54,red)):show(at(4),centered(960,980,'Factorisation première',62,red))}
 </>;break;
 case 'example':body=<>{frame()}{equation(72,505,at(1))}
  {f<at(3)?show(at(2),<>{arrow(960,580,685,at(2))}{centered(960,810,'Décomposition en produit',64,red)}{centered(960,895,'de facteurs premiers',64,red)}</>):show(at(3),<>{arrow(960,580,685,at(3))}{centered(960,835,'Factorisation première',76,red)}</>)}
 </>;break;
 case 'pronunciation':{
  if(revised){
   body=<PronunciationWord word="decomposition" frame={f} syllableStarts={[1,2,3,4,5].map(at)} wholeStart={at(6)}/>;
   break;
  }
  const scale=1+.025*Math.sin(Math.PI*p(at(1),28))+.025*Math.sin(Math.PI*p(at(2),28));
  body=<>{frame()}<g transform={`translate(960 637) scale(${scale}) translate(-960 -637)`}>{centered(960,675,'Décomposition',110,'#00B0F0')}</g></>;break;
 }
 case 'vocabulary':{
  const cards=[{x:540,y:440,lines:['Décomposition'],word:0},{x:1380,y:440,lines:['Facteurs premiers'],word:1},{x:540,y:770,lines:['Divisions','successives'],word:2},{x:1380,y:770,lines:['Arbre de','factorisation'],word:3}];
  body=<>{frame()}{cards.map(v=>{const start=cue('word'+v.word,at(v.word+1)),active=f>=start&&f<start+65,scale=1+.02*Math.sin(Math.PI*p(start,28));return <g data-box-heading={reviewed?undefined:true} data-vocabulary-card key={v.word} transform={`translate(${v.x} ${v.y}) scale(${scale}) translate(${-v.x} ${-v.y})`}>
   <rect x={v.x-345} y={v.y-65} width="690" height={v.lines.length===1?135:195} rx="20" fill={active?'#FDFDCC':'white'} stroke={charter.turquoise} strokeWidth="4"/>
   {v.lines.map((line,i)=><text key={i} x={v.x} y={v.y+20+i*70} textAnchor="middle" fontSize="56" fontWeight="700" fill={active?red:charter.ink}>{line}{!reviewed&&i===v.lines.length-1?' :':''}</text>)}
  </g>;})}</>;break;
 }
 }
 const badge=<SectionHeader title={scene.title}/>;
 return <AbsoluteFill style={{background:charter.background,fontFamily:charter.font,color:charter.ink}}><svg width="1920" height="1080" viewBox="0 0 1920 1080" data-factorization-scene={scene.kind}>{scene.kind!=='intro'&&(revised?<TeachingEntrance frame={f}>{badge}{scene.kind!=='pronunciation'&&box(scene.kind==='theorem'?330:735)}</TeachingEntrance>:badge)}{revised&&scene.kind!=='intro'?<g opacity={p(13,10)}>{body}</g>:body}</svg><Audio src={staticFile(scene.audio)}/></AbsoluteFill>;
};
