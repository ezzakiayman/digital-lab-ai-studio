import React from 'react';
import {AbsoluteFill,Audio,Easing,interpolate,staticFile,useCurrentFrame} from 'remotion';
import {Timeline} from '../lib/timeline';
import {charter} from '../lib/charter';
import {ObjectiveBanner} from './ObjectiveDeclaration';
import {QuestionMark} from './QuestionMark';
import {LinkedObjective,TeachingEntrance} from './StoryboardVisuals';
import {PronunciationWord} from './PronunciationWord';
import {SectionHeader} from './SectionHeader';
import {headingLabel} from '../lib/presentation';
type Scene=Extract<Timeline['scenes'][number],{type:'fractions'}>;
const red='#E60012',blue='#0070C0',green=charter.turquoise;
/** Native editable fraction, with a distinct denominator colour when pedagogically relevant. */
export const Fraction:React.FC<{x:number;y:number;n:React.ReactNode;d:React.ReactNode;size?:number;width?:number;denominatorColor?:string;numeratorScale?:number;denominatorScale?:number}>=({x,y,n,d,size=86,width=150,denominatorColor=charter.ink,numeratorScale=1,denominatorScale=1})=><g data-fraction>
 <text x={x} y={y-22} textAnchor="middle" fontSize={size} transform={numeratorScale===1?undefined:`translate(${x} ${y-22}) scale(${numeratorScale}) translate(${-x} ${22-y})`}>{n}</text>
 <path d={`M${x-width/2} ${y} H${x+width/2}`} stroke={charter.ink} strokeWidth="4"/>
 <text x={x} y={y+size} textAnchor="middle" fontSize={size} fill={denominatorColor} transform={`translate(${x} ${y+size*.65}) scale(${denominatorScale}) translate(${-x} ${-y-size*.65})`}>{d}</text>
