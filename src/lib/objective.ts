// Stable pedagogical order: never rotate this palette based on topic or count.
export const objectiveColors=['#E60012','#0DBBA1','#7061AA','#D28B14'] as const;
export function objectiveColor(index:number){if(!Number.isInteger(index)||index<0||index>3)throw Error('Objective explanations support one to four ordered links');return objectiveColors[index];}
// One title size across every line; wrap text instead of shrinking individual phrases.
export const objectiveTitleFontSize=72;
export const ppcmObjectiveTerms=[
 {text:'Déterminer',x:320,width:380,y:235,fontSize:objectiveTitleFontSize,anchor:511,labelX:511,labelY:710,bottom:610},
 {text:'le plus petit multiple commun',x:720,width:1016,y:235,fontSize:objectiveTitleFontSize,anchor:1730,labelX:1580,labelY:710,bottom:610},
 {text:'de deux entiers positifs non nuls',x:588,width:1124,y:345,fontSize:objectiveTitleFontSize,anchor:1150,labelX:1150,labelY:870,bottom:770},
] as const;
