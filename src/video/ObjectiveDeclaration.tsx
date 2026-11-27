import React from 'react';
import {Img,staticFile,Easing,interpolate} from 'remotion';
import {objectiveColor,ppcmObjectiveTerms} from '../lib/objective';
export const ObjectiveBanner:React.FC<React.PropsWithChildren<{layout?:'standard'|'single-line'}>>=({children,layout='standard'})=>{
 const single=layout==='single-line',targetWidth=single?132:202,targetHeight=targetWidth*187/202;
 return <g data-section="declaration-of-objective" data-objective-layout={layout}>
 <defs><filter id="objective-shadow" x="-10%" y="-20%" width="130%" height="160%"><feDropShadow dx="12" dy="16" stdDeviation="5" floodColor="#555" floodOpacity="0.55"/></filter></defs>
 <rect data-objective-banner x={single?32:82} y={single?150:110} width={single?1856:1755} height={single?220:310} rx="50" fill="white" stroke="#2D77CB" strokeWidth="8" filter="url(#objective-shadow)"/>
 <foreignObject data-objective-target x={single?62:100} y={single?260-targetHeight/2:165} width={targetWidth} height={targetHeight}><Img src={staticFile('brand/objective-target.png')} style={{width:targetWidth,height:targetHeight}}/></foreignObject>
 {children}
</g>;
};
export const ObjectiveDeclaration:React.FC<{frame:number;starts:number[];explanationsFrom:number[];invalidFrom:number}>=({frame,starts,explanationsFrom,invalidFrom})=>{
 const progress=(start:number,duration=18)=>interpolate(frame,[start,start+duration],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)});
 return <ObjectiveBanner>
  {ppcmObjectiveTerms.map((term,i)=>{
   const start=starts[i]??Infinity,p=progress(start),anchor=term.anchor,color=objectiveColor(i),underline=term.y+20;
   const active=frame>=start&&(i===ppcmObjectiveTerms.length-1||frame<(starts[i+1]??Infinity));
   const shaft=i===1?`M${anchor} ${underline} V500 Q${anchor} 525 ${anchor-25} 525 H${term.labelX+25} Q${term.labelX} 525 ${term.labelX} 550 V${term.bottom}`:`M${anchor} ${underline} V${term.bottom}`;
   return <g key={term.text} data-link-index={i}>
    {active&&<rect x={term.x-8} y={term.y-term.fontSize+5} width={term.width+16} height={term.fontSize+17} rx="10" fill={color} opacity={0.1*progress(start,10)}/>}
    <text data-objective-title x={term.x} y={term.y} fontSize={term.fontSize} fontWeight="700" fill={active?color:'#41476D'}>{term.text}</text>
    <path d={`M${term.x} ${underline} H${term.x+term.width}`} pathLength="1" stroke={color} strokeWidth="4" strokeDasharray="1" strokeDashoffset={1-p} fill="none" opacity={frame>=start?1:0}/>
    <g opacity={frame>=start?1:0} fill="none" stroke={color} strokeWidth="4">
     <path d={shaft} pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress(start+8,20)}/>
     <path d={`M${term.labelX-20} ${term.bottom-24} L${term.labelX} ${term.bottom} L${term.labelX+20} ${term.bottom-24}`} opacity={progress(start+24,8)}/>
    </g>
    <g opacity={progress(explanationsFrom[i]??start+24,14)} transform={`translate(0,${8*(1-progress(explanationsFrom[i]??start+24,14))})`}>
     {i===0&&<text x={term.labelX} y={term.labelY} textAnchor="middle" fontSize="68" fill="#1D1D1D">Trouver</text>}
     {i===1&&<text x={term.labelX} y={term.labelY} textAnchor="middle" fontSize="58" fill="#1D1D1D" direction="rtl" unicodeBidi="plaintext">المضاعف المشترك الأصغر</text>}
     {i===2&&<><text x={term.labelX} y={term.labelY} textAnchor="middle" fontSize="64" fontWeight="700" fill="#4472C4">58 <tspan fill="#70AD47">✓</tspan>   12 <tspan fill="#70AD47">✓</tspan></text>
      <text x={term.labelX} y={term.labelY+120} textAnchor="middle" fontSize="64" fontWeight="700" opacity={progress(invalidFrom)} fill="#4472C4">0 <tspan fill="#E60012">✕</tspan>   −3 <tspan fill="#E60012">✕</tspan></text></>}
    </g>
   </g>;
  })}
 </ObjectiveBanner>;
};