</g>;
export const Fractions:React.FC<{scene:Scene}>=({scene})=>{
 const revised=scene.revision!==undefined;
 const reviewed=scene.revision==='2026-11-12';
 const f=useCurrentFrame(),at=(i:number)=>scene.beats[i]?.from??0,cue=(k:string,b:number)=>scene.cues[k]??b;
 const p=(s:number,d=18)=>interpolate(f,[s,s+d],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)});
 const show=(s:number,n:React.ReactNode)=><g opacity={p(revised?Math.max(13,s):s)} transform={`translate(0,${8*(1-p(revised?Math.max(13,s):s))})`}>{n}</g>;
 const pop=(s:number,x:number,y:number,n:React.ReactNode)=>{const z=interpolate(f,[s,s+8,s+20],[.94,1.025,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});return <g opacity={p(s,10)} transform={`translate(${x} ${y}) scale(${z}) translate(${-x} ${-y})`}>{n}</g>;};
 const txt=(x:number,y:number,n:React.ReactNode,size=64,color=charter.ink,weight=400)=><text x={x} y={y} fontSize={size} fill={color} fontWeight={weight}>{n}</text>;
 const center=(y:number,n:React.ReactNode,size=72,color=charter.ink)=><text x="960" y={y} textAnchor="middle" fontSize={size} fill={color}>{n}</text>;
 const frac=(x:number,y:number,n:React.ReactNode,d:React.ReactNode,size=86,width=150,denominatorColor=charter.ink)=><Fraction {...{x,y,n,d,size,width,denominatorColor}}/>;
 const box=<rect data-content-box x="169" y="270" width="1599" height="735" rx="28" fill={charter.background} stroke={green} strokeWidth="6"/>;
 const frame=revised?null:box;
 const badge=revised?<TeachingEntrance frame={f}><SectionHeader title={scene.title}/>{scene.kind!=='pronunciation'&&box}</TeachingEntrance>:<><rect x="194" y="111" width={scene.kind==='denominator'?900:510} height="90" rx="30" fill={green}/>{txt(233,175,scene.title,64,'white',700)}</>;
 const question=(x:number,y:number)=> <g transform={`translate(${x-960} ${y-673})`}><QuestionMark/></g>;
 const animateQuestion=(x:number,y:number)=>{
  const start=cue('question',0);
  const scale=interpolate(f,[start,start+6,start+17],[.86,1.09,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.out(Easing.quad)});
  return <g opacity={p(start-1,5)} transform={`translate(${x} ${y}) scale(${scale})`}>
   <QuestionMark x={-66} y={-71} width={132}/>
  </g>;
 };
 const inline=(x:number,y:number,n:React.ReactNode,size=66)=><text x={x} y={y} dominantBaseline="central" fontSize={size}>{n}</text>;
 const reveal=(name:string,x:number,y:number,style:{
  size?:number;centered?:boolean;aligned?:boolean;bold?:boolean;emphasis?:readonly string[];italic?:readonly string[];
 }={})=><text data-word-reveal={name} x={x} y={y} xmlSpace="preserve" fontSize={style.size??66}
  textAnchor={style.centered?'middle':'start'} dominantBaseline={style.aligned?'central':undefined} fontWeight={style.bold?700:400}>
  {scene.reveals?.[name]?.map(({text,from},i)=><tspan key={i} opacity={f>=from?1:0}
   fill={style.emphasis?.includes(text)?red:undefined}
   fontWeight={style.emphasis?.includes(text)?700:undefined}
   fontStyle={style.italic?.includes(text)?'italic':undefined}>{(i?' ':'')+text}</tspan>)}
 </text>;
 let body:React.ReactNode;
 switch(scene.kind){
 case 'intro':{
  if(revised){
   body=<LinkedObjective frame={f} title="Simplifier une fraction et réduire deux fractions au même dénominateur" measure={2185} size={47} fadeBeforeNext={reviewed} links={[
    {from:0,width:678,start:at(1),content:x=>show(cue('arabic0',at(1)+24),<text x={x} y="720" textAnchor="middle" fontSize="84" direction="rtl" unicodeBidi="plaintext">اختزال</text>)},
    {from:771,width:1414,start:at(2),content:x=>show(cue('arabic1',at(2)+24),<text x={x} y="720" textAnchor="middle" fontSize="84" direction="rtl" unicodeBidi="plaintext">توحيد المقام</text>)},
   ]}/>;
   break;
  }
  const first=f>=at(1)&&f<at(2),second=f>=at(2);
  const title=(x:number,y:number,s:string,active:boolean,color:string)=><g>{active&&<rect x={x-8} y={y-70} width={s==='Simplifier une fraction'?776:s==='réduire'?258:1336} height="88" rx="10" fill={color} opacity=".1"/>}<text data-objective-title x={x} y={y} fontSize="72" fontWeight="700" fill={active?color:charter.navy}>{s}</text></g>;
  body=<ObjectiveBanner>
   {title(340,230,'Simplifier une fraction',first,red)}{txt(1120,230,'et',72,charter.navy,700)}{title(1205,230,'réduire',second,green)}
   {title(340,350,'deux fractions au même dénominateur',second,green)}
   {[{start:at(1),color:red,path:'M720 250 H270 V500 C270 555 480 555 480 610',underline:'M340 250 H1100',x:480,label:'اختزال'},{start:at(2),color:green,path:'M1000 370 V480 C1000 545 1280 545 1280 610',underline:'M340 370 H1660',x:1280,label:'توحيد المقام'}].map((t,i)=><g key={i} data-link-index={i} opacity={f>=t.start?1:0} stroke={t.color} strokeWidth="4" fill="none"><path d={t.underline} pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(t.start)}/><path data-objective-connector d={t.path} pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(t.start+8,24)}/><path d={`M${t.x-20} 586 L${t.x} 610 L${t.x+20} 586`} opacity={p(t.start+25,8)}/><text x={t.x} y="745" textAnchor="middle" fontSize="84" direction="rtl" unicodeBidi="plaintext" stroke="none" fill={charter.ink} opacity={p(cue('arabic'+i,t.start+30))}>{t.label}</text></g>)}
  </ObjectiveBanner>;break;
 }
 case 'irreducible':{
  if(reviewed){
   const conclusion=cue('conclusion',at(4));
   const x=818+142*p(at(1),15)-232*p(conclusion,15);
   const y=632-150*p(at(2)-15,20);
   const pulse=(name:string)=>1+.24*Math.sin(Math.PI*p(cue(name,0)-1,15));
   body=<>
    <Fraction x={x} y={y} n={23} d={41} size={96} width={150} numeratorScale={pulse('numerator')} denominatorScale={pulse('denominator')}/>
    {f<at(1)&&<>{inline(948,y,'=',84)}{animateQuestion(1090,y)}</>}
    {show(at(2),center(707,<>PGCD(23 ; 41) = <tspan fill={red}>1</tspan></>,76))}
    {show(at(3),center(851,'23 et 41 sont premiers entre eux',66))}
    {reveal('conclusion',x+122,y,{aligned:true,emphasis:['irréductible']})}
   </>;
   break;
  }
  body=<>{frame}{frac(650,440,23,41,105,150)}
  {f<at(1)&&<>{txt(820,475,'=',100)}{question(1080,445)}</>}
  {show(at(2),center(655,<>PGCD(23 ; 41) = <tspan fill={red}>1</tspan></>,76))}
  {show(at(3),center(775,'23 et 41 sont premiers entre eux',66))}
  {show(at(4),<>{txt(820,475,'est',64)}{txt(950,475,'irréductible',76,red,700)}</>)}
  </>;break;
 }
 case 'reducible':{
  if(reviewed){
   const division=[cue('division2',at(2)),cue('division3',at(3)),cue('division6',at(4))];
   const step=division.findLastIndex(start=>f>=start);
   const divisor=[2,3,6][step];
   const conclusion=scene.reveals?.conclusion?.[0]?.from??at(6);
   const x=818-163*p(at(1),16)+305*p(at(5),16)-310*p(conclusion,16);
   const y=631-74*p(at(1),16)-37*p(at(5),16);
   const emphasis=step<0?1:1+.055*Math.sin(Math.PI*p(division[step],16));
   body=<>
    {frac(x,y,42,36,100,150)}
    {f<at(1)&&<>{inline(948,y,'=',84)}{animateQuestion(1090,y)}</>}
    {f>=at(1)&&f<at(5)&&show(at(1),<>
     {inline(824,y,'=',84)}
     <g transform={`translate(1130 ${y}) scale(${emphasis}) translate(-1130 ${-y})`}>
      {frac(1130,y,<>42 <tspan fill={red}>÷ {divisor??'…'}</tspan></>,<>36 <tspan fill={red}>÷ {divisor??'…'}</tspan></>,92,440)}
     </g>
    </>)}
    {show(at(5),center(793,<>PGCD(42 ; 36) = <tspan fill={red} opacity={f>=cue('gcd',at(5))?1:0}>6</tspan></>,76))}
    {reveal('conclusion',x+122,y,{aligned:true,emphasis:['réductible','6']})}
   </>;
   break;
  }
  let divisor=0;if(f>=at(4))divisor=6;else if(f>=at(3))divisor=3;else if(f>=at(2))divisor=2;
  body=<>{frame}{frac(600,455,42,36,105,150)}
   {f<at(1)&&<>{txt(760,490,'=',100)}{question(1030,455)}</>}
   {f>=at(1)&&f<at(5)&&show(at(1),<>{txt(760,490,'=',100)}{pop(divisor?at(divisor===2?2:divisor===3?3:4):at(1),1140,455,frac(1140,455,<>42 <tspan fill={red}>÷ {divisor||'…'}</tspan></>,<>36 <tspan fill={red}>÷ {divisor||'…'}</tspan></>,95,440))}</>)}
   {show(at(5),center(710,<>PGCD(42 ; 36) = <tspan fill={red}>6</tspan></>,76))}
   {show(at(6),<>{txt(780,490,'est',64)}{txt(910,490,'réductible',76,red,700)}{txt(1320,490,'par 6',64)}</>)}
  </>;break;
 }
 case 'definition':{
  const variable=(value:string)=>revised?<tspan fontStyle="italic">{value}</tspan>:value;
  if(reviewed){
   body=<>
    {reveal('fractionLabel',447,490,{aligned:true})}
    {f>=cue('fraction',at(1))&&frac(892,490,variable('a'),variable('b'),70,110)}
    {reveal('irreducible',999,490,{aligned:true,emphasis:['est','irréductible']})}
    {reveal('condition',960,680,{centered:true,italic:['a','b']})}
    {reveal('coprime',960,823,{centered:true,bold:true})}
   </>;
   break;
  }
  body=<>{frame}{show(at(1),<>{txt(240,430,'Une fraction',66)}{frac(720,410,variable('a'),variable('b'),68,100)}{txt(830,430,'est irréductible',66,red,700)}</>)}
   {show(cue('condition',at(1)),txt(240,610,<>si et seulement si {variable('a')} et {variable('b')}</>,66))}
   {show(cue('coprime',at(1)),txt(240,735,'sont premiers entre eux.',66,charter.ink,700))}</>;
  break;
 }
 case 'property':body=reviewed?<>
  {reveal('first',960,496,{centered:true,size:72})}
  {reveal('second',960,645,{centered:true,size:72})}
  {reveal('third',960,794,{centered:true,size:72})}
 </>:<>{frame}{show(at(1),txt(240,440,'Le plus petit dénominateur commun',66))}{show(cue('fractions',at(1)),txt(240,560,'de deux fractions est le PPCM',66))}{show(cue('denominators',at(1)),txt(240,680,'de leurs deux dénominateurs.',66))}</>;break;
 case 'common':{
  const zoom=(s:number)=>1+.12*Math.sin(Math.PI*p(s,30));
  body=<>{frame}{pop(cue('firstFraction',0),770,390,<Fraction x={770} y={390} n={5} d={9} size={82} width={120} denominatorColor={f>=at(1)?blue:charter.ink} denominatorScale={zoom(at(1))}/>)}{show(cue('secondFraction',0),txt(930,420,'et',66))}{pop(cue('secondFraction',0),1160,390,<Fraction x={1160} y={390} n={7} d={15} size={82} width={120} denominatorColor={f>=at(1)?blue:charter.ink} denominatorScale={zoom(at(1)+30)}/>)}
  {show(at(2),center(650,<>PPCM(<tspan fill={blue}>9 ; 15</tspan>){f>=at(5)&&<> = <tspan fill={red}>45</tspan></>}</>,80))}
  {f<at(5)&&[45,90,135,180].map((n,i)=><g key={n}>{pop(cue('multiple'+i,at(3)+i*20),660+i*200,820,txt(590+i*200,845,n,76,blue,700))}</g>)}
  {f>=at(4)&&f<at(5)&&<ellipse cx="635" cy="820" rx="76" ry="58" fill="none" stroke={red} strokeWidth="5" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(cue('minimum',at(4)),24)}/>}
 </>;break;}
 case 'denominator':body=reviewed?<>
  {show(cue('formula',0),center(458,<>PPCM(15 ; 9) = <tspan fill={red} opacity={f>=cue('formulaResult',0)?1:0}>45</tspan></>,84))}
  {reveal('result',960,631,{centered:true,emphasis:['45']})}
  {f>=cue('fractionLead',at(1))&&inline(712,806,'de')}
  {f>=cue('fractionPair',at(1))&&<>{frac(877,806,5,9,80,100)}{inline(979,806,'et')}{frac(1155,806,7,15,80,100)}</>}
 </>:<>{frame}{center(425,<>PPCM(15 ; 9) = <tspan fill={red}>45</tspan></>,84)}
  {show(at(1),<>{center(610,<><tspan fill={red}>45</tspan> est le plus petit dénominateur commun</>,60)}{txt(620,815,'de',64)}{frac(850,790,5,9,80,100)}{txt(1000,815,'et',64)}{frac(1190,790,7,15,80,100)}</>)}
 </>;break;
 case 'pronunciation':body=revised?<PronunciationWord word="irreductible" frame={f} syllableStarts={[1,2,3,4].map(at)} wholeStart={at(5)}/>:<>{frame}{center(435,'IRRÉDUCTIBLE',104,'#00B0F0')}{show(at(1),<text x="960" y="650" textAnchor="middle" fontSize="98" xmlSpace="preserve"><tspan fill={blue}>i - </tspan><tspan fill={red}>ré</tspan><tspan fill={blue}> - </tspan><tspan fill="#70AD47">duc</tspan><tspan fill={blue}> - tible</tspan></text>)}{show(at(2),center(835,'irréductible',82,blue))}</>;break;
 case 'vocabulary':body=<>{frame}{[{word:'Dénominateur',x:280},{word:'Irréductible',x:1110}].map((v,i)=><g key={v.word} data-box-heading><rect x={v.x-35} y="355" width="555" height="115" rx="18" fill={f>=at(i+1)?'#E7F9F5':'white'} stroke={green} strokeWidth="4"/>{txt(v.x,432,revised?headingLabel(v.word):v.word,66,charter.ink,700)}</g>)}
  {reviewed?<>
   {f>=cue('vocabularyOne',at(1))&&frac(520,650,1,2,108,135,red)}
   {f>=cue('denominator',at(1)+35)&&<ellipse cx="520" cy="720" rx="70" ry="65" stroke={red} strokeWidth="5" fill="none"/>}
   {f>=cue('vocabularyTwo',at(2))&&frac(1350,650,3,4,108,135)}
  </>:<>
   {show(at(1),frac(520,650,1,2,108,135,red))}{show(cue('denominator',at(1)+35),<ellipse cx="520" cy="720" rx="70" ry="65" stroke={red} strokeWidth="5" fill="none"/>)}{show(at(2),frac(1350,650,3,4,108,135))}
  </>}
 </>;break;
 }
 return <AbsoluteFill style={{background:charter.background,fontFamily:charter.font,color:charter.ink}}><svg width="1920" height="1080" viewBox="0 0 1920 1080" fill={charter.ink} data-fractions-scene={scene.kind}>{scene.kind!=='intro'&&badge}{revised&&scene.kind!=='intro'?<g opacity={reviewed?p(2,8):p(13,10)}>{body}</g>:body}</svg><Audio src={staticFile(scene.audio)}/></AbsoluteFill>;
};
