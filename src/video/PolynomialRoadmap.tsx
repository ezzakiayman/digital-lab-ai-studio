import React from 'react';
import {Easing, interpolate} from 'remotion';
import {charter} from '../lib/charter';
import {objectiveColor} from '../lib/objective';
import {objectiveEntrance} from '../lib/presentation';
import {ObjectiveBanner} from './ObjectiveDeclaration';

export const polynomialObjective = 'Déterminer le degré d’un polynôme';
const fontSize = 64;
// Measured Arial Bold advances for the title and the explained phrase.
const titleX = 486;
const phraseWidth = 604;
const phraseX = titleX + phraseWidth/2;
const conceptNames = ['Binôme','Trinôme','Polynôme'];
export const PolynomialRoadmap: React.FC<{frame:number; beats:number[]; conceptStarts:number[]}> =
 ({frame,beats,conceptStarts}) => {
  const [,meaning,roadmap,firstPart,secondPart,focus] = beats;
  const motion = objectiveEntrance(frame,meaning,'single-line');
  const progress = (start:number,length=16) => interpolate(frame,[start,start+length],[0,1],{
   extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic),
  });
  const line = (x:number, top:number, end:number, start:number, color:string, keyword=false) =>
   <g stroke={color} fill="none" strokeWidth={4} opacity={frame>=start?1:0}>
    <path data-objective-connector={keyword?true:undefined} d={`M${x} ${top} V${end}`} pathLength="1"
     strokeDasharray="1" strokeDashoffset={1-progress(start,21)}/>
    <path d={`M${x-16} ${end-22} L${x} ${end} L${x+16} ${end-22}`} opacity={progress(start+21,6)}/>
   </g>;
  const number = (x:number, n:number, active:boolean) => <g data-roadmap-part={n}>
   <rect x={x-40} y="544" width="80" height="80" rx="17" fill={active?'#00866F':charter.turquoise}/>
   <text x={x} y="602" textAnchor="middle" fontSize="54" fontWeight="700" fill="white">{n}</text>
  </g>;
  const firstScale=1+.07*progress(focus,28);
  return <g data-objective-entrance transform={`translate(0 ${motion.offsetY})`}>
   <ObjectiveBanner layout="single-line">
    <text data-objective-title x={titleX} y="282" fontSize={fontSize} fontWeight="700" fill="#263956">
     {polynomialObjective}
    </text>
   </ObjectiveBanner>
   <g data-link-index="0" opacity={progress(meaning,8)*(1-progress(roadmap,12))}>
    <path d={`M${titleX} 302 H${titleX+phraseWidth}`} stroke={objectiveColor(0)} strokeWidth="4"
     pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress(meaning)}/>
    {line(phraseX,302,570,meaning+9,objectiveColor(0),true)}
    <text x={phraseX} y="650" fontSize="54" textAnchor="middle" fill={charter.ink} opacity={progress(meaning+17)}>
     trouver la valeur du degré
    </text>
    <text x={phraseX} y="717" fontSize="54" textAnchor="middle" fill={charter.ink} opacity={progress(meaning+17)}>
     par un calcul
    </text>
   </g>
   <g opacity={progress(roadmap)}>
    {line(595,371,525,roadmap,objectiveColor(2))}
    {number(595,1,frame>=firstPart&&(frame<secondPart||frame>=focus))}
    <g transform={`translate(595 780) scale(${firstScale}) translate(-595 -780)`}>
     {conceptNames.map((name,i)=><text key={name} x="595" y={710+i*86} textAnchor="middle" fontSize="63"
      fontWeight="700" fill={charter.ink} opacity={progress(conceptStarts[i])}>{name}</text>)}
    </g>
    <g opacity={1-progress(focus)}>
     {line(1345,371,525,roadmap+6,objectiveColor(2))}
     {number(1345,2,frame>=secondPart)}
     <text x="1345" y="740" textAnchor="middle" fontSize="59" fontWeight="700" fill={charter.ink}
      opacity={progress(secondPart)}>Déterminer le degré</text>
    </g>
   </g>
  </g>;
 };

