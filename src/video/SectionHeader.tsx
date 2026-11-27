import React from 'react';
import {headingLabel} from '../lib/presentation';
import {charter} from '../lib/charter';
export const SectionHeader:React.FC<{title:string}>=({title})=>{
 const label=headingLabel(title),width=Math.max(510,label.length*35+80);
 return <g data-section-header><rect x="194" y="111" width={width} height="90" rx="30" fill={charter.turquoise}/><text x="233" y="175" fontSize="64" fontWeight="700" fill="white">{label}</text></g>;
};
