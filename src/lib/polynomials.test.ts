import {test} from 'node:test';
import assert from 'node:assert/strict';
import {expressionData,reducedTermCount,Monomial} from './polynomials';
import {headingLabel,objectiveEntrance} from './presentation';
test('All source examples have the claimed number of unlike terms after reduction',()=>{
 const expected={binome:2,'trois-termes':3,trinome:3,'deux-termes':2,'quatre-termes':4,'synthese-trinome':3,'synthese-polynome':4};
 for(const [id,e] of Object.entries(expressionData)){
  // Independent pairwise comparison of exponent triples, not the map algorithm.
  let unlike=0;
  for(let i=0;i<e.terms.length;i++)if(!e.terms.slice(0,i).some(t=>t.exponents.every((x,j)=>x===e.terms[i].exponents[j])))unlike++;
  assert.equal(unlike,expected[id as keyof typeof expected]);assert.equal(reducedTermCount(e.terms),unlike);
 }
 const same:Monomial[]=[{coefficient:1,exponents:[1,0,0]},{coefficient:2,exponents:[1,0,0]}];assert.equal(reducedTermCount(same),1);
 assert.equal(reducedTermCount([{coefficient:1,exponents:[1,0,0]},{coefficient:-1,exponents:[1,0,0]}]),0);
 assert.throws(()=>reducedTermCount([{coefficient:1,exponents:[-1,0,0]}]));
});
test('Objective starts centred, moves monotonically upwards, settles before explanations',()=>{
 assert.equal(objectiveEntrance(0,240).offsetY+110+310/2,540);
 let before=Infinity;for(let f=0;f<=240;f++){const v=objectiveEntrance(f,240);assert.ok(v.offsetY<=before);before=v.offsetY;}
 assert.equal(objectiveEntrance(237,240).offsetY,0);assert.equal(objectiveEntrance(237,240).settled,true);
 assert.equal(objectiveEntrance(0,240,'single-line').offsetY+150+220/2,540);
});
test('Headers receive exactly one final spaced colon',()=>{
 for(const input of ['Exemple','Définition :','Propriété:','Synthèse  : '])assert.match(headingLabel(input),/^[^:]+ :$/);
});
