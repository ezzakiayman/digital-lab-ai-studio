import React from 'react';
import {useCurrentFrame} from 'remotion';
import {charter} from '../lib/charter';
import {Timeline} from '../lib/timeline';
import {easeReveal, LinkedObjective, TeachingVideo} from './StoryboardVisuals';

type Scene = Extract<Timeline['scenes'][number], {type: 'signed-addition'}>;
type Sign = '+' | '−';
type Shape = 'square' | 'triangle' | 'large' | 'small';
type Token = {
 label?: string;
 shape?: Shape;
 color?: string;
 width: number;
 role?: string;
 from?: number;
 pendingUntil?: number;
};
const blue = '#263ADB';
const red = '#E60012';
const green = '#138247';
const orange = '#E77D23';
const signColor = (sign: Sign) => sign === '+' ? green : red;

const symbol = (label: string, width = 68, color = charter.ink, role?: string): Token =>
 ({label, width, color, role});
const magnitude = (shape: Shape, role?: string): Token => ({shape, width: 91, role});
const signed = (sign: Sign, shape: Shape, side: 'left' | 'right'): Token[] => [
 symbol('(', 38), symbol(sign, 63, signColor(sign), side + '-sign'),
 magnitude(shape, side + '-magnitude'), symbol(')', 38),
];
const operands = (left: Sign, right: Sign, a: Shape, b: Shape): Token[] => [
 ...signed(left, a, 'left'), symbol('+', 92), ...signed(right, b, 'right'),
];
const pendingSign = (sign: Sign): Token[] => [
 symbol('=', 93), symbol(sign, 68, signColor(sign)), symbol('…', 82, '#596578'),
];
const result = (sign: Sign, a: Shape, operator: Sign, b: Shape): Token[] => [
 symbol('=', 93), symbol(sign, 68, signColor(sign)), symbol('(', 38),
 magnitude(a, 'result-first'), symbol(operator, 75, charter.ink, 'result-operation'),
 magnitude(b, 'result-second'), symbol(')', 38),
];

function Equation({frame, y, tokens, focus, pulseAt, start}: {
 frame: number;
 y: number;
 tokens: Token[];
 focus?: readonly string[];
 pulseAt?: number;
 start: number;
}) {
 let x = 960 - tokens.reduce((total, item) => total + item.width, 0) / 2;
 const pulse = pulseAt === undefined ? 0 : Math.sin(Math.PI * easeReveal(frame, pulseAt, 18));
 return <g data-signed-equation opacity={easeReveal(frame, start - 1, 10)} fontFamily="Cambria Math, Times New Roman, serif">
  {tokens.map((item, i) => {
   const center = x + item.width / 2;
   x += item.width;
   const active = item.role !== undefined && focus?.includes(item.role);
   const scale = 1 + (active ? .2 * pulse : 0);
   const side = item.shape === 'small' ? 43 : item.shape === 'large' ? 70 : 61;
   const size = item.label === '(' || item.label === ')' ? 90 : 77;
   return <g key={i} data-equation-token={item.role}
    opacity={item.from === undefined ? 1 : easeReveal(frame, item.from - 1, 8)}
    transform={`translate(${center} ${y}) scale(${scale})`}>
    {item.pendingUntil !== undefined && frame < item.pendingUntil
     ? <text x="0" y="2" textAnchor="middle" dominantBaseline="central" fontSize="73" fill="#596578">…</text>
     : item.shape === 'triangle'
     ? <path d="M0 -34 L34 29 H-34 Z" fill={blue}/>
     : item.shape
       ? <rect x={-side / 2} y={-side / 2} width={side} height={side} rx="2" fill={blue}/>
       : <text x="0" y="2" textAnchor="middle" dominantBaseline="central" fontSize={size} fill={item.color}>{item.label}</text>}
    {active && pulseAt === undefined && <ellipse rx={item.shape ? 46 : 31} ry={item.shape ? 47 : 34} fill="none" stroke={orange} strokeWidth="5"/>}
   </g>;
  })}
 </g>;
}

