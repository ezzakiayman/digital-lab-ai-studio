// Integer arithmetic, never a visual guess or an AI-generated formula.
export function positiveDivisors(n:number):number[]{
 if(!Number.isSafeInteger(n)||n<1||n>1000000)throw Error('Expected a positive integer at most 1000000');
 const low:number[]=[],high:number[]=[];
 for(let d=1;d*d<=n;d++)if(n%d===0){low.push(d);if(d*d!==n)high.push(n/d);}
 return low.concat(high.reverse());
}
export function isPrime(n:number){return Number.isSafeInteger(n)&&n>=2&&positiveDivisors(n).length===2;}
export const primeRanges=[
 {min:0,max:10,label:'Inférieurs à 10',color:'#2E75B6',values:[2,3,5,7]},
 {min:10,max:20,label:'Entre 10 et 20',color:'#70AD47',values:[11,13,17,19]},
 {min:20,max:30,label:'Entre 20 et 30',color:'#ED7D31',values:[23,29]},
 {min:30,max:40,label:'Entre 30 et 40',color:'#7030A0',values:[31,37]},
 {min:40,max:50,label:'Entre 40 et 50',color:'#00A3A3',values:[41,43,47]},
 {min:50,max:60,label:'Entre 50 et 60',color:'#C00000',values:[53,59]},
 {min:60,max:70,label:'Entre 60 et 70',color:'#BF9000',values:[61,67]},
 {min:70,max:80,label:'Entre 70 et 80',color:'#3B5998',values:[71,73,79]},
 {min:80,max:90,label:'Entre 80 et 90',color:'#D6336C',values:[83,89]},
 {min:90,max:100,label:'Entre 90 et 100',color:'#548235',values:[97]},
] as const;
export const primesBelow100=primeRanges.flatMap(r=>[...r.values]);
