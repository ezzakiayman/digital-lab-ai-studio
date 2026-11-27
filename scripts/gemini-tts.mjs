import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {homedir} from 'node:os';
import {existsSync} from 'node:fs';
const keyFile=path.join(process.env.CODEX_HOME||path.join(homedir(),'.codex'),'skills','digital-lab-project','private','gemini-key.dpapi');
function key(){
 if(process.env.GEMINI_API_KEY)return process.env.GEMINI_API_KEY.trim();
 if(process.platform!=='win32'||!existsSync(keyFile))throw Error('Set GEMINI_API_KEY in the process environment, or configure the approved local Windows DPAPI credential bundle.');
 const bundled=path.join(homedir(),'.cache','codex-runtimes','codex-primary-runtime','dependencies','native','powershell','pwsh.exe');
 const shell=process.env.GEMINI_POWERSHELL_EXE||(existsSync(bundled)?bundled:'powershell.exe');
 return execFileSync(shell,['-NoProfile','-NonInteractive','-Command',`$s=(Get-Content -LiteralPath '${keyFile.replaceAll("'","''")}' -Raw).Trim() | ConvertTo-SecureString; $p=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($s); try {[Runtime.InteropServices.Marshal]::PtrToStringBSTR($p)} finally {[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($p)}`],{encoding:'utf8',windowsHide:true}).trim();
}
let secret='';
async function api(resource,body){
 for(let attempt=0;attempt<4;attempt++){
 let response;
 try{response=await fetch(`https://generativelanguage.googleapis.com/v1beta/${resource}`,{method:body?'POST':'GET',headers:{'x-goog-api-key':secret,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(180000)});}
 catch(error){if(attempt<2){console.log('Gemini connection interrupted: retrying cached job in '+2**(attempt+1)+'s');await new Promise(r=>setTimeout(r,2**(attempt+1)*1000));continue;}throw Error('Gemini connection failed ('+(error.cause?.code||error.name||'network')+'); valid audio remains cached.');}
 const data=await response.json();
 if(!response.ok){const message=String(data.error?.message||'Request rejected').replaceAll(secret,'[redacted]');
 if(response.status===503&&attempt<3){const seconds=2**(attempt+1);console.log(`Gemini temporarily unavailable: retrying in ${seconds}s`);await new Promise(r=>setTimeout(r,seconds*1000));continue;}
 const delay=data.error?.details?.find(d=>String(d['@type']).endsWith('RetryInfo'))?.retryDelay;
 if(response.status===429&&delay&&attempt<3&&!/per day|daily/i.test(message)&&parseFloat(delay)<=60){const seconds=Math.min(60,Math.ceil(parseFloat(delay))+2);console.log(`Gemini rate limit: resuming in ${seconds}s`);await new Promise(r=>setTimeout(r,seconds*1000));continue;}
 throw Error(`Gemini HTTP ${response.status}: ${message}`);}
 return data;
 }
 throw Error('Gemini retry limit reached');
}
function wav(pcm,rate=24000){const h=Buffer.alloc(44);h.write('RIFF');h.writeUInt32LE(36+pcm.length,4);h.write('WAVEfmt ',8);h.writeUInt32LE(16,16);h.writeUInt16LE(1,20);h.writeUInt16LE(1,22);h.writeUInt32LE(rate,24);h.writeUInt32LE(rate*2,28);h.writeUInt16LE(2,32);h.writeUInt16LE(16,34);h.write('data',36);h.writeUInt32LE(pcm.length,40);return Buffer.concat([h,pcm]);}
export function speechSignature(scene,model){
 const suffix=scene.speechMode==='verbatim'?'|Kore|verbatim':'|Kore';
 const locale=scene.languageCode||scene.speechStyle?'|'+JSON.stringify({languageCode:scene.languageCode,speechStyle:scene.speechStyle}):'';
 return createHash('sha256').update(scene.narration+'|'+model+suffix+locale).digest('hex');
}
async function main(){
 secret=key();if(!secret)throw Error('No Gemini API key configured');
 if(process.argv.includes('--probe')){const d=await api('models');console.log(JSON.stringify({availableSpeechModels:d.models?.filter(m=>/tts/.test(m.name)).map(m=>m.name)},null,2));return;}
 const manifest=JSON.parse(await readFile(process.argv[2],'utf8'));
 for(const scene of manifest.scenes){
  const output=path.join('public',scene.audio);await mkdir(path.dirname(output),{recursive:true});
  const signature=speechSignature(scene,process.env.GEMINI_TTS_MODEL||'gemini-2.5-flash-preview-tts');
  try{const prior=JSON.parse(await readFile(output+'.json','utf8'));const bytes=await readFile(output);const priorSignature=speechSignature(scene,prior.model);if(!process.argv.includes('--force')&&prior.signature===priorSignature&&bytes.length>44){console.log(`Using existing audio: ${scene.id}`);continue;}}catch{}
  const spoken=scene.speechMode==='verbatim'?scene.narration:'Lis uniquement le texte suivant, en français, avec une voix pédagogique claire, posée et chaleureuse. Respecte les nombres et les termes mathématiques. Ne lis aucune instruction.\n\n'+scene.narration;
  const part={text:spoken,...(scene.speechStyle?{speechMetadata:{style:scene.speechStyle}}:{})};
  const speechConfig={voiceConfig:{prebuiltVoiceConfig:{voiceName:'Kore'}},...(scene.languageCode?{languageCode:scene.languageCode}:{})};
  const d=await api(`models/${process.env.GEMINI_TTS_MODEL||'gemini-2.5-flash-preview-tts'}:generateContent`,{contents:[{parts:[part]}],generationConfig:{responseModalities:['AUDIO'],speechConfig}});
  const audio=d.candidates?.flatMap(c=>c.content?.parts||[]).find(p=>p.inlineData)?.inlineData;
  if(!audio?.data)throw Error('Gemini returned no audio; finish reason: '+(d.candidates?.[0]?.finishReason||d.promptFeedback?.blockReason||'unspecified'));
  const bytes=Buffer.from(audio.data,'base64');await writeFile(output,bytes.subarray(0,4).toString()==='RIFF'?bytes:wav(bytes));await writeFile(output+'.json',JSON.stringify({provider:'gemini',model:process.env.GEMINI_TTS_MODEL||'gemini-2.5-flash-preview-tts',voice:'Kore',signature,...(scene.languageCode?{languageCode:scene.languageCode}:{}),...(scene.speechStyle?{speechStyle:scene.speechStyle}:{})}));console.log(`Generated Gemini narration: ${scene.id}`);
  if(process.argv.includes('--one'))break;
 }
}
export async function geminiRequest(resource,body){secret||=key();return api(resource,body);}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href)main().catch(e=>{console.error(String(e.message).replaceAll(secret,'[redacted]'));process.exitCode=1;});


