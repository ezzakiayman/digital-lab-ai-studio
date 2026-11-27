import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition} from '@remotion/renderer';
import {mkdir,readFile,writeFile} from 'node:fs/promises';
import path from 'node:path';
import {duration,timelineSchema} from '../src/lib/timeline';
import {objectiveEntrance} from '../src/lib/presentation';
async function main(){
 const review=process.argv.includes('--review');
 const videoOnly=process.argv.includes('--video-only'),revised=review||process.argv.includes('--revised'),keyframes=process.argv.includes('--keyframes');
 const out=review?'outputs/n3-sem2-vdp1-2026-11-12':revised?'outputs/n3-sem2-vdp1-2026-11-10':process.argv.includes('--v4')?'outputs/n3-sem2-vdp1-v4':process.argv.includes('--v3')?'outputs/n3-sem2-vdp1-v3':process.argv.includes('--revision')?'outputs/n3-sem2-vdp1-v2':'outputs/n3-sem2-vdp1';await mkdir(out,{recursive:true});
 const stem=review?'primes-review':revised?'primes-v2':'primes';
 const timeline=timelineSchema.parse(JSON.parse(await readFile(`src/video/${stem}-lesson.json`,'utf8')));
 const filename=revised?'P1_MATHS_N3_SEM2_VDP1.mp4':'Digital-Lab-3AC-Nombres-premiers.mp4';
 const serveUrl=await bundle({entryPoint:path.resolve('src/video/index.ts')});
 const inputProps={timeline};const composition=await selectComposition({serveUrl,id:'DigitalLab',inputProps});const options={serveUrl,composition,inputProps};
 let from=0;const frames=[];
 for(const scene of timeline.scenes){
  const final=from+scene.durationInFrames-15;
  if(!videoOnly)await renderStill({...options,frame:final,output:`${out}/${scene.id}.png`});frames.push({scene:scene.id,frame:final});
  if(scene.type==='primes'&&!videoOnly){
   if(scene.kind==='intro')for(const [i,offset] of [0,...scene.beats.slice(1).map(b=>b.from+34)].entries())await renderStill({...options,frame:from+offset,output:`${out}/objective-${i}.png`});
   if(revised&&scene.kind==='intro')await renderStill({...options,frame:from+objectiveEntrance(0,scene.beats[1].from,'single-line').start+16,output:`${out}/objective-moving.png`});
   if(revised&&scene.kind==='pronunciation')await renderStill({...options,frame:from+scene.beats[2].from+14,output:`${out}/pronunciation-syllables.png`});
   if(!keyframes&&scene.kind==='divisors')for(const [i,b] of scene.beats.entries())await renderStill({...options,frame:from+Math.min(scene.durationInFrames-1,b.from+20),output:`${out}/${scene.id}-step-${i}.png`});
   if(!keyframes&&scene.kind==='prime-ranges')for(const [i,b] of scene.beats.entries())await renderStill({...options,frame:from+Math.min(scene.durationInFrames-1,b.from+30),output:`${out}/${scene.id}-row-${i}.png`});
  }
  if(review&&scene.type==='primes'&&scene.kind==='vocabulary'){
   const c=scene.cues;
   const checkpoints={
    'before-11':c.eleven-1,'show-11':c.eleven,'before-pair':c.divisorPair-1,'show-pair':c.divisorPair,
    'centered-pair':c.divisorPair+30,'before-band':c.orangeBand-1,'orange-band':c.orangeBand,
    'before-statement':c.statement0-1,'statement-11':c.statement0,
    'statement-est':c.statement1,'statement-un':c.statement2,'statement-nombre':c.statement3,
    'statement-premier':c.statement4,'before-blink':c.blinkPair-1,'blink-pair':c.blinkPair+9,
   };
   for(const [name,local] of Object.entries(checkpoints)){
    const frame=from+local;
    frames.push({scene:'review-'+name,frame});
    if(!videoOnly)await renderStill({...options,frame,output:`${out}/review-${name}.png`});
   }
  }
  from+=scene.durationInFrames;
 }
 await writeFile(`${out}/timeline.json`,JSON.stringify(timeline,null,2));await writeFile(`${out}/review-frames.json`,JSON.stringify(frames,null,2));
 console.log(`Prime lesson previews ready; ${duration(timeline)/30}s, ${timeline.scenes.length} scenes.`);
 if(process.argv.includes('--stills'))return;
 let last=-1;await renderMedia({...options,codec:'h264',pixelFormat:'yuv420p',crf:18,concurrency:4,outputLocation:`${out}/${filename}`,onProgress:({progress})=>{const pct=Math.floor(progress*100);if(pct%10===0&&pct!==last){console.log(`Render ${pct}%`);last=pct;}}});
 console.log('Full prime-numbers video rendered.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
