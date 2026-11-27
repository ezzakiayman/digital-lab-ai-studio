import {mkdir,readFile,writeFile} from 'node:fs/promises';
import {elevenRequest} from './elevenlabs-tts.mjs';

// Account identifiers stay in ignored local configuration; rules are not screen text.
const cache='private/quotient-pronunciation-dictionary.json';
await mkdir('private',{recursive:true});
let dictionary;
try{dictionary=JSON.parse(await readFile(cache,'utf8'));}catch(error){
 if(error.code!=='ENOENT')throw error;
 const rules=[['Quo','kɔ'],['quotient','kɔsjɑ̃'],['Quotient','kɔsjɑ̃']]
  .map(([string_to_replace,phoneme])=>({type:'phoneme',alphabet:'ipa',string_to_replace,phoneme,
   word_boundaries:true,case_sensitive:true}));
 rules.push({type:'alias',string_to_replace:'Tient',alias:'cyan',word_boundaries:true,case_sensitive:true});
 const name='Digital Lab · quotient · français';
 const listing=await (await elevenRequest('pronunciation-dictionaries?limit=100')).json();
 const existing=listing.pronunciation_dictionaries?.find(item=>item.name===name);
 const response=existing??await (await elevenRequest('pronunciation-dictionaries/add-from-rules',{
  name,rules,
 })).json();
 dictionary={id:response.id,version_id:response.version_id??response.latest_version_id,rules};
 if(!dictionary.id||!dictionary.version_id)throw Error('Missing pronunciation dictionary identifiers');
 await writeFile(cache,JSON.stringify(dictionary,null,2));
}
const path='src/video/n3-sem4-vdp2-v2-voice-plan.json';
const plan=JSON.parse(await readFile(path,'utf8'));
plan.scenes[0].pronunciationDictionaryLocators=[{
 pronunciation_dictionary_id:dictionary.id,version_id:dictionary.version_id,
}];
await writeFile(path,JSON.stringify(plan,null,2));
console.log('French phoneme dictionary attached to the revised pronunciation take.');
