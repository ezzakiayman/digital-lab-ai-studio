import {test} from 'node:test';
import assert from 'node:assert/strict';
import {gcd,lcm} from './ppcm';
import {ppcmSchema} from './timeline';
import plan from '../video/n3-plan.json';
test('PPCM examples and product identity are mathematically valid',()=>{
 assert.equal(lcm(6,4),12);assert.equal(gcd(6,4),2);assert.equal(lcm(72,8),72);assert.equal(8*9,72);
 for(let a=1;a<=40;a++)for(let b=1;b<=40;b++){const l=lcm(a,b);assert.equal(l%a,0);assert.equal(l%b,0);assert.equal(l*gcd(a,b),a*b);}
 for(const n of [0,-3,1.5,Infinity])assert.throws(()=>lcm(n,4));
});
test('N3 plan covers every storyboard slide with narration, keeping author instructions out',()=>{
 assert.deepEqual([...new Set(plan.scenes.flatMap(s=>s.sourceSlides))].sort((a,b)=>a-b),Array.from({length:39},(_,i)=>i+1));
 for(const scene of plan.scenes){assert.ok(scene.narration.length>10);assert.doesNotMatch(scene.narration,/Animer la voix|Insérer le fichier|Afficher le texte/i);}
});
test('PPCM timeline rejects unordered or out-of-bounds beats',()=>{
 const scene={...plan.scenes[0],durationInFrames:300,beats:[{stage:0,from:0,text:'Bonjour'},{stage:1,from:100,text:'Déterminer'}]};
 assert.ok(ppcmSchema.safeParse(scene).success);
 assert.equal(ppcmSchema.safeParse({...scene,beats:[{stage:0,from:20,text:'Bonjour'}]}).success,false);
 assert.equal(ppcmSchema.safeParse({...scene,beats:[{stage:0,from:0,text:'Bonjour'},{stage:1,from:350,text:'Trop tard'}]}).success,false);
});
