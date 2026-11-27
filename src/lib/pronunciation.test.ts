import {test} from 'node:test';
import assert from 'node:assert/strict';
import {timelineSchema} from './timeline';
import lesson from '../video/n3-sem4-vdp2-v2-lesson.json';

test('Editable pronunciation keeps its complete spelling, measured parts and distinct audio cues',()=>{
 const scene=lesson.scenes.find(s=>s.kind==='pronunciation')!;
 const check=(pronunciation:unknown,beats=scene.beats)=>timelineSchema.safeParse({
  ...lesson,scenes:[{...scene,pronunciation,beats}],
 }).success;
 assert.ok(check(scene.pronunciation));
 assert.equal(check({...scene.pronunciation,syllables:['quo','tien']}),false);
 assert.equal(check({...scene.pronunciation,advances:[117]}),false);
 assert.equal(check(scene.pronunciation,scene.beats.slice(0,-1)),false);
 assert.equal(check(scene.pronunciation,scene.beats.map(b=>({...b,from:0}))),false);
});
