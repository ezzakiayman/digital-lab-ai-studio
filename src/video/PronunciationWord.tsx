import React from 'react';
import {Easing, interpolate} from 'remotion';

const blue = '#087ABA';
const syllableColors = [blue, '#21A972', '#E60000', '#7061AA', '#9A5C00'];
const fontSize = 176;

// Arial Bold widths at 64 px, scaled with the visible font.
const advance = {bi:57, tri:64, po:78, ly:54, nôme:171, pre:100, mier:136,
 sem:129, blables:222, dé:75, com:132, si:54, tion:117, ir:43, ré:61, duc:114, tible:132};
export const pronunciationParts = {
 binome:['bi','nôme'],
 trinome:['tri','nôme'],
 polynome:['po','ly','nôme'],
 premier:['pre','mier'],
 semblables:['sem','blables'],
 decomposition:['dé','com','po','si','tion'],
 irreductible:['ir','ré','duc','tible'],
} as const;
type Word = keyof typeof pronunciationParts;
const ease = (frame:number,start:number,length:number) => interpolate(frame,[start,start+length],[0,1],{
 extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic),
});
function blend(color:string,progress:number) {
 const rgb = (hex:string) => [1,3,5].map(index=>parseInt(hex.slice(index,index+2),16));
 return 'rgb('+rgb(color).map((channel,index)=>Math.round(channel+(rgb(blue)[index]-channel)*progress)).join(',')+')';
}
export const PronunciationWord: React.FC<{word:Word; frame:number; syllableStarts:number[]; wholeStart:number}> =
 ({word,frame,syllableStarts,wholeStart}) => {
  const parts = pronunciationParts[word];
  return <PronunciationLine word={word} parts={parts} advances={parts.map(part=>advance[part])}
   frame={frame} syllableStarts={syllableStarts} wholeStart={wholeStart}/>;
 };

// Measured advances at 64 px let new editable words reuse the approved motion.
export const PronunciationLine: React.FC<{
 word:string;parts:readonly string[];advances:readonly number[];frame:number;syllableStarts:number[];wholeStart:number;
}> = ({word,parts,advances,frame,syllableStarts,wholeStart}) => {
  const widths = advances.map(width=>width*fontSize/64);
  const transition = Math.max(syllableStarts[parts.length-1]+18,wholeStart-14);
  const recolor = ease(frame,transition,12);
  const join = ease(frame,transition+7,20);
  const gap = 76*(1-join);
  const total = widths.reduce((sum,width)=>sum+width,0) + (parts.length-1)*gap;
  let left = 960-total/2;
  return <g data-pronunciation-word={parts.join('')} data-pronunciation-joined={join===1}>
   {parts.map((part,index)=>{
    const x = left;
    const width = widths[index];
    left += width+gap;
    const progress = ease(frame,syllableStarts[index],12);
    const color = parts.length===2&&index===1?syllableColors[2]:syllableColors[index%syllableColors.length];
    const clip = `pronunciation-${word}-${index}`;
    return <g key={part} data-syllable={part}>
     <defs><clipPath id={clip}><rect x={x-3} y="405" width={(width+gap+6)*progress} height="250"/></clipPath></defs>
     <g clipPath={`url(#${clip})`} fontFamily="Arial, sans-serif" fontSize={fontSize} fontWeight="700">
      <text x={x} y="594" fill={blend(color,recolor)}>{part}</text>
      {index<parts.length-1 && <text x={x+width+8} y="594" fill={blue} opacity={1-recolor}>-</text>}
     </g>
    </g>;
   })}
  </g>;
 };

