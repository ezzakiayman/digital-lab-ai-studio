import React from 'react';
import {charter} from '../lib/charter';
import {easeReveal, MathFormula, MathVariable} from './StoryboardVisuals';

type Word = {word: string; startFrame: number};
type Props = {slide: number; frame: number; words?: readonly Word[]};

const red = '#ED101B';
const green = '#159B74';
const blue = '#0070C0';
const middle = 960;
const size = 128;
const monomial = '4x²y³';
const binomial = '2x + y';
const variableWidths = [0.59, 0.58, 0.37, 0.60, 0.37];
const binaryWidths = [0.59, 0.58, 0.26, 0.59, 0.26, 0.60];

function wordKey(word: string) {
  return word.toLocaleLowerCase('fr').normalize('NFD').replace(/\p{M}/gu, '').replace(/[^a-z0-9]/g, '');
}

function wordFrame(words: readonly Word[], wanted: string, fallback: number) {
  const key = wordKey(wanted);
  const word = words.find(entry => wordKey(entry.word) === key);
  return word?.startFrame ?? fallback;
}

// MathFormula uses these advances for the professional Cambria Math glyphs.
function tokenCentre(widths: number[], index: number) {
  const sum = (items: number[]) => items.reduce((total, width) => total + width, 0);
  return middle + size * (sum(widths.slice(0, index)) + widths[index] / 2 - sum(widths) / 2);
}

function revealInk(progress: number) {
  return `rgba(29,29,29,${progress})`;
}

function Ring({x, y, rx, ry, progress, color=red}: {
  x: number; y: number; rx: number; ry: number; progress: number; color?: string;
}) {
  return <ellipse cx={x} cy={y} rx={rx} ry={ry} fill="none" stroke={color} strokeWidth="4.5"
    pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress} opacity={progress} />;
}

function Arrow({x=middle, top, end, progress}: {x?: number; top: number; end: number; progress: number}) {
  if (end<=top) return null;
  const tip = top + (end-top)*progress;
  const head = Math.min(1, progress*4);
  return <g fill="none" stroke={blue} strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" opacity={head}>
    <path d={`M ${x} ${top} V ${tip}`} />
    <path d={`M ${x-13*head} ${tip-20*head} L ${x} ${tip} L ${x+13*head} ${tip-20*head}`} />
  </g>;
}

function Label({y, progress=1, children, color=charter.ink}: {
  y: number; progress?: number; children: React.ReactNode; color?: string;
}) {
  return <text x={middle} y={y+7*(1-progress)} textAnchor="middle" fontFamily={charter.font}
    fontSize="68" fontWeight="600" fill={color} opacity={progress}>{children}</text>;
}

function VerdictMark({valid, y, progress}: {valid: boolean; y: number; progress: number}) {
  const path = valid ? 'M 0 31 L 24 53 L 71 -9' : 'M 5 0 L 59 55 M 59 0 L 5 55';
  return <path d={path} transform={`translate(1220 ${y-58})`} fill="none" stroke={valid?green:'#D71920'}
    strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" pathLength="1"
    strokeDasharray="1" strokeDashoffset={1-progress} opacity={progress} />;
}

function SpokenFormula({binary=false, y, frame, words}: {
  binary?: boolean; y: number; frame: number; words: readonly Word[];
}) {
  const tokens = binary
    ? [['deux', 11], ['x', 16], ['', 0], ['plus', 21], ['', 0], ['y', 27]] as const
    : [['quatre', 11], ['x', 17], ['carré', 22], ['y', 27], ['cube', 33]] as const;
  const tokenColors = Object.fromEntries(tokens.map(([word, fallback], index) => [
    index, revealInk(.58 + .42*easeReveal(frame, wordFrame(words, word, fallback), 7)),
  ]));
  return <MathFormula formula={binary?binomial:monomial} y={y} size={size} tokenColors={tokenColors} />;
}

