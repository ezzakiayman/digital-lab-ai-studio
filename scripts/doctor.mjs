import {execFileSync} from 'node:child_process';
import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {homedir} from 'node:os';
import path from 'node:path';
let errors=0;
function check(label,fn){try{console.log('PASS '+label+': '+fn());}catch(e){errors++;console.error('FAIL '+label+': '+String(e.message).split('\n')[0]);}}
check('Node',()=>process.version);
for(const exe of ['ffmpeg','ffprobe'])check(exe,()=>execFileSync(exe,['-version'],{encoding:'utf8',windowsHide:true}).split('\n')[0]);
check('Locked dependencies',()=>{for(const name of ['remotion','@remotion/renderer','next','tsx','zod'])if(!existsSync(path.join('node_modules',name,'package.json')))throw Error('Run npm ci; missing '+name);return 'required JS packages present';});
check('Question artwork',()=>{const b=readFileSync('public/brand/question-mark.png');if(createHash('sha256').update(b).digest('hex')!=='a4e77332c60fc71ca8664c0c2173a7623e49488fdb695c6a9c861bf80333ae6d')throw Error('Approved question artwork changed');return 'approved 1254×1254 PNG hash';});
check('Target artwork',()=>{if(!existsSync('public/brand/objective-target.png'))throw Error('Missing target asset');return 'present';});
check('All live timeline audio',()=>{
 if(process.argv.includes('--portable')){const demo=JSON.parse(readFileSync('src/video/demo-lesson.json','utf8'));for(const scene of demo.scenes)if(!existsSync(path.join('public',scene.audio)))throw Error('Missing demo audio');return 'portable demo audio present; production media not included in Git';}
 const names=['lesson','comparison','full-lesson','n3-lesson','primes-lesson','primes-v2-lesson','primes-review-lesson','fractions-lesson','polynomials-lesson','polynomials-v2-lesson','factorization-lesson','factorization-v2-lesson','factorization-review-lesson','fractions-v2-lesson','fractions-review-lesson','like-terms-lesson','polynomial-subtraction-lesson','signed-addition-lesson','n1-sem2-vdp3-lesson','n1-sem2-vdp4-lesson','n3-sem3-vdp1-lesson','n3-sem3-vdp2-lesson','n3-sem3-vdp3-lesson','n3-sem3-vdp4-lesson','n3-sem3-vdp1-v2-lesson','n3-sem3-vdp2-v2-lesson','n3-sem3-vdp3-v2-lesson','n3-sem3-vdp4-v2-lesson'];let count=0;
 for(const name of names){const t=JSON.parse(readFileSync(`src/video/${name}.json`,'utf8'));for(const file of [t.audio,...t.scenes.map(s=>s.audio)].filter(Boolean)){const resolved=path.resolve('public',file),base=path.resolve('public')+path.sep;if(!resolved.startsWith(base)||!existsSync(resolved))throw Error('Missing/nonlocal audio '+file);count++;}}
 return count+' local audio references';
});
const bundle=path.join(process.env.CODEX_HOME||path.join(homedir(),'.codex'),'skills','digital-lab-project','private','gemini-key.dpapi');
console.log('New voice credential: '+(process.env.GEMINI_API_KEY?.trim()?'process environment configured':process.platform==='win32'&&existsSync(bundle)?'local encrypted bundle present (not decrypted by doctor)':'not configured; cached rendering still works'));
const elevenBundle=path.join(process.env.CODEX_HOME||path.join(homedir(),'.codex'),'skills','digital-lab-project','private','elevenlabs-key.dpapi');
console.log('Available ElevenLabs credential: '+(process.env.ELEVENLABS_API_KEY?.trim()?'process environment configured':process.platform==='win32'&&existsSync(elevenBundle)?'local encrypted bundle present (not decrypted by doctor)':'not configured; cached rendering still works'));
if(process.argv.includes('--full')){
 const pos=process.argv.indexOf('--python'),python=pos<0?'python':process.argv[pos+1];
 check('Python video tools',()=>execFileSync(python,['-c',"import sys,torch,torchaudio,uroman,numpy,PIL,faster_whisper; print(sys.version.split()[0], 'torch='+torch.__version__, 'torchaudio='+torchaudio.__version__, 'cuda='+str(torch.cuda.is_available()))"],{encoding:'utf8',windowsHide:true,timeout:120000}).trim());
}
process.exitCode=errors?1:0;
