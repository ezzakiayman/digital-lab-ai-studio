import React from 'react';
import {AbsoluteFill,Audio,Sequence,staticFile,useCurrentFrame} from 'remotion';
import {Timeline} from '../lib/timeline';
import {NegativeComparison} from './NegativeComparison';
import {LessonSection} from './LessonSection';
import {Ppcm} from './Ppcm';
import {Primes} from './Primes';
import {Fractions} from './Fractions';
import {Polynomials} from './Polynomials';
import {Factorization} from './Factorization';
import {LikeTerms} from './LikeTerms';
import {PolynomialSubtraction} from './PolynomialSubtraction';
import {MonomialStudy} from './MonomialStudy';
import {VdpSequence} from './VdpSequence';
import {SignedAddition} from './SignedAddition';
import {charter} from '../lib/charter';
export {charter} from '../lib/charter';
const Property:React.FC<{scene:Extract<Timeline['scenes'][number],{type:'property'}>}>=({scene})=>{
 const frame=useCurrentFrame();
 const active=(target:string)=>scene.cues.some(c=>c.target===target&&frame>=c.from&&frame<c.to);
 return <AbsoluteFill style={{background:'white',fontFamily:charter.font,color:charter.ink}}>
  <svg width="1920" height="1080" viewBox="0 0 1920 1080">
   <rect x="194" y="111" width="1543" height="90" rx="30" fill={charter.turquoise}/>
   <text x="233" y="175" fill="white" fontSize="64" fontWeight="700" letterSpacing="0.9">{scene.title}</text>
   {frame>=15&&<g>
    <rect x="169" y="279" width="1599" height="277" rx="21" fill="white" stroke={charter.turquoise} strokeWidth="7"/>
    {active('condition')&&<path d="M251 309 L868 313 L868 416 L251 412 Z" fill={charter.highlight}/>}
    {active('conclusion')&&<path d="M583 405 L1486 411 L1486 514 L583 508 Z" fill={charter.highlight}/>}
    <text x="190" y="383" fontSize="64" fill={charter.ink} letterSpacing="0.45">Si <tspan fontWeight="700">deux nombres sont négatifs</tspan>, alors <tspan fontWeight="700">le plus petit</tspan></text>
    <text x="190" y="480" fontSize="64" fill={charter.ink} letterSpacing="0.45">est celui qui a <tspan fontWeight="700">la plus grande valeur absolue.</tspan></text>
   </g>}
  </svg>
  {scene.audio&&<Audio src={staticFile(scene.audio)}/>}
 </AbsoluteFill>;
};
export const Lesson:React.FC<{timeline:Timeline}>=({timeline})=>{let start=0;return <AbsoluteFill>{timeline.audio&&<Audio src={staticFile(timeline.audio)}/>} {timeline.scenes.map(scene=>{const from=start;start+=scene.durationInFrames;return <Sequence key={scene.id} from={from} durationInFrames={scene.durationInFrames}>{scene.type==='property'?<Property scene={scene}/>:scene.type==='negative-comparison'?<NegativeComparison scene={scene}/>:scene.type==='ppcm'?<Ppcm scene={scene}/>:scene.type==='primes'?<Primes scene={scene}/>:scene.type==='fractions'?<Fractions scene={scene}/>:scene.type==='polynomials'?<Polynomials scene={scene}/>:scene.type==='factorization'?<Factorization scene={scene}/>:scene.type==='like-terms'?<LikeTerms scene={scene}/>:scene.type==='polynomial-subtraction'?<PolynomialSubtraction scene={scene}/>:scene.type==='signed-addition'?<SignedAddition scene={scene}/>:scene.type==='monomial-study'?<MonomialStudy scene={scene}/>:scene.type==='vdp-sequence'?<VdpSequence scene={scene}/>:<LessonSection scene={scene}/>}</Sequence>;})}</AbsoluteFill>;};