function TermRings({binary, y, first, second}: {binary: boolean; y: number; first: number; second: number}) {
  if (!binary) return <Ring x={middle} y={y-42} rx={183} ry={89} progress={first} />;
  return <>
    <Ring x={(tokenCentre(binaryWidths,0)+tokenCentre(binaryWidths,1))/2} y={y-34}
      rx={84} ry={72} progress={first} />
    <Ring x={tokenCentre(binaryWidths,5)} y={y-26} rx={53} ry={66} progress={second} />
  </>;
}

function Classification({slide, frame, words=[]}: Props) {
  const binary = slide >= 10;
  const stage = slide - (binary?10:6);
  const cue = (word: string, fallback: number) => wordFrame(words,word,fallback);
  const show = (start: number, length=10) => easeReveal(frame,start,length);
  if (stage===0) return <SpokenFormula binary={binary} frame={frame} y={565} words={words} />;
  // The diagram grows downwards. Move the existing expression up once and
  // keep this anchor through the term-count and verdict shots.
  const y = 295 + (stage===1 ? 270*(1-show(0,18)) : 0);
  const firstArrow = stage===1 ? show(3,15) : stage===2 ? 1 : show(cue('donc',22)-13,15);
  const label = stage===1 ? show(cue('expression',10)) : 1;
  const count = cue(binary?'deux':'seul',18);
  const verdict = cue('monôme',36);
  return <>
    <MathFormula formula={binary?binomial:monomial} y={y} size={size} />
    {stage===2 && <TermRings binary={binary} y={y} first={show(1,13)} second={show(9,13)} />}
    {stage===3 && binary && <g opacity={1-show(cue('donc',22),10)}>
      <TermRings binary y={y} first={1} second={1} />
    </g>}
    <Arrow top={y+69} end={stage===3?586:515} progress={firstArrow} />
    {stage<3 && <Label y={608} progress={label}>Expression algébrique</Label>}
    {stage===2 && <>
      <Arrow top={642} end={782} progress={show(13,13)} />
      <Label y={889} progress={show(Math.max(17,count))}>{binary?'Deux termes':'Un seul terme'}</Label>
    </>}
    {stage===3 && <>
      <Label y={690} progress={show(Math.max(6,verdict-12))}>{binary?'N’est pas un monôme':'Monôme'}</Label>
      <VerdictMark valid={!binary} y={y} progress={show(verdict,12)} />
    </>}
  </>;
}

function Elements({slide, frame, words=[]}: Props) {
  const y = 495;
  const cue = (word: string, fallback: number) => wordFrame(words,word,fallback);
  const show = (start: number, length=10) => easeReveal(frame,start,length);
  const coefficient = tokenCentre(variableWidths,0);
  const x = tokenCentre(variableWidths,1);
  const yVariable = tokenCentre(variableWidths,3);
  const first = show(cue('x',4),9);
  const second = show(cue('y',16),9);
  const coefficientStep = slide===15 || slide===16;
  if (slide===14) return <SpokenFormula frame={frame} y={y} words={words} />;
  const colors: Record<number,string> = {};
  if (coefficientStep) colors[0] = green;
  if (slide===18 || (slide===17 && first>0)) colors[1] = red;
  if (slide===18 || (slide===17 && second>0)) colors[3] = red;
  return <>
    <MathFormula formula={monomial} size={size} y={y} tokenColors={colors} />
    {slide===15 && <Ring x={coefficient} y={y-42} rx={46} ry={66} color={green}
      progress={show(Math.max(0,cue('quatre',8)-6),13)} />}
    {slide===16 && <>
      <Arrow x={coefficient} top={y+30} end={700} progress={show(0,17)} />
      <text x={coefficient-16} y="796" fontSize="65" fontWeight="600" fontFamily={charter.font}
        fill={green} opacity={show(cue('coefficient',15)-6)}>4 est le coefficient</text>
    </>}
    {slide===17 && <>
      <Ring x={x} y={y-27} rx={39} ry={50} progress={first} />
      <Ring x={yVariable} y={y-22} rx={39} ry={54} progress={second} />
    </>}
    {slide===18 && <>
      <Arrow x={x} top={y+36} end={690} progress={show(0,17)} />
      <Arrow x={yVariable} top={y+36} end={690} progress={show(3,17)} />
      <g opacity={show(cue('variables',17)-4)} fontFamily={charter.font} fontSize="58" fontWeight="600">
        <text x={x} y="770" textAnchor="middle" fill={red}><MathVariable name="x" /></text>
        <text x={(x+yVariable)/2} y="770" textAnchor="middle">et</text>
        <text x={yVariable} y="770" textAnchor="middle" fill={red}><MathVariable name="y" /></text>
        <text x={yVariable+41} y="770">sont les <tspan fill={red}>variables</tspan></text>
      </g>
    </>}
  </>;
}

