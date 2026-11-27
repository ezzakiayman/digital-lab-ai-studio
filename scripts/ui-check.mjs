// Uses the renderer's installed headless browser for local DOM smoke checks.
import {openBrowser} from '@remotion/renderer';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
const server=spawn(process.execPath,['node_modules/next/dist/bin/next','start','--hostname','127.0.0.1','--port','3210'],{stdio:'ignore',windowsHide:true});
for(let i=0;i<40;i++){try{if((await fetch('http://127.0.0.1:3210')).ok)break;}catch{}await new Promise(r=>setTimeout(r,250));}
const browser=await openBrowser('chrome');
try{
 const page=await browser.newPage({context:()=>null,logLevel:'error',indent:false,pageIndex:0,onBrowserLog:null,onLog:()=>{}});
 await page.setViewport({width:1500,height:1100,deviceScaleFactor:1});
 await page.goto({url:'http://127.0.0.1:3210',timeout:30000});
 await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,1500));});
 const result=await page.evaluate(()=>({title:document.querySelector('h1')?.textContent,editor:!!document.querySelector('textarea'),svg:!!document.querySelector('svg'),overflow:document.documentElement.scrollWidth>innerWidth}));
 assert.equal(result.title,'Atelier vidéo');assert.equal(result.editor,true);assert.equal(result.svg,true);assert.equal(result.overflow,false);
 console.log('Desktop studio DOM checks passed',result);
 await page.evaluate(()=>{const s=document.querySelector('select');s.value='example';s.dispatchEvent(new Event('change',{bubbles:true}));});
 await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,300));});
 const example=await page.evaluate(()=>({json:JSON.parse(document.querySelector('textarea').value),text:document.querySelector('svg')?.textContent}));
 assert.equal(example.json.scenes[0].type,'negative-comparison');assert.match(example.text,/Exemple 1/);
 console.log('Example selection updates JSON and live SVG preview');
 await page.evaluate(()=>{const s=document.querySelector('select');s.value='full';s.dispatchEvent(new Event('change',{bubbles:true}));});
 await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,300));});
 const full=await page.evaluate(()=>({json:JSON.parse(document.querySelector('textarea').value),clips:document.querySelectorAll('.clip').length}));
 assert.equal(full.clips,8);assert.equal(full.json.scenes.reduce((n,s)=>n+s.durationInFrames,0),5400);
 console.log('Full lesson selector loads eight scenes and 180 seconds');
 await page.evaluate(()=>{const s=document.querySelector('select');s.value='n3';s.dispatchEvent(new Event('change',{bubbles:true}));});
 await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,300));});
 const n3=await page.evaluate(()=>({json:JSON.parse(document.querySelector('textarea').value),clips:document.querySelectorAll('.clip').length,text:document.querySelector('svg')?.textContent}));
 assert.equal(n3.clips,15);assert.equal(n3.json.level,'3AC');assert.equal(n3.json.scenes[0].type,'ppcm');assert.match(n3.text,/multiple commun/);
 console.log('PPCM selector loads fifteen Gemini-narrated scenes and live preview');
 const objective=await page.evaluate(()=>[...document.querySelectorAll('[data-objective-title]')].map(t=>({size:getComputedStyle(t).fontSize,weight:getComputedStyle(t).fontWeight,font:getComputedStyle(t).fontFamily,forcedWidth:t.hasAttribute('textLength')||t.hasAttribute('lengthAdjust'),x:t.getBBox().x,right:t.getBBox().x+t.getBBox().width,width:t.getComputedTextLength()})));
 assert.equal(objective.length,3);
 for(const t of objective){assert.equal(t.size,'72px');assert.equal(t.weight,'700');assert.match(t.font,/Arial/);assert.equal(t.forcedWidth,false);assert.ok(t.x>=310&&t.right<=1800);}
 assert.ok(objective[0].right<objective[1].x);
 assert.ok(objective[2].x>511&&objective[2].right<1730);
 console.log('Objective title uses uniform 72px Arial bold with natural glyph proportions and clear connectors',objective.map(({size,width})=>({size,width})));
 for(const index of [1,5,9,11]){
  await page.evaluate(i=>document.querySelectorAll('.clip')[i].click(),index);
  await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,250));});
  const box=await page.evaluate(()=>{const r=document.querySelector('rect[data-content-box]');return r?{stroke:r.getAttribute('stroke'),fill:r.getAttribute('fill')}:null;});
  assert.deepEqual(box,{stroke:'#0DBBA1',fill:'#FFFFFF'});
 }
 await page.evaluate(()=>document.querySelectorAll('.clip')[2].click());
 await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,250));});
 const letters=await page.evaluate(()=>[...document.querySelectorAll('[data-acronym-letter]')].map(g=>({letter:g.querySelector('text').textContent,x:g.querySelector('text').getAttribute('x'),shaft:g.querySelector('path').getAttribute('d')})));
 assert.deepEqual(letters.map(l=>l.letter),['P','P','C','M']);
 for(const l of letters)assert.ok(l.shaft.startsWith(`M${l.x} `));
 console.log('Definition/property/verification/synthesis share the charter; acronym arrows start at their actual letters');
 await page.evaluate(()=>{const s=document.querySelector('select');s.value='primes';s.dispatchEvent(new Event('change',{bubbles:true}));});
 await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,300));});
 const primes=await page.evaluate(()=>({json:JSON.parse(document.querySelector('textarea').value),clips:document.querySelectorAll('.clip').length,letters:[...document.querySelectorAll('[data-objective-title]')].map(t=>({size:getComputedStyle(t).fontSize,forced:t.hasAttribute('textLength')})),arrows:[...document.querySelectorAll('[data-link-index]')].map(g=>{const paths=g.querySelectorAll('path'),shaft=paths[1],head=paths[2],end=shaft.getPointAtLength(shaft.getTotalLength()),tip=head.getPointAtLength(head.getTotalLength()/2);return Math.hypot(end.x-tip.x,end.y-tip.y);})}));
 assert.equal(primes.clips,11);assert.equal(primes.json.scenes[0].type,'primes');
 assert.deepEqual(primes.letters,Array.from({length:3},()=>({size:'72px',forced:false})));
 for(const gap of primes.arrows)assert.ok(gap<0.1,'Objective arrowhead is detached from its shaft');
 const layout=await page.evaluate(()=>{
  const title=[...document.querySelectorAll('[data-section="declaration-of-objective"] text')].filter(t=>t.getAttribute('font-size')==='72');
  const baselines=[...new Set(title.map(t=>Number(t.getAttribute('y'))))];
  const left=Math.min(...title.map(t=>t.getBBox().x)),right=Math.max(...title.map(t=>t.getBBox().x+t.getBBox().width));
  const card=document.querySelector('[data-objective-banner]'),icon=document.querySelector('[data-objective-target]');
  const cardX=Number(card.getAttribute('x')),cardRight=cardX+Number(card.getAttribute('width'));
  const iconX=Number(icon.getAttribute('x')),iconRight=iconX+Number(icon.getAttribute('width'));
  const boxes=title.map(t=>t.getBBox());let collisions=0;
  const columns=[...document.querySelectorAll('[data-link-index]')].map(g=>{
   const path=g.querySelectorAll('path')[1],length=path.getTotalLength();
   for(let n=0;n<=200;n++){const q=path.getPointAtLength(length*n/200);if(boxes.some(b=>q.x>b.x-2&&q.x<b.x+b.width+2&&q.y>b.y-2&&q.y<b.y+b.height+2))collisions++;}
   return path.getPointAtLength(length).x;
  });
  return {baselines,left,right,columns,collisions,leftPadding:iconX-cardX,rightPadding:cardRight-right,iconGap:left-iconRight,cardHeight:Number(card.getAttribute('height'))};
 });
 assert.deepEqual(layout.baselines,[285]);assert.equal(layout.left,220);assert.ok(layout.right<1880);
 assert.ok(Math.abs(layout.leftPadding-layout.rightPadding)<5);assert.ok(layout.iconGap>=24);assert.equal(layout.cardHeight,220);
 assert.deepEqual(layout.columns,[480,960,1440]);assert.equal(layout.collisions,0);
 console.log('Single-line objective fits naturally; icon/text padding is balanced; explanation columns and connectors pass',layout);
 for(let i=0;i<primes.clips;i++){
  await page.evaluate(index=>document.querySelectorAll('.clip')[index].click(),i);
  await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,150));});
  const visual=await page.evaluate(()=>({text:document.querySelector('svg')?.textContent,outside:[...document.querySelectorAll('svg text')].filter(t=>{const b=t.getBBox();return b.x<50||b.x+b.width>1875||b.y<45||b.y+b.height>1040;}).map(t=>t.textContent),box:document.querySelector('rect[data-content-box]')?.getAttribute('stroke'),numbers:[...document.querySelectorAll('[data-prime-number]')].map(g=>Number(g.getAttribute('data-prime-number'))),question:(()=>{const i=document.querySelector('[data-question-mark] img');return i?{src:i.getAttribute('src'),width:i.naturalWidth,height:i.naturalHeight,loaded:i.complete}:null;})()}));
  assert.deepEqual(visual.outside,[],'Prime scene text overflows: '+i);
  assert.doesNotMatch(visual.text,/Animer|Afficher le|Insérer le|synchronisation|voix off|Bonjour|Aujourd’hui|Je commence|Je prends|Je passe|Quels sont|Voici tous/i);
  const kind=primes.json.scenes[i].kind;
  if(kind==='question'){assert.ok(visual.question?.loaded);assert.equal(visual.question.width,1254);assert.equal(visual.question.height,1254);assert.ok(visual.question.src.endsWith('/brand/question-mark.png'));assert.doesNotMatch(visual.text,/\?/);}
  if(kind==='definition')assert.doesNotMatch(visual.text,/Uniquement 1 et lui-même/);
  if(kind==='divisors')assert.doesNotMatch(visual.text,/Exactement deux diviseurs|Quatre diviseurs positifs/);
  if(kind==='one')assert.doesNotMatch(visual.text,/Il faut exactement/);
  if(kind==='prime-ranges')assert.doesNotMatch(visual.text,/Entre \d|Inférieurs à 10\b/);
  if(kind==='all-primes')assert.doesNotMatch(visual.text,/apprendre par cœur|25 nombres/);
  if(kind==='vocabulary')assert.doesNotMatch(visual.text,/Exactement deux diviseurs/);
  if(i>0)assert.equal(visual.box,'#0DBBA1');
  if(primes.json.scenes[i].kind==='all-primes')assert.deepEqual(visual.numbers,[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]);
 }
 console.log('Prime lesson: eleven scenes, uniform objective type, attached arrowheads, complete 25-prime table, common frames and text bounds passed');
 console.log('Narration-only/director text excluded; approved 1254×1254 question artwork loads in the live preview');
 for(const selection of ['primes-v2','primes-review']){
 await page.evaluate(value=>{
  const select=document.querySelector('select');
  select.value=value;
  select.dispatchEvent(new Event('change',{bubbles:true}));
 },selection);
 await page.evaluate(()=>new Promise(resolve=>setTimeout(resolve,250)));
 const revisedPrimes=await page.evaluate(()=>{
  const title=document.querySelector('[data-objective-title]');
  const links=[...document.querySelectorAll('[data-link-index]')].map(group=>{
   const [underline,shaft,head]=group.querySelectorAll('path');
   const a=underline.getPointAtLength(0),b=underline.getPointAtLength(underline.getTotalLength());
   const start=shaft.getPointAtLength(0),end=shaft.getPointAtLength(shaft.getTotalLength());
   const tip=head.getPointAtLength(head.getTotalLength()/2);
   const label=group.querySelector('[data-objective-explanation-center]')?.getAttribute('data-objective-explanation-center')
    ??group.querySelector('text').getAttribute('x');
   return Math.abs(start.x-end.x)<.1&&Math.abs((a.x+b.x)/2-start.x)<.1
    &&Math.abs(start.y-a.y)<.1&&Math.hypot(end.x-tip.x,end.y-tip.y)<.1&&+label===end.x;
  });
  return {
   scenes:JSON.parse(document.querySelector('textarea').value).scenes,
   title:title.textContent.trim(),color:title.getAttribute('fill'),right:title.getBBox().x+title.getBBox().width,
   motion:document.querySelector('[data-objective-entrance]').getAttribute('transform'),links,
  };
 });
 assert.equal(revisedPrimes.scenes.length,11);
 assert.deepEqual(revisedPrimes.scenes.flatMap(scene=>scene.sourceSlides),Array.from({length:32},(_,index)=>index+1));
 assert.ok(revisedPrimes.scenes.slice(1).every(scene=>scene.audio.startsWith('primes-v2-paced/')));
 assert.equal(revisedPrimes.scenes[0].audio,selection==='primes-review'?'primes-review-2026-11-12/objectif.wav':'primes-v2-paced/objectif.wav');
 assert.equal(revisedPrimes.title,'Reconnaître et vérifier si un nombre est premier');
 assert.equal(revisedPrimes.color,'#263956');
 assert.ok(revisedPrimes.right<1860);
 assert.match(revisedPrimes.motion,/280/);
 assert.deepEqual(revisedPrimes.links,[true,true,true]);
 for(let i=1;i<revisedPrimes.scenes.length;i++){
  await page.evaluate(index=>document.querySelectorAll('.clip')[index].click(),i);
  await page.evaluate(()=>new Promise(resolve=>setTimeout(resolve,100)));
  const result=await page.evaluate(()=>{
   const svg=document.querySelector('svg');
   return {
    text:svg.textContent,
    outOfBounds:[...svg.querySelectorAll('text')].filter(t=>{
     const b=t.getBBox();
     return b.x<50||b.x+b.width>1875||b.y<45||b.y+b.height>1040;
    }).map(t=>t.textContent),
    headings:[...svg.querySelectorAll('[data-section-header], [data-box-heading]')].map(g=>g.textContent),
    count:svg.querySelectorAll('[data-prime-number]').length,
    question:svg.querySelector('[data-question-mark] img')?.getAttribute('src'),
    syllables:[...svg.querySelectorAll('[data-syllable]')].map(g=>g.dataset.syllable),
   };
  });
  assert.deepEqual(result.outOfBounds,[],'Revised prime scene text bounds '+i);
  assert.doesNotMatch(result.text,/Animer|Afficher le|Insérer le|voix off|Bonjour|Aujourd’hui|Quels sont|Prononciation|preu-mié/i);
  assert.ok(result.headings.length>0&&result.headings.every(label=>label.endsWith(' :')));
  const kind=revisedPrimes.scenes[i].kind;
  if(kind==='question')assert.ok(result.question?.endsWith('/brand/question-mark.png'));
  if(kind==='all-primes')assert.equal(result.count,25);
  if(kind==='pronunciation')assert.deepEqual(result.syllables,['pre','mier']);
 }
 console.log(selection+': all 32 source slides, three straight attached arrows, navy title, colon headings, approved question artwork and pronunciation passed');
 }
 await page.evaluate(()=>{const s=document.querySelector('select');s.value='fractions';s.dispatchEvent(new Event('change',{bubbles:true}));});
 await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,300));});
 const fractions=await page.evaluate(()=>({json:JSON.parse(document.querySelector('textarea').value),clips:document.querySelectorAll('.clip').length,title:[...document.querySelectorAll('[data-objective-title]')].map(t=>({x:Number(t.getAttribute('x')),y:Number(t.getAttribute('y')),size:getComputedStyle(t).fontSize,font:getComputedStyle(t).fontFamily,right:t.getBBox().x+t.getBBox().width,forced:t.hasAttribute('textLength')})),arrows:[...document.querySelectorAll('[data-objective-connector]')].map(t=>t.getAttribute('d'))}));
 assert.equal(fractions.clips,9);assert.equal(fractions.json.scenes[0].type,'fractions');
 for(const t of fractions.title){assert.equal(t.size,'72px');assert.match(t.font,/Arial/);assert.ok(t.right<1800);assert.equal(t.forced,false);}
 assert.equal(fractions.title[0].x,fractions.title[2].x);assert.equal(fractions.arrows.length,2);
 const connectorCheck=await page.evaluate(()=>{let collisions=0,detached=0;const bounds=[...document.querySelectorAll('[data-objective-title]')].map(t=>t.getBBox());for(const g of document.querySelectorAll('[data-link-index]')){const paths=g.querySelectorAll('path'),shaft=paths[1],head=paths[2],n=shaft.getTotalLength(),end=shaft.getPointAtLength(n),tip=head.getPointAtLength(head.getTotalLength()/2);if(Math.hypot(end.x-tip.x,end.y-tip.y)>.1)detached++;for(let i=0;i<=300;i++){const q=shaft.getPointAtLength(n*i/300);if(bounds.some(b=>q.x>b.x-2&&q.x<b.x+b.width+2&&q.y>b.y-2&&q.y<b.y+b.height+2))collisions++;}}return {collisions,detached};});
 assert.deepEqual(connectorCheck,{collisions:0,detached:0});
 for(let i=0;i<fractions.clips;i++){
  await page.evaluate(index=>document.querySelectorAll('.clip')[index].click(),i);
  await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,120));});
  const content=await page.evaluate(()=>({text:document.querySelector('svg').textContent,box:document.querySelector('[data-content-box]')?.getAttribute('stroke'),outside:[...document.querySelectorAll('svg text')].filter(t=>{const b=t.getBBox();return b.x<50||b.x+b.width>1875||b.y<45||b.y+b.height>1040;}).map(t=>t.textContent),question:!!document.querySelector('[data-question-mark] img')?.complete}));
  assert.deepEqual(content.outside,[],'Fraction scene bounds '+i);
  assert.doesNotMatch(content.text,/Bonjour|Aujourd’hui|Je prends|Je retiens|Afficher|Animer|voix off|synchronisation|Est-ce que|Pourquoi/);
  if(i>0)assert.equal(content.box,'#0DBBA1');
  if([1,2].includes(i)){assert.equal(content.question,true);assert.doesNotMatch(content.text,/\?/);}
 }
 console.log('Fractions: nine scenes, uniform 72px wrapped objective, attached clear arrows, main-area-only text, original question assets, all SVG text bounds passed');
 await page.evaluate(()=>{const s=document.querySelector('select');s.value='polynomials';s.dispatchEvent(new Event('change',{bubbles:true}));});
 await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,300));});
 const algebra=await page.evaluate(()=>({json:JSON.parse(document.querySelector('textarea').value),clips:document.querySelectorAll('.clip').length,transform:document.querySelector('[data-objective-entrance]').getAttribute('transform'),fonts:[...document.querySelectorAll('[data-objective-title]')].map(t=>getComputedStyle(t).fontSize)}));
 assert.equal(algebra.clips,13);assert.equal(algebra.json.level,'2AC');assert.match(algebra.transform,/275/);assert.ok(algebra.fonts.every(s=>s==='72px'));
 for(const s of algebra.json.scenes)assert.ok(s.audio.startsWith('polynomials-paced/'));
 for(let i=0;i<algebra.clips;i++){
  await page.evaluate(index=>document.querySelectorAll('.clip')[index].click(),i);
  await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,120));});
  const r=await page.evaluate(()=>({text:document.querySelector('svg').textContent,headers:[...document.querySelectorAll('[data-section-header] text,[data-box-heading]')].map(t=>t.textContent),outside:[...document.querySelectorAll('svg text')].filter(t=>{const b=t.getBBox();return b.x<40||b.x+b.width>1880||b.y<45||b.y+b.height>1040;}).map(t=>t.textContent),box:document.querySelector('[data-content-box]')?.getAttribute('stroke')}));
  assert.deepEqual(r.outside,[],'Polynomial text bounds '+i);
  for(const header of r.headers)assert.match(header,/ :$/);
  assert.doesNotMatch(r.text,/Bonjour|Aujourd’hui|Je prends|Afficher|Animer|voix off|De combien/);
  if(i>0)assert.equal(r.box,'#0DBBA1');
 }
 console.log('Polynomials: 13 scenes, centred initial objective, uniform 72px type, all headers have colons, bounded central content and restored Google TTS audio paths passed');
 await page.evaluate(()=>{
  const select=document.querySelector('select');
  select.value='polynomials-v2';
  select.dispatchEvent(new Event('change',{bubbles:true}));
 });
 await page.evaluate(()=>new Promise(resolve=>setTimeout(resolve,250)));
 const revised=await page.evaluate(()=>{
  const title=document.querySelector('[data-objective-title]');
  const banner=document.querySelector('[data-objective-banner]');
  const link=document.querySelector('[data-link-index]');
  const [underline,shaft,head]=link.querySelectorAll('path');
  const [underStart,underEnd]=[underline.getPointAtLength(0),underline.getPointAtLength(underline.getTotalLength())];
  const [start,end]=[shaft.getPointAtLength(0),shaft.getPointAtLength(shaft.getTotalLength())];
  const tip=head.getPointAtLength(head.getTotalLength()/2);
  return {
   scenes:JSON.parse(document.querySelector('textarea').value).scenes,
   title:title.textContent.trim(),ink:title.getAttribute('fill'),titleWidth:title.getBBox().width,
   bannerWidth:banner.getBBox().width,transform:document.querySelector('[data-objective-entrance]').getAttribute('transform'),
   straight:Math.abs(start.x-end.x)<.1,
   joins:Math.abs((underStart.x+underEnd.x)/2-start.x)<.1&&Math.abs(underStart.y-start.y)<.1
    &&Math.hypot(tip.x-end.x,tip.y-end.y)<.1&&+link.querySelector('text').getAttribute('x')===end.x,
  };
 });
 assert.equal(revised.scenes.length,16);
 assert.deepEqual(revised.scenes.flatMap(scene=>scene.sourceSlides),Array.from({length:55},(_,index)=>index+1));
 assert.ok(revised.scenes.every(scene=>scene.audio.startsWith('polynomials-v2-paced/')));
 assert.equal(revised.title,'Déterminer le degré d’un polynôme');
 assert.equal(revised.ink,'#263956');
 assert.ok(revised.titleWidth<revised.bannerWidth-220&&revised.straight&&revised.joins);
 assert.match(revised.transform,/280/);
 for(let i=1;i<revised.scenes.length;i++){
  await page.evaluate(index=>document.querySelectorAll('.clip')[index].click(),i);
  await page.evaluate(()=>new Promise(resolve=>setTimeout(resolve,100)));
  const review=await page.evaluate(()=>{
   const svg=document.querySelector('svg');
   return {
    text:svg.textContent, headings:[...svg.querySelectorAll('[data-section-header] text,[data-box-heading]')].map(node=>node.textContent),
    outside:[...svg.querySelectorAll('text')].filter(node=>{
     const box=node.getBBox();
     return box.x<40||box.x+box.width>1880||box.y<45||box.y+box.height>1040;
    }).map(node=>node.textContent),
    math:[...svg.querySelectorAll('[data-math-role]')].map(node=>({
     role:node.dataset.mathRole,text:node.textContent,ink:node.getAttribute('fill'),
     italic:node.getAttribute('font-style')==='italic',y:+node.getAttribute('y'),
    })),
    pronunciation:svg.querySelector('[data-pronunciation-word]')?.dataset.pronunciationWord,
   };
  });
  assert.deepEqual(review.outside,[],'Revised polynomial text bounds '+i);
  assert.doesNotMatch(review.text,/Bonjour|Aujourd’hui|Je prends|Afficher|Animer|voix off|De combien|Prononciation|preu-mié/);
  assert.ok(review.headings.every(label=>label.endsWith(' :')));
  assert.ok(review.math.filter(node=>node.role==='operator').every(node=>node.ink==='#1D1D1D'));
  assert.ok(review.math.every(node=>node.italic===(node.role==='variable')));
  if(revised.scenes[i].id==='exemple-binome'){
   assert.deepEqual(review.math.map(node=>node.text),['5','x','+','3','y','3']);
   assert.ok(review.math[5].y<review.math[4].y);
  }
  if(revised.scenes[i].kind==='pronunciation')assert.match(review.pronunciation,/^(binôme|trinôme|polynôme)$/);
 }
 console.log('Revised polynomials: 55 source slides, 16 scenes, straight attached objective arrow, navy title, neutral operators, raised powers, syllables and text bounds passed');
 await page.evaluate(()=>{const s=document.querySelector('select');s.value='factorization';s.dispatchEvent(new Event('change',{bubbles:true}));});
 await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,250));});
 const factors=await page.evaluate(()=>({json:JSON.parse(document.querySelector('textarea').value),clips:document.querySelectorAll('.clip').length,motion:document.querySelector('[data-objective-entrance]').getAttribute('transform'),titles:[...document.querySelectorAll('[data-objective-title]')].map(t=>({size:getComputedStyle(t).fontSize,forced:t.hasAttribute('textLength')}))}));
 assert.equal(factors.clips,5);assert.equal(factors.json.level,'3AC');assert.match(factors.motion,/275/);assert.ok(factors.titles.every(t=>t.size==='72px'&&!t.forced));
 const joins=await page.evaluate(()=>{const bounds=[...document.querySelectorAll('[data-objective-title]')].map(t=>t.getBBox());let collisions=0,gaps=[];for(const g of document.querySelectorAll('[data-link-index]')){const paths=g.querySelectorAll('path'),shaft=paths[1],head=paths[2],length=shaft.getTotalLength(),end=shaft.getPointAtLength(length),tip=head.getPointAtLength(head.getTotalLength()/2);gaps.push(Math.hypot(end.x-tip.x,end.y-tip.y));for(let i=0;i<=300;i++){const q=shaft.getPointAtLength(length*i/300);if(bounds.some(b=>q.x>b.x-2&&q.x<b.x+b.width+2&&q.y>b.y-2&&q.y<b.y+b.height+2))collisions++;}}return {collisions,gaps};});
 assert.equal(joins.collisions,0);assert.ok(joins.gaps.every(g=>g<.1));
 for(let i=0;i<factors.clips;i++){
  await page.evaluate(index=>document.querySelectorAll('.clip')[index].click(),i);await page.evaluate(async()=>{await new Promise(r=>setTimeout(r,100));});
  const scene=await page.evaluate(()=>({text:document.querySelector('svg').textContent,box:document.querySelector('[data-content-box]')?.getAttribute('stroke'),headers:[...document.querySelectorAll('[data-section-header] text,[data-box-heading]')].map(t=>t.textContent),values:[...document.querySelectorAll('[data-factor]')].map(g=>g.getAttribute('data-factor')),outside:[...document.querySelectorAll('svg text')].filter(t=>{const b=t.getBBox();return b.x<40||b.x+b.width>1880||b.y<45||b.y+b.height>1040;}).map(t=>t.textContent)}));
  assert.deepEqual(scene.outside,[],'Factorisation text bounds '+i);for(const h of scene.headers)assert.match(h,/ :$/);if(i>0)assert.equal(scene.box,'#0DBBA1');
  assert.doesNotMatch(scene.text,/Bonjour|Aujourd’hui|Afficher|Animer|voix off|Au cours/);
  if(i===1){assert.deepEqual(scene.values,['2^3','3^2','5^1']);assert.match(scene.text,/ordre des facteurs près/);}
  if(i===2)assert.deepEqual(scene.values,['2^3','3^2']);
 }
 console.log('Prime factorisation: five scenes, exact powers, theorem order qualifier, centred objective, clear/attached links, colons and bounded main-only text passed');
 for(const [selection,count,slides,type,links] of [
  ['n3-sem3-vdp1-v2',9,30,'VDP',3],['n3-sem3-vdp2-v2',6,18,'VDP',3],
  ['n3-sem3-vdp3-v2',10,31,'VDP',4],['n3-sem3-vdp4-v2',14,47,'VDP',2],
  ['n3-sem3-vdp1',9,30,'VDP',3],['n3-sem3-vdp2',6,18,'VDP',3],
  ['n3-sem3-vdp3',10,31,'VDP',4],['n3-sem3-vdp4',14,47,'VDP',2],
  ['signed-addition',4,26,'VDP',2],['like-terms',7,27,'VDP',2],['factorization-v2',5,13,'VDP',3],['factorization-review',5,13,'VDP',3],
  ['fractions-v2',9,28,'VDP',2],['fractions-review',9,28,'VDP',2],['subtraction',8,47,'VM',1],
 ]){
  await page.evaluate(value=>{
   const select=document.querySelector('select');
   select.value=value;
   select.dispatchEvent(new Event('change',{bubbles:true}));
  },selection);
  await page.evaluate(()=>new Promise(resolve=>setTimeout(resolve,250)));
  const lesson=await page.evaluate(()=>{
   const title=document.querySelector('[data-objective-title]');
   const arrowGroups=[...document.querySelectorAll('[data-link-index]')];
   return {
    timeline:JSON.parse(document.querySelector('textarea').value),
    clips:document.querySelectorAll('.clip').length,
    titleColor:title.getAttribute('fill'),
    titleRight:title.getBBox().x+title.getBBox().width,
    motion:document.querySelector('[data-objective-entrance]').getAttribute('transform'),
    arrows:arrowGroups.map(group=>{
     const [line,shaft,head]=group.querySelectorAll('path');
     const a=line.getPointAtLength(0),b=line.getPointAtLength(line.getTotalLength());
     const start=shaft.getPointAtLength(0),end=shaft.getPointAtLength(shaft.getTotalLength());
     const tip=head.getPointAtLength(head.getTotalLength()/2);
     return Math.abs(start.x-end.x)<.1&&Math.abs((a.x+b.x)/2-start.x)<.1
      &&Math.abs(start.y-a.y)<.1&&Math.hypot(end.x-tip.x,end.y-tip.y)<.1;
    }),
   };
  });
  assert.equal(lesson.clips,count);
  assert.equal(lesson.timeline.videoType,type);
  assert.deepEqual(lesson.timeline.scenes.flatMap(s=>s.sourceSlides),Array.from({length:slides},(_,index)=>index+1));
  assert.equal(lesson.titleColor,'#263956');
  assert.ok(lesson.titleRight<1860);
  assert.match(lesson.motion,/280/);
  assert.deepEqual(lesson.arrows,Array(links).fill(true));
  let mathGlyphs=0;
  for(let i=1;i<count;i++){
   await page.evaluate(index=>document.querySelectorAll('.clip')[index].click(),i);
   await page.evaluate(()=>new Promise(resolve=>setTimeout(resolve,100)));
   const review=await page.evaluate(()=>{
    const svg=document.querySelector('svg');
    return {
     text:svg.textContent, headings:[...svg.querySelectorAll('[data-section-header], [data-box-heading]')].map(g=>g.textContent),
     variables:[...svg.querySelectorAll('[data-math-role="variable"]')].map(node=>node.textContent),
     joinedWord:svg.querySelector('[data-pronunciation-word]')?.getAttribute('data-pronunciation-word'),
     cards:[...svg.querySelectorAll('[data-vocabulary-card]')].map(node=>node.textContent),
     outside:[...svg.querySelectorAll('text')].filter(node=>{
      const b=node.getBBox();
      return b.x<45||b.x+b.width>1875||b.y<45||b.y+b.height>1040;
     }).map(node=>node.textContent),
    };
   });
   assert.deepEqual(review.outside,[],selection+' scene '+i+' text bounds');
   assert.ok(review.headings.every(h=>h.endsWith(' :')));
   assert.doesNotMatch(review.text,/Bonjour|Aujourd’hui|Animer la voix|Insérer le fichier|Prononciation :|preu-mié/);
   assert.ok(review.variables.every(g=>g==='𝒙'||g==='𝒚'||g==='𝒛'));
   if(lesson.timeline.scenes[i].kind==='pronunciation'){
    const words={'like-terms':'semblables','factorization-v2':'décomposition','factorization-review':'décomposition','fractions-v2':'irréductible','fractions-review':'irréductible'};
    assert.equal(review.joinedWord,lesson.timeline.scenes[i].pronunciation?.word??words[selection]);
   }
   if(selection==='factorization-review'&&lesson.timeline.scenes[i].kind==='vocabulary'){
    assert.equal(review.cards.length,4);
    assert.ok(review.cards.every(card=>!card.includes(':')));
   }
   mathGlyphs+=review.variables.length;
  }
  if(selection==='like-terms'||selection==='subtraction')assert.ok(mathGlyphs>0);
  console.log(selection,slides+' source slides, straight arrows, bounds and mathematical glyphs passed');
 }
 await page.setViewport({width:390,height:844,deviceScaleFactor:1});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 console.log('Mobile overflow check passed');
}finally{await browser.close({silent:true});server.kill();}
