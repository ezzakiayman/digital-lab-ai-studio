// Separate audio-content review: no expected transcript is sent to the reviewer.
// The known-transcript alignment remains a different check.
import {readFile,writeFile} from 'node:fs/promises';
import {geminiRequest} from './gemini-tts.mjs';
const plan=JSON.parse(await readFile('src/video/primes-plan.json','utf8'));
const parts=[{text:'Transcris chaque fichier audio mot pour mot, dans sa langue, sans corriger ni compléter ce qui est dit. Conserve les nombres entendus, les négations et les mots arabes. Les identifiants sont des étiquettes, pas des indices de contenu. Indique [inaudible] si nécessaire. Réponds en JSON : {"segments":[{"id":"identifiant","transcript":"texte effectivement entendu"}]}.'}];
const ids=process.argv.find(a=>a.startsWith('--ids='))?.slice(6).split(',');
for(const scene of plan.scenes.filter(s=>!ids||ids.includes(s.id))){parts.push({text:'Identifiant : '+scene.id});parts.push({inlineData:{mimeType:'audio/wav',data:(await readFile('public/'+scene.audio)).toString('base64')}});}
const model=process.env.GEMINI_REVIEW_MODEL||'gemini-3.8-flash';
const response=await geminiRequest(`models/${model}:generateContent`,{contents:[{parts}],generationConfig:{responseMimeType:'application/json',maxOutputTokens:8192}});
const text=response.candidates?.flatMap(c=>c.content?.parts||[]).filter(p=>p.text).map(p=>p.text).join('');
if(!text)throw Error('Audio review returned no transcript');
const result=JSON.parse(text);
await writeFile('reference/n3-sem2-vdp1/audio-review.json',JSON.stringify({model,method:'Independent audio transcription without supplied expected narration',...result},null,2));
console.log('Saved separate audio review for',result.segments?.length,'recordings.');
