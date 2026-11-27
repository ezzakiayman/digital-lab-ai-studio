import {test} from 'node:test';
import assert from 'node:assert/strict';
import {objectiveColor,objectiveColors,objectiveTitleFontSize,ppcmObjectiveTerms} from './objective';
import timeline from '../video/n3-lesson.json';
test('one to four objective links always use the same ordered palette',()=>{
 for(const count of [1,2,3,4])assert.deepEqual(Array.from({length:count},(_,i)=>objectiveColor(i)),objectiveColors.slice(0,count));
 assert.throws(()=>objectiveColor(-1));assert.throws(()=>objectiveColor(4));
});
test('keyword underlines are separate and remain inside the banner',()=>{
 assert.equal(objectiveTitleFontSize,72);
 for(const [i,term] of ppcmObjectiveTerms.entries()){assert.ok(term.x>=310&&term.x+term.width<=1800);assert.equal(term.fontSize,objectiveTitleFontSize);if(i&&term.y===ppcmObjectiveTerms[i-1].y)assert.ok(term.x>ppcmObjectiveTerms[i-1].x+ppcmObjectiveTerms[i-1].width);}
 assert.ok(ppcmObjectiveTerms[0].anchor<ppcmObjectiveTerms[2].x);
 assert.ok(ppcmObjectiveTerms[1].anchor>ppcmObjectiveTerms[2].x+ppcmObjectiveTerms[2].width);
});
function ordered(...values:Array<number|undefined>){const n=values.map(v=>{if(typeof v!=='number')throw Error('Missing aligned cue');return v;});for(let i=1;i<n.length;i++)assert.ok(n[i]>n[i-1]);}
test('new timeline uses aligned words for the objective and progressive numbers',()=>{
 assert.equal(timeline.scenes[0].title,'Déclaration de l’objectif');
 for(const scene of timeline.scenes)assert.equal(scene.timingMethod,'MMS_FA known-transcript alignment');
 const objective=timeline.scenes[0];ordered(objective.cues.explanation1,objective.cues.explanation2,objective.cues.positiveExamples,objective.cues.invalidExamples);
 const multiples=timeline.scenes.find(s=>s.kind==='multiples')!;
 ordered(multiples.cues.number12,multiples.cues.number24,multiples.cues.number36,multiples.cues.circle12);
});
