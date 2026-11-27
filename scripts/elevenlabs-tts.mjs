import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {homedir} from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
const credential=path.join(process.env.CODEX_HOME||path.join(homedir(),'.codex'),'skills','digital-lab-project','private','elevenlabs-key.dpapi');
let secret='';
function key(){
 if(process.env.ELEVENLABS_API_KEY)return process.env.ELEVENLABS_API_KEY.trim();
 if(process.platform!=='win32'||!existsSync(credential))throw Error('Configure ELEVENLABS_API_KEY or the approved local encrypted ElevenLabs credential.');
 const bundled=path.join(homedir(),'.cache','codex-runtimes','codex-primary-runtime','dependencies','native','powershell','pwsh.exe');
 return execFileSync(process.env.ELEVENLABS_POWERSHELL_EXE||(existsSync(bundled)?bundled:'powershell.exe'),['-NoProfile','-NonInteractive','-Command',`$s=(Get-Content -LiteralPath '${credential.replaceAll("'","''")}' -Raw).Trim() | ConvertTo-SecureString; $p=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($s); try {[Runtime.InteropServices.Marshal]::PtrToStringBSTR($p)} finally {[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($p)}`],{encoding:'utf8',windowsHide:true}).trim();
}
async function api(resource,body){
 secret||=key();
 for(let attempt=0;attempt<3;attempt++){
  let r;try{r=await fetch('https://api.elevenlabs.io/v1/'+resource,{method:body?'POST':'GET',headers:{'xi-api-key':secret,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(180000)});}catch(e){if(attempt<2){console.log('Voice connection interrupted; retrying in 3s');await new Promise(r=>setTimeout(r,3000));continue;}throw Error('Voice connection failed; generated audio remains cached.');}
  if(r.ok)return r;
  const message=(await r.text()).replaceAll(secret,'[redacted]');
  const delay=Number(r.headers.get('retry-after')||3);
  if(attempt<2&&(r.status>=500||(r.status===429&&!/quota_exceeded|insufficient|limit_reached/i.test(message)))&&delay<=60){console.log('Voice service temporarily unavailable; retrying in '+delay+'s');await new Promise(r=>setTimeout(r,delay*1000));continue;}
  throw Error(`ElevenLabs HTTP ${r.status}: ${message.slice(0,1500)}`);
 }
}
async function main(){
 const voice=process.env.ELEVENLABS_VOICE_ID||'e1kzF2oNiC1xDfUP7Yxo',model=process.env.ELEVENLABS_MODEL||'eleven_multilingual_v2';
 if(process.argv.includes('--probe')){const data=await (await api('voices/'+encodeURIComponent(voice))).json();console.log(JSON.stringify({voiceAvailable:true,voiceId:data.voice_id,name:data.name,labels:data.labels},null,2));return;}
 const plan=JSON.parse(await readFile(process.argv[2],'utf8'));
 for(const scene of plan.scenes){
  const settings={stability:scene.stability??.65,similarity_boost:.75,style:0,use_speaker_boost:true,speed:scene.speed??1};
  const language_code=scene.languageCode;
  const dictionary=scene.pronunciationDictionaryLocators?{pronunciation_dictionary_locators:scene.pronunciationDictionaryLocators}:{};
  const output=path.join('public',scene.audio),receipt=output+'.json';await mkdir(path.dirname(output),{recursive:true});
  const signature=createHash('sha256').update(JSON.stringify({text:scene.narration,voice,model,settings,language_code,...dictionary})).digest('hex');
  try{const prior=JSON.parse(await readFile(receipt,'utf8'));if(!process.argv.includes('--force')&&prior.signature===signature&&(await readFile(output)).length>44){console.log('Using existing ElevenLabs audio: '+scene.id);continue;}}catch{}
  const r=await api('text-to-speech/'+encodeURIComponent(voice)+'?output_format=mp3_44100_128',{text:scene.narration,model_id:model,voice_settings:settings,language_code,...dictionary});
  const bytes=Buffer.from(await r.arrayBuffer());if(bytes.length<100)throw Error('Voice service returned empty audio');
  const compressed=output.replace(/\.wav$/,'.mp3');await writeFile(compressed,bytes);
  execFileSync('ffmpeg',['-y','-v','error','-i',compressed,'-ac','1','-ar','24000','-c:a','pcm_s16le',output],{windowsHide:true,stdio:['ignore','ignore','pipe']});
  await writeFile(receipt,JSON.stringify({provider:'elevenlabs',voice,model,signature,settings,languageCode:language_code,...dictionary,sourceEncoding:'mp3_44100_128; decoded to mono PCM24kHz for alignment'},null,2));
  console.log('Generated ElevenLabs narration: '+scene.id);
  if(process.argv.includes('--one'))break;
 }
}
export async function elevenRequest(resource,body){return api(resource,body);}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href)
 main().catch(e=>{console.error(String(e.message).replaceAll(secret,'[redacted]'));process.exitCode=1;});
