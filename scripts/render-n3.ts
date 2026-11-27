import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition} from '@remotion/renderer';
import {mkdir,readFile,writeFile} from 'node:fs/promises';
import path from 'node:path';
import {timelineSchema,duration} from '../src/lib/timeline';
async function main(){
 const preview=process.argv.includes('--preview');
 const out=process.argv.includes('--v4')?'outputs/n3-v4':process.argv.includes('--v3')?'outputs/n3-v3':process.argv.includes('--revision')?'outputs/n3-v2':'outputs/n3';
 const timeline=timelineSchema.parse(JSON.parse(await readFile(preview?'reference/n3/preview.json':'src/video/n3-lesson.json','utf8')));await mkdir(out,{recursive:true});
 const serveUrl=await bundle({entryPoint:path.resolve('src/video/index.ts')});
 const inputProps={timeline};const composition=await selectComposition({serveUrl,id:'DigitalLab',inputProps});const options={serveUrl,composition,inputProps};
 let from=0;for(const scene of timeline.scenes){const offset=from+Math.min(scene.durationInFrames-1,Math.floor(scene.durationInFrames*0.85));await renderStill({...options,frame:offset,output:`${out}/${scene.id}.png`});from+=scene.durationInFrames;}
 for(const frame of [0,280,430,650])await renderStill({...options,frame,output:`${out}/objective-${frame}.png`});
 await renderStill({...options,frame:timeline.scenes[0].durationInFrames-15,output:`${out}/objective-final.png`});
 let acronymFrom=0;for(const scene of timeline.scenes){if(scene.type==='ppcm'&&scene.kind==='acronym'){for(let i=0;i<4;i++)await renderStill({...options,frame:acronymFrom+Math.min(scene.durationInFrames-1,(scene.cues?.['word'+i]??scene.beats[i].from)+30),output:`${out}/acronym-${i+1}.png`});break;}acronymFrom+=scene.durationInFrames;}
 if(!preview)await writeFile(`${out}/timeline.json`,JSON.stringify(timeline,null,2));
 console.log(`Rendering ${duration(timeline)/30}s of PPCM with Gemini narration.`);
 if(process.argv.includes('--stills')||preview)return;
 let last=-1;await renderMedia({...options,codec:'h264',pixelFormat:'yuv420p',crf:18,outputLocation:`${out}/Digital-Lab-3AC-PPCM.mp4`,concurrency:4,onProgress:({progress})=>{const p=Math.floor(progress*100);if(p%10===0&&p!==last){console.log(`Render ${p}%`);last=p;}}});
 console.log('PPCM video rendered.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
