import React from 'react';
import {AbsoluteFill,Audio,Easing,interpolate,staticFile,useCurrentFrame} from 'remotion';
import {Timeline} from '../lib/timeline';
import {charter} from '../lib/charter';
import {objectiveColor,objectiveTitleFontSize} from '../lib/objective';
import {positiveDivisors,primeRanges,primesBelow100} from '../lib/primes';
import {ObjectiveBanner} from './ObjectiveDeclaration';
import {QuestionMark} from './QuestionMark';
import {PrimeObjective} from './PrimeObjective';
import {PronunciationWord} from './PronunciationWord';
import {SectionHeader} from './SectionHeader';
import {headingLabel} from '../lib/presentation';

type Scene=Extract<Timeline['scenes'][number],{type:'primes'}>;
const red='#E60012',blue='#0070C0';
export const Primes:React.FC<{scene:Scene}>=({scene})=>{
 const f=useCurrentFrame();
 const revised=scene.revision!==undefined;
 const reviewed=scene.revision==='2026-11-12';
 const at=(i:number)=>scene.beats[i]?.from??0;
 const cue=(name:string,fallback:number)=>scene.cues[name]??fallback;
 const p=(start:number,d=18)=>interpolate(f,[start,start+d],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)});
 const reveal=(start:number,node:React.ReactNode)=>{
  const progress=p(revised?Math.max(13,start):start);
  return <g opacity={progress} transform={`translate(0,${8*(1-progress)})`}>{node}</g>;
 };
 const pop=(start:number,x:number,y:number,node:React.ReactNode)=>{
  const scale=interpolate(f,[start,start+8,start+20],[0.94,1.025,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <g opacity={p(start,10)} transform={`translate(${x},${y}) scale(${scale}) translate(${-x},${-y})`}>{node}</g>;
 };
 const text=(x:number,y:number,s:React.ReactNode,size=62,color=charter.ink,bold=false)=><text x={x} y={y} fontSize={size} fill={color} fontWeight={bold?700:400}>{s}</text>;
 const center=(y:number,s:React.ReactNode,size=72,color=charter.ink)=> <text x="960" y={y} textAnchor="middle" fontSize={size} fill={color} fontWeight="700">{s}</text>;
 const entrance=p(0,13);
 const enter=(node:React.ReactNode)=><g opacity={.2+.8*entrance} transform={`translate(0,${12*(1-entrance)})`}>{node}</g>;
 const box=<rect data-content-box x="169" y="270" width="1599" height="735" rx="28" fill={charter.background} stroke={charter.turquoise} strokeWidth="6"/>;
 const frame=revised?enter(box):box;
 const badge=revised?enter(<SectionHeader title={scene.title}/>):<><rect x="194" y="111" width={scene.title==='Définition'?510:scene.title==='À retenir'?470:450} height="90" rx="30" fill={charter.turquoise}/>{text(233,175,scene.title,64,'white',true)}</>;
 const arrow=(x:number,y:number,end:number,start:number,color=blue)=><g fill="none" stroke={color} strokeWidth="5" opacity={f>=start?1:0}><path d={`M${x} ${y} V${end}`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(start,22)}/><path d={`M${x-19} ${end-22} L${x} ${end} L${x+19} ${end-22}`} opacity={p(start+(revised?22:14),8)}/></g>;
 const tile=(n:number,x:number,y:number,color:string,start:number,w=190,h=76)=>pop(start,x+w/2,y+h/2,<g data-prime-number={n}><rect x={x} y={y} width={w} height={h} rx="12" fill={color}/><text x={x+w/2} y={y+h/2+21} textAnchor="middle" fontSize="60" fill="white" fontWeight="700">{n}</text></g>);
 let body:React.ReactNode;
 switch(scene.kind){
 case 'intro':{
  if(revised){
   body=<PrimeObjective frame={f} starts={scene.beats.map(b=>b.from)} cues={scene.cues} arabicLabel={reviewed?'تَحَقَّق':undefined}/>;
   break;
  }
  const terms=[
   {text:'Reconnaître',x:220,y:285,width:416,anchor:428,labelX:480},
   {text:'vérifier',x:740,y:285,width:240,anchor:860,labelX:960},
   {text:'premier',x:1596,y:285,width:264,anchor:1728,labelX:1440},
  ];
  body=<ObjectiveBanner layout="single-line">
   {text(656,285,'et',objectiveTitleFontSize,charter.navy,true)}
   {text(1000,285,'si un nombre est',objectiveTitleFontSize,charter.navy,true)}
   {terms.map((t,i)=>{
    const start=at(i+1),color=objectiveColor(i),active=f>=start&&(i===2||f<at(i+2)),underline=t.y+20;
    const shaft=i===0?'M428 305 V480 C428 520 480 520 480 560 V610':i===1?'M860 305 V450 C860 500 960 500 960 550 V610':'M1728 305 V450 C1728 500 1440 500 1440 550 V610';
    return <g key={t.text} data-link-index={i}>
     {active&&<rect x={t.x-8} y={t.y-objectiveTitleFontSize+5} width={t.width+16} height={objectiveTitleFontSize+17} rx="10" fill={color} opacity={0.1*p(start,10)}/>}
     <text data-objective-title x={t.x} y={t.y} fontSize={objectiveTitleFontSize} fontWeight="700" fill={active?color:charter.navy}>{t.text}</text>
     <path d={`M${t.x} ${underline} H${t.x+t.width}`} pathLength="1" stroke={color} strokeWidth="4" strokeDasharray="1" strokeDashoffset={1-p(start)} fill="none" opacity={f>=start?1:0}/>
     <g stroke={color} strokeWidth="4" fill="none" opacity={f>=start?1:0}><path d={shaft} pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(start+8,20)}/><path d={`M${t.labelX-20} 586 L${t.labelX} 610 L${t.labelX+20} 586`} opacity={p(start+24,8)}/></g>
     {i===0&&reveal(cue('explanation0',start+24),<text x={t.labelX} y="710" textAnchor="middle" fontSize="68" fill={charter.ink}>Identifier</text>)}
     {i===1&&reveal(cue('explanation1',start+24),<text x={t.labelX} y="710" textAnchor="middle" fontSize="76" direction="rtl" unicodeBidi="plaintext" fill={charter.ink}>تحقق</text>)}
    </g>;
   })}
   {[2,3,5,7,11].map((n,i)=>{
    const [x,y]=[[1320,710],[1440,800],[1500,905],[1560,710],[1380,905]][i];
    return <g key={n}>{pop(cue('prime'+i,at(3)+i*15),x,y,<g><circle cx={x} cy={y} r="47" fill={['#8FAADC','#70AD47','#111111','#ED7D31','#FFC000'][i]}/><text x={x} y={y+20} textAnchor="middle" fontSize="57" fill="white" fontWeight="700">{n}</text></g>)}</g>;
   })}
  </ObjectiveBanner>;break;
 }
 case 'definition':body=<>{frame}
  {reveal(at(1),text(220,380,<>Un entier positif <tspan fontStyle="italic">p</tspan> est un nombre <tspan fill={red} fontWeight="700">premier</tspan></>,62))}
  {reveal(cue('condition',at(1)),text(220,480,'si et seulement s’il admet exactement',62))}
  {reveal(cue('two',at(1)),text(220,580,<><tspan fill={red} fontWeight="700">deux diviseurs positifs distincts</tspan> : <tspan fill={red}>1 et {revised?<tspan fontStyle="italic">p</tspan>:'p'}.</tspan></>,62))}
  {reveal(cue('focus',at(2)),<>{arrow(960,635,715,at(2),red)}{pop(cue('focus',at(2)),960,790,center(820,<>1 <tspan fill={charter.ink}>et</tspan> <tspan fontStyle="italic">p</tspan></>,104,red))}</>)}</>;break;
 case 'divisors':{
  const n=scene.value!,ds=positiveDivisors(n),prime=ds.length===2;
  body=<>{frame}{pop(revised?13:at(0),960,380,center(415,n,112))}
   {reveal(at(1),center(550,`Les diviseurs positifs de ${n} sont :`,60))}
   {ds.map((d,i)=>{const x=960+(i-(ds.length-1)/2)*250;return <g key={d}>{pop(cue('divisor'+i,at(1)+i*12),x,650,<text x={x} y="695" textAnchor="middle" fontSize="94" fontWeight="700" fill={red}>{d}</text>)}</g>;})}
   {reveal(cue('conclusion',at(2)),<>
    <rect x="310" y="765" width="1300" height="105" rx="12" fill={charter.highlight}/>
    {center(840,prime?`${n} est un nombre premier`:<>{n} <tspan fill={red}>n’est pas</tspan> un nombre premier</>,68)}
   </>)}
  </>;break;
 }
 case 'one':body=<>{frame}{reveal(at(1),<>
  {center(reviewed?635:390,<>Le nombre <tspan fill={red}>1</tspan> n’est pas premier</>,74)}
  {pop(at(1)+16,960,reviewed?420:530,center(reviewed?475:570,'1',110,red))}
  {center(reviewed?763:700,'Un seul diviseur positif : 1',68)}
 </>)}</>;break;
 case 'question':{
  const prompt=center(400,<>Les nombres premiers <tspan fill={red}>inférieurs à 100</tspan></>,66);
  body=<>{frame}{revised?reveal(13,prompt):prompt}{pop(at(1)+10,960,673,<QuestionMark/>)}</>;break;
 }
 case 'prime-ranges':body=<>{frame}{revised?reveal(13,center(350,'Les nombres premiers inférieurs à 100',62,charter.navy)):center(350,'Les nombres premiers inférieurs à 100',62,charter.navy)}
  {primeRanges.slice(scene.rangeStart!,scene.rangeStart!+5).map((range,row)=>{const y=400+row*116,startX=960-(range.values.length*190+(range.values.length-1)*45)/2;return <g key={range.min} data-prime-range={range.min}>
   {range.values.map((n,col)=><g key={n}>{tile(n,startX+col*235,y,range.color,cue(`row${row}number${col}`,at(row)+col*12))}</g>)}
  </g>;})}
 </>;break;
 case 'all-primes':body=<>{frame}{revised?reveal(13,center(365,'Les nombres premiers inférieurs à 100',62,charter.navy)):center(365,'Les nombres premiers inférieurs à 100',62,charter.navy)}
  {primesBelow100.map((n,i)=>{const range=primeRanges.find(r=>(r.values as readonly number[]).includes(n))!;return <g key={n}>{tile(n,320+(i%5)*260,420+Math.floor(i/5)*100,range.color,revised?13:0,235,82)}</g>;})}
 </>;break;
 case 'pronunciation':body=revised?<PronunciationWord word="premier" frame={f} syllableStarts={[at(1),at(2)]} wholeStart={at(3)}/>:<>{frame}{center(395,'Premier',112,'#00B0F0')}
  {reveal(at(1),<>{center(625,<><tspan fill={blue}>Pre</tspan><tspan fill={blue}> - </tspan><tspan fill={red}>mier</tspan></>,112)}{center(815,'Prononciation : preu-mié',66)}</>)}
 </>;break;
 case 'vocabulary':{
 const axis=1090;
 const pairStart=cue('divisorPair',at(1)),blinkStart=cue('blinkPair',at(3));
 const blinkPhase=Math.max(0,Math.min(36,f-blinkStart));
 const pairOpacity=1-.63*Math.sin(Math.PI*blinkPhase/18)**2;
 body=<>{frame}
  {['Diviseur','Divisible','Premier'].map((word,i)=>{const y=345+i*205,start=at(i+1);return <g key={word}>{reveal(start,<><rect x="230" y={y} width="430" height="95" rx="18" fill="white" stroke={charter.turquoise} strokeWidth="4"/><g data-box-heading>{text(270,y+66,revised?headingLabel(word):word,62,charter.ink,true)}</g></>)}</g>;})}
  {reviewed?<>
   {f>=cue('eleven',at(1))&&<text x={axis} y="399" textAnchor="middle" fontSize="100" fontWeight="700" fill={charter.ink}>11</text>}
   {arrow(axis,423,511,pairStart,blue)}
   {f>=cue('orangeBand',at(2))&&<rect x={axis-240} y="525" width="480" height="110" rx="16" fill="#FFBA70"/>}
   {f>=pairStart&&<text x={axis} y="605" textAnchor="middle" fontSize="82" fontWeight="700" fill={charter.ink} opacity={pairOpacity}>1 et 11</text>}
   {arrow(axis,660,755,cue('conclusionArrow',at(3)),blue)}
   <text x={axis} y="855" textAnchor="middle" fontSize="60" fontWeight="700" fill={charter.ink} xmlSpace="preserve">
    {['11','est','un','nombre','premier'].map((word,i)=><tspan key={word}
     fill={word==='premier'?red:undefined} opacity={f>=cue('statement'+i,at(3))?1:0}>{(i?' ':'')+word}</tspan>)}
   </text>
  </>:<>
   {reveal(at(1),<>{text(1025,380,'11',100,charter.ink,true)}{arrow(1090,415,515,at(1),blue)}{text(890,605,'1 et 11',82,charter.ink,true)}</>)}
   {reveal(at(2),<rect x="850" y="525" width="480" height="110" rx="16" fill={charter.highlight} opacity={0.7}/>)}
   {f>=at(2)&&text(890,605,'1 et 11',82,charter.ink,true)}
   {reveal(at(3),<>{arrow(1090,660,755,at(3),blue)}{text(770,855,<>11 est un nombre <tspan fill={red}>premier</tspan></>,53,charter.ink,true)}</>)}
  </>}
 </>;break;
 }
 }
 return <AbsoluteFill style={{background:charter.background,fontFamily:charter.font,color:charter.ink}}><svg width="1920" height="1080" viewBox="0 0 1920 1080" data-prime-scene={scene.kind}>{scene.kind!=='intro'&&badge}{body}</svg><Audio src={staticFile(scene.audio)}/></AbsoluteFill>;
};
