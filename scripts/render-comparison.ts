import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition} from '@remotion/renderer';
import {mkdir} from 'node:fs/promises';
import path from 'node:path';
import data from '../src/video/comparison.json';
import {timelineSchema} from '../src/lib/timeline';
const timeline=timelineSchema.parse(data);
async function main(){
 await mkdir('outputs/comparison',{recursive:true});
 const serveUrl=await bundle({entryPoint:path.resolve('src/video/index.ts')});
 const inputProps={timeline};const composition=await selectComposition({serveUrl,id:'DigitalLab',inputProps});
 const options={serveUrl,composition,inputProps};
 for(const second of [14,27,36])await renderStill({...options,frame:second*30,output:`outputs/comparison/generated-${second}.png`});
 await renderMedia({...options,codec:'h264',pixelFormat:'yuv420p',crf:18,outputLocation:'outputs/comparison/generated.mp4',concurrency:4});
 console.log('Comparison example rendered.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
