import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition} from '@remotion/renderer';
import {readFile,mkdir} from 'node:fs/promises';
import path from 'node:path';
import {timelineSchema} from '../src/lib/timeline';
async function main(){
 const out=process.argv.find(a=>a.startsWith('--out='))?.slice(6)||'outputs';
 const files=process.argv.slice(2).filter(a=>a!=='--still'&&!a.startsWith('--out='));
 const serveUrl=await bundle({entryPoint:path.resolve('src/video/index.ts')});
 await mkdir(out,{recursive:true});
 for(const [i,file] of (files.length?files:['src/video/demo-lesson.json']).entries()){
  const timeline=timelineSchema.parse(JSON.parse(await readFile(file,'utf8')));
  const inputProps={timeline}; const composition=await selectComposition({serveUrl,id:'DigitalLab',inputProps});
  const options={serveUrl,composition,inputProps};
  if(process.argv.includes('--still'))await renderStill({...options,frame:90,output:path.join(out,`scene-${i+1}.png`)});
  else await renderMedia({...options,codec:'h264',pixelFormat:'yuv420p',crf:18,outputLocation:path.join(out,`lesson-${i+1}.mp4`),concurrency:2});
  console.log(`Rendered ${file}`);
 }
}
main().catch(e=>{console.error(e);process.exitCode=1;});