function Degree({slide,frame,words=[]}: Props) {
  const cue = (word: string, fallback: number) => wordFrame(words,word,fallback);
  const show = (start: number, length=10) => easeReveal(frame,start,length);
  const y = 292;
  if (slide===21) return <SpokenFormula frame={frame} y={y} words={words} />;
  const colors: Record<number,string> = {};
  if (slide>=23) colors[2] = green;
  if (slide>=24) colors[4] = green;
  const xExponent = slide===23;
  const expIndex = xExponent ? 2 : 4;
  const expCue = xExponent ? cue('deux',18) : cue('trois',18);
  const draw = slide===22 ? show(2,14) : slide===26 ? show(1,15) : 1;
  return <>
    <MathFormula formula={monomial} y={y} size={size} tokenColors={colors} />
    {slide===22 && <>
      <Ring x={tokenCentre(variableWidths,1)} y={y-27} rx={39} ry={50} progress={show(cue('x',6)-3)} />
      <Ring x={tokenCentre(variableWidths,3)} y={y-22} rx={39} ry={54} progress={show(cue('y',18)-3)} />
    </>}
    {(slide===23 || slide===24) && <Ring x={tokenCentre(variableWidths,expIndex)}
      y={y-83} rx={31} ry={41} progress={show(2,13)} />}
    <Arrow top={y+64} end={502} progress={draw} />
    {slide===22 && <Label y={600} progress={show(cue('x',9)-2)}><MathVariable name="x" /> et <MathVariable name="y" /></Label>}
    {slide>=23 && slide<=25 && <>
      <g opacity={slide===23?show(expCue-2):1}>
        <MathFormula formula="2" x={slide===23?middle:slide===24?middle-104*show(0,13):middle-104}
          size={82} y={600} tokenColors={{0:green}} />
      </g>
      {slide>=24 && <g opacity={slide===24?show(expCue-5):1}>
        <Label y={600}>et</Label>
        <MathFormula formula="3" x={middle+104} size={82} y={600} tokenColors={{0:green}} />
      </g>}
    </>}
    {slide===25 && <>
      <Arrow top={638} end={774} progress={show(1,17)} />
      <g opacity={show(cue('deux',18)-3)}>
        <MathFormula formula="2 + 3 = 5" size={84} y={897} tokenColors={{
          0:green, 2:revealInk(show(cue('plus',22)-3)), 4:show(cue('trois',26)-3)>0?green:'transparent',
          6:show(cue('cinq',34)-5)>0?green:'transparent', 8:show(cue('cinq',34)-5)>0?green:'transparent',
        }} />
      </g>
    </>}
    {slide===26 && <g opacity={show(cue('cinq',18)-4)}><MathFormula formula="5" size={95} y={614} tokenColors={{0:green}} /></g>}
  </>;
}

export function MonomialDiagrams(props: Props) {
  const {slide} = props;
  if (slide>=6 && slide<=13) return <Classification {...props} />;
  if (slide>=14 && slide<=18) return <Elements {...props} />;
  if (slide>=21 && slide<=26) return <Degree {...props} />;
  return null;
}
