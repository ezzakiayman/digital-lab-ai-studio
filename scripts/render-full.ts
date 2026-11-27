import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition} from '@remotion/renderer';
import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
import data from '../src/video/full-lesson.json';
import {timelineSchema} from '../src/lib/timeline';
async function main(){
 const timeline=timelineSchema.parse(data);await mkdir('outputs/full',{recursive:true});
 const serveUrl=await bundle({entryPoint:path.resolve('src/video/index.ts')});
 const inputProps={timeline};const composition=await selectComposition({serveUrl,id:'DigitalLab',inputProps});
 const options={serveUrl,composition,inputProps};
 for(const second of [10,37,52,85,120,132,145,165,175])await renderStill({...options,frame:second*30,output:`outputs/full/frame-${second}.png`});
 await writeFile('outputs/full/timeline.json',JSON.stringify(timeline,null,2));
 await renderMedia({...options,codec:'h264',pixelFormat:'yuv420p',crf:18,outputLocation:'outputs/full/Digital-Lab-Comparer-et-ranger.mp4',concurrency:4,onProgress:({progress})=>{const p=Math.floor(progress*100);if(p%10===0&&p!==last){console.log(`Render ${p}%`);last=p;}}});
 console.log('Full lesson rendered.');
}
let last=-1;main().catch(e=>{console.error(e);process.exitCode=1;});
