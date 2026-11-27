import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition} from '@remotion/renderer';
import {mkdir,readFile,writeFile} from 'node:fs/promises';
import path from 'node:path';
import {duration,timelineSchema} from '../src/lib/timeline';
import {objectiveEntrance} from '../src/lib/presentation';
async function main(){
 const out='outputs/n3-sem2-vdp2';await mkdir(out,{recursive:true});
 const timeline=timelineSchema.parse(JSON.parse(await readFile('src/video/factorization-lesson.json','utf8')));
 const serveUrl=await bundle({entryPoint:path.resolve('src/video/index.ts')});
 const inputProps={timeline},composition=await selectComposition({serveUrl,id:'DigitalLab',inputProps});const options={serveUrl,composition,inputProps};
 let offset=0;const frames=[];
 for(const s of timeline.scenes){
  const final=offset+s.durationInFrames-15;frames.push({scene:s.id,frame:final});
  if(!process.argv.includes('--video-only')){
   await renderStill({...options,frame:final,output:`${out}/${s.id}.png`});
   if(s.type==='factorization'){
    if(s.kind==='intro')for(const [name,f] of [['center',0],['moving',objectiveEntrance(0,s.beats[1].from).start+16],['top',s.beats[1].from-2]] as const)await renderStill({...options,frame:offset+f,output:`${out}/objective-${name}.png`});
    for(const [i,b] of s.beats.entries())await renderStill({...options,frame:offset+Math.min(s.durationInFrames-1,b.from+35),output:`${out}/${s.id}-step-${i}.png`});
    if(s.kind==='theorem'||s.kind==='example')for(const [name,from] of Object.entries(s.cues).filter(([k])=>k.startsWith('factor')))await renderStill({...options,frame:offset+from+24,output:`${out}/${s.id}-${name}.png`});
   }
  }
  offset+=s.durationInFrames;
 }
 await writeFile(`${out}/timeline.json`,JSON.stringify(timeline,null,2));await writeFile(`${out}/review-frames.json`,JSON.stringify(frames,null,2));
 console.log(`Factorisation previews ready: ${duration(timeline)/30}s.`);if(process.argv.includes('--stills'))return;
 let last=-1;await renderMedia({...options,codec:'h264',pixelFormat:'yuv420p',crf:18,concurrency:4,outputLocation:`${out}/P1_MATHS_N3_SEM2_VDP2.mp4`,onProgress:({progress})=>{const pct=Math.floor(progress*100);if(pct%10===0&&pct!==last){console.log(`Render ${pct}%`);last=pct;}}});console.log('Full prime-factorisation video rendered.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
