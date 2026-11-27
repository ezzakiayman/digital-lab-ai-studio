import React from 'react';
import {AbsoluteFill,Audio,staticFile,useCurrentFrame,interpolate,Easing} from 'remotion';
import {Timeline} from '../lib/timeline';
import {gcd,lcm} from '../lib/ppcm';
import {ObjectiveDeclaration} from './ObjectiveDeclaration';
import {objectiveColor} from '../lib/objective';
import {charter} from '../lib/charter';
type Scene=Extract<Timeline['scenes'][number],{type:'ppcm'}>;
const teal='#0DBBA1',ink='#1D1D1D',red='#E60012',navy='#41476D',yellow='#FDFD99',blue='#0070C0';
export const Ppcm:React.FC<{scene:Scene}>=({scene})=>{
 const f=useCurrentFrame();
 const at=(n:number)=>scene.beats.find(b=>b.stage===n)?.from??0;
 const cue=(key:string,fallback:number)=>scene.cues?.[key]??fallback;
 const progress=(from:number,d=16)=>interpolate(f,[from,from+d],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)});
 const revealAt=(from:number,children:React.ReactNode)=>{const p=progress(from);return <g opacity={p} transform={`translate(0,${8*(1-p)})`}>{children}</g>;};
 const reveal=(n:number,children:React.ReactNode)=>revealAt(at(n),children);
 const popAt=(from:number,children:React.ReactNode,x=960,y=600)=>{const scale=interpolate(f,[from,from+8,from+20],[0.94,1.025,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});return <g opacity={progress(from,10)} transform={`translate(${x},${y}) scale(${scale}) translate(${-x},${-y})`}>{children}</g>;};
 const text=(x:number,y:number,s:React.ReactNode,size=62,color=ink,bold=false)=><text x={x} y={y} fontSize={size} fill={color} fontWeight={bold?700:400}>{s}</text>;
 const center=(y:number,s:React.ReactNode,size=80,color=ink)=><text x="960" y={y} textAnchor="middle" fontSize={size} fill={color} fontWeight="700">{s}</text>;
 const sectionColor=charter.turquoise;
 const box=(y:number,h:number)=><rect data-content-box x="169" y={y} width="1599" height={h} rx="28" fill={charter.background} stroke={sectionColor} strokeWidth="6"/>;
 const formula=(y:number,s:React.ReactNode,size=76)=>center(y,s,size);
 const arrow=(y:number,from:number)=><g fill="none" stroke={red} strokeWidth="5"><path d={`M960 ${y} v70`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress(from,20)}/><path d={`M942 ${y+48} L960 ${y+70} L978 ${y+48}`} opacity={progress(from+14,8)}/></g>;
 const badge=<><rect x="194" y="111" width={scene.title==='Définition'?510:scene.title==='Propriété 1'||scene.title==='Propriété 2'?470:450} height="90" rx="30" fill={sectionColor}/>{text(233,175,scene.title,64,'white',true)}</>;
 const assumptions=text(220,350,'x et y sont deux entiers positifs non nuls.',58);
 const prop1=<>{text(220,460,<>Si <tspan fontStyle="italic">x</tspan> est un <tspan fontWeight="700">multiple</tspan> de <tspan fontStyle="italic">y</tspan>, alors :</>,62)}{formula(620,<>PPCM(x ; y) = <tspan fill={red}>x</tspan></>)}</>;
 const prop2=formula(535,<>PPCM(x ; y) × PGCD(x ; y) = x × y</>,67);
 let body:React.ReactNode;
 switch(scene.kind){
 case 'intro':body=<ObjectiveDeclaration frame={f} starts={[at(1),at(2),at(3)]} explanationsFrom={[cue('explanation1',at(1)+24),cue('explanation2',at(2)+24),cue('positiveExamples',at(3)+24)]} invalidFrom={cue('invalidExamples',at(4))}/>;break;
 case 'definition':body=<>{badge}{box(270,380)}{reveal(0,assumptions)}{reveal(1,<>{text(220,455,'Le plus petit multiple commun non nul',62,ink,true)}{text(220,555,'de x et de y est noté :',62)}{arrow(680,at(1))}{formula(880,'PPCM(x ; y)',104)}</>)}</>;break;
 case 'acronym':body=<>{badge}{box(270,650)}{['Plus','Petit','Commun','Multiple'].map((word,i)=>{const x=390+i*380,start=cue('letter'+i,at(i)),wordFrom=cue('word'+i,at(i)+22),active=f>=start&&(i===3||f<cue('letter'+(i+1),at(i+1))),color=objectiveColor(i),scale=interpolate(f,[start,start+8,start+22],[1,1.12,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});return <g key={word} data-acronym-letter={i}>
 <text x={x} y="410" textAnchor="middle" fontSize="116" fontWeight="700" fill={active?color:ink} transform={`translate(${x},375) scale(${scale}) translate(${-x},-375)`}>{['P','P','C','M'][i]}</text>
 <g fill="none" stroke={color} strokeWidth="4" opacity={f>=start?1:0}><path d={`M${x} 440 V620`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress(start+5,20)}/><path d={`M${x-18} 598 L${x} 620 L${x+18} 598`} opacity={progress(start+20,8)}/></g>
 {popAt(wordFrom,<text x={x} y="750" textAnchor="middle" fontSize="68" fontWeight="700" fill={ink}><tspan fill={color}>{word[0]}</tspan>{word.slice(1)}</text>,x,720)}
 </g>;})}{reveal(3,center(1000,'Plus Petit Commun Multiple',62,navy))}</>;break;
 case 'multiples':body=<>{badge}{box(270,700)}{reveal(0,center(390,'Deux entiers positifs : 6 et 4',76))}{reveal(1,text(235,530,'Multiples communs non nuls :',60))}{[12,24,36].map((n,i)=><g key={n}>{popAt(cue('number'+n,at(1)+i*15),text(440+i*430,720,n,108,blue,true),500+i*430,680)}</g>)}<ellipse cx="500" cy="683" rx="118" ry="80" pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress(cue('circle12',at(2)),24)} opacity={f>=cue('circle12',at(2))?1:0} stroke={red} strokeWidth="6" fill="none"/>{revealAt(cue('circle12',at(2)),center(875,'Le plus petit est 12.',70,red))}</>;break;
 case 'lcm-result':body=<>{badge}{box(300,460)}{reveal(0,<>{center(455,'Le plus petit multiple commun de 6 et 4',62)}<rect x="365" y="525" width="1190" height="150" fill={yellow}/>{formula(635,<>PPCM(6 ; 4) = <tspan fill={red}>{lcm(6,4)}</tspan></>,98)}</>)}</>;break;
 case 'property1':body=<>{badge}{box(270,550)}{reveal(1,assumptions)}{reveal(2,prop1)}</>;break;
 case 'divisible-example':body=<>{badge}{box(270,745)}{reveal(0,center(375,<><tspan fill={red}>72</tspan> et 8</>,88))}{popAt(at(1),formula(515,<><tspan fill={red}>72</tspan> = 8 × 9</>))}{reveal(2,<>{arrow(550,at(2))}{center(740,<><tspan fill={red}>72</tspan> est un multiple de 8.</>,66)}</>)}{reveal(3,<><rect x="420" y="815" width="1080" height="130" fill={yellow}/>{formula(905,<>PPCM(<tspan fill={red}>72</tspan> ; 8) = <tspan fill={red}>{lcm(72,8)}</tspan></>,84)}</>)}</>;break;
 case 'property2':body=<>{badge}{box(270,500)}{reveal(0,assumptions)}{reveal(1,<>{prop2}{text(220,690,'Le PPCM multiplié par le PGCD est égal à x × y.',55)}</>)}</>;break;
 case 'product-example':body=<>{badge}{box(270,700)}{reveal(0,center(385,'6 et 4',88))}{popAt(at(1),formula(590,<>PPCM(6 ; 4) = <tspan fill={blue}>{lcm(6,4)}</tspan></>,88))}{popAt(at(2),formula(800,<>PGCD(6 ; 4) = <tspan fill={blue}>{gcd(6,4)}</tspan></>,88))}</>;break;
 case 'verification':body=<>{badge}{box(270,745)}{reveal(0,<>{formula(395,'PPCM(6 ; 4) × PGCD(6 ; 4)',65)}{formula(535,<>12 × 2 = <tspan fill={blue}>24</tspan></>,88)}</>)}{popAt(at(1),formula(685,<>6 × 4 = <tspan fill={blue}>24</tspan></>,88))}{reveal(2,<>{formula(835,'PPCM(6 ; 4) × PGCD(6 ; 4) = 6 × 4',58)}{center(950,'La propriété est vérifiée.',60,'#00B050')}</>)}</>;break;
 case 'pronunciation':body=<>{badge}{reveal(0,center(460,'MULTIPLE',140,teal))}{reveal(1,center(780,<><tspan fill="#087EB7">mul-</tspan><tspan fill={red}>ti-</tspan><tspan fill="#E8A31B">ple</tspan></>,126))}</>;break;
 case 'summary':body=<>{badge}{box(270,700)}{reveal(1,<>{text(220,390,'Déterminer le PPCM de deux entiers',66,ink,true)}{text(220,495,'positifs non nuls.',66,ink,true)}</>)}{reveal(2,formula(780,<>PPCM(6 ; 4) = <tspan fill={blue}>12</tspan></>,98))}</>;break;
 case 'summary1':body=<>{badge}{box(270,600)}{reveal(0,<>{assumptions}{prop1}</>)}</>;break;
 case 'summary2':body=<>{badge}{box(270,550)}{reveal(0,<>{assumptions}{prop2}</>)}</>;break;
 case 'vocabulary':body=<>{badge}{box(270,650)}{['multiple','commun','ppcm'].map((word,i)=>{const start=cue(word,0);const p=progress(start);const pulse=f<start?0:f<start+54?0.18+0.16*Math.sin((f-start)/54*Math.PI):0;return <g key={word}>{revealAt(start,<><rect x="420" y={345+i*180} width="1080" height="140" rx="15" fill={yellow} opacity={pulse}/>{center(455+i*180,i===2?'PPCM':word,i===2?110:100,[teal,navy,red][i])}</>)}</g>;})}</>;break;
 }
 return <AbsoluteFill style={{background:'white',fontFamily:'Arial, sans-serif'}}><svg width="1920" height="1080" viewBox="0 0 1920 1080">{body}</svg><Audio src={staticFile(scene.audio)}/></AbsoluteFill>;
};
