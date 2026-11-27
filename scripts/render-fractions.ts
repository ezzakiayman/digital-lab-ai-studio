import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition} from '@remotion/renderer';
import {mkdir,readFile,writeFile} from 'node:fs/promises';
import path from 'node:path';
import {duration,timelineSchema} from '../src/lib/timeline';
async function main(){
 const out='outputs/n3-sem2-vdp3';await mkdir(out,{recursive:true});
 const timeline=timelineSchema.parse(JSON.parse(await readFile('src/video/fractions-lesson.json','utf8')));
 const serveUrl=await bundle({entryPoint:path.resolve('src/video/index.ts')});
 const inputProps={timeline},composition=await selectComposition({serveUrl,id:'DigitalLab',inputProps});const options={serveUrl,composition,inputProps};
 let from=0;const frames=[];
 for(const scene of timeline.scenes){
  const final=from+scene.durationInFrames-15;frames.push({scene:scene.id,frame:final});
  if(!process.argv.includes('--video-only')){
   await renderStill({...options,frame:final,output:`${out}/${scene.id}.png`});
   if(scene.type==='fractions')for(const [i,b] of scene.beats.entries())await renderStill({...options,frame:from+Math.min(scene.durationInFrames-1,b.from+32),output:`${out}/${scene.id}-step-${i}.png`});
  }
  from+=scene.durationInFrames;
 }
 await writeFile(`${out}/timeline.json`,JSON.stringify(timeline,null,2));await writeFile(`${out}/review-frames.json`,JSON.stringify(frames,null,2));
 console.log(`Reviewed lesson previews ready; ${duration(timeline)/30}s, ${timeline.scenes.length} scenes.`);
 if(process.argv.includes('--stills'))return;
 let last=-1;await renderMedia({...options,codec:'h264',pixelFormat:'yuv420p',crf:18,concurrency:4,outputLocation:`${out}/Digital-Lab-3AC-Fractions.mp4`,onProgress:({progress})=>{const pct=Math.floor(progress*100);if(pct%10===0&&pct!==last){console.log(`Render ${pct}%`);last=pct;}}});
 console.log('Full fractions video rendered.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
