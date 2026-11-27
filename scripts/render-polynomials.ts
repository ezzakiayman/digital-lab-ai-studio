import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition} from '@remotion/renderer';
import {mkdir,readFile,writeFile} from 'node:fs/promises';
import path from 'node:path';
import {duration,timelineSchema} from '../src/lib/timeline';
import {objectiveEntrance} from '../src/lib/presentation';
async function main(){
 const revised=process.argv.includes('--revised'),elevenlabs=process.argv.includes('--elevenlabs');
 if(revised&&elevenlabs)throw Error('The 55-slide revision uses Google Kore.');
 const out=revised?'outputs/n2-sem2-vdp1-2026-11-10':elevenlabs?'outputs/n2-sem2-vdp1':'outputs/n2-sem2-vdp1-google';await mkdir(out,{recursive:true});
 const timeline=timelineSchema.parse(JSON.parse(await readFile(revised?'src/video/polynomials-v2-lesson.json':'src/video/polynomials-lesson.json','utf8')));
 const expectedAudio=revised?'polynomials-v2-paced/':elevenlabs?'polynomials-elevenlabs-paced/':'polynomials-paced/';
 if(timeline.scenes.some(s=>s.type!=='polynomials'||!s.audio.startsWith(expectedAudio)))throw Error('Timeline voice does not match this output. Prepare/pace the selected provider before rendering; the other voice export is preserved.');
 const serveUrl=await bundle({entryPoint:path.resolve('src/video/index.ts')});
 const inputProps={timeline},composition=await selectComposition({serveUrl,id:'DigitalLab',inputProps});const options={serveUrl,composition,inputProps};
 let from=0;const frames=[];
 for(const s of timeline.scenes){
  const final=from+s.durationInFrames-15;frames.push({scene:s.id,frame:final});
  if(!process.argv.includes('--video-only')&&(!process.argv.includes('--objective-only')||s.id==='objectif')){
   await renderStill({...options,frame:final,output:`${out}/${s.id}.png`});
   if(s.type==='polynomials'){
    if(s.kind==='intro')for(const [label,frame] of [['center',0],['moving',objectiveEntrance(0,s.beats[1].from).start+16],['top',s.beats[1].from-2]] as const)await renderStill({...options,frame:from+frame,output:`${out}/objective-${label}.png`});
    if(revised&&s.kind==='intro')for(const [label,beat] of [['link',1],['roadmap',4]] as const)
     await renderStill({...options,frame:from+s.beats[beat].from+30,output:`${out}/objective-${label}.png`});
    if(revised&&s.kind==='pronunciation')
     await renderStill({...options,frame:from+s.beats[1].from+14,output:`${out}/${s.id}-first-syllable.png`});
    if(revised&&s.id==='exemple-polynome')
     await renderStill({...options,frame:from+s.beats[7].from+23,output:`${out}/${s.id}-exposants.png`});
    if(!process.argv.includes('--keyframes')&&['intro','example','synthesis'].includes(s.kind))for(const [i,b] of s.beats.entries())await renderStill({...options,frame:from+Math.min(s.durationInFrames-1,b.from+30),output:`${out}/${s.id}-step-${i}.png`});
   }
  }
  from+=s.durationInFrames;
 }
 await writeFile(`${out}/timeline.json`,JSON.stringify(timeline,null,2));await writeFile(`${out}/review-frames.json`,JSON.stringify(frames,null,2));
 console.log(`Polynomial previews ready; ${duration(timeline)/30}s, ${timeline.scenes.length} scenes.`);
 if(process.argv.includes('--stills')||process.argv.includes('--objective-only'))return;
 let last=-1;await renderMedia({...options,codec:'h264',pixelFormat:'yuv420p',crf:18,concurrency:4,outputLocation:`${out}/P1_MATHS_N2_SEM2_VDP1.mp4`,onProgress:({progress})=>{const pct=Math.floor(progress*100);if(pct%10===0&&pct!==last){console.log(`Render ${pct}%`);last=pct;}}});console.log('Full polynomial video rendered.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
