export function gcd(a:number,b:number):number{
 if(!Number.isSafeInteger(a)||!Number.isSafeInteger(b)||a<=0||b<=0)throw Error('Positive nonzero safe integers required');
 while(b){[a,b]=[b,a%b];}return a;
}
export function lcm(a:number,b:number):number{const result=(a/gcd(a,b))*b;if(!Number.isSafeInteger(result))throw Error('LCM exceeds safe integer range');return result;}
