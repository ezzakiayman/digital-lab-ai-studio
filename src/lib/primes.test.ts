import {test} from 'node:test';
import assert from 'node:assert/strict';
import {isPrime,positiveDivisors,primeRanges,primesBelow100} from './primes';
import plan from '../video/primes-plan.json';
test('prime examples and every listed integer satisfy the exact divisor definition',()=>{
 assert.deepEqual(positiveDivisors(41),[1,41]);assert.deepEqual(positiveDivisors(10),[1,2,5,10]);assert.deepEqual(positiveDivisors(1),[1]);
 assert.equal(isPrime(1),false);assert.equal(isPrime(0),false);assert.equal(isPrime(-7),false);assert.equal(isPrime(2),true);assert.equal(isPrime(49),false);assert.equal(isPrime(97),true);
 // Independent exhaustive divisor count catches missing, repeated or composite entries.
 const expected=Array.from({length:100},(_,n)=>n).filter(n=>Array.from({length:n},(_,d)=>d+1).filter(d=>n%d===0).length===2);
 assert.equal(primesBelow100.length,25);assert.deepEqual(primesBelow100,expected);
 for(const r of primeRanges)assert.deepEqual(r.values,expected.filter(n=>n>r.min&&n<r.max));
 assert.throws(()=>positiveDivisors(0));assert.throws(()=>positiveDivisors(2.5));assert.throws(()=>isPrime(1000003));
});
test('reviewed narration covers all 32 slides and excludes authoring directions',()=>{
 assert.equal(plan.scenes.length,11);
 assert.deepEqual([...new Set(plan.scenes.flatMap(s=>s.sourceSlides))].sort((a,b)=>a-b),Array.from({length:32},(_,i)=>i+1));
 for(const scene of plan.scenes){assert.equal(scene.narration,scene.beats.map(b=>b.text).join(' '));assert.doesNotMatch(scene.narration,/afficher|animer|synchronisation|insérer le fichier/i);}
 assert.match(plan.scenes.find(s=>s.kind==='definition')!.narration,/diviseurs positifs distincts/);
});
