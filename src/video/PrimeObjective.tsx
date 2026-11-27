import React from 'react';
import {Easing, interpolate} from 'remotion';
import {charter} from '../lib/charter';
import {objectiveColor} from '../lib/objective';
import {objectiveEntrance} from '../lib/presentation';
import {ObjectiveBanner} from './ObjectiveDeclaration';

const title = 'Reconnaître et vérifier si un nombre est premier';
// Measured Arial Bold advances at 64 px. The banner text begins at x=300.
const terms = [
 {x:300,width:371},
 {x:764,width:215},
 {x:1529,width:236},
];
const examples = [
 {number:2,dx:-87,y:711,color:'#8FAADC'},
 {number:3,dx:0,y:766,color:'#70AD47'},
 {number:5,dx:54,y:856,color:'#111111'},
 {number:7,dx:87,y:711,color:'#ED7D31'},
 {number:11,dx:-54,y:856,color:'#FFC000'},
];

export const PrimeObjective: React.FC<{frame:number; starts:number[]; cues:Record<string,number>; arabicLabel?:string}> =
 ({frame,starts,cues,arabicLabel='تحقق'}) => {
  const [,first,second,third] = starts;
  const entrance = objectiveEntrance(frame,first,'single-line');
  const progress = (start:number,length=16) => interpolate(frame,[start,start+length],[0,1],{
   extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic),
  });
  return <g data-objective-entrance transform={`translate(0 ${entrance.offsetY})`}>
   <ObjectiveBanner layout="single-line">
    <text data-objective-title x="300" y="282" fontSize="64" fontWeight="700" fill="#263956">{title}</text>
   </ObjectiveBanner>
   {terms.map(({x,width},i)=>{
    const start=starts[i+1],color=objectiveColor(i),midpoint=x+width/2;
    const next=starts[i+2];
    const fade=next===undefined?1:1-progress(next,12);
    return <g key={x} data-link-index={i} opacity={progress(start,8)*fade}>
     <path d={`M${x} 303 H${x+width}`} pathLength="1" fill="none" stroke={color} strokeWidth="4"
      strokeDasharray="1" strokeDashoffset={1-progress(start,14)}/>
     <g stroke={color} strokeWidth="4" fill="none">
      <path data-objective-connector d={`M${midpoint} 303 V598`} pathLength="1" strokeDasharray="1"
       strokeDashoffset={1-progress(start+8,21)}/>
      <path d={`M${midpoint-15} 576 L${midpoint} 598 L${midpoint+15} 576`}
       opacity={progress(start+29,7)}/>
     </g>
     {i===0&&<text x={midpoint} y="704" textAnchor="middle" fontSize="64" fill={charter.ink}
      opacity={progress(cues.explanation0??first+24)}>identifier</text>}
     {i===1&&<text x={midpoint} y="704" textAnchor="middle" fontSize="73" direction="rtl"
      unicodeBidi="plaintext" fill={charter.ink} opacity={progress(cues.explanation1??second+24)}>{arabicLabel}</text>}
     {i===2&&<g data-objective-explanation-center={midpoint}>{examples.map(({number,dx,y,color},index)=>{
      const cx=midpoint+dx;
      const reveal=progress(cues['prime'+index]??third+20+index*14,12);
      return <g key={number} opacity={reveal} transform={`translate(0 ${10*(1-reveal)})`}>
       <circle cx={cx} cy={y} r="44" fill={color}/>
       <text x={cx} y={y+18} textAnchor="middle" fontWeight="700" fontSize="52" fill="white">{number}</text>
      </g>;
     })}</g>}
    </g>;
   })}
  </g>;
 };

