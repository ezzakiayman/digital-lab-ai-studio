import React from 'react';
import {staticFile, useCurrentFrame} from 'remotion';
import {Timeline} from '../lib/timeline';
import {charter} from '../lib/charter';
import {MonomialDiagrams} from './MonomialDiagrams';
import {PronunciationLine} from './PronunciationWord';
import {easeReveal, MathFormula, MathVariable, TeachingEntrance, TeachingVideo} from './StoryboardVisuals';

type Scene = Extract<Timeline['scenes'][number], {type:'monomial-study'}>;
const green='#009F73', red='#E60012', blue='#007CBA';

function Definition({scene,frame}:{scene:Scene;frame:number}){
 const words=scene.wordCues.filter(w=>w.startFrame>=scene.beats[1].from-1);
 const first=scene.sourceSlides[0]===4;
 let index=0;
 return <>
  <TeachingEntrance frame={frame}>
   <rect x="150" y="216" width="1620" height="548" rx="32" fill="white" stroke={charter.turquoise} strokeWidth="6"/>
   <rect x="190" y="163" width={first?745:1130} height="99" rx="30" fill={charter.turquoise}/>
   <text x="231" y="231" fontWeight="700" fontSize="61" fill="white">{scene.title}</text>
  </TeachingEntrance>
  {scene.lines?.map((line,row)=><text key={row} x="960" y={477+row*99} textAnchor="middle" fontSize="65" xmlSpace="preserve">
   {line.split(' ').map((word,column)=>{
    const at=index++;
    const start=words[at]?.startFrame??scene.beats[1].from;
    return <tspan key={at} opacity={easeReveal(frame,start-2,7)}
     fontWeight={first&&(at===1||at>=7)?700:400}>{(column?' ':'')+word}</tspan>;
   })}
  </text>)}
 </>;
}

const summaryLabels=['Monôme','Coefficient','Variables','Degré'];
function SummaryValue({row}:{row:number}){
 if(row===0)return <MathFormula formula="4x²y³" x={1340} y={0} size={93}/>;
 if(row===1)return <text x="1340" textAnchor="middle" fontFamily="Cambria, serif" fontWeight="700" fontSize="88" fill={green}>4</text>;
 if(row===2)return <text x="1340" textAnchor="middle" fontSize="78" xmlSpace="preserve"><tspan fill={red}><MathVariable name="x"/></tspan>{' et '}<tspan fill={red}><MathVariable name="y"/></tspan></text>;
 return <text x="1340" textAnchor="middle" fontFamily="Cambria, serif" fontWeight="700" fontSize="78" xmlSpace="preserve"><tspan fill={red}>2</tspan>{' + '}<tspan fill={red}>3 = 5</tspan></text>;
}

function Summary({scene,stage,frame}:{scene:Scene;stage:number;frame:number}){
 const local=frame-scene.beats[stage].from;
 const index=Math.max(0,stage-1);
 const firstMoves=stage===1?easeReveal(local,0,18):stage>1?1:0;
 return <>
  {summaryLabels.slice(0,Math.max(1,stage)).map((label,row)=>{
   const active=stage>0&&index===row;
   const rowProgress=active?easeReveal(local,0,13):1;
   const fade=stage===0?easeReveal(frame,-5,13):rowProgress;
   const dy= row===0 ? (1-firstMoves)*279 : 0;
   const dx= row===0 ? (1-firstMoves)*334 : 0;
   const y=189+row*228;
   const token=scene.wordCues.find(w=>w.startFrame>=scene.beats[stage].from&&w.word.toLocaleLowerCase('fr').replace(/[.,:]/g,'')===['quatre','quatre','x','cinq'][row]);
   const valueStart=token?token.startFrame-scene.beats[stage].from:21;
   const answer=active?easeReveal(local,Math.max(12,valueStart-2),10):1;
   return <g key={label} opacity={stage===1&&row===0?1:fade} transform={'translate('+dx+' '+(y+dy)+')'}>
    <rect x="300" y="-75" width="540" height="141" rx="30" fill="white" stroke={charter.turquoise} strokeWidth="5"/>
    {stage>0&&<>
     <text x="570" y="17" textAnchor="middle" fontSize="67" fontWeight="700" opacity={rowProgress}>{label}</text>
     <g transform={'translate(926 0) scale('+(active?easeReveal(local,5,13):1)+' 1)'} fill="#00AA50">
      <path d="M0 -10 H100 V-29 L138 0 100 29 V10 H0Z"/>
     </g>
     <g transform="translate(0 26)" opacity={answer}><SummaryValue row={row}/></g>
    </>}
   </g>;
  })}
  {stage===4&&scene.showSourceDuplicate&&<text x="742" y="548" textAnchor="middle" fontSize="32" opacity={easeReveal(local,0,12)}>Degré</text>}
 </>;
}

export function MonomialStudy({scene}:{scene:Scene}){
 const frame=useCurrentFrame();
 const stage=scene.beats.reduce((last,b,i)=>frame>=b.from?i:last,0);
 const local=frame-scene.beats[stage].from;
 const reading=scene.reading;
 return <TeachingVideo frame={frame} audio={scene.audio}>
  {scene.kind==='definition'&&<Definition scene={scene} frame={frame}/>}
  {scene.kind==='diagram'&&<MonomialDiagrams slide={scene.sourceSlides[stage]} frame={local}
   words={scene.wordCues.filter(w=>w.startFrame>=scene.beats[stage].from&&w.startFrame<(scene.beats[stage+1]?.from??scene.durationInFrames))
    .map(w=>({...w,startFrame:w.startFrame-scene.beats[stage].from}))}/>}
  {scene.kind==='recap'&&<Summary scene={scene} stage={stage} frame={frame}/>}
  {reading&&<>
   <image href={staticFile('n2-sem1-vdp4-v2/microphone.png')} x="1673.6" y="831.4" width="140" height="210"/>
   <text x="960" y="278" textAnchor="middle" fontWeight="700" fontSize="112" fill={blue}>{reading.word}</text>
   <rect x="335" y="345" width="1250" height="512" rx="48" fill="white" stroke={charter.turquoise} strokeWidth="5"/>
   <g transform="translate(192 172) scale(.8)">
    <PronunciationLine word={reading.word} parts={reading.parts} advances={reading.advances} colors={[blue,'#21A972']}
     frame={frame} syllableStarts={scene.beats.slice(1,3).map(b=>b.from)} wholeStart={scene.beats[3].from}/>
   </g>
  </>}
 </TeachingVideo>;
}

