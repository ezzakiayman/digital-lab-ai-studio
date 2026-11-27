import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import {execFileSync} from 'node:child_process';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import path from 'node:path';
import {z} from 'zod';
import {timelineSchema} from '../src/lib/timeline';

const weekFour = ['n3-sem4-vdp1','n3-sem4-vdp2-v2'] as const;
const weekOne = ['n2-sem1-vdp3','n2-sem1-vdp4'] as const;
const weekThree = ['n3-sem3-vdp1','n3-sem3-vdp2','n3-sem3-vdp3','n3-sem3-vdp4'] as const;
const weekThreeV2 = weekThree.map(stem=>stem+'-v2');
const weekThreeV3 = weekThree.map(stem=>stem+'-v3');
const weekThreeV4 = weekThree.map(stem=>stem+'-v4');
const lessons = {
 'n2-sem1-vdp4-v2': {folder:'n2-sem1-vdp4-v2',file:'P1_MATHS_N2_SEM1_VDP4_V2'},
 'n1-sem2-vdp4-v2': {folder:'n1-sem2-vdp4-v2',file:'P1_MATHS_N1_SEM2_VDP4_V2'},
 'n3-sem3-vdp4-v7': {folder:'n3-sem3-v7/vdp4',file:'P1_MATHS_N3_SEM3_VDP4_V7'},
 'n3-sem3-vdp4-v6': {folder:'n3-sem3-v6/vdp4',file:'P1_MATHS_N3_SEM3_VDP4_V6'},
 'n3-sem3-vdp4-v5': {folder:'n3-sem3-v5/vdp4',file:'P1_MATHS_N3_SEM3_VDP4_V5'},
 'n3-sem3-vdp3-v6': {folder:'n3-sem3-v6/vdp3',file:'P1_MATHS_N3_SEM3_VDP3_V6'},
 'n3-sem3-vdp3-v5': {folder:'n3-sem3-v5/vdp3',file:'P1_MATHS_N3_SEM3_VDP3_V5'},
 'n3-sem3-vdp2-v5': {folder:'n3-sem3-v5/vdp2',file:'P1_MATHS_N3_SEM3_VDP2_V5'},
 'n3-sem3-vdp1-v6': {folder:'n3-sem3-v6/vdp1',file:'P1_MATHS_N3_SEM3_VDP1_V6'},
 'n3-sem3-vdp1-v5': {folder:'n3-sem3-v5/vdp1',file:'P1_MATHS_N3_SEM3_VDP1_V5'},
 'n1-sem3-vdp1-v5': {folder:'n1-sem3-vdp1-v5',file:'P1_MATHS_N1_SEM3_VDP1_V5'},
 'n1-sem3-vdp1-v4': {folder:'n1-sem3-vdp1-v4',file:'P1_MATHS_N1_SEM3_VDP1_V4'},
 'n1-sem3-vdp1-v3': {folder:'n1-sem3-vdp1-v3',file:'P1_MATHS_N1_SEM3_VDP1_V3'},
 'n1-sem3-vdp1-v2': {folder:'n1-sem3-vdp1-v2',file:'P1_MATHS_N1_SEM3_VDP1_V2'},
 'n3-sem4-vdp2-v2': {folder:'n3-sem4-v2/vdp2',file:'P1_MATHS_N3_SEM4_VDP2_V2'},
 'n3-sem4-vdp1': {folder:'n3-sem4/vdp1',file:'P1_MATHS_N3_SEM4_VDP1'},
 'n3-sem4-vdp2': {folder:'n3-sem4/vdp2',file:'P1_MATHS_N3_SEM4_VDP2'},
 'n1-sem3-vdp1': {folder:'n1-sem3-vdp1',file:'P1_MATHS_N1_SEM3_VDP1'},
 'n2-sem1-vdp3': {folder:'n2-sem1/vdp3',file:'P1_MATHS_N2_SEM1_VDP3'},
 'n2-sem1-vdp4': {folder:'n2-sem1/vdp4',file:'P1_MATHS_N2_SEM1_VDP4'},
 'n3-sem3-vdp1-v4': {folder:'n3-sem3-v4/vdp1',file:'P1_MATHS_N3_SEM3_VDP1_V4'},
 'n3-sem3-vdp2-v4': {folder:'n3-sem3-v4/vdp2',file:'P1_MATHS_N3_SEM3_VDP2_V4'},
 'n3-sem3-vdp3-v4': {folder:'n3-sem3-v4/vdp3',file:'P1_MATHS_N3_SEM3_VDP3_V4'},
 'n3-sem3-vdp4-v4': {folder:'n3-sem3-v4/vdp4',file:'P1_MATHS_N3_SEM3_VDP4_V4'},
 'n3-sem3-vdp1-v3': {folder:'n3-sem3-v3/vdp1',file:'P1_MATHS_N3_SEM3_VDP1_V3'},
 'n3-sem3-vdp2-v3': {folder:'n3-sem3-v3/vdp2',file:'P1_MATHS_N3_SEM3_VDP2_V3'},
 'n3-sem3-vdp3-v3': {folder:'n3-sem3-v3/vdp3',file:'P1_MATHS_N3_SEM3_VDP3_V3'},
 'n3-sem3-vdp4-v3': {folder:'n3-sem3-v3/vdp4',file:'P1_MATHS_N3_SEM3_VDP4_V3'},
 'n3-sem3-vdp1-v2': {folder:'n3-sem3-v2/vdp1',file:'P1_MATHS_N3_SEM3_VDP1_V2'},
 'n3-sem3-vdp2-v2': {folder:'n3-sem3-v2/vdp2',file:'P1_MATHS_N3_SEM3_VDP2_V2'},
 'n3-sem3-vdp3-v2': {folder:'n3-sem3-v2/vdp3',file:'P1_MATHS_N3_SEM3_VDP3_V2'},
 'n3-sem3-vdp4-v2': {folder:'n3-sem3-v2/vdp4',file:'P1_MATHS_N3_SEM3_VDP4_V2'},
 'n3-sem3-vdp1': {folder:'n3-sem3/vdp1',file:'P1_MATHS_N3_SEM3_VDP1'},
 'n3-sem3-vdp2': {folder:'n3-sem3/vdp2',file:'P1_MATHS_N3_SEM3_VDP2'},
 'n3-sem3-vdp3': {folder:'n3-sem3/vdp3',file:'P1_MATHS_N3_SEM3_VDP3'},
 'n3-sem3-vdp4': {folder:'n3-sem3/vdp4',file:'P1_MATHS_N3_SEM3_VDP4'},
 'signed-addition': {folder:'n1-sem2-vdp2', file:'P1_MATHS_N1_SEM2_VDP2'},
 'n1-sem2-vdp3': {folder:'n1-sem2-vdp3', file:'P1_MATHS_N1_SEM2_VDP3'},
 'n1-sem2-vdp4': {folder:'n1-sem2-vdp4', file:'P1_MATHS_N1_SEM2_VDP4'},
 'like-terms': {folder:'n2-sem2-vdp2', file:'P1_MATHS_N2_SEM2_VDP2'},
 'factorization-v2': {folder:'n3-sem2-vdp2-2026-11-10', file:'P1_MATHS_N3_SEM2_VDP2'},
 'factorization-review': {folder:'n3-sem2-vdp2-2026-11-12', file:'P1_MATHS_N3_SEM2_VDP2'},
 'fractions-v2': {folder:'n3-sem2-vdp3-2026-11-10', file:'P1_MATHS_N3_SEM2_VDP3'},
 'fractions-review': {folder:'n3-sem2-vdp3-2026-11-12', file:'P1_MATHS_N3_SEM2_VDP3'},
 'polynomial-subtraction': {folder:'n2-sem2-vm4', file:'P1_MATHS_N2_SEM2_VM4'},
};
type Lesson = keyof typeof lessons;
const deliveryEntry = z.object({
 cell: z.string().regex(/^[A-Z]{1,3}[1-9]\d*$/),
 version: z.number().int().positive(),
 gid: z.string().regex(/^\d+$/).optional(),
 linkVersion: z.number().int().positive().optional(),
}).strict();

