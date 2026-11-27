import {mkdir,readFile,writeFile,copyFile} from 'node:fs/promises';
import {elevenRequest} from './elevenlabs-tts.mjs';
const cache='private/n3-sem3-irrationnel-dictionary.json';
await mkdir('private',{recursive:true});
let dictionary;
try{dictionary=JSON.parse(await readFile(cache,'utf8'));}catch(error){
 if(error.code!=='ENOENT')throw error;
 const rules=[{type:'phoneme',alphabet:'ipa',string_to_replace:'Sion',phoneme:'sjɔ',word_boundaries:true,case_sensitive:true}];
 const name='Digital Lab · irrationnel · français';
 const listing=await (await elevenRequest('pronunciation-dictionaries?limit=100')).json();
 const existing=listing.pronunciation_dictionaries?.find(x=>x.name===name);
 const response=existing??await (await elevenRequest('pronunciation-dictionaries/add-from-rules',{name,rules})).json();
 dictionary={id:response.id,version_id:response.version_id??response.latest_version_id,rules};
 if(!dictionary.id||!dictionary.version_id)throw Error('Missing dictionary identifiers');
 await writeFile(cache,JSON.stringify(dictionary,null,2));
}
for(const file of ['src/video/n3-sem3-vdp4-v5-plan.json','src/video/n3-sem3-vdp4-v5-voice-plan.json']){
 const plan=JSON.parse(await readFile(file,'utf8'));
 const scene=plan.scenes.find(s=>s.id==='vdp4-prononciation-5');
 if(!scene)throw Error('Missing pronunciation scene');
 const archive='public/n3-sem3-elevenlabs-v5-vdp4/pre-diction';await mkdir(archive,{recursive:true});
 for(const ext of ['.wav','.wav.json','.mp3']){
  const target=`${archive}/${scene.id}${ext}`;
  try{await readFile(target);}catch(e){if(e.code!=='ENOENT')throw e;await copyFile('public/'+scene.audio.replace(/\.wav$/,ext),target);}
 }
 scene.pronunciationDictionaryLocators=[{pronunciation_dictionary_id:dictionary.id,version_id:dictionary.version_id}];
 await writeFile(file,JSON.stringify(plan,null,2));
}
console.log('Oral French vowel dictionary attached to one pronunciation take; source words and main voice unchanged.');
