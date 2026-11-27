import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Timeline} from '../lib/timeline';
import {charter} from '../lib/charter';
import {headingLabel} from '../lib/presentation';
import {easeReveal,LinkedObjective,MathFormula,TeachingVideo} from './StoryboardVisuals';
import {QuestionMark} from './QuestionMark';

type Scene=Extract<Timeline['scenes'][number],{type:'polynomial-subtraction'}>;
const subtract='(8x + 7y) − (6x + 4y)';
const opposite='(8x + 7y) + (−6x − 4y)';
const flat='8x + 7y − 6x − 4y';
const grouped='8x − 6x + 7y − 4y';
const answer='2x + 3y';
const horizontal=['Je transforme la soustraction en addition','J’enlève les parenthèses','Je regroupe les termes semblables','Je calcule'];
const vertical=['Je change les signes du polynôme à soustraire','J’effectue l’addition verticale','J’écris le résultat'];

function ColumnAddition({x=960,y=460,size=92,showX=false,showY=false,highlight,question=false}:{
 x?:number;y?:number;size?:number;showX?:boolean;showY?:boolean;highlight?:'x'|'y';question?:boolean;
}){
 const a=x-size*1.7,b=x+size*1.7, symbol=x-size*4.3;
 const first=y,second=y+size*1.2,line=y+size*1.48,total=y+size*2.48;
 return <g data-column-addition>
  {highlight&&<rect x={(highlight==='x'?a:b)-size*1.55} y={y-size*.95} width={size*2.72} height={size*3.7}
   rx="19" fill={highlight==='x'?'#E6F3FC':'#FCE7EF'} stroke={highlight==='x'?'#0070C0':'#C00000'} strokeWidth="4"/>}
  <MathFormula formula="8x" x={a} y={first} size={size} colorAxes/>
  <MathFormula formula="+" x={b-size*1.1} y={first} size={size}/>
  <MathFormula formula="7y" x={b} y={first} size={size} colorAxes/>
  <MathFormula formula="+" x={symbol} y={second} size={size}/>
  <MathFormula formula="−" x={a-size*1.1} y={second} size={size}/>
  <MathFormula formula="6x" x={a} y={second} size={size} colorAxes/>
  <MathFormula formula="−" x={b-size*1.1} y={second} size={size}/>
  <MathFormula formula="4y" x={b} y={second} size={size} colorAxes/>
  <path d={`M${symbol-size*.42} ${line} H${b+size*1.45}`} stroke={charter.ink} strokeWidth="4"/>
  <MathFormula formula="=" x={symbol} y={total} size={size}/>
  <MathFormula formula={showX?'2x':'…'} x={a} y={total} size={size} colorAxes/>
  <MathFormula formula="+" x={b-size*1.1} y={total} size={size}/>
  <MathFormula formula={showY?'3y':'…'} x={b} y={total} size={size} colorAxes/>
  {question&&<QuestionMark x={b+size*1.9} y={total-size*.88} width={size*1.2}/>}
 </g>;
}

