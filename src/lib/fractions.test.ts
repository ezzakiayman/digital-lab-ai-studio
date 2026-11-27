import {test} from 'node:test';
import assert from 'node:assert/strict';
import plan from '../video/fractions-lesson.json';
import {timelineSchema} from './timeline';
import {gcd,lcm} from './ppcm';
test('Fraction storyboard coverage and its independently enumerated divisors',()=>{
 const t=timelineSchema.parse(plan);
 assert.equal(t.scenes.length,9);
 assert.deepEqual([...new Set(t.scenes.flatMap(s=>'sourceSlides' in s?s.sourceSlides:[]))].sort((a,b)=>a-b),Array.from({length:28},(_,i)=>i+1));
 const common=(a:number,b:number)=>Array.from({length:Math.min(a,b)},(_,i)=>i+1).filter(d=>a%d===0&&b%d===0);
 assert.deepEqual(common(23,41),[1]);assert.deepEqual(common(42,36),[1,2,3,6]);
 assert.equal(gcd(23,41),1);assert.equal(gcd(42,36),6);
 for(const divisor of [2,3,6])assert.equal((42/divisor)*36,(36/divisor)*42);
 const multiples=Array.from({length:180},(_,i)=>i+1).filter(n=>n%9===0&&n%15===0);
 assert.deepEqual(multiples,[45,90,135,180]);assert.equal(lcm(9,15),multiples[0]);assert.equal(gcd(3,4),1);
});
test('Fraction timeline rejects cues beyond scene and invalid beat ordering',()=>{
 const p=timelineSchema.parse(plan);const first=p.scenes[0];if(first.type!=='fractions')throw Error('Expected reviewed fractions scene');first.cues={invalid:first.durationInFrames};assert.equal(timelineSchema.safeParse(p).success,false);
 const q=structuredClone(plan);q.scenes[0].beats[1].from=0;assert.equal(timelineSchema.safeParse(q).success,false);
});