async function main(){
const args=process.argv.slice(2);
const selected=args.filter(x=>!x.startsWith('--')).flatMap(x=>x==='week-four'?weekFour:x==='week-one'?weekOne:x==='week-three-v4'?weekThreeV4:x==='week-three-v3'?weekThreeV3:x==='week-three-v2'?weekThreeV2:x==='week-three'?weekThree:[x]);
if(selected.some(x=>!Object.hasOwn(lessons,x)))throw Error('Unknown lesson in batch');
const stills=args.includes('--stills');
const proof=args.includes('--math-proof');
const keyFrames=args.includes('--key-frames');
const deliveryArgs=args.filter(arg=>arg.startsWith('--google-publish'));
let deliveries: Record<string,z.infer<typeof deliveryEntry>> | undefined;
if(deliveryArgs.length){
 const manifest=deliveryArgs[0].match(/^--google-publish=(.+)$/)?.[1];
 if(!manifest||deliveryArgs.length!==1||!selected.length||stills){
  throw Error('Use --google-publish=PATH with explicit video lessons and without --stills');
 }
 deliveries=z.record(z.string(),deliveryEntry).parse(JSON.parse(await readFile(manifest,'utf8')));
 for(const stem of selected as Lesson[]){
  if(!deliveries[stem]||!lessons[stem].file.includes('_VDP')){
   throw Error('Missing Google delivery entry for VDP '+stem);
  }
  const entry=deliveries[stem];
  if(entry.version>1&&(!entry.linkVersion||entry.linkVersion>entry.version)){
   throw Error('Provide the existing Google linkVersion for revised VDP '+stem);
  }
 }
}
const serveUrl=await bundle({entryPoint:path.resolve('src/video/index.ts')});
for(const stem of (selected.length?selected:Object.keys(lessons).filter(stem=>!stem.endsWith('-review')&&stem!=='signed-addition'&&!stem.startsWith('n3-sem3-')&&!stem.startsWith('n1-sem2-')&&!stem.startsWith('n2-sem1-')&&!stem.startsWith('n1-sem3-')&&!stem.startsWith('n3-sem4-'))) as Lesson[]){
 const {folder,file}=lessons[stem];
 const out=path.join('outputs',folder);
 await mkdir(out,{recursive:true});
 const timeline=timelineSchema.parse(JSON.parse(await readFile(`src/video/${stem}-lesson.json`,'utf8')));
 const inputProps={timeline};
 const composition=await selectComposition({serveUrl,id:'DigitalLab',inputProps});
 const options={serveUrl,composition,inputProps};
 const checkpoints:{name:string;frame:number}[]=[];
 let offset=0;
 for(const s of timeline.scenes){
  const add=(name:string,frame:number)=>checkpoints.push({name,frame:offset+Math.min(s.durationInFrames-1,frame)});
  add(s.id,s.durationInFrames-15);
  if('kind' in s&&'beats' in s){
   const at=(i:number)=>s.beats[i].from;
   if(s.type==='monomial-study'){
    for(const [i,beat] of s.beats.entries()){
     const end=s.beats[i+1]?.from??s.durationInFrames;
     add(s.id+'-stage-'+i,Math.max(beat.from,end-12));
    }
   }
   if(s.kind==='intro'){
    add('objective-centred',0);
    add('objective-moving',Math.max(15,at(1)-36)+16);
    const last=Math.min(s.beats.length-1,s.type==='like-terms'?2:3);
    for(let i=1;i<=last;i++)add('objective-link-'+i,(i+1<s.beats.length&&!(s.type==='like-terms'&&i===2)?at(i+1):s.durationInFrames)-18);
   }
   if(s.type==='vdp-sequence'){
    if(stem==='n1-sem2-vdp4-v2'&&s.id==='vdp4-opposes')for(let i=0;i<s.beats.length;i++)add('sign-correction-step-'+i,at(i)+25);
    if(s.pronunciation?.style==='simplifier'){
     for(let i=1;i<s.beats.length-1;i++){
      add(s.id+'-before-syllable-'+i,at(i)-1);
      add(s.id+'-syllable-'+i,at(i)+13);
     }
     add(s.id+'-separator-fade',at(s.beats.length-1)-8);
     add(s.id+'-joining',at(s.beats.length-1)+3);
     add(s.id+'-joined',at(s.beats.length-1)+20);
    }
    if(stem.startsWith('n3-sem4-')){
     for(const [index,item] of s.art.entries()){
      if(item.frame!==undefined){
       add(s.id+'-before-reveal-'+index,item.frame-1);
       add(s.id+'-reveal-'+index,item.frame+18);
      }
     }
    }
    if(stem==='n1-sem2-vdp4-v2'||stem.endsWith('-v4')||/^n3-sem3-vdp1-v[56]$/.test(stem)||/^n3-sem3-vdp[234]-v[567]$/.test(stem)){
     for(const [index,item] of s.art.entries()){
      const name='revision-'+s.id+'-'+index;
      if(item.frame!==undefined){
       if(/^n3-sem3-vdp1-v[56]$/.test(stem)||/^n3-sem3-vdp[234]-v[567]$/.test(stem))add(name+'-before',Math.max(0,item.frame-1));
       add(name,item.frame+20);
      }
      if(item.kind==='status')add(name+'-faux',at(item.at)+18);
      if(item.pulseFrame!==undefined)add(name+'-voix',item.pulseFrame+13);
      if(item.repeatPulse)add(name+'-repeated',at(item.pulse??item.at)+60);
      if(/^n3-sem3-vdp[34]-v[567]$/.test(stem)&&item.toFrame!==undefined)add(name+'-before-fade',item.toFrame-1);
      for(const pulse of item.setPulses??[])add(name+'-pulse-'+pulse.target,pulse.frame+13);
      for(const f of item.focus??[])add(name+'-'+f.target,f.start+18);
     }
    }
    if(stem.startsWith('n2-sem1-')){
     for(const item of s.art){
      for(const token of item.tokenMarks??[]){
       add(s.id+'-exponent-'+token.index+'-before',at(token.at)-1);
       add(s.id+'-exponent-'+token.index,at(token.at)+18);
      }
     }
    }
    for(const item of s.art){
     if(item.kind==='clip'&&item.frame!==undefined&&item.clipFrames){
      for(const [index,part] of [.26,.43,.53,.76].entries()){
       add(s.id+'-clip-'+index,item.frame+Math.floor(item.clipFrames*part));
      }
     }
    }
    if(s.objective){
     for(const [index,link] of s.objective.links.entries()){
      const upcoming=s.objective.links[index+1];
      add('vdp-link-'+(index+1),Math.min(at(link.at)+68,(upcoming?at(upcoming.at):s.durationInFrames)-15));
     }
    }else{
     for(let i=0;i<s.beats.length-1;i++){
      add(s.id+'-step-'+i,at(i)+Math.floor((at(i+1)-at(i))*.63));
     }
    }
   }
   if(s.type==='signed-addition'){
    for(let i=1;i<s.beats.length;i++){
     const next=s.beats[i+1]?.from??s.durationInFrames;
     add(s.id+'-slide-'+s.sourceSlides[i],at(i)+Math.floor((next-at(i))*.75));
    }
    for(const name of ['commonPlus','commonMinus','largePlus','keepPlus','largeMinus','keepMinus','triangle','difference','zero']){
     if(s.cues[name]!==undefined)add(s.id+'-'+name,s.cues[name]+12);
    }
   }
   if(s.kind==='pronunciation')add(s.type==='vdp-sequence'?s.id+'-syllables':'syllables',at(s.beats.length-2)+15);
   if(s.type==='like-terms'&&s.kind==='comparison')add(s.id+'-exponents',at(4)+25);
   if(s.type==='like-terms'&&s.kind==='synthesis')for(let i=2;i<=4;i++)add('recap-'+(i-1),at(i)-12);
   if(s.type==='factorization'&&s.kind==='theorem')add('factorization-pending',s.cues.factor1+22);
   if(s.type==='factorization'&&s.revision==='2026-11-12'){
    if(s.kind==='intro'){
     add('before-red-link-fade',s.cues.redEnd-12);
     add('red-link-cleared',s.cues.redEnd);
     add('before-green-link-fade',s.cues.greenEnd-12);
     add('green-link-cleared',s.cues.greenEnd);
    }
    if(s.kind==='theorem'||s.kind==='example'){
     for(let i=0;i<(s.kind==='theorem'?3:2);i++){
      add(s.id+'-before-base-'+i,s.cues['emphasis'+i]-1);
      add(s.id+'-red-base-'+i,s.cues['emphasis'+i]);
     }
    }
    if(s.kind==='pronunciation'){
     for(let i=1;i<=5;i++)add('syllable-'+i,at(i)+13);
     add('joined-word',at(6)+18);
    }
   }
   if(s.type==='fractions'&&s.kind==='common')add('ppcm-minimum',at(5)-15);
   if(s.type==='fractions'&&s.kind==='reducible')add('division-by-6',at(5)-15);
   if(s.type==='fractions'&&s.revision==='2026-11-12'){
    if(s.kind==='intro')add('objective-handoff',at(2));
    if(s.kind==='irreducible'||s.kind==='reducible')add(s.id+'-question',s.cues.question+7);
    if(s.kind==='irreducible'){
     add('numerator-pulse',s.cues.numerator+7);
     add('denominator-pulse',s.cues.denominator+7);
    }
    if(s.kind==='reducible')add('division-by-3',s.cues.division3+20);
    if(s.kind==='definition'||s.kind==='property'||s.kind==='denominator'){
     const line=Object.values(s.reveals??{})[0];
     add(s.id+'-word-reveal',line[1].from);
    }
    if(s.kind==='vocabulary'){
     add('before-first-fraction',s.cues.vocabularyOne-1);
     add('first-fraction',s.cues.vocabularyOne);
     add('before-denominator-ring',s.cues.denominator-1);
     add('denominator-ring',s.cues.denominator);
     add('before-second-fraction',s.cues.vocabularyTwo-1);
     add('second-fraction',s.cues.vocabularyTwo);
    }
   }
   if(s.type==='polynomial-subtraction'&&s.kind==='vertical'){
    add('column-x',at(4)-15);
    add('column-y',at(6)-15);
   }
   if(s.type==='polynomial-subtraction'&&s.kind==='horizontal')add('horizontal-grouped',at(8)-14);
  }
  offset+=s.durationInFrames;
 }
 await writeFile(path.join(out,'timeline.json'),JSON.stringify(timeline,null,2));
 await writeFile(path.join(out,'review-frames.json'),JSON.stringify(checkpoints,null,2));
 console.log(stem,composition.durationInFrames,'frames');
 if(stills){
  for(const {name,frame} of checkpoints.filter(item=>{
   if(proof&&stem==='n1-sem2-vdp4-v2')return ['sign-correction-step-0','sign-correction-step-4','sign-correction-step-5'].includes(item.name);
   if(proof&&stem==='n3-sem3-vdp4-v7')return ['revision-vdp4-rationnel-decimal-0-before-fade','revision-vdp4-rationnel-decimal-1'].includes(item.name);
   if(proof&&stem==='n3-sem3-vdp4-v6')return /^revision-vdp4-droite-propriete-\d+$/.test(item.name)||['vdp4-droite-propriete','vdp4-prononciation-5-syllable-3','vdp4-prononciation-5-syllable-4','vdp4-prononciation-5-joined'].includes(item.name);
   if(proof&&stem==='n3-sem3-vdp4-v5'&&args.includes('--anchors-only'))return /^revision-vdp4-irrationnel-(?:pi|racine)-[12]$/.test(item.name);
   if(proof&&stem==='n3-sem3-vdp4-v5')return item.name.startsWith('revision-')&&!item.name.endsWith('-before')||['vdp4-rationnels','vdp4-reels','vdp4-droite-propriete','vdp4-droite-exemple','vdp4-entiers','vdp4-vocabulaire','vdp4-prononciation-5-joined','vdp4-prononciation-6-joined','vdp4-irrationnels','vdp4-rationnel-periodique'].includes(item.name);
   if(proof&&/^n3-sem3-vdp3-v[56]$/.test(stem))return ['revision-vdp3-fraction-225-1','revision-vdp3-fraction-225-2','revision-vdp3-fraction-1-1','revision-vdp3-fraction-moins-5-1','vdp3-fraction-225','vdp3-fraction-1','vdp3-fraction-moins-5'].includes(item.name);
   if(proof&&stem==='n3-sem3-vdp1-v6')return item.name==='vdp1-definition'||/^revision-vdp1-definition-[234](?:-before)?$/.test(item.name);
   if(proof&&stem==='n1-sem3-vdp1')return item.name.endsWith('-trois-termes-step-4')||item.name.endsWith('-signes-operation-step-1');
   if(proof&&(stem.endsWith('-v4')||stem==='n3-sem3-vdp1-v5'))return item.name.startsWith('revision-')||item.name==='vdp-link-1';
   if(keyFrames)return !item.name.includes('-step-')&&!item.name.startsWith('objective-link-');
   return !proof||['termes-semblables-exponents','column-y','synthese'].includes(item.name);
  }))
   await renderStill({...options,frame,output:path.join(out,name+'.png')});
 }else{
  let last=-1;
  await renderMedia({...options,codec:'h264',pixelFormat:'yuv420p',crf:18,concurrency:4,
   outputLocation:path.join(out,file+'.mp4'),onProgress:({progress})=>{
    const pct=Math.floor(progress*100/10)*10;
    if(pct!==last){console.log(stem,pct+'%');last=pct;}
   }});
  console.log('Rendered',file+'.mp4');
  const delivery=deliveries?.[stem];
  if(delivery){
   const deliveryArgs=['scripts/google_vdp.py',delivery.version>1?'revise':'deliver','--cell',delivery.cell,
    '--version',String(delivery.version),'--mp4',path.join(out,file+'.mp4')];
   if(delivery.gid)deliveryArgs.push('--gid',delivery.gid);
   if(delivery.version>1&&delivery.linkVersion)deliveryArgs.push('--link-version',String(delivery.linkVersion));
   execFileSync(process.env.DIGITAL_LAB_PYTHON||'python',deliveryArgs,{stdio:'inherit'});
  }
 }
}
}
main().catch(error=>{console.error(error);process.exitCode=1;});