export function PolynomialSubtraction({scene}:{scene:Scene}){
 const frame=useCurrentFrame(),at=(i:number)=>scene.beats[i].from;
 const stage=scene.beats.reduce((n,b)=>frame>=b.from?b.stage:n,0);
 const cue=(name:string,fallback:number)=>scene.cues[name]??fallback;
 const show=(start:number,node:React.ReactNode)=><g opacity={easeReveal(frame,Math.max(13,start),14)}>{node}</g>;
 const label=(x:number,y:number,t:string,size=56,fill=charter.ink)=>
  <text x={x} y={y} textAnchor="middle" fontSize={size} fill={fill} fontWeight="700">{t}</text>;
 const step=(text:string,y:number)=>label(960,y,text,53,'#263956');
 const expr=(formula:string,y:number,size=82,background?:string,mark?:number[])=>
  <MathFormula formula={formula} y={y} size={size} colorAxes background={background} mark={mark}/>;
 const methodCard=(x:number,y:number,text:string)=> <g data-box-heading>
  <rect x={x-335} y={y-65} width="670" height="85" rx="18" fill="#E8F8F5" stroke={charter.turquoise} strokeWidth="3"/>
  {label(x,y,headingLabel(text),48,'#263956')}
 </g>;
 let body:React.ReactNode;
 switch(scene.kind){
  case 'intro':
   body=<LinkedObjective frame={frame} title="Effectuer la soustraction de deux polynômes" measure={1371} size={64} links={[
    {from:0,width:1371,start:at(1),content:x=>show(cue('difference',at(1)+24),label(x,718,'Calculer leur différence',65))},
   ]}/>;
   break;
  case 'task':{
   const across=scene.method==='horizontal',list=across?horizontal:vertical;
   const steps=across?3:2;
   body=stage<steps?<>{show(13,<>
    {label(960,385,across?'Effectuer la soustraction horizontale':'Effectuer la soustraction verticale',60,'#263956')}
    {label(960,464,'des deux polynômes :',57,'#263956')}
   </>)}
   {stage< (across?2:1)?show(13,<>
    <MathFormula formula="(8x + 7y)" x={670} y={700} size={102} colorAxes/>
    {label(960,693,'et',58)}
    <MathFormula formula="(6x + 4y)" x={1260} y={700} size={102} colorAxes/>
   </>):show(at(across?2:1),across?expr(subtract,720,106,'#FFF3DA',[10]):<ColumnAddition y={590} size={84} question/>)}</>:
   <>{show(at(steps),label(960,380,'Étapes à suivre :',62,'#263956'))}
    {list.map((name,i)=>{
     const start=at(steps+1+i),y=496+i*116;
     return <g key={name}>
      {show(at(steps)+i*8,<><circle cx="310" cy={y-18} r="38" fill={charter.turquoise}/>
       {label(310,y-2,String(i+1),48,'white')}</>)}
      {show(start,<><rect x="382" y={y-67} width="1290" height="94" rx="19" fill="#E8F8F5" stroke={charter.turquoise} strokeWidth="3"/>
       <text x="422" y={y-6} fontSize="49" fill={charter.ink}>{name}</text></>)}
     </g>;
    })}</>;
   break;
  }
  case 'opposite':{
   const across=scene.method==='horizontal';
   const partial=stage<3?'(8x + 7y) + (…)':stage<4?'(8x + 7y) + (−6x + …)':opposite;
   body=<>{show(13,step(across?horizontal[0]:vertical[0],374))}
    {show(13,expr(across?subtract:'6x + 4y',526,98,undefined,across&&stage===1?[10]:undefined))}
    {stage>=1&&show(at(1),expr(across?'= '+partial:'−6x − 4y',732,100,'#E8F8F5'))}
   </>;
   break;
  }
  case 'horizontal':{
   const active=stage<3?horizontal[1]:stage<6?horizontal[2]:horizontal[3];
   body=<>{show(13,step(active,369))}
    {show(13,expr(subtract,481,78))}
    {show(13,expr('= '+opposite,604,78,undefined,stage===1?[2,10,14,23]:undefined))}
    {show(at(2),<MathFormula formula={'= '+flat} y={720} size={77} colorAxes
     markSpans={stage===4?[[2,3],[10,13]]:stage===5?[[5,8],[15,18]]:undefined}/>)}
    {show(at(4),expr('= '+(stage===4?'8x − 6x + …':grouped),839,77))}
    {show(at(8),expr('= '+(stage===8?'2x + …':answer),956,85,'#E8F8F5'))}
   </>;
   break;
  }
  case 'vertical':{
   const x=frame>=cue('resultX',at(3)),y=frame>=cue('resultY',at(5));
   body=<>{show(13,step(stage<6?vertical[1]:vertical[2],373))}
    {stage===0?show(13,expr('(8x + 7y) + (−6x − 4y)',631,96)):
     show(at(1),<ColumnAddition y={533} size={103} showX={x} showY={y} highlight={stage>=2&&stage<4?'x':stage>=4&&stage<6?'y':undefined}/>)}
    {stage>=7&&show(at(7),expr(subtract+' = '+answer,953,63,'#E8F8F5'))}
   </>;
   break;
  }
  case 'synthesis':
   body=<>{show(at(2),<>{methodCard(590,424,'Soustraction horizontale')}
     <MathFormula formula={subtract} x={590} y={601} size={51} colorAxes/>
     <MathFormula formula={'= '+answer} x={590} y={731} size={78} colorAxes background={stage>=4?'#E8F8F5':undefined}/></>)}
    {show(at(3),<>{methodCard(1335,424,'Soustraction verticale')}
     <ColumnAddition x={1335} y={544} size={66} showX showY/></>)}
    {show(at(4),expr(answer,919,105,'#E8F8F5'))}</>;
   break;
 }
 return <TeachingVideo frame={frame} audio={scene.audio} title={scene.kind==='intro'?undefined:scene.title}>{body}</TeachingVideo>;
}

