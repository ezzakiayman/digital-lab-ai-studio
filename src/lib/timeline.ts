import {z} from 'zod';
export const sceneSchema=z.object({id:z.string().min(1),type:z.literal('property'),title:z.string().min(1).max(90),durationInFrames:z.number().int().min(60).max(3600),narration:z.string(),audio:z.string().nullable(),cues:z.array(z.object({from:z.number().int().nonnegative(),to:z.number().int().positive(),target:z.enum(['condition','conclusion'])}))}).superRefine((s,c)=>{for(const cue of s.cues) if(cue.from>=cue.to||cue.to>s.durationInFrames)c.addIssue({code:'custom',message:'Cue outside scene or reversed'});});
const exampleEvent=z.object({target:z.enum(['prompt','signs','arrowA','arrowB','absoluteA','absoluteB','redA','redB','greater','focusA','given','therefore','resultA','less','resultB']),from:z.number().int().nonnegative(),to:z.number().int().positive()});
export const exampleSchema=z.object({id:z.string().min(1),type:z.literal('negative-comparison'),title:z.string().min(1).max(22),durationInFrames:z.number().int().min(60).max(3600),narration:z.string(),audio:z.string().nullable(),sourceSlides:z.array(z.number().int().min(1)),operands:z.tuple([z.number().finite().negative(),z.number().finite().negative()]),events:z.array(exampleEvent)}).superRefine((s,c)=>{if(s.operands[0]>=s.operands[1])c.addIssue({code:'custom',message:'This demonstration requires a < b < 0'});for(const e of s.events)if(e.from>=e.to||e.to>s.durationInFrames)c.addIssue({code:'custom',message:'Event outside scene or reversed'});});
export const sectionSchema=z.object({id:z.string().min(1),type:z.literal('lesson-section'),section:z.enum(['intro','phonetics','property-lead','opposite-signs','number-line','summary']),title:z.string(),durationInFrames:z.number().int().min(30).max(3600),audio:z.string().nullable(),narration:z.string(),sourceSlides:z.array(z.number().int().positive()),events:z.array(z.object({target:z.string(),from:z.number().int().nonnegative(),to:z.number().int().positive()}))}).superRefine((s,c)=>{for(const e of s.events)if(e.from>=e.to||e.to>s.durationInFrames)c.addIssue({code:'custom',message:'Invalid section event bounds'});});
export const ppcmSchema=z.object({id:z.string().min(1),type:z.literal('ppcm'),kind:z.enum(['intro','definition','acronym','multiples','lcm-result','property1','divisible-example','property2','product-example','verification','pronunciation','summary','summary1','summary2','vocabulary']),title:z.string().min(1),cues:z.record(z.string(),z.number().int().nonnegative()).optional(),timingMethod:z.string().optional(),durationInFrames:z.number().int().min(30).max(18000),audio:z.string().min(1),narration:z.string().min(1),sourceSlides:z.array(z.number().int().positive()).min(1),beats:z.array(z.object({stage:z.number().int().nonnegative(),from:z.number().int().nonnegative(),text:z.string()})).min(1)}).superRefine((s,c)=>{let last=-1;for(const b of s.beats){if(b.from<=last||b.from>=s.durationInFrames)c.addIssue({code:'custom',message:'PPCM beat must be ordered and within scene'});last=b.from;}if(s.beats[0].from!==0)c.addIssue({code:'custom',message:'PPCM scene must start at frame zero'});});
export const primesSchema=z.object({id:z.string().min(1),type:z.literal('primes'),revision:z.enum(['2026-11-10','2026-11-12']).optional(),holdSeconds:z.number().min(0.5).max(10).optional(),kind:z.enum(['intro','definition','divisors','one','question','prime-ranges','all-primes','pronunciation','vocabulary']),title:z.string().min(1),value:z.union([z.literal(10),z.literal(41)]).optional(),rangeStart:z.union([z.literal(0),z.literal(5)]).optional(),cues:z.record(z.string(),z.number().int().nonnegative()),timingMethod:z.string(),durationInFrames:z.number().int().min(30).max(18000),audio:z.string().min(1),narration:z.string().min(1),sourceSlides:z.array(z.number().int().positive()).min(1),beats:z.array(z.object({stage:z.number().int().nonnegative(),from:z.number().int().nonnegative(),text:z.string()})).min(1)}).superRefine((s,c)=>{
 let last=-1;for(const [i,b] of s.beats.entries()){if(b.from<=last||b.from>=s.durationInFrames||b.stage!==i)c.addIssue({code:'custom',message:'Prime lesson beats must be ordered, consecutive and within scene'});last=b.from;}
 if(s.beats[0].from!==0)c.addIssue({code:'custom',message:'Scene must start at frame zero'});
 for(const t of Object.values(s.cues))if(t>=s.durationInFrames)c.addIssue({code:'custom',message:'Cue outside scene'});
 if(s.kind==='divisors'&&s.value===undefined)c.addIssue({code:'custom',message:'Divisor example requires its reviewed integer'});
 if(s.kind==='prime-ranges'&&s.rangeStart===undefined)c.addIssue({code:'custom',message:'Prime list requires its range group'});
 if(s.revision&&s.kind==='pronunciation'&&s.beats.length!==4)c.addIssue({code:'custom',message:'Premier needs its introduction, two syllables and whole word'});
});
export const fractionsSchema=z.object({id:z.string().min(1),type:z.literal('fractions'),revision:z.enum(['2026-11-10','2026-11-12']).optional(),kind:z.enum(['intro','irreducible','reducible','definition','property','common','denominator','pronunciation','vocabulary']),title:z.string().min(1),holdSeconds:z.number().min(.5).max(10).optional(),cues:z.record(z.string(),z.number().int().nonnegative()),reveals:z.record(z.string(),z.array(z.object({text:z.string().min(1),from:z.number().int().nonnegative()})).min(1)).optional(),timingMethod:z.string(),durationInFrames:z.number().int().min(30).max(18000),audio:z.string().min(1),narration:z.string().min(1),sourceSlides:z.array(z.number().int().positive()).min(1),beats:z.array(z.object({stage:z.number().int().nonnegative(),from:z.number().int().nonnegative(),text:z.string()})).min(1)}).superRefine((s,c)=>{
 let last=-1;for(const [i,b] of s.beats.entries()){if(b.stage!==i||b.from<=last||b.from>=s.durationInFrames)c.addIssue({code:'custom',message:'Fraction beat must be ordered and within scene'});last=b.from;}
 if(s.beats[0].from!==0)c.addIssue({code:'custom',message:'Scene must start at frame zero'});
 for(const t of Object.values(s.cues))if(t>=s.durationInFrames)c.addIssue({code:'custom',message:'Cue outside scene'});
 for(const line of Object.values(s.reveals??{})) {
  if(line.some(({from},i)=>from>=s.durationInFrames||i>0&&from<line[i-1].from))
   c.addIssue({code:'custom',message:'Fraction word reveals must be ordered and within scene'});
 }
});
export const polynomialsSchema=z.object({id:z.string().min(1),type:z.literal('polynomials'),revision:z.literal('2026-11-10').optional(),kind:z.enum(['intro','definition','example','pronunciation','synthesis','vocabulary','inclusion','next']),title:z.string().min(1),concept:z.enum(['binome','trinome','polynome']).optional(),expressionKey:z.enum(['binome','trois-termes','trinome','deux-termes','quatre-termes','synthese-trinome','synthese-polynome']).optional(),valid:z.boolean().optional(),objectiveVariant:z.enum(['original','content-matched']).optional(),holdSeconds:z.number().min(.5).max(10).optional(),cues:z.record(z.string(),z.number().int().nonnegative()),timingMethod:z.string(),durationInFrames:z.number().int().min(30).max(18000),audio:z.string().min(1),narration:z.string().min(1),sourceSlides:z.array(z.number().int().positive()).min(1),beats:z.array(z.object({stage:z.number().int().nonnegative(),from:z.number().int().nonnegative(),text:z.string()})).min(1)}).superRefine((s,c)=>{
 let last=-1;for(const [i,b] of s.beats.entries()){if(b.stage!==i||b.from<=last||b.from>=s.durationInFrames)c.addIssue({code:'custom',message:'Polynomial beat must be consecutive, ordered and within scene'});last=b.from;}
 if(s.beats[0].from!==0)c.addIssue({code:'custom',message:'Scene must start at zero'});
 for(const t of Object.values(s.cues))if(t>=s.durationInFrames)c.addIssue({code:'custom',message:'Cue outside scene'});
 if(['definition','example','pronunciation'].includes(s.kind)&&!s.concept)c.addIssue({code:'custom',message:'Scene requires its reviewed concept'});
 if(s.kind==='example'&&(!s.expressionKey||s.valid===undefined))c.addIssue({code:'custom',message:'Example requires expression and classification'});
 if(s.revision&&s.kind==='intro'&&s.beats.length!==6)c.addIssue({code:'custom',message:'The two-part roadmap needs six beats'});
 if(s.revision&&s.kind==='pronunciation'&&s.beats.length!==(s.concept==='polynome'?5:4))c.addIssue({code:'custom',message:'Pronunciation needs a beat for each syllable and the full word'});
});
export const factorizationSchema=z.object({id:z.string().min(1),type:z.literal('factorization'),revision:z.enum(['2026-11-10','2026-11-12']).optional(),kind:z.enum(['intro','theorem','example','pronunciation','vocabulary']),title:z.string().min(1),value:z.union([z.literal(72),z.literal(360)]).optional(),holdSeconds:z.number().min(.5).max(10).optional(),cues:z.record(z.string(),z.number().int().nonnegative()),timingMethod:z.string(),durationInFrames:z.number().int().min(30).max(18000),audio:z.string().min(1),narration:z.string().min(1),sourceSlides:z.array(z.number().int().positive()).min(1),beats:z.array(z.object({stage:z.number().int().nonnegative(),from:z.number().int().nonnegative(),text:z.string()})).min(1)}).superRefine((s,c)=>{
 let last=-1;for(const [i,b] of s.beats.entries()){if(b.stage!==i||b.from<=last||b.from>=s.durationInFrames)c.addIssue({code:'custom',message:'Factorisation beats must be consecutive, ordered and within scene'});last=b.from;}
 if(s.beats[0].from!==0)c.addIssue({code:'custom',message:'Scene must start at zero'});
 for(const t of Object.values(s.cues))if(t>=s.durationInFrames)c.addIssue({code:'custom',message:'Cue outside scene'});
 if(s.kind==='theorem'&&s.value!==360)c.addIssue({code:'custom',message:'The reviewed theorem example is360'});
 if(s.kind==='example'&&s.value!==72)c.addIssue({code:'custom',message:'The reviewed second example is72'});
});
const algebraScene=z.object({
 id:z.string().min(1), title:z.string().min(1), sourceSlides:z.array(z.number().int().positive()).min(1),
 durationInFrames:z.number().int().min(30).max(18000), audio:z.string().min(1), narration:z.string().min(1),
 timingMethod:z.string(), holdSeconds:z.number().min(.5).max(10).optional(),
 cues:z.record(z.string(),z.number().int().nonnegative()),
 beats:z.array(z.object({stage:z.number().int().nonnegative(),from:z.number().int().nonnegative(),text:z.string()})).min(1),
});
function checkAlgebraBeats(s:z.infer<typeof algebraScene>,c:z.RefinementCtx,expected:number){
 if(s.beats.length!==expected||s.beats[0].from!==0||s.beats.some((b,i)=>b.stage!==i||b.from>=s.durationInFrames||(i>0&&b.from<=s.beats[i-1].from)))
  c.addIssue({code:'custom',message:'Algebra scene beats must match its stages and stay within its duration'});
 if(Object.values(s.cues).some(frame=>frame>=s.durationInFrames))c.addIssue({code:'custom',message:'Cue outside scene'});
}
export const likeTermsSchema=algebraScene.extend({
 type:z.literal('like-terms'),kind:z.enum(['intro','definition','comparison','pronunciation','synthesis','vocabulary']),
 example:z.enum(['like','unlike']).optional(),
}).superRefine((s,c)=>{
 checkAlgebraBeats(s,c,{intro:4,definition:2,comparison:7,pronunciation:4,synthesis:5,vocabulary:1}[s.kind]);
 if(s.kind==='comparison'&&!s.example)c.addIssue({code:'custom',message:'Comparison needs its reviewed example'});
});
export const polynomialSubtractionSchema=algebraScene.extend({
 type:z.literal('polynomial-subtraction'),kind:z.enum(['intro','task','opposite','horizontal','vertical','synthesis']),
 method:z.enum(['horizontal','vertical']).optional(),
}).superRefine((s,c)=>{
 const across=s.method==='horizontal';
 checkAlgebraBeats(s,c,{intro:2,task:across?8:6,opposite:across?5:2,horizontal:11,vertical:8,synthesis:5}[s.kind]);
 if((s.kind==='task'||s.kind==='opposite')&&!s.method)c.addIssue({code:'custom',message:'Subtraction scene needs a method'});
});
const signedAdditionCues={
 intro:['plus','negative','absolute'],
 same:['positive','negative','commonPlus','commonMinus','square','triangle'],
 different:['casePositive','caseNegative','keepLarger','largePlus','keepPlus','largeMinus','keepMinus','difference'],
 opposites:['positive','negative','zero'],
};
const signedAdditionSchema=algebraScene.extend({
 type:z.literal('signed-addition'),
 kind:z.enum(['intro','same','different','opposites']),
}).superRefine((s,c)=>{
 checkAlgebraBeats(s,c,{intro:3,same:9,different:10,opposites:4}[s.kind]);
 if(s.sourceSlides.length!==s.beats.length)c.addIssue({code:'custom',path:['sourceSlides'],message:'Each signed-addition beat must have a source slide'});
 for(const cue of signedAdditionCues[s.kind]){
  if(s.cues[cue]===undefined)c.addIssue({code:'custom',path:['cues',cue],message:'Required narration cue'});
 }
});
const monomialStudySchema=algebraScene.extend({
 type:z.literal('monomial-study'),
 kind:z.enum(['definition','diagram','recap','reading']),
 wordCues:z.array(z.object({word:z.string().min(1),startFrame:z.number().int().nonnegative()})),
 lines:z.array(z.string()).optional(),
 reading:z.object({word:z.string().min(1),parts:z.tuple([z.string(),z.string()]),advances:z.tuple([z.number().positive(),z.number().positive()])}).optional(),
 showSourceDuplicate:z.boolean().optional(),
}).superRefine((s,c)=>{
 checkAlgebraBeats(s,c,s.kind==='reading'?4:s.sourceSlides.length);
 if((s.kind==='reading')!==Boolean(s.reading)||s.reading&&s.reading.parts.join('')!==s.reading.word)
  c.addIssue({code:'custom',message:'The two written units must spell the vocabulary word'});
 if(s.kind==='definition'&&!s.lines?.length)
  c.addIssue({code:'custom',message:'Missing learner definition'});
 if(s.wordCues.some((w,i)=>w.startFrame>=s.durationInFrames||i>0&&w.startFrame<s.wordCues[i-1].startFrame))
  c.addIssue({code:'custom',message:'Word cues must be ordered and inside the audio scene'});
});
const vdpVisualSchema=z.object({
 kind:z.enum(['math','text','card','arrow','ring','question','alert','axis','axis-root','sets','status','number-node','algebra','clip']),
 value:z.string(),x:z.number().min(0).max(1920),y:z.number().min(0).max(1080),size:z.number().positive().max(600),
 at:z.number().int().nonnegative(),to:z.number().int().positive().optional(),pulse:z.number().int().nonnegative().optional(),
 frame:z.number().int().nonnegative().optional(),color:z.string().regex(/^#[0-9a-f]{6}$/i).optional(),
 toFrame:z.number().int().positive().optional(),
 pulseFrame:z.number().int().nonnegative().optional(),draw:z.boolean().optional(),
 repeatPulse:z.boolean().optional(),
 setPulses:z.array(z.object({target:z.enum(['real','rational','irrational']),frame:z.number().int().nonnegative()})).max(3).optional(),
 clipFrames:z.number().int().positive().optional(),
 background:z.string().regex(/^#[0-9a-f]{6}$/i).optional(),
 tokenColors:z.array(z.object({index:z.number().int().nonnegative(),at:z.number().int().nonnegative(),
  color:z.string().regex(/^#[0-9a-f]{6}$/i)})).max(24).optional(),
 tokenMarks:z.array(z.object({index:z.number().int().nonnegative(),at:z.number().int().nonnegative(),
  endIndex:z.number().int().nonnegative().optional(),to:z.number().int().positive().optional(),
  color:z.string().regex(/^#[0-9a-f]{6}$/i).optional()})).max(12).optional(),
 focus:z.array(z.object({target:z.enum(['denominator','exponent','decimal']),
  start:z.number().int().nonnegative(),end:z.number().int().positive()})).max(3).optional(),
 weight:z.number().int().min(100).max(900).optional(),rtl:z.boolean().optional(),moveFrom:z.number().min(0).max(1920).optional(),
});
const vdpSequenceSchema=algebraScene.extend({
 type:z.literal('vdp-sequence'),kind:z.enum(['intro','open','teaching','pronunciation']),speechMode:z.literal('verbatim').optional(),
 art:z.array(vdpVisualSchema).max(30),
 transition:z.boolean().optional(),
 objective:z.object({
  title:z.string().min(1),measure:z.number().positive(),size:z.number().min(36).max(72),
  mathSuffix:z.string().min(1).max(80).optional(),mathOffset:z.number().positive().optional(),
  formula:z.object({
   value:z.string().min(1),offset:z.number().nonnegative(),width:z.number().positive(),size:z.number().positive().max(72),
  }).optional(),
  links:z.array(z.object({offset:z.number().nonnegative(),width:z.number().positive(),at:z.number().int().positive(),endFrame:z.number().int().positive().optional(),art:z.array(vdpVisualSchema)})).min(1).max(4),
 }).optional(),
 pronunciation:z.object({
  word:z.string().min(1),syllables:z.array(z.string().min(1)).min(2).max(6),
  style:z.literal('simplifier').optional(),advances:z.array(z.number().positive()).min(2).max(6).optional(),
 }).optional(),
}).superRefine((s,c)=>{
 checkAlgebraBeats(s,c,s.beats.length);
 const last=s.beats.length-1;
 if((s.kind==='intro')!==Boolean(s.objective))c.addIssue({code:'custom',message:'VDP objective data must match its scene'});
 if((s.kind==='pronunciation')!==Boolean(s.pronunciation)||s.pronunciation&&s.pronunciation.syllables.length+2!==s.beats.length)
  c.addIssue({code:'custom',message:'Pronunciation needs one beat per syllable and a whole-word beat'});
 if(s.pronunciation?.style==='simplifier'&&(
  s.pronunciation.advances?.length!==s.pronunciation.syllables.length||
  s.pronunciation.syllables.join('').toLocaleLowerCase('fr')!==s.pronunciation.word.toLocaleLowerCase('fr')))
  c.addIssue({code:'custom',message:'Reference pronunciation needs measured parts that spell the complete word'});
 if(s.objective?.links.some((link,i)=>link.at>last||link.offset+link.width>s.objective!.measure+1||i>0&&link.at<=s.objective!.links[i-1].at||link.endFrame!==undefined&&(link.endFrame>s.durationInFrames||link.endFrame<=(s.beats[link.at]?.from??0))))
  c.addIssue({code:'custom',message:'Invalid objective link order or measurement'});
 if(s.objective&&(Boolean(s.objective.mathSuffix)!==Boolean(s.objective.mathOffset)||
  s.objective.mathOffset!==undefined&&s.objective.mathOffset>=s.objective.measure
  ||s.objective.formula&&(Boolean(s.objective.mathSuffix)||
    s.objective.formula.offset+s.objective.formula.width>s.objective.measure+1)))
  c.addIssue({code:'custom',message:'Invalid measured objective formula'});
 const art=[...s.art,...(s.objective?.links.flatMap(link=>link.art)??[])];
 if(art.some(a=>a.at>last||a.to!==undefined&&(a.to<=a.at||a.to>last)||a.pulse!==undefined&&a.pulse>last||a.frame!==undefined&&a.frame>=s.durationInFrames
  ||a.toFrame!==undefined&&(a.toFrame>s.durationInFrames||a.toFrame<=(a.frame??s.beats[a.at]?.from??0))
  ||a.pulseFrame!==undefined&&a.pulseFrame>=s.durationInFrames
  ||a.setPulses?.some(p=>a.kind!=='sets'||p.frame>=s.durationInFrames)
  ||a.focus?.some(f=>f.start>=f.end||f.end>s.durationInFrames)
  ||a.kind==='clip'&&(a.frame===undefined||!a.clipFrames||a.frame+a.clipFrames>s.durationInFrames
    ||!/^\w[\w/-]*\.mp4$/i.test(a.value))
  ||a.tokenMarks?.some(mark=>mark.endIndex!==undefined&&(mark.endIndex<mark.index||mark.endIndex>=a.value.length)
    ||mark.to!==undefined&&(mark.to<=mark.at||mark.to>last))
  ||[...a.tokenColors??[],...a.tokenMarks??[]].some(token=>a.kind!=='algebra'||token.at>last||token.index>=a.value.length||a.value[token.index]===' ')))
  c.addIssue({code:'custom',message:'VDP cues must keep visuals within their scene'});
});
export const timelineSchema=z.object({version:z.literal(1),lesson:z.string(),level:z.enum(['1AC','2AC','3AC']),videoType:z.enum(['VM','VDP']),fps:z.literal(30),audio:z.string().nullable().optional(),scenes:z.array(z.union([sceneSchema,exampleSchema,sectionSchema,ppcmSchema,primesSchema,fractionsSchema,polynomialsSchema,factorizationSchema,likeTermsSchema,polynomialSubtractionSchema,signedAdditionSchema,monomialStudySchema,vdpSequenceSchema])).min(1).max(100)}).superRefine((t,c)=>{if(new Set(t.scenes.map(s=>s.id)).size!==t.scenes.length)c.addIssue({code:'custom',message:'Scene IDs must be unique'});});
export type Timeline=z.infer<typeof timelineSchema>;
export const duration=(t:Timeline)=>t.scenes.reduce((a,s)=>a+s.durationInFrames,0);
export function compareNegative(a:number,b:number){if(!Number.isFinite(a)||!Number.isFinite(b)||a>=0||b>=0)throw Error('Two finite strictly negative numbers required');return a<b?'<':a>b?'>':'=';}

