import React,{createRef} from 'react';
import {createRoot} from 'react-dom/client';
import {flushSync} from 'react-dom';
import {Player} from '@remotion/player';
import {useCurrentFrame} from 'remotion';
import {VdpSequence} from '../../src/video/VdpSequence';
import {MonomialStudy} from '../../src/video/MonomialStudy';
import {captureSvg} from './capture-svg';
const host=createRoot(document.getElementById('root'));
let scene,ref,records,lastSeen;
function View({scene}){
 const frame=useCurrentFrame();
 return <div data-capture-frame={frame}>{scene.type==='monomial-study'?<MonomialStudy scene={scene}/>:<VdpSequence scene={scene}/>}</div>;
}
window.captureSetup=async s=>{
 scene=s;ref=createRef();records=[];lastSeen=new Map();
 flushSync(()=>host.render(<Player key={s.id} ref={ref} component={View} inputProps={{scene:s}} compositionWidth={1920}
  compositionHeight={1080} durationInFrames={s.durationInFrames} fps={30} initiallyMuted
  controls={false} acknowledgeRemotionLicense style={{width:1920,height:1080}}/>));
 await document.fonts.ready;
 await new Promise(r=>requestAnimationFrame(r));
};
window.captureFrames=(from,to)=>{
 for(let f=from;f<to;f++){
  flushSync(()=>ref.current.seekTo(f));
  const view=document.querySelector('[data-capture-frame]');
  if(Number(view?.dataset.captureFrame)!==f)throw Error('Unsettled frame '+f+' of '+scene.id);
  const svg=view.querySelector('svg');
  if(!svg)throw Error('No SVG');
  const stage=scene.beats.findLastIndex(b=>b.from<=f);
  const slideGroup=scene.kind==='diagram'?String(scene.sourceSlides[stage]).padStart(3,'0'):'000';
  const layers=captureSvg(svg);
  for(const node of layers){
   const identity=slideGroup+'|'+node.id+'|'+node.kind+'|'+(node.props.text||node.props.asset||'');
   let current=lastSeen.get(identity);
   if(!current||current.outFrame!==f){
    current={id:scene.id+'-'+String(records.length+1).padStart(3,'0'),name:node.name,kind:node.kind,order:0,
      inFrame:f,outFrame:f,props:{},sortKey:slideGroup+'|'+node.order,_last:{}};
    lastSeen.set(identity,current);records.push(current);
   }
   current.outFrame=f+1;
   for(const [prop,val] of Object.entries(node.props)){
    const repr=JSON.stringify(val);
    if(current._last[prop]!==repr){
     (current.props[prop]||=[]).push([f,val]);current._last[prop]=repr;
    }
   }
  }
 }
};
window.captureFinish=()=>{
 records.sort((a,b)=>a.sortKey<b.sortKey?-1:a.sortKey>b.sortKey?1:a.inFrame-b.inFrame);
 return records.map(({sortKey,_last,...entry},order)=>({...entry,order}));
};

