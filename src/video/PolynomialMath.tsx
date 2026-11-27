import React from 'react';
import {charter} from '../lib/charter';
import {expressionData, type ExpressionKey} from '../lib/polynomials';

type Token = {text: string; x: number; width: number; role: 'number' | 'variable' | 'power' | 'operator'; term: number; axis?: string};

function layout(id: ExpressionKey) {
 const tokens: Token[] = [];
 const spans: {left: number; right: number}[] = [];
 let x = 0;
 const add = (text: string, role: Token['role'], width: number, term: number, axis?: string) => {
  tokens.push({text, role, x, width, term, axis});
  x += width;
 };
 expressionData[id].terms.forEach(({coefficient, exponents}, term) => {
  if (term > 0) x += .22;
  const left = x;
  if (term > 0 || coefficient < 0) {
   add(coefficient < 0 ? '−' : '+', 'operator', .59, term);
   x += .22;
  }
  const magnitude = Math.abs(coefficient);
  if (magnitude !== 1 || exponents.every(exponent => exponent === 0)) {
   const digits = String(magnitude);
   add(digits, 'number', digits.length * .59, term);
  }
  exponents.forEach((exponent, index) => {
   if (exponent === 0) return;
   add('xyz'[index], 'variable', [.48, .5, .47][index], term);
   if (exponent > 1) {
    const digits = String(exponent);
    add(digits, 'power', digits.length * .59 * .62, term, 'xyz'[index]);
   }
  });
  spans.push({left, right: x});
 });
 return {tokens, spans, width: x};
}

/** Cambria Bold advances at the baseline and a separately sized, raised exponent. */
export const PolynomialMath: React.FC<{
 id: ExpressionKey; x?: number; y: number; size?: number; highlight?: boolean;
 active?: number; progress?: number; compare?: 'variable' | 'power';
}> = ({id, x=960, y, size=126, highlight=true, active=-1, progress=1, compare}) => {
 const {tokens, spans, width} = layout(id);
 const left = x - width*size/2;
 const at = (offset: number) => left + offset*size;
 const data = expressionData[id];
 const ring = (cx: number, cy: number, rx: number, ry: number, key: string) => (
  <ellipse key={key} cx={cx} cy={cy} rx={rx} ry={ry} fill="none" stroke="#E60012"
   strokeWidth={4.5} pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress} opacity={progress}/>
 );
 return <g data-expression={id} aria-label={data.labels.join(' ')}>
  {highlight && <rect x={left-35} y={y-size*.93} width={width*size+70} height={size*1.25}
   rx="22" fill={id==='trois-termes'||id==='deux-termes'?'#E4EFF8':'#FFDC69'}/>}
  {tokens.map(({text, role, x: offset, term}, index) => (
   <text key={index} data-math-role={role} data-math-term-index={term}
    x={at(offset)} y={role==='power'?y-size*.43:y} fontSize={role==='power'?size*.62:size}
    fontFamily="Cambria, Times New Roman, serif" fontWeight="700"
    fontStyle={role==='variable'?'italic':'normal'} fill={role==='operator'?charter.ink:data.colors[term]}>
    {text}
   </text>
  ))}
  {active>=0 && spans[active] && ring(at((spans[active].left+spans[active].right)/2),y-size*.3,
   (spans[active].right-spans[active].left)*size/2+6,size*.54,'term')}
  {compare && tokens.filter(t=>t.role===compare && t.term<2 && (id!=='quatre-termes'
   ||(compare==='power'?t.axis==='y':t.text===(t.term===0?'x':'y')))).map((t,i)=>ring(at(t.x+t.width/2),
    compare==='power'?y-size*.62:y-size*.23,t.width*size/2+5,size*(compare==='power'?.27:.35),'part'+i))}
 </g>;
};

