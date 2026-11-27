import React from 'react';
import {Img,staticFile} from 'remotion';

// Keep the existing scene slot. Size and center the bubble using its visible
// bounds because the supplied PNG has uneven transparent padding.
export const QuestionMark:React.FC<{x?:number;y?:number;width?:number}>=({x=817.5,y=520,width=285})=>{
 const slotScale=width/95;
 const height=102*slotScale;
 const imageScale=74*slotScale/800;
 const size=1254*imageScale;
 const left=44*slotScale-504*imageScale;
 const top=51.5*slotScale-581.5*imageScale;
 return <foreignObject data-question-mark="approved" x={x} y={y} width={width} height={height}>
  <div style={{position:'relative',width,height,overflow:'hidden'}}>
   <Img src={staticFile('brand/question-mark.png')} alt="Question" style={{position:'absolute',left,top,width:size,height:size}}/>
  </div>
 </foreignObject>;
};
