import {test} from 'node:test';
import assert from 'node:assert/strict';
import {compareNegative,duration,timelineSchema} from './timeline';
import data from '../video/lesson.json';
import comparison from '../video/comparison.json';
import full from '../video/full-lesson.json';
test('negative order reverses absolute-value order',()=>{assert.equal(compareNegative(-3,-2),'<');assert.equal(compareNegative(-2,-3),'>');assert.equal(compareNegative(-2,-2),'=');assert.throws(()=>compareNegative(0,-2));assert.throws(()=>compareNegative(NaN,-2));});
test('timeline rejects cues beyond duration and duplicate IDs',()=>{const t=timelineSchema.parse(data);assert.equal(duration(t),360);assert.equal(timelineSchema.safeParse({...t,scenes:[{...t.scenes[0],cues:[{from:90,to:400,target:'condition'}]}]}).success,false);assert.equal(timelineSchema.safeParse({...t,scenes:[t.scenes[0],t.scenes[0]]}).success,false);});
test('example data supports the demonstrated implication and rejects invalid operands/timing',()=>{
 const t=timelineSchema.parse(comparison);const s=t.scenes[0];assert.equal(s.type,'negative-comparison');
 if(s.type!=='negative-comparison')throw Error('Wrong template');
 assert.equal(compareNegative(...s.operands),'<');assert.ok(Math.abs(s.operands[0])>Math.abs(s.operands[1]));
 for(const operands of [[-2,-3],[-3,0],[-3,-3]])assert.equal(timelineSchema.safeParse({...t,scenes:[{...s,operands}]}).success,false);
 assert.equal(timelineSchema.safeParse({...t,scenes:[{...s,events:[{target:'less',from:100,to:99}]}]}).success,false);
 assert.equal(timelineSchema.safeParse({...t,scenes:[{...s,events:[{target:'less',from:100,to:1200}]}]}).success,false);
});
test('full lesson has continuous 180-second coverage with one narration track',()=>{
 const t=timelineSchema.parse(full);assert.equal(duration(t),5400);assert.ok(t.audio);
 assert.equal(t.scenes[3].title,'Propriété 1 (comparer deux nombres négatifs):');
 assert.equal(t.scenes[4].title,'Propriété 1');
 assert.equal(t.scenes.length,8);assert.ok(t.scenes.every(s=>s.audio===null));
 let start=0;const offsets=t.scenes.map(s=>{const from=start;start+=s.durationInFrames;return from;});
 assert.deepEqual(offsets,[0,840,1260,1440,1740,2850,4020,5100]);
 const last=t.scenes.at(-1);assert.equal(last?.type,'lesson-section');
 assert.equal(timelineSchema.safeParse({...t,scenes:[{...last,events:[{target:'line',from:0,to:999}]}]}).success,false);
});
