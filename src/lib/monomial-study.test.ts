import assert from 'node:assert/strict';
import test from 'node:test';
import {timelineSchema} from './timeline';
import raw from '../video/n2-sem1-vdp4-v2-lesson.json';

test('the revised monomial lesson follows the new 33-slide storyboard and its approved final card',()=>{
 const {scenes}=timelineSchema.parse(raw);
 assert.deepEqual(scenes.flatMap(s=>'sourceSlides' in s?s.sourceSlides:[]),Array.from({length:33},(_,i)=>i+1));
 assert.equal(scenes.length,10);
 const definition=scenes.find(s=>s.id==='definition-degre');
 assert.ok(definition?.type==='monomial-study');
 assert.equal(definition.lines?.join(' '),'Le degré d’un monôme non nul est la somme des exposants de ses variables.');
 const intro=scenes[0];
 assert.ok(intro.type==='vdp-sequence'&&intro.objective);
 assert.equal(intro.objective.links.length,2);
 assert.equal(intro.objective.links[1].art.length,0);
 assert.ok(!/\p{Script=Arabic}/u.test(intro.narration));
 const readings=scenes.flatMap(s=>s.type==='monomial-study'&&s.reading?[s.reading.parts]:[]);
 assert.deepEqual(readings,[['Mo','nôme'],['De','gré']]);
 const summary=scenes.at(-1);
 assert.ok(summary?.type==='monomial-study'&&summary.kind==='recap'&&summary.showSourceDuplicate);
});

