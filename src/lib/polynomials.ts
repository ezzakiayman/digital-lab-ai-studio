export type Monomial={coefficient:number;exponents:[number,number,number]};
export function reducedTermCount(terms:Monomial[]):number{
 const grouped=new Map<string,number>();
 for(const t of terms){if(!Number.isFinite(t.coefficient)||t.exponents.some(e=>!Number.isSafeInteger(e)||e<0))throw Error('Polynomial terms require finite coefficients and nonnegative integer exponents');const key=t.exponents.join(',');grouped.set(key,(grouped.get(key)||0)+t.coefficient);}
 return [...grouped.values()].filter(c=>c!==0).length;
}
export const expressionData={
 binome:{labels:['5x','+ 3y³'],widths:[180,300],colors:['#0070C0','#00B050'],terms:[{coefficient:5,exponents:[1,0,0]},{coefficient:3,exponents:[0,3,0]}]},
 'trois-termes':{labels:['x','+ 2y','+ 1'],widths:[120,280,220],colors:['#0070C0','#00B050','#1D1D1D'],terms:[{coefficient:1,exponents:[1,0,0]},{coefficient:2,exponents:[0,1,0]},{coefficient:1,exponents:[0,0,0]}]},
 trinome:{labels:['2x²','+ 4y','− 1'],widths:[240,280,220],colors:['#0070C0','#00B050','#803DA5'],terms:[{coefficient:2,exponents:[2,0,0]},{coefficient:4,exponents:[0,1,0]},{coefficient:-1,exponents:[0,0,0]}]},
 'deux-termes':{labels:['x','− 3y'],widths:[140,300],colors:['#0070C0','#00B050'],terms:[{coefficient:1,exponents:[1,0,0]},{coefficient:-3,exponents:[0,1,0]}]},
 'quatre-termes':{labels:['x³y²','+ xy³','− x³','+ 5'],widths:[300,320,250,220],colors:['#1D1D1D','#1D1D1D','#1D1D1D','#1D1D1D'],terms:[{coefficient:1,exponents:[3,2,0]},{coefficient:1,exponents:[1,3,0]},{coefficient:-1,exponents:[3,0,0]},{coefficient:5,exponents:[0,0,0]}]},
 'synthese-trinome':{labels:['2x','+ 5y','− 4'],widths:[180,250,200],colors:['#1D1D1D','#1D1D1D','#1D1D1D'],terms:[{coefficient:2,exponents:[1,0,0]},{coefficient:5,exponents:[0,1,0]},{coefficient:-4,exponents:[0,0,0]}]},
 'synthese-polynome':{labels:['x','+ y','− 2z','+ 1'],widths:[120,180,240,180],colors:['#1D1D1D','#1D1D1D','#1D1D1D','#1D1D1D'],terms:[{coefficient:1,exponents:[1,0,0]},{coefficient:1,exponents:[0,1,0]},{coefficient:-2,exponents:[0,0,1]},{coefficient:1,exponents:[0,0,0]}]},
} satisfies Record<string,{labels:string[];widths:number[];colors:string[];terms:Monomial[]}>;
export type ExpressionKey=keyof typeof expressionData;