export const SignedAddition: React.FC<{scene: Scene}> = ({scene}) => {
 const frame = useCurrentFrame();
 const at = (i: number) => scene.beats[i].from;
 const stage = scene.beats.findLastIndex(beat => frame >= beat.from);
 const cue = (name: string) => scene.cues[name];
 const show = (start: number, children: React.ReactNode) =>
  <g opacity={easeReveal(frame, Math.max(13, start), 14)}>{children}</g>;
 const line = (y: number, children: React.ReactNode, size = 52) =>
  <text x="960" y={y} textAnchor="middle" fontSize={size}>{children}</text>;
 const step = (n: number, text: string) => <><tspan fill="#067B6D" fontWeight="700">{n}. </tspan>{text}</>;
 const illustration = <g data-box-heading>
  <path d="M251 598 V627 M237 615 L251 629 L265 615" fill="none" stroke={orange} strokeWidth="5"/>
  <rect x="222" y="646" width="334" height="58" rx="16" fill={charter.turquoise}/>
  <text x="245" y="686" fontSize="41" fontWeight="700" fill="white">Illustration :</text>
 </g>;

 if (scene.kind === 'intro') {
  return <TeachingVideo frame={frame} audio={scene.audio}>
   <LinkedObjective frame={frame} title="Additionner avec la valeur absolue" measure={1062} size={64}
    fadeBeforeNext links={[
     {from:0, width:359, start:at(1), content:x=>show(cue('plus'),
      <text x={x} y="740" textAnchor="middle" fontFamily="Cambria Math" fontSize="124" fill={red}>+</text>)},
     {from:539, width:523, start:at(2), content:x=>show(cue('negative'),
      <text x={x} y="730" textAnchor="middle" fontSize="62">La valeur absolue de <tspan fontWeight="700" fill={red}>−5</tspan>
       <tspan opacity={easeReveal(frame,cue('absolute')-1,8)}> est <tspan fill={blue} fontWeight="700">5</tspan></tspan>
      </text>)},
    ]}/>
  </TeachingVideo>;
 }

 let body: React.ReactNode;
 if (scene.kind === 'same') {
  const complete = stage >= 8;
  const example = stage === 2 || stage === 3 || stage === 5 || stage === 6;
  const sign: Sign = stage === 3 || stage === 6 ? '−' : '+';
  const showSign = stage === 5 || stage === 6;
  const signAt = cue(stage === 2 ? 'positive' : stage === 3 ? 'negative' : stage === 5 ? 'commonPlus' : 'commonMinus');
  const full = (s: Sign) => [
   ...operands(s,s,'square','triangle'),
   ...result(s,'square','+','triangle').map(item=>({
    ...item, from:cue('square'), pendingUntil:item.role==='result-second'?cue('triangle'):undefined,
   })),
  ];
  body = <>
   {show(at(1),line(382,'Pour additionner deux nombres entiers de même signe :'))}
   {show(at(4),line(477,step(1,'Je garde le signe commun des deux nombres.')))}
   {show(at(7),line(562,step(2,'J’additionne leurs valeurs absolues.')))}
   {(example || complete) && show(at(stage),illustration)}
   {example && <Equation frame={frame} y={810} start={at(stage)}
    tokens={[...operands(sign,sign,'square','triangle'),...(showSign?pendingSign(sign).map(t=>({...t,from:signAt})):[])]}
    focus={['left-sign','right-sign']} pulseAt={signAt}/>}
   {complete && <>
    <Equation frame={frame} y={786} start={at(8)} tokens={full('+')}/>
    <Equation frame={frame} y={918} start={at(8)} tokens={full('−')}/>
   </>}
  </>;
 } else if (scene.kind === 'different') {
  const examples = stage >= 4 && stage <= 7;
  const complete = stage >= 9;
  const sign: Sign = stage >= 6 ? '−' : '+';
  const other: Sign = sign === '+' ? '−' : '+';
  const showSign = stage === 5 || stage === 7;
  const start = cue(stage === 4 ? 'largePlus' : stage === 5 ? 'keepPlus' : stage === 6 ? 'largeMinus' : 'keepMinus');
  const full = (s: Sign, opposite: Sign) => [
   ...operands(s,opposite,'large','small'),
   ...result(s,'large','−','small').map(item=>({...item,from:cue('difference')})),
  ];
  body = <>
   {show(at(1),line(368,'Pour additionner deux nombres entiers de signes contraires :',50))}
   {show(at(3),line(438,'Si leurs valeurs absolues sont différentes',44))}
   {show(cue('keepLarger'),line(512,step(1,'Je garde le signe du nombre ayant la plus grande valeur absolue.'),47))}
   {show(at(8),line(580,step(2,'Je soustrais la plus petite valeur absolue de la plus grande.'),47))}
   {(stage === 2 || examples || complete) && show(at(stage),illustration)}
   {stage===2 && <>
    <Equation frame={frame} y={786} start={cue('casePositive')} tokens={operands('+','−','large','small')}/>
    <Equation frame={frame} y={918} start={cue('caseNegative')} tokens={operands('−','+','large','small')}/>
   </>}
   {examples && <Equation frame={frame} y={822} start={at(stage)} tokens={[
    ...operands(sign,other,'large','small'),...(showSign?pendingSign(sign).map(t=>({...t,from:start})):[]),
   ]} focus={frame>=start?[showSign?'left-sign':'left-magnitude']:[]}/>}
   {complete && <>
    <Equation frame={frame} y={786} start={at(9)} tokens={full('+','−')}/>
    <Equation frame={frame} y={918} start={at(9)} tokens={full('−','+')}/>
   </>}
  </>;
 } else {
  body = <>
   {show(at(1),line(455,<>La somme de deux nombres opposés est toujours égale à <tspan fill={blue} fontWeight="700">zéro.</tspan></>))}
   {stage>=2 && show(at(2),illustration)}
   {stage>=2 && <Equation frame={frame} y={809} start={cue('positive')} tokens={[
    ...signed('+','square','left'),
    ...[symbol('+',92),...signed('−','square','right')].map(t=>({...t,from:cue('negative')})),
    ...[symbol('=',93),symbol('0',82,blue,'zero')].map(t=>({...t,from:cue('zero')})),
   ]}/>}
  </>;
 }
 return <TeachingVideo frame={frame} audio={scene.audio} title={scene.title}>{body}</TeachingVideo>;
};
