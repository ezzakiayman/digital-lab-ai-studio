import {test} from 'node:test';
import assert from 'node:assert/strict';
import {primeFactorization,powerDigits} from './factorization';
test('Every factor is prime and its reconstructed product equals the original integer',()=>{
 const prime=(n:number)=>{for(let d=2;d<n;d++)if(n%d===0)return false;return n>=2;};
 for(let n=2;n<=500;n++){
  const factors=primeFactorization(n);assert.ok(factors.every(f=>prime(f.prime)&&f.exponent>0));
  assert.equal(factors.reduce((p,f)=>p*f.prime**f.exponent,1),n);
  assert.equal(new Set(factors.map(f=>f.prime)).size,factors.length);
 }
 assert.deepEqual(primeFactorization(360),[{prime:2,exponent:3},{prime:3,exponent:2},{prime:5,exponent:1}]);
 assert.deepEqual(primeFactorization(72),[{prime:2,exponent:3},{prime:3,exponent:2}]);
 for(const n of [0,1,-3,2.5,1000001])assert.throws(()=>primeFactorization(n));
 assert.equal(powerDigits(123),'¹²³');
});
