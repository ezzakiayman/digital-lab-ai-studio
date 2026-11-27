import React from 'react';
import {AbsoluteFill, Audio, Easing, interpolate, staticFile} from 'remotion';
import {charter} from '../lib/charter';
import {objectiveColor} from '../lib/objective';
import {objectiveEntrance} from '../lib/presentation';
import {ObjectiveBanner} from './ObjectiveDeclaration';
import {SectionHeader} from './SectionHeader';

export const easeReveal=(frame:number,start:number,length=16)=>interpolate(frame,[start,start+length],[0,1],{
 extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic),
});

export function TeachingEntrance({frame,children}:{frame:number;children:React.ReactNode}){
 const progress=easeReveal(frame,0,13);
 return <g opacity={.2+.8*progress} transform={`translate(0 ${12*(1-progress)})`}>{children}</g>;
}

export function TeachingVideo({frame,audio,title,boxed=true,children}:{
 frame:number;audio:string;title?:string;boxed?:boolean;children:React.ReactNode;
}){
 return <AbsoluteFill style={{background:'white',fontFamily:charter.font,color:charter.ink}}>
  <svg width="1920" height="1080" viewBox="0 0 1920 1080" fill={charter.ink}>
   {title&&<TeachingEntrance frame={frame}>
    <SectionHeader title={title}/>
    {boxed&&<rect data-content-box x="169" y="270" width="1599" height="735" rx="28"
     fill="white" stroke={charter.turquoise} strokeWidth="6"/>}
   </TeachingEntrance>}
   {children}
  </svg>
  <Audio src={staticFile(audio)}/>
 </AbsoluteFill>;
}

type Link = {from:number;width:number;start:number;end?:number;content?:(x:number)=>React.ReactNode};
export function LinkedObjective({frame,title,measure,size,links,fadeBeforeNext=false,mathSuffix,mathOffset,formula}:{
 frame:number;title:string;measure:number;size:number;links:Link[];fadeBeforeNext?:boolean;
 mathSuffix?:string;mathOffset?:number;formula?:(left:number,scale:number)=>React.ReactNode;
}){
 const scale=size/64;
 const x=1030-measure*scale/2;
 const {offsetY}=objectiveEntrance(frame,links[0].start,'single-line');
 return <g data-objective-entrance transform={`translate(0 ${offsetY})`}>
  <ObjectiveBanner layout="single-line">
   <text data-objective-title x={x} y="282" fontSize={size} fontWeight="700" fill="#263956">{title}
    {mathSuffix&&mathOffset!==undefined&&<tspan x={x+mathOffset*scale} fontFamily={mathFont} fontWeight="400">
     {[...mathSuffix].map(glyph=>mathLetters[glyph]??glyph).join('')}
    </tspan>}
   </text>
   {formula?.(x,scale)}
  </ObjectiveBanner>
  {links.map(({from,width,start,end,content},index)=>{
   const left=x+from*scale, right=left+width*scale, mid=(left+right)/2;
   const color=objectiveColor(index), next=links[index+1]?.start;
   const fadeStart=end!==undefined?end-12:next===undefined?undefined:next-(fadeBeforeNext?12:0);
   const opacity=easeReveal(frame,start,8)*(fadeStart===undefined?1:1-easeReveal(frame,fadeStart,12));
   return <g data-link-index={index} key={index} opacity={opacity}>
    <g fill="none" stroke={color} strokeWidth="4">
     <path d={`M${left} 303 H${right}`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-easeReveal(frame,start,14)}/>
     {content&&<>
      <path data-objective-connector d={`M${mid} 303 V580`} pathLength="1" strokeDasharray="1" strokeDashoffset={1-easeReveal(frame,start+8,21)}/>
      <path d={`M${mid-15} 558 L${mid} 580 L${mid+15} 558`} opacity={easeReveal(frame,start+29,7)}/>
     </>}
    </g>
    {content&&<g data-objective-explanation-center={mid}>{content(mid)}</g>}
   </g>;
  })}
 </g>;
}

const powerDigits:Record<string,string>={'¹':'1','²':'2','³':'3','⁴':'4'};
const mathLetters:Record<string,string>={x:'𝒙',y:'𝒚',z:'𝒛',a:'𝒂'};
const mathWidths:Record<string,number>={x:.58,y:.60,z:.56,a:.58};
const mathFont='Cambria Math, Cambria, serif';

export function MathVariable({name}:{name:'x'|'y'|'z'}){
 return <tspan fontFamily={mathFont} fontWeight="400" fontStyle="normal">{mathLetters[name]}</tspan>;
}

export function MathFormula({formula,x=960,y,size=82,colorAxes=false,background,mark,markSpans,markColor='#E60012',markProgress=1,tokenColors,tokenMarks}:{
 formula:string;x?:number;y:number;size?:number;colorAxes?:boolean;background?:string;
 mark?:number[];markSpans?:[number,number][];markColor?:string;markProgress?:number;
 tokenColors?:Record<number,string>;tokenMarks?:{index:number;endIndex?:number;color?:string;progress:number}[];
}){
 let position=0;
 const tokens=[...formula].map((glyph,index)=>{
  const variable=Object.hasOwn(mathLetters,glyph);
  const power=powerDigits[glyph];
  const width=glyph===' ' ? .26 : power ? .37 : variable ? mathWidths[glyph] : /[()]/.test(glyph) ? .36 : .59;
  const axis=variable?glyph:power?formula[index-1]:/\d/.test(glyph)&&/[xyz]/.test(formula[index+1]??'')?formula[index+1]:'';
  const ink=tokenColors?.[index]??(colorAxes?(axis==='x'?'#0070C0':axis==='y'?'#C00000':charter.ink):charter.ink);
  const token={glyph,power,variable,width,offset:position,ink};
  position+=width;
  return token;
 });
 const left=x-position*size/2;
 return <g data-formula={formula} aria-label={formula} fontFamily="Cambria, Times New Roman, serif" fontWeight="700">
  {background&&<rect x={left-23} y={y-size*.92} width={position*size+46} height={size*1.22} rx="17" fill={background}/>}
  {tokens.map((t,i)=>t.glyph===' '?null:<text key={i} x={left+t.offset*size} y={t.power?y-size*.43:y}
   fontSize={t.power?size*.62:size} fill={t.ink} data-math-role={t.power?'power':t.variable?'variable':undefined}
   fontFamily={t.variable?mathFont:undefined} fontWeight={t.variable?400:undefined} fontStyle="normal">
   {t.variable?mathLetters[t.glyph]:t.power??t.glyph}
  </text>)}
  {[
   ...(markSpans??mark?.map(i=>[i,i] as const)??[]).map(([first,last])=>({first,last,progress:markProgress,color:markColor,term:false})),
   ...(tokenMarks??[]).map(({index,endIndex,color,progress})=>({
    first:index,last:endIndex??index,progress,color:color??markColor,term:endIndex!==undefined&&endIndex>index,
   })),
  ].map(({first,last,progress,color,term})=>{
   const a=tokens[first], b=tokens[last];
   if(!a||!b)return null;
   const width=b.offset+b.width-a.offset;
   const exponent=first===last&&a.power;
   return <ellipse key={first} cx={left+(a.offset+width/2)*size} cy={y-size*(exponent ? .63 : term ? .32 : .26)}
    rx={size*width/2+(term?40:8)} ry={size*(exponent ? .29 : term ? .77 : .40)} fill="none" stroke={color} strokeWidth="4"
    opacity={progress} pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress}/>;
  })}
 </g>;
}

