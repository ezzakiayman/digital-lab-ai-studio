import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Timeline} from '../lib/timeline';
import {charter} from '../lib/charter';
import {headingLabel} from '../lib/presentation';
import {easeReveal,LinkedObjective,MathFormula,MathVariable,TeachingVideo} from './StoryboardVisuals';
import {PronunciationWord} from './PronunciationWord';

type Scene=Extract<Timeline['scenes'][number],{type:'like-terms'}>;
const red='#E60012', blue='#0070C0', green='#008959';
const cards=[
 {title:'Terme',formula:'2x + 5',pair:['2x','5']},
 {title:'Variables',formula:'3x + 2y',pair:['x','y']},
 {title:'Exposant',formula:'5x²',note:'L’exposant est 2'},
 {title:'Semblables',formula:'',pair:['3x','7x'],note:'sont semblables'},
];

export function LikeTerms({scene}:{scene:Scene}){
 const frame=useCurrentFrame(), at=(i:number)=>scene.beats[i].from, cue=(key:string,fallback:number)=>scene.cues[key]??fallback;
 const show=(start:number,content:React.ReactNode)=>{
  const p=easeReveal(frame,Math.max(13,start));
  return <g opacity={p} transform={`translate(0 ${8*(1-p)})`}>{content}</g>;
 };
 const label=(x:number,y:number,content:React.ReactNode,size=58,color=charter.ink,bold=false)=>
  <text x={x} y={y} textAnchor="middle" fill={color} fontSize={size} fontWeight={bold?700:400}>{content}</text>;
 const arrow=(x:number,y:number,end:number,start:number,color=green)=>
  <g fill="none" stroke={color} strokeWidth="5" opacity={frame>=start?1:0}>
   <path d={`M${x} ${y} V${end}`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-easeReveal(frame,start,20)}/>
   <path d={`M${x-15} ${end-19} L${x} ${end} L${x+15} ${end-19}`} opacity={easeReveal(frame,start+20,6)}/>
  </g>;
 const pair=(a:string,b:string,x:number,y:number,size=72,gap=155)=><>
  <MathFormula formula={a} x={x-gap} y={y} size={size}/>
  {label(x,y-3,'et',size*.65)}
  <MathFormula formula={b} x={x+gap} y={y} size={size}/>
 </>;
 let body:React.ReactNode;
 switch(scene.kind){
  case 'intro':
   body=<LinkedObjective frame={frame} title="Réduire un polynôme en regroupant les termes semblables" measure={1811} size={54} links={[
    {from:0,width:656,start:at(1),content:x=>show(cue('sum',at(1)+24),<MathFormula formula="2x + 8x = 10x" x={x} y={710} size={83}/>)},
    {from:1231,width:580,start:at(2),content:x=><>
     {show(cue('likePair',at(2)),<>{pair('2x','8x',x-26,690,67,104)}{label(x+194,692,'✓',66,green,true)}</>)}
     {show(cue('unlikePair',at(3)),<>{pair('2x³','8x',x-26,838,67,104)}{label(x+194,841,'✕',63,red,true)}</>)}
    </>},
   ]}/>;
   break;
  case 'definition':
   body=<>{show(at(1),label(960,485,<>Les <tspan fontWeight="700">termes semblables</tspan> d’un polynôme</>,64))}
    {show(cue('sameVariables',at(1)),label(960,610,<>ont les <tspan fill={red} fontWeight="700">mêmes variables</tspan></>,64))}
    {show(cue('samePowers',at(1)),label(960,735,<>avec les <tspan fill={blue} fontWeight="700">mêmes exposants</tspan>.</>,64))}</>;
   break;
  case 'comparison':{
   const like=scene.example==='like',stage=scene.beats.reduce((n,b)=>frame>=b.from?b.stage:n,0);
   const original=like?['5xy','4xy']:['x³y','x²y'];
   const expanded=['5xy = 5x¹y¹','4xy = 4x¹y¹'];
   const showExpanded=[cue('expand0',at(3)),cue('expand1',at(3))];
   const mark=stage===1?[like?1:0]:stage===2?[like?2:2]:like?stage===4?[8]:stage===5?[10]:undefined:undefined;
   body=<>{original.map((formula,i)=>{
    const isExpanded=like&&frame>=showExpanded[i];
    const index=like?mark:stage===3&&i===0||stage===4&&i===1?[1]:mark;
    return <g key={i}>{show(13,<MathFormula formula={isExpanded?expanded[i]:formula} x={i===0?570:1350}
     y={449} size={82} background={like?'#FFDC69':'#F5DDF3'} mark={index}
     markColor={stage>=3?like?blue:green:red} markProgress={easeReveal(frame,at(stage),14)}/>)}</g>;
   })}
   {show(13,label(960,445,'et',50))}
   {show(at(1),label(960,585,<>Mêmes variables : <MathVariable name="x"/>{stage>=2&&<> et <MathVariable name="y"/></>}</>,59))}
   {show(like?at(4):at(3),label(960,688,like?<>Même exposant de <MathVariable name="x"/> : <tspan fill={blue}>1</tspan></>:
    <>Exposant de <MathVariable name="x"/> dans <MathVariable name="x"/>³<MathVariable name="y"/> : <tspan fill={red}>3</tspan></>,55))}
   {show(like?at(5):at(4),label(960,777,like?<>Même exposant de <MathVariable name="y"/> : <tspan fill={blue}>1</tspan></>:
    <>Exposant de <MathVariable name="x"/> dans <MathVariable name="x"/>²<MathVariable name="y"/> : <tspan fill={red}>2</tspan></>,55))}
   {!like&&show(at(5),<MathFormula formula="3 ≠ 2" x={1420} y={760} size={80}/>)}
   {show(at(6),<>{arrow(960,799,850,at(6),like?green:red)}
    {label(960,937,like?'Les deux termes sont semblables.':'Les deux termes ne sont pas semblables.',63,like?green:red,true)}</>)}</>;
   break;
  }
  case 'pronunciation':
   body=<PronunciationWord word="semblables" frame={frame} syllableStarts={[at(1),at(2)]} wholeStart={at(3)}/>;
   break;
  case 'synthesis':{
   const index=cards.findLastIndex((_,i)=>frame>=at(i+1));
   const card=cards[index];
   const start=card?at(index+1):0;
   const example=card?cue('summaryExample'+index,start+18):0;
   const result=card?cue('summaryResult'+index,example+30):0;
   body=card&&<>{show(start,<><rect x="655" y="315" width="610" height="92" rx="17" fill="white" stroke={charter.turquoise} strokeWidth="4"/>
    <g data-box-heading>{label(960,380,headingLabel(card.title),61,charter.ink,true)}</g></>)}
    {show(example,<>{arrow(960,430,502,example)}
     {card.formula?<MathFormula formula={card.formula} y={632} size={112}/>:pair('3x','7x',960,632,92)}</>)}
    {show(result,<>{arrow(960,668,753,result)}
     {index<2?pair(card.pair![0],card.pair![1],960,880,88):label(960,880,card.note,66,green,true)}</>)}</>;
   break;
  }
  case 'vocabulary':
   body=show(13,<>{cards.map(({title},i)=>{
    const x=i%2?1360:560,y=i<2?460:766;
    const start=cue('word'+i,i*35);
    const active=frame>=start&&frame<start+38;
    return <g key={title} data-box-heading><rect x={x-295} y={y-85} width="590" height="120" rx="20"
     fill={active?'#E8F8F5':'white'} stroke={charter.turquoise} strokeWidth="4"/>
     {label(x,y,headingLabel(title),64,active?'#087F71':charter.ink,true)}</g>;
   })}</>);
   break;
 }
 return <TeachingVideo frame={frame} audio={scene.audio} title={scene.kind==='intro'?undefined:scene.title} boxed={scene.kind!=='pronunciation'}>{body}</TeachingVideo>;
}

