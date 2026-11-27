import {build} from 'esbuild';
import {createServer} from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import {openBrowser} from '@remotion/renderer';

const root=process.cwd();
const src=path.resolve(process.argv[2]||'src/video/n2-sem1-vdp4-v2-lesson.json');
const output=path.resolve(process.argv[3]||'outputs/n2-sem1-vdp4-v2/after-effects-work');
const timeline=JSON.parse(await fs.readFile(src,'utf8'));
await fs.mkdir(output,{recursive:true});
const bundle=await build({entryPoints:['scripts/after-effects/capture-browser.jsx'],absWorkingDir:root,bundle:true,write:false,
 format:'iife',outfile:'capture.js',minify:false,loader:{'.css':'empty','.woff2':'empty','.woff':'empty','.ttf':'empty'},
 plugins:[{name:'visual-capture',setup(builder){
  builder.onResolve({filter:/^remotion$/},args=>/[\\/]StoryboardVisuals\.tsx$/.test(args.importer)?
   {path:'remotion',namespace:'capture-without-audio'}:null);
  builder.onLoad({filter:/.*/,namespace:'capture-without-audio'},()=>({
   contents:"export * from 'remotion'; export const Audio=()=>null;",resolveDir:root,
  }));
 }}],
 define:{'process.env.NODE_ENV':'"production"'},logLevel:'silent'});
const server=createServer(async(req,res)=>{
 try{
  const target=new URL(req.url,'http://localhost');
  if(target.pathname==='/'){
   res.setHeader('Content-Type','text/html; charset=utf-8');
   res.end('<!doctype html><html><head><meta charset="utf-8"><style>*{box-sizing:border-box}html,body,#root{margin:0;width:1920px;height:1080px;overflow:hidden}</style></head><body><div id="root"></div><script src="/capture.js"></script></body></html>');return;
  }
  if(target.pathname==='/capture.js'){res.setHeader('Content-Type','text/javascript; charset=utf-8');res.end(bundle.outputFiles.find(f=>f.path.endsWith('.js')).contents);return;}
  const relative=decodeURIComponent(target.pathname).replace(/^\/(?:public\/)?/,'');
  const assets=new Set(['brand/objective-target.png','n2-sem1-vdp4-v2/microphone.png']);
  if(assets.has(relative)){
   res.setHeader('Content-Type','image/png');
   res.end(await fs.readFile(path.join(root,'public',relative)));return;
  }
  res.writeHead(404).end();
 }catch(err){res.writeHead(500).end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const browser=await openBrowser('chrome');
try{
 const page=await browser.newPage({context:()=>null,logLevel:'error',indent:false,pageIndex:0,onBrowserLog:null,onLog:()=>{}});
 await page.setViewport({width:1920,height:1080,deviceScaleFactor:1});
 await page.goto({url:'http://127.0.0.1:'+server.address().port+'/',timeout:30000});
 const final={version:1,width:1920,height:1080,fps:30,scenes:[]};
 for(const scene of timeline.scenes){
  await page.evaluate(async scene=>{await window.captureSetup(scene);},scene);
  for(let from=0;from<scene.durationInFrames;from+=100){
   await page.evaluate(({from,to})=>window.captureFrames(from,to),{from,to:Math.min(from+100,scene.durationInFrames)});
  }
  const layers=await page.evaluate(()=>window.captureFinish());
  const sceneData={id:scene.id,title:scene.title,frames:scene.durationInFrames,sourceSlides:scene.sourceSlides,beats:scene.beats,audio:scene.audio,layers};
  if(!layers.length)throw Error('Empty scene '+scene.id);
  await fs.writeFile(path.join(output,'capture-'+scene.id+'.json'),JSON.stringify(sceneData));
  console.log(scene.id,scene.durationInFrames,'frames',layers.length,'layers');
  final.scenes.push(sceneData);
 }
 await fs.writeFile(path.join(output,'capture.json'),JSON.stringify(final));
 console.log('Complete:',final.scenes.reduce((n,s)=>n+s.frames,0),'frames');
}finally{await browser.close({silent:true});server.closeAllConnections();await new Promise(r=>server.close(r));}

