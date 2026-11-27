import assert from 'node:assert/strict';
import test from 'node:test';
import demo from '../video/demo-lesson.json';
import {duration,timelineSchema} from './timeline';

test('The portable default is a valid twelve-second timeline using only its silent demo asset',()=>{
 const timeline=timelineSchema.parse(demo);
 assert.equal(duration(timeline),360);
 assert.ok(timeline.scenes.every(scene=>scene.audio==='demo/silence.wav'));
});
