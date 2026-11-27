import React from 'react';
import {OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import './VdpFormula.css';
import {PronunciationLine} from './PronunciationWord';
import {Timeline} from '../lib/timeline';
import {charter} from '../lib/charter';
import {QuestionMark} from './QuestionMark';
import {easeReveal, LinkedObjective, MathFormula, TeachingVideo} from './StoryboardVisuals';

type Scene = Extract<Timeline['scenes'][number], {type: 'vdp-sequence'}>;
type Visual = Scene['art'][number];
type Beat = Scene['beats'][number];
const red = '#D60019';
const blue = '#007DBA';
const green = '#087746';
const purple = '#66539F';
const gold = '#F5BE32';
const axisZero = 875;
const axisStep = 151;

const focusClasses = new Set(['vdp-math-denominator', 'vdp-math-exponent', 'vdp-math-decimal']);

function Formula({value, x, y, size, color, focus, frame = 0}: Pick<Visual, 'value' | 'x' | 'y' | 'size' | 'color' | 'focus'> & {frame?:number}) {
 const markup = React.useMemo(() => katex.renderToString(value, {
  displayMode: true, output: 'htmlAndMathml',
  strict: code => code === 'htmlExtension' ? 'ignore' : 'error',
  trust: context => context.command === '\\htmlClass' && 'class' in context && focusClasses.has(context.class),
 }), [value]);
 const focusStyles=Object.fromEntries((focus??[]).map(({target,start,end})=>[
  '--vdp-'+target, easeReveal(frame,start-1,9)*(1-easeReveal(frame,end-1,9)),
 ]));
 const width = Math.min(1620, 2 * Math.min(x - 14, 1906 - x));
 const height = Math.max(400, size * 5);
 return <foreignObject data-vdp-formula={value} x={x-width/2} y={y-height/2} width={width} height={height}>
  <div className="vdp-formula" style={{display:'grid',placeItems:'center',width:'100%',height:'100%',fontSize:size,color:color??charter.ink,...focusStyles}}
   dangerouslySetInnerHTML={{__html:markup}}/>
 </foreignObject>;
}

function Arrow({item: {value, x, y, size, color, draw}, progress}: {item: Visual; progress: number}) {
 const angle = value === 'down' ? 90 : value === 'left' ? 180 : 0;
 const tail = -size/2;
 const tip = draw ? tail + size * progress : size/2;
 const head = Math.min(tip-tail, 20);
 const halfStroke = draw ? 3 : 5;
 const halfHead = draw ? 12 : 16;
 return <g fill={color??blue} transform={'translate('+x+' '+y+') rotate('+angle+')'}>
  <path d={`M${tail} ${-halfStroke} H${tip-head} V${-halfHead} L${tip} 0 L${tip-head} ${halfHead} V${halfStroke} H${tail} Z`}/>
 </g>;
}

function Axis({y}: {y:number}) {
 const letters:Record<number,string> = {'-2':'F','-1':'E',0:'O',1:'A',2:'B',3:'C',4:'D'};
 return <g data-vdp-axis textAnchor="middle" fontSize="36">
  <path d={'M245 '+y+' H1714 m-19 -12 19 12 -19 12'} fill="none" stroke={charter.ink} strokeWidth="4"/>
  {Array.from({length:10},(_,i)=>i-4).map(n=>{
   const x=axisZero+n*axisStep;
   return <g key={n}>
    <path d={'M'+x+' '+(y-13)+' v26'} stroke={charter.ink} strokeWidth={n===0?5:3}/>
    <text x={x} y={y+65}>{String(n).replace('-','−')}</text>
    {letters[n]&&<text x={x} y={y-31} fontWeight="700">{letters[n]}</text>}
   </g>;
  })}
 </g>;
}

function AxisRoot({y}: {y:number}) {
 const x = axisZero + Math.SQRT2*axisStep;
 return <g data-vdp-axis-root={Math.SQRT2}>
  <path d={'M'+(axisZero+axisStep)+' '+(y+11)+' H'+(axisZero+2*axisStep)} stroke={red} strokeWidth="4"/>
  <path d={'M'+x+' '+(y-89)+' V'+(y-7)} stroke={red} strokeWidth="4"/>
  <circle cx={x} cy={y} r="8" fill={red}/>
  <text x={x} y={y-104} textAnchor="middle" fontSize="40" fontWeight="700" fill={red}>M</text>
  <Formula value={"\\sqrt{2}"} x={x} y={y+104} size={35} color={red}/>
 </g>;
}

function Sets({y,sourceFull=false,pulses,frame=0}: {y:number;sourceFull?:boolean;pulses?:Visual['setPulses'];frame?:number}) {
 const opacity=(target:'real'|'rational'|'irrational')=>{
  const start=pulses?.find(p=>p.target===target)?.frame;
  return start===undefined?1:1-.3*Math.sin(Math.PI*easeReveal(frame,start-1,28));
 };
 return <g data-vdp-number-sets textAnchor="middle" fontSize="49" fontWeight="700">
  <rect x="460" y={y-124} width="1000" height="260" rx="24" fill="white" stroke={charter.turquoise} strokeWidth="5"/>
  <path d={'M463 '+(y-17)+' V'+(y-100)+' Q463 '+(y-121)+' 485 '+(y-121)+' H1435 Q1457 '+(y-121)+' 1457 '+(y-100)+' V'+(y-17)+' Z'} fill={gold}/>
  <text x="960" y={y-48} opacity={opacity('real')}>Les nombres réels</text>
  <path d={'M460 '+(y-17)+' H1460 M960 '+(y-17)+' V'+(y+136)} stroke={charter.turquoise} strokeWidth="5"/>
  {sourceFull?<>
   <text x="710" y={y+43} opacity={opacity('rational')}><tspan x="710">Les nombres</tspan><tspan x="710" dy="59">rationnels</tspan></text>
   <text x="1210" y={y+43} opacity={opacity('irrational')}><tspan x="1210">Les nombres</tspan><tspan x="1210" dy="59">irrationnels</tspan></text>
  </>:<>
   <text x="710" y={y+79} fill={blue}>Les rationnels</text>
   <text x="1210" y={y+79} fill={purple}>Les irrationnels</text>
  </>}
 </g>;
}

function VisualItem({item, frame, beats, anchor=0, relative=false}: {
 item:Visual; frame:number; beats:Beat[]; anchor?:number; relative?:boolean;
}) {
 const start=relative ? Math.max(34,beats[item.at].from) : (item.frame??beats[item.at].from);
 const pulseAt=item.pulseFrame??(item.pulse===undefined?undefined:beats[item.pulse].from);
 const repeat=item.repeatPulse&&pulseAt!==undefined&&frame>=pulseAt;
 const pulse=pulseAt===undefined ? 0 : repeat ? Math.sin(Math.PI*((frame-pulseAt)%48)/48) : Math.sin(Math.PI*easeReveal(frame,pulseAt-1,26));
 const end=item.toFrame??(item.to===undefined?undefined:beats[item.to].from);
 const opacity=(start===0?1:easeReveal(frame,start-1,13))*(end===undefined?1:1-easeReveal(frame,end-1,9))*(repeat?1-.22*pulse:1);
 const x=anchor+item.x+(item.moveFrom===undefined?0:(item.moveFrom-item.x)*(1-easeReveal(frame,start,33)));
 const {y,size,value,weight,color,kind}=item;
 const scale=1+.10*pulse;
 if (opacity===0) return null;
 let content:React.ReactNode;
 switch(kind){
  case 'math':
   content=<Formula value={value} x={x} y={y} size={size} color={color} focus={item.focus} frame={frame}/>;
   break;
  case 'algebra':
   content=<MathFormula formula={value} x={x} y={y+size*.33} size={size} background={item.background}
    tokenColors={Object.fromEntries((item.tokenColors??[]).filter(token=>frame>=beats[token.at].from).map(token=>[token.index,token.color]))}
    tokenMarks={item.tokenMarks?.map(token=>({
     index:token.index,endIndex:token.endIndex,color:token.color,
     progress:easeReveal(frame,beats[token.at].from-1,16)*
      (token.to===undefined?1:1-easeReveal(frame,beats[token.to].from-1,10)),
    }))}/>;
   break;
  case 'clip':
   content=<Sequence from={start} durationInFrames={item.clipFrames} layout="none">
    <foreignObject x={x-700} y={y-size/2} width="1400" height={size}>
     <OffthreadVideo muted src={staticFile(value)} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
    </foreignObject>
   </Sequence>;
   break;
  case 'card':
   content=<g data-vocabulary-card>
    <rect x={x-272} y={y-60} width="544" height="120" rx="25"
     fill={pulse>0.1?'#E6FAF6':'white'} stroke={charter.turquoise} strokeWidth={5+3*pulse}/>
    <text x={x} y={y} textAnchor="middle" dominantBaseline="central" fontSize={size} fontWeight="700">{value}</text>
   </g>;
   break;
  case 'arrow':
   content=<Arrow item={{...item,x}} progress={easeReveal(frame,start-1,20)}/>;
   break;
  case 'ring':
   content=<ellipse cx={x} cy={y} rx={size*.68} ry={size*.36} fill="none" stroke={color??red} strokeWidth="5"/>;
   break;
  case 'question':
   content=<QuestionMark x={x-size/2} y={y-size/2} width={size}/>;
   break;
  case 'number-node':
   content=<g>
    <rect x={x-96} y={y-64} width="192" height="128" rx="8" fill="white" stroke="#575757" strokeWidth="3"/>
    <Formula value={value} x={x} y={y} size={size} color={color}/>
   </g>;
   break;
  case 'status':
   content=<g>
    <rect x={x-100} y={y-42} width="200" height="84" rx="22" fill="#FFF1F3" stroke={color??red} strokeWidth="3"/>
    <text x={x} y={y} textAnchor="middle" dominantBaseline="central" fontSize={size} fontWeight="700" fill={color??red}>{value}</text>
   </g>;
   break;
  case 'alert':
   content=<g aria-label="Attention">
    <path d={'M'+x+' '+(y-size/2)+' L'+(x+size*.55)+' '+(y+size*.45)+' H'+(x-size*.55)+' Z'}
     fill="#FFF1C6" stroke="#D0840C" strokeWidth="6" strokeLinejoin="round"/>
    <text x={x} y={y+12} textAnchor="middle" dominantBaseline="central" fontSize={size*.65} fontWeight="700">!</text>
   </g>;
   break;
  case 'axis':
   content=<Axis y={y}/>;
   break;
  case 'axis-root':
   content=<AxisRoot y={y}/>;
   break;
  case 'sets':
   content=<Sets y={y} sourceFull={value==='source-full'} pulses={item.setPulses} frame={frame}/>;
   break;
  default:
   content=<text x={x} y={y} textAnchor="middle" dominantBaseline="central" fontSize={size} xmlSpace="preserve"
    fontWeight={weight??400} fill={color} direction={item.rtl?'rtl':undefined} unicodeBidi={item.rtl?'plaintext':undefined}>{value}</text>;
 }
 return <g data-vdp-visual={kind} opacity={opacity}
  transform={scale===1?undefined:'translate('+x+' '+y+') scale('+scale+') translate('+(-x)+' '+(-y)+')'}>{content}</g>;
}

function Pronunciation({scene, frame}: {scene:Scene; frame:number}) {
 const pronunciation=scene.pronunciation!;
 const {word,syllables}=pronunciation;
 const joinedAt=scene.beats[syllables.length+1].from;
 const joined=easeReveal(frame,joinedAt,17);
 const syllableColors=[blue,red,green,purple];
 const totalWidth=syllables.reduce((sum,part)=>sum+part.length*64,0)+(syllables.length-1)*86;
 let cursor=960-totalWidth/2;
 return <g textAnchor="middle" fontWeight="700">
  <text x="960" y="454" fontSize="108" fill={blue}>{word}</text>
  <g opacity={1-joined}>
   {syllables.map((part,i)=>{
    const width=part.length*64;
    const start=scene.beats[i+1].from;
    const reveal=easeReveal(frame,start-1,13);
    const x=cursor+width/2;
    cursor+=width+86;
    return <g key={i} opacity={reveal} transform={'translate(0 '+(11*(1-reveal))+')'} fill={syllableColors[i%syllableColors.length]}>
     <text x={x} y="730" fontSize="105">{part}</text>
     {i>0&&<text x={x-width/2-43} y="728" fontSize="66" fill="#737F8C">–</text>}
    </g>;
   })}
  </g>
  <text data-pronunciation-word={word} x="960" y="730" fill={blue} fontSize="125"
   opacity={joined} transform={'translate(0 '+(15*(1-joined))+')'}>{word}</text>
 </g>;
}

export function VdpSequence({scene}: {scene:Scene}) {
 const frame=useCurrentFrame();
 if(scene.pronunciation?.style==='simplifier'){
  const {word,syllables,advances}=scene.pronunciation;
  return <TeachingVideo frame={frame} audio={scene.audio}>
   {scene.art.map((item,i)=><VisualItem key={i} item={item} frame={frame} beats={scene.beats}/>)}
   <PronunciationLine word={word} parts={syllables} advances={advances!} frame={frame}
    syllableStarts={scene.beats.slice(1,-1).map(beat=>beat.from)} wholeStart={scene.beats.at(-1)!.from}/>
  </TeachingVideo>;
 }
 const objective=scene.objective;
 if (objective) {
  return <TeachingVideo frame={frame} audio={scene.audio}>
   <LinkedObjective title={objective.title} measure={objective.measure} size={objective.size}
    mathSuffix={objective.mathSuffix} mathOffset={objective.mathOffset}
    formula={objective.formula ? (left,scale)=><Formula
     value={objective.formula!.value} x={left+(objective.formula!.offset+objective.formula!.width/2)*scale}
     y={260} size={objective.formula!.size*scale} color="#263956"/> : undefined}
    frame={frame} fadeBeforeNext links={objective.links.map(link=>{
     const start=scene.beats[link.at].from;
     const relativeBeats=scene.beats.map(beat=>({...beat,from:beat.from-start}));
     return {from:link.offset,width:link.width,start,end:link.endFrame,content:link.art.length?(x:number)=>link.art.map((item,i)=>
      <VisualItem key={i} item={{...item,x:item.x-960,at:item.at===0?link.at:item.at}}
       frame={frame-start} beats={relativeBeats} anchor={x} relative/>):undefined};
    })}/>
  </TeachingVideo>;
 }
 return <TeachingVideo frame={frame} audio={scene.audio} title={scene.kind==='open'?undefined:scene.title}>
  {scene.pronunciation && <Pronunciation scene={scene} frame={frame}/>}
  {scene.art.map((item,i)=><VisualItem key={i} item={item} frame={frame} beats={scene.beats}/>)}
  {scene.transition && frame<13 && <rect width="1920" height="1080" fill="black" opacity={1-easeReveal(frame,0,13)}/>}
 </TeachingVideo>;
}


