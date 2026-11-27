/** Permanent 2026-11-05 user rules, opt-in motion preserves older approved exports. */
export const headingLabel=(title:string)=>title.trim().replace(/[\s:：]+$/u,'')+' :';
export function objectiveEntrance(frame:number,explanationStart:number,layout:'standard'|'single-line'='standard'){
 const start=Math.max(15,explanationStart-36),end=Math.max(start+1,explanationStart-3);
 const t=Math.max(0,Math.min(1,(frame-start)/(end-start)));
 const eased=t*t*(3-2*t);
 return {offsetY:(layout==='standard'?275:280)*(1-eased),settled:frame>=end,start,end};
}
