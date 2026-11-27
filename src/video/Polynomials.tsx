import React from 'react';
import {AbsoluteFill,Audio,Easing,interpolate,staticFile,useCurrentFrame} from 'remotion';
import {Timeline} from '../lib/timeline';
import {charter} from '../lib/charter';
import {objectiveColor} from '../lib/objective';
import {headingLabel,objectiveEntrance} from '../lib/presentation';
import {expressionData,ExpressionKey,reducedTermCount} from '../lib/polynomials';
import {ObjectiveBanner} from './ObjectiveDeclaration';
import {SectionHeader} from './SectionHeader';
import {PolynomialMath} from './PolynomialMath';
import {PolynomialRoadmap, polynomialObjective} from './PolynomialRoadmap';
import {PronunciationWord, pronunciationParts} from './PronunciationWord';
type Scene=Extract<Timeline['scenes'][number],{type:'polynomials'}>;
const red='#E60012',green='#00B050';
const names={binome:'Binôme',trinome:'Trinôme',polynome:'Polynôme'};
export const PolynomialExpression:React.FC<{id:ExpressionKey;y:number;size?:number;active?:number;activeProgress?:number;highlight?:boolean;x?:number}>=({id,y,size=100,active=-1,activeProgress=1,highlight=true,x=960})=>{
 const e=expressionData[id],scale=size/100,total=e.widths.reduce((a,w)=>a+w,0)*scale;let left=x-total/2;
 return <g data-expression={id}>
  {highlight&&<rect x={x-total/2-30} y={y-size-20} width={total+60} height={size+60} rx="22" fill={id==='trois-termes'||id==='deux-termes'?'#E4EFF8':'#FFDF69'}/>}
  {e.labels.map((label,i)=>{const cx=left+e.widths[i]*scale/2;left+=e.widths[i]*scale;return <g key={i} data-math-term={label}>{i===active&&<ellipse cx={cx} cy={y-size*.35} rx={e.widths[i]*scale/2+10} ry={size*.72} stroke={red} strokeWidth="5" fill="none" pathLength="1" strokeDasharray="1" strokeDashoffset={1-activeProgress} opacity={activeProgress}/>}<text x={cx} y={y} fontSize={size} fontFamily="Cambria Math, Times New Roman, serif" textAnchor="middle" fill={e.colors[i]}>{label.split(/([xyz])/).map((part,j)=><tspan key={j} fontStyle={/^[xyz]$/.test(part)?'italic':'normal'}>{part}</tspan>)}</text></g>;})}
 </g>;
};
export const Polynomials:React.FC<{scene:Scene}>=({scene})=>{
 const f=useCurrentFrame(),at=(i:number)=>scene.beats[i]?.from??0,cue=(n:string,b:number)=>scene.cues[n]??b;
 const revised=scene.revision==='2026-11-10';
 const p=(s:number,d=18)=>interpolate(f,[s,s+d],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)});
 const show=(s:number,n:React.ReactNode)=>{
  const progress=p(revised?Math.max(13,s):s);
  return <g opacity={progress} transform={`translate(0,${8*(1-progress)})`}>{n}</g>;
 };
 const txt=(x:number,y:number,n:React.ReactNode,size=64,color=charter.ink,bold=false)=><text x={x} y={y} fontSize={size} fill={color} fontWeight={bold?700:400}>{n}</text>;
 const center=(y:number,n:React.ReactNode,size=72,color=charter.ink)=><text x="960" y={y} textAnchor="middle" fontSize={size} fill={color}>{n}</text>;
 const arrow=(x:number,y:number,end:number,start:number,color=red)=><g stroke={color} fill="none" strokeWidth="5" opacity={f>=start?1:0}><path d={`M${x} ${y} V${end}`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(start,24)}/><path d={`M${x-18} ${end-22} L${x} ${end} L${x+18} ${end-22}`} opacity={p(start+(revised?24:18),8)}/></g>;
 const entrance=p(0,13);
 const enter=(node:React.ReactNode)=><g opacity={.2+.8*entrance} transform={`translate(0,${12*(1-entrance)})`}>{node}</g>;
 const box=<rect data-content-box x="169" y="270" width="1599" height="735" rx="28" fill={charter.background} stroke={charter.turquoise} strokeWidth="6"/>;
 const frame=revised?enter(box):box;
 const Expression=revised?PolynomialMath:PolynomialExpression;
 let body:React.ReactNode;
 switch(scene.kind){
 case 'intro':{
  if(revised){
   body=<PolynomialRoadmap frame={f} beats={scene.beats.map(b=>b.from)} conceptStarts={[0,1,2].map(i=>cue('concept'+i,at(3)+i*24))}/>;
   break;
  }
  const original=scene.objectiveVariant==='original',motion=objectiveEntrance(f,at(1),original?'single-line':'standard');
  const terms=original?[{text:'Déterminer',x:220,y:285,w:390,labelX:480,label:'Trouver une réponse'},{text:'degré',x:715,y:285,w:200,labelX:1440,label:'0, 1, 2…'}]:[{text:'binôme',x:448,y:350,w:256,labelX:480,label:'2 termes'},{text:'trinôme',x:852,y:350,w:264,labelX:960,label:'3 termes'},{text:'polynôme',x:1328,y:350,w:340,labelX:1440,label:'un ou plusieurs termes'}];
  body=<g data-objective-entrance transform={`translate(0 ${motion.offsetY})`}>
   <ObjectiveBanner layout={original?'single-line':'standard'}>
    {original?<>{txt(630,285,'le',72,charter.navy,true)}{txt(940,285,'d’un polynôme',72,charter.navy,true)}</>:<>{txt(340,230,'Reconnaître',72,charter.navy,true)}{txt(340,350,'un',72,charter.navy,true)}{txt(704,350,', un',72,charter.navy,true)}{txt(1136,350,'et un',72,charter.navy,true)}</>}
    {terms.map((t,i)=>{const start=at(i+1),color=objectiveColor(i),active=f>=start&&(i===terms.length-1||f<at(i+2)),underline=t.y+20,anchor=t.x+t.w/2;
     return <g key={t.text} data-link-index={i}>
      {active&&<rect x={t.x-8} y={t.y-70} width={t.w+16} height="88" rx="10" fill={color} opacity=".1"/>}
      <text data-objective-title x={t.x} y={t.y} fontSize="72" fontWeight="700" fill={active?color:charter.navy}>{t.text}</text>
      <g opacity={f>=start?1:0} stroke={color} strokeWidth="4" fill="none"><path d={`M${t.x} ${underline} H${t.x+t.w}`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(start)}/><path data-objective-connector d={`M${anchor} ${underline} V480 C${anchor} 540 ${t.labelX} 540 ${t.labelX} 610`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(start+8,24)}/><path d={`M${t.labelX-20} 586 L${t.labelX} 610 L${t.labelX+20} 586`} opacity={p(start+24,8)}/></g>
      {show(start+16,<text x={t.labelX} y="725" textAnchor="middle" fontSize={i===2?52:62} fill={charter.ink}>{t.label}</text>)}
     </g>;
    })}
   </ObjectiveBanner>
  </g>;break;
 }
 case 'definition':{
  const concept=scene.concept!,poly=concept==='polynome',count=concept==='binome'?'deux':'trois';
  const emphasis=(key:string)=>62*(1+.04*Math.sin(Math.PI*p(cue(key,at(1)),26)));
  body=<>{frame}{show(at(1),<>{txt(235,420,<>Un <tspan fill={red} fontWeight="700" fontSize={emphasis('keyword')}>{names[concept].toLowerCase()}</tspan> est une expression algébrique</>,62)}{txt(235,535,<>réduite composée <tspan fill={red} fontWeight="700" fontSize={emphasis('count')}>{poly?'d’un ou plusieurs termes':`de ${count} termes`}</tspan>{poly?'.':''}</>,62)}</>)}
   {!poly&&show(cue('distinct',at(1)),<>{txt(235,650,'qui n’ont pas les mêmes variables',62)}{txt(235,765,'avec les mêmes exposants.',62)}</>)}
  </>;break;
 }
 case 'example':{
  const key=scene.expressionKey!,data=expressionData[key],count=reducedTermCount(data.terms),poly=scene.concept==='polynome',countBeat=poly?1:count+2,conclusionBeat=poly?2:count+3;
  if(revised){
   const variablesBeat=poly?6:countBeat+1;
   const hasComparison=key!=='deux-termes';
   const conclusion=at(scene.beats.length-1);
   const different=cue('different',at(variablesBeat));
   const firstTerm=2;
   const active=Array.from({length:count},(_,i)=>i).find(i=>f>=at(firstTerm+i)&&f<at(firstTerm+i+1))??-1;
   const compare=hasComparison&&f>=at(variablesBeat)&&f<conclusion
    ?poly&&f>=at(7)?'power':!poly&&f>=different?undefined:'variable':undefined;
   const ring=active>=0?Math.min(p(at(firstTerm+active),14),1-p(at(firstTerm+active+1)-8,8))
    :compare?p(compare==='power'?at(7):at(variablesBeat),13):0;
   const countName=count===2?'Deux':count===3?'Trois':'4';
   const result=scene.valid?names[scene.concept!]:`N’est pas un ${names[scene.concept!].toLowerCase()}`;
   body=<>{frame}{show(0,<PolynomialMath id={key} y={465} active={active} compare={compare} progress={ring}/>)}
    {show(at(countBeat),<>{arrow(960,515,572,at(countBeat),green)}{center(650,<><tspan fill={red} fontWeight="700">{countName}</tspan> termes</>,72)}</>)}
    {hasComparison&&show(different,<>{arrow(960,673,723,different,green)}{center(793,'Différents',62,red)}</>)}
    {show(conclusion,<>{arrow(960,hasComparison?812:680,hasComparison?863:802,conclusion,green)}
     {center(hasComparison?954:912,result,70,scene.valid&&key!=='quatre-termes'?green:red)}
     {txt(1540,472,scene.valid?'✓':'✕',96,scene.valid?green:red,true)}</>)}
   </>;
   break;
  }
  let active=-1;if(!poly)for(let i=0;i<count;i++)if(f>=at(i+2)&&f<at(i+3))active=i;
  const ring=active<0?0:Math.min(p(at(active+2),18),1-p(at(active+3)-8,8));
  body=<>{frame}{show(0,<PolynomialExpression id={key} y={470} active={active} activeProgress={ring}/>)}
   {show(at(countBeat),<>{arrow(960,525,625,at(countBeat))}{center(730,`${count===2?'Deux':count===3?'Trois':'Quatre'} termes`,76,red)}</>)}
   {show(at(conclusionBeat),<>{arrow(960,775,840,at(conclusionBeat))}{center(925,scene.valid?names[scene.concept!]:`N’est pas un ${names[scene.concept!].toLowerCase()}`,70,red)}{txt(1540,490,scene.valid?'✓':'✕',104,scene.valid?green:red,true)}</>)}
  </>;break;
 }
 case 'pronunciation':{
  if(revised){
   const word=scene.concept!;
   const parts=pronunciationParts[word];
   body=<PronunciationWord word={word} frame={f} syllableStarts={parts.map((_,i)=>at(i+1))} wholeStart={at(parts.length+1)}/>;
   break;
  }
  const word=names[scene.concept!];body=<>{frame}{center(440,word,112,'#00B0F0')}{show(at(1),center(670,scene.concept==='binome'?<><tspan fill="#0070C0">Bi</tspan><tspan fill={red}> - nôme</tspan></>:<><tspan fill="#0070C0">Po</tspan><tspan fill={red}> - ly</tspan><tspan fill={green}> - nôme</tspan></>,100))}{show(at(2),center(855,word.toLowerCase(),82,'#0070C0'))}</>;break;
 }
 case 'synthesis':{
  const cols=[{x:460,word:'Binôme',label:'2 termes',id:'binome',size:58},{x:960,word:'Trinôme',label:'3 termes',id:'synthese-trinome',size:50},{x:1460,word:'Polynôme',label:'un ou plusieurs',id:'synthese-polynome',size:45}] as const;
  body=<>{frame}{cols.map((v,i)=>{
   const start=at(i+1),count=cue('summaryCount'+i,start),example=cue('summaryExample'+i,start);
   const heading=<><rect x={v.x-215} y="340" width="430" height="105" rx="18" fill="white" stroke={charter.turquoise} strokeWidth="4"/>
    <text data-box-heading x={v.x} y="412" textAnchor="middle" fontSize="60" fontWeight="700" fill={charter.ink}>{headingLabel(v.word)}</text></>;
   const countBlock=<>{arrow(v.x,475,555,count,green)}
    <text x={v.x} y="645" textAnchor="middle" fontSize={i===2?48:64} fill={red}>{v.label}</text>
    {i===2&&<text x={v.x} y="705" textAnchor="middle" fontSize="48" fill={red}>termes</text>}</>;
   const exampleBlock=<>{arrow(v.x,i===2?735:710,795,revised?example:start+12,green)}
    <Expression id={v.id} y={900} x={v.x} size={v.size} highlight={false}/></>;
   return <g key={v.word} data-vocabulary-column>
    {revised?<>{show(start,heading)}{show(count,countBlock)}{show(example,exampleBlock)}</>
     :show(start,<>{heading}{countBlock}{exampleBlock}</>)}
   </g>;
  })}</>;break;
 }
 case 'vocabulary':body=<>{frame}{[{x:530,y:440,word:'Binôme'},{x:1380,y:440,word:'Trinôme'},{x:960,y:770,word:'Polynôme'}].map((v,i)=>{const start=cue('word'+i,i*25),scale=1+.035*Math.sin(Math.PI*p(start,28));return <g key={v.word} transform={`translate(${v.x} ${v.y}) scale(${scale}) translate(${-v.x} ${-v.y})`}><rect x={v.x-260} y={v.y-80} width="520" height="125" rx="20" fill="white" stroke={charter.turquoise} strokeWidth="4"/><text data-box-heading x={v.x} y={v.y+5} textAnchor="middle" fontSize="72" fontWeight="700" fill={f>=start&&f<start+35?red:charter.ink}>{headingLabel(v.word)}</text></g>;})}</>;break;
 case 'inclusion':{
  const columns=[{x:590,id:'binome',name:'Binôme'},{x:1330,id:'trinome',name:'Trinôme'}] as const;
  body=<>{frame}{show(0,<>{center(379,'Le binôme et le trinôme',62,charter.navy)}
   {center(459,'sont des polynômes particuliers.',62,charter.navy)}</>)}
   {columns.map(({x,id,name},i)=>{
    const start=at(i+1),label=cue('inclusionName'+i,start+18),poly=cue('inclusionPolynomial'+i,label+25);
    return <g key={id}>
     {show(start,<PolynomialMath id={id} x={x} y={610} size={86}/>)}
     {show(label,<>{arrow(x,653,704,label,green)}<text x={x} y="774" textAnchor="middle" fontSize="65" fill={green}>{name}</text></>)}
     {show(poly,<>{arrow(x,801,856,poly,green)}<text x={x} y="935" textAnchor="middle" fontSize="65" fill={green}>Polynôme</text></>)}
    </g>;
   })}
  </>;break;
 }
 case 'next':body=show(cue('nextTitle',0),<text x="960" y="557" textAnchor="middle" fontSize="82"
  fontWeight="700" fill="#087ABA">{polynomialObjective}</text>);break;
 }
 const header=<SectionHeader title={scene.title}/>;
 return <AbsoluteFill style={{background:charter.background,fontFamily:charter.font,color:charter.ink}}><svg width="1920" height="1080" viewBox="0 0 1920 1080" data-polynomial-scene={scene.kind}>{scene.kind!=='intro'&&scene.kind!=='next'&&(revised?enter(header):header)}{body}</svg><Audio src={staticFile(scene.audio)}/></AbsoluteFill>;
};
