export function primeFactorization(value:number):Array<{prime:number;exponent:number}>{
 if(!Number.isSafeInteger(value)||value<2||value>1_000_000)throw Error('Factorisation requires an integer between2 and1000000');
 const factors:Array<{prime:number;exponent:number}>=[];let n=value;
 for(let p=2;p*p<=n;p++)if(n%p===0){let exponent=0;while(n%p===0){n/=p;exponent++;}factors.push({prime:p,exponent});}
 if(n>1)factors.push({prime:n,exponent:1});return factors;
}
export const powerDigits=(n:number)=>String(n).split('').map(d=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[Number(d)]).join('');
