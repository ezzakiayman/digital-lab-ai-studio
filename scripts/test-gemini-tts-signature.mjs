import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {speechSignature} from './gemini-tts.mjs';

test('Existing speech caches retain their legacy signatures without locale/style',()=>{
 for(const speechMode of ['verbatim',undefined]){
  const scene={narration:'Expression numérique.',speechMode};
  const suffix=speechMode==='verbatim'?'|Kore|verbatim':'|Kore';
  const legacy=createHash('sha256').update(scene.narration+'|model'+suffix).digest('hex');
  assert.equal(speechSignature(scene,'model'),legacy);
 }
});
test('A locale or style change cannot silently reuse the old accented recording',()=>{
 const base={narration:'Expression.',speechMode:'verbatim'};
 const signatures=[base,{...base,languageCode:'fr-FR'}, {...base,languageCode:'en-US'},
  {...base,languageCode:'fr-FR',speechStyle:'Accent français naturel.'}].map(s=>speechSignature(s,'model'));
 assert.equal(new Set(signatures).size,4);
});
