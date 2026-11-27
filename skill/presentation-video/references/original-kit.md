---
name: presentation-video
description: Make a presentation video (slides + voice-over + screen recordings + captions + music) from code with free tools — Node, Playwright, ffmpeg, a free AI voice or your own voice, and word timing so each bullet appears exactly when it is said. Use when asked to "make a presentation video", "turn these slides into a video", "product demo video", "explainer with voice-over" or "pitch video".
---

# Presentation video kit

Make a 16:9 presentation video (or 9:16 for Reels/Shorts) the way a motion designer would, but **from code**:

- you write the slides in one small file (`video.js`): title, bullets, image or screen recording, and what is said;
- a voice reads each slide (an AI voice for free, or your own recording);
- every word of the voice gets its exact time, so **each bullet appears the moment it is said**, and captions
  light up word by word;
- the slides are HTML/CSS (any design you can make in a web page), rendered frame by frame into an MP4 with
  the voice and quiet background music.

Everything here is **free**. Tested on Linux (Ubuntu) with Node 22; it works on macOS and Windows (WSL) the same way.

> **How to use this file with an AI coding agent:** for Claude Code, save it as
> `~/.claude/skills/presentation-video/SKILL.md` (or `.claude/skills/presentation-video/SKILL.md` inside the
> project). For Codex or others, put it in the project as `AGENTS.md` (or link to it from there). Then just
> say: *"make a presentation video about X, follow the presentation-video skill"*.

---

## 1. Tools you need (and why)

| Tool | What it does here | Cost | Install |
|---|---|---|---|
| **Node.js 22** | Runs the renderer | Free | `nvm install 22` ([nvm](https://github.com/nvm-sh/nvm)) |
| **Playwright** (Chromium) | Opens the slides as a web page and takes one screenshot per frame | Free | `npm i playwright && npx playwright install chromium` |
| **ffmpeg** (`ffmpeg-static`, `ffprobe-static`) | Turns the screenshots into a video, mixes voice + music, cuts screen recordings | Free | `npm i ffmpeg-static ffprobe-static` (no system ffmpeg needed) |
| **Fonts** (`@fontsource/*`) | Real fonts set by code (Inter for Latin, Cairo for Arabic) | Free | `npm i @fontsource/inter @fontsource/cairo` |
| **Python 3.10+ venv** with `torch`, `torchaudio`, `uroman` | **Word timing** (forced alignment): finds when each word is said in the audio | Free, CPU only, ~1.2 GB model downloaded once | see step 2 |
| **A voice** (pick one) | Reads the slides | Free | see section 4 |
| **OBS Studio** (optional) | Screen recordings of an app/website demo | Free | [obsproject.com](https://obsproject.com) |
| **Audacity** (optional) | Record your own voice, cut noise | Free | [audacityteam.org](https://www.audacityteam.org) |
| **Music** (optional) | Quiet background bed | Free | [Pixabay Music](https://pixabay.com/music/) or YouTube Audio Library (check each track's license) |

**What about Remotion?** Remotion (React → video) is a good alternative and does the same job; see section 9.
This kit uses plain HTML/CSS + Playwright instead: no React, no build step, and it is what the code below was
tested with.

---

## 2. Setup (once)

```bash
mkdir presentation-video && cd presentation-video
npm init -y
npm i playwright ffmpeg-static ffprobe-static @fontsource/inter @fontsource/cairo
npx playwright install chromium          # on Linux, if it asks: npx playwright install-deps

python3 -m venv .venv
.venv/bin/pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install uroman numpy edge-tts
```

Then create the 2 files from section 8 (`render.js`, `align_words.py`), and `tts.js` if you use the Gemini voice.

Folder layout:

```
presentation-video/
├── render.js           ← the renderer (section 8)
├── align_words.py      ← word timing (section 8)
├── tts.js              ← optional: Gemini voice for every slide (section 8)
├── .env                ← GEMINI_API_KEY=...   (never share/commit this file)
└── projects/
    └── my-demo/
        ├── video.js    ← the slides + what is said
        ├── voice/      ← 1.mp3, 2.mp3 … (one per slide)
        ├── art/        ← images, screenshots, logos
        ├── rec/        ← screen recordings (.mp4)
        ├── music.mp3   ← optional
        └── out/        ← video.mp4, stills (made by render.js)
```

**RAM:** word timing uses ~3–4 GB the first time per slide (cached after), rendering ~1 GB. Close heavy apps on an
8 GB machine. Speed: about **2–3 s of work per second of video** at 1080p on a laptop.

---

## 3. The workflow (do it in this order)

1. **Script first.** Write what will be said, slide by slide. ~130–150 words per minute in English
   (~100–110 in Arabic). A 2-minute presentation ≈ 8–12 slides. Read it out loud once before recording.
2. **Slides file** `projects/<name>/video.js` (section 5): title, bullets with their cue words, image/clip, text.
3. **Voice** for each slide → `voice/1.mp3`, `voice/2.mp3`… (section 4). Listen to all of them.
4. **Check the look fast:** `node render.js <name> --stills` → one picture per slide in `out/`. Fix layout.
5. **Render:** `node render.js <name>` → `projects/<name>/out/video.mp4`. Watch it fully once.
6. Fix → render again (voices and word times are cached; only changed slides are re-timed).

---

## 4. The voice (free options)

The text in `video.js` must be **exactly what is said** in the audio file (that is how word timing works).

**A. Your own voice (best for a real presentation).** Record each slide as its own file in Audacity
(Effect → Noise Reduction, then Normalize to −1 dB), export `voice/1.mp3`, `voice/2.mp3`… and paste what you
actually said into `text`.

**B. Microsoft Edge voices (free, no key).** Many languages and accents:

```bash
.venv/bin/edge-tts --list-voices | grep -E "en-US|ar-"          # pick one
.venv/bin/edge-tts --voice en-US-AndrewNeural --text "Welcome to our app." --write-media projects/my-demo/voice/1.mp3
```

If it fails with **403**, update it: `.venv/bin/pip install -U edge-tts` (Microsoft changes its token now and then).

**C. Google Gemini TTS (free tier, the most natural).** Get a free key at
[aistudio.google.com](https://aistudio.google.com) → put `GEMINI_API_KEY=...` in `.env` → `node tts.js <name>`
voices every slide that has `text` but no audio yet. Free tier ≈ **10 calls per day, 3 per minute**; on a
`429` error wait until tomorrow (never switch to a paid key by accident). Voices: Charon, Kore, Puck, Iapetus,
Enceladus, Leda… The prompt **must** keep the `### DIRECTOR'S NOTES … #### TRANSCRIPT` layout, otherwise the
notes are read aloud. If the model name stops working, check the current TTS model name in the Gemini API docs
and change `MODEL` in `tts.js`.

**D. ElevenLabs** — very good, but the free plan does not allow commercial use. Only if you pay.

Rules for good voice text: numbers and units in words when they must be read a certain way ("twenty percent"),
no abbreviations the voice could misread, short sentences, a comma where you want a breath.

---

## 5. Writing `video.js`

```js
// projects/my-demo/video.js
module.exports = {
  size: [1920, 1080],          // 16:9. Vertical Reel/Short: [1080, 1920]
  fps: 30,
  lang: 'en', dir: 'ltr',      // Arabic: lang: 'ar', dir: 'rtl'
  captions: true,              // word-by-word captions at the bottom (good for social media)
  music: 'music.mp3',          // optional; looped, ducked under the voice, faded out at the end
  musicVolume: 0.25,           // optional
  colors: { bg: '#0f172a', text: '#f8fafc', accent: '#38bdf8', muted: '#94a3b8' },   // optional theme
  css: '',                     // optional extra CSS (your brand)

  slides: [
    // cover slide, no voice: lasts `dur` seconds
    { title: 'Taskly in 90 seconds', subtitle: 'Product demo · May 2026', dur: 3 },

    // title + bullets; each bullet appears when its cue word is said (the 2nd item of each pair)
    { audio: 'voice/1.mp3',
      text: 'Teams lose hours every week. Tasks live in chats, emails and sticky notes.',
      title: 'The problem',
      bullets: [['Hours lost every week', 'hours'], ['Tasks in chats and emails', 'chats'], ['Sticky notes everywhere', 'sticky']],
      image: 'art/problem.png' },                       // optional picture on the side

    // screen recording: plays in sync with the video (slide lasts at least as long as the clip)
    { audio: 'voice/2.mp3', text: 'Here is how you add a task in two clicks.', title: 'Live demo', clip: 'rec/add-task.mp4' },

    // fully custom slide: any HTML; T.at('word') = the second that word is said
    { audio: 'voice/3.mp3', text: 'Our users saved forty percent of their meeting time.',
      html: (T) => `<div style="position:absolute;inset:0;display:grid;place-items:center">
        <div class="pop" style="--t:${T.at('forty')}s;font:800 260px Inter;color:#38bdf8">40%</div></div>`,
      hold: 1 },                                        // stay 1 s more after the voice ends
  ],
};
```

Slide fields:

| Field | Meaning |
|---|---|
| `audio`, `text` | The voice file and **exactly** what it says (needed for timing) |
| `title`, `subtitle` | Title (with an accent bar) and a smaller line. A slide with only these is centered (cover) |
| `bullets` | `[[text on screen, cue word], …]`. Cue = a word from `text`; `null` = appears at the start |
| `image` | A picture from the project folder (PNG/JPG), shown beside the bullets or alone |
| `clip` | A screen recording (MP4); cut into frames once and played in sync |
| `html(T)` | Your own slide. Helpers: `T.at('word', n)` (n-th time it is said), `T.start`, `T.end`, `T.img('art/x.png')`, `T.words` |
| `dur` | Length of a slide without voice |
| `hold` | Extra seconds after the voice (to let people read) |

Built-in animations for your own HTML: add a class and `style="--t:<seconds>"`:
`up` (slides up), `fade`, `pop` (scales in). You can write any CSS `@keyframes` too: every animation is
paused and set to the exact frame time, so **CSS animations with `animation-delay` = a time in seconds on the
whole video** render perfectly frame by frame. Don't use JavaScript timers (`setTimeout`, `requestAnimationFrame`)
for motion: they don't follow the render clock.

---

## 6. Commands

```bash
node render.js my-demo --stills        # one picture per slide → projects/my-demo/out/still-N.jpg
node render.js my-demo --frame 12.5    # the exact frame at 12.5 s → out/frame.jpg
node render.js my-demo                 # full video → projects/my-demo/out/video.mp4
```

Output: H.264 + AAC, `yuv420p`, `+faststart`, loudness −14 LUFS: plays everywhere and is ready for YouTube,
LinkedIn, Instagram, WhatsApp. If Chromium is somewhere else: `CHROMIUM_PATH=/path/to/chrome node render.js …`.

---

## 7. ffmpeg cookbook (things you'll need around the video)

`FF=$(node -p "require('ffmpeg-static')")` then:

```bash
# Cut a screen recording from 0:12 to 0:40 (re-encode = exact cut)
$FF -ss 12 -to 40 -i rec/raw.mp4 -c:v libx264 -crf 18 -an rec/add-task.mp4

# Speed up a long screen recording ×2 (no sound)
$FF -i rec/raw.mp4 -vf "setpts=PTS/2" -an rec/fast.mp4

# Crop a recording to one area (w:h:x:y), e.g. remove the browser bar
$FF -i rec/raw.mp4 -vf "crop=1920:980:0:100" -an rec/cropped.mp4

# Grab one frame as an image (a thumbnail, or the last frame of a clip)
$FF -ss 5 -i out/video.mp4 -frames:v 1 thumb.jpg
$FF -sseof -0.1 -i rec/add-task.mp4 -frames:v 1 last.jpg

# Clean and level a voice recording
$FF -i raw-voice.wav -af "highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5" voice/1.mp3

# Make the 16:9 video vertical for Reels/Shorts with a blurred background
$FF -i out/video.mp4 -filter_complex "[0]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];[0]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:a copy vertical.mp4

# Smaller file for WhatsApp/email (higher crf = smaller)
$FF -i out/video.mp4 -c:v libx264 -crf 28 -preset slow -c:a aac -b:a 96k small.mp4

# Join two finished videos (same size/fps) with a 1 s crossfade (offset = length of the first − 1)
$FF -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=29[v];[0:a][1:a]acrossfade=d=1[a]" -map "[v]" -map "[a]" joined.mp4

# Burn an .srt subtitle file into a video
$FF -i out/video.mp4 -vf "subtitles=subs.srt:force_style='FontSize=24'" -c:a copy subbed.mp4

# Check length, size, loudness
$(node -p "require('ffprobe-static').path") -v error -show_entries format=duration -of csv=p=0 out/video.mp4
$FF -i out/video.mp4 -af ebur128 -f null - 2>&1 | grep "I:" | tail -1
```

Gotcha: to loop a sound bed, give each copy its own `-i` or use `-stream_loop -1 -i file` (as `render.js`
does); `asplit` + `acrossfade` silently drops a copy.

---

## 8. The code

### `render.js`

```js
// Presentation video renderer: slides written in projects/<name>/video.js, timed to the voice, rendered frame by frame
// (Playwright screenshots → ffmpeg), then the voices + optional music are mixed in.
// Usage: node render.js <name>             → projects/<name>/out/video.mp4
//        node render.js <name> --stills    → one picture per slide (fast check)
//        node render.js <name> --frame 3.5 → the frame at 3.5 s
const fs = require('fs');
const path = require('path');
const { execFile, spawn } = require('child_process');
const { promisify } = require('util');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const FFMPEG = require('ffmpeg-static');
const FFPROBE = require('ffprobe-static').path;

const run = promisify(execFile);
const PY = process.env.PYTHON || path.join(__dirname, '.venv/bin/python');
const PAD = 0.4; // seconds of slide before and after each voice line

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const plain = (s) => s.toLowerCase().replace(/[ً-ْٰـ]/g, '').replace(/[^\p{L}\p{N}]/gu, '');
const url = (f) => pathToFileURL(f).href;

async function seconds(file) {
  const { stdout } = await run(FFPROBE, ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file]);
  return parseFloat(stdout);
}

// Time of every spoken word (align_words.py), cached next to the audio until the text changes.
async function words(audio, text) {
  const cache = `${audio}.words.json`;
  if (fs.existsSync(cache)) { const c = JSON.parse(fs.readFileSync(cache, 'utf8')); if (c.text === text) return c.words; }
  const stdout = await new Promise((resolve, reject) => {
    execFile(PY, [path.join(__dirname, 'align_words.py'), FFMPEG, audio], { maxBuffer: 1e7, timeout: 600e3 },
      (err, out) => (err ? reject(err) : resolve(out))).stdin.end(text);
  });
  const list = JSON.parse(stdout).map((w) => ({ w: w.w, at: w.t, end: w.t + w.d }));
  fs.writeFileSync(cache, JSON.stringify({ text, words: list }));
  return list;
}

// A screen recording becomes numbered JPGs (cut once); the page swaps them frame by frame.
async function clipFrames(file, fps, out) {
  const dir = path.join(out, 'clips', path.basename(file).replace(/\W/g, '_'));
  if (!fs.existsSync(path.join(dir, '00001.jpg'))) {
    fs.mkdirSync(dir, { recursive: true });
    await run(FFMPEG, ['-y', '-loglevel', 'error', '-i', file, '-vf', `fps=${fps},scale=1600:-2`, '-q:v', '3', path.join(dir, '%05d.jpg')]);
  }
  return { dir, count: fs.readdirSync(dir).length };
}

// Slide times: PAD + voice + PAD (+ hold), at least as long as its clip, or `dur` when it has no voice.
async function timeline(dir, spec, out) {
  let t = 0;
  const slides = [];
  for (const s of spec.slides) {
    const audio = s.audio && path.join(dir, s.audio);
    const len = audio ? await seconds(audio) : 0;
    const ws = audio ? (await words(audio, s.text)).map((w) => ({ ...w, at: w.at + t + PAD, end: w.end + t + PAD })) : [];
    const clip = s.clip && { ...(await clipFrames(path.join(dir, s.clip), spec.fps, out)), seconds: await seconds(path.join(dir, s.clip)) };
    const dur = s.dur || Math.max(audio ? PAD + len + PAD : 3, clip ? clip.seconds : 0);
    slides.push({ ...s, audio, clip, start: t, voiceAt: t + PAD, end: t + dur + (s.hold || 0), words: ws });
    t = slides.at(-1).end;
  }
  return slides;
}

// T = helpers for a slide: T.at('word') = when that word is said (seconds on the whole video).
function helpers(s, dir) {
  return {
    start: s.start, end: s.end, words: s.words,
    at(part, n = 1) {
      const hits = s.words.filter((w) => plain(w.w).includes(plain(part)));
      if (!hits[n - 1]) throw new Error(`"${part}" (#${n}) is not said in: ${s.text}`);
      return +hits[n - 1].at.toFixed(2);
    },
    img: (file) => url(path.join(dir, file)),
  };
}

// The built-in slide layout: title, bullets (each appears on its cue word), image or screen recording.
function slideHtml(s, T) {
  if (s.html) return s.html(T);
  const media = s.clip ? `<img class="media fade" style="--t:${s.start}s" data-frames="${url(s.clip.dir)}" data-count="${s.clip.count}" data-from="${s.start}">`
    : s.image ? `<img class="media fade" style="--t:${s.start + 0.2}s" src="${T.img(s.image)}">` : '';
  const bullets = (s.bullets || []).map(([text, cue]) => `<li class="up" style="--t:${cue ? T.at(cue) : s.start + 0.3}s">${esc(text)}</li>`).join('');
  const cls = media && bullets ? 'split' : !media && !bullets ? 'cover' : '';
  return `<div class="slide ${cls}">
    ${s.title ? `<h1 class="up" style="--t:${s.start + 0.1}s">${esc(s.title)}</h1>` : ''}
    ${s.subtitle ? `<p class="sub fade" style="--t:${s.start + 0.4}s">${esc(s.subtitle)}</p>` : ''}
    <div class="body">${bullets ? `<ul>${bullets}</ul>` : ''}${media}</div></div>`;
}

// Captions (spec.captions: true): lines of ~6 words, each word lights up when said.
function captions(s) {
  const groups = [];
  for (let i = 0; i < s.words.length; i += 6) groups.push(s.words.slice(i, i + 6));
  return groups.map((g, k) => `<div class="line" dir="auto" style="--a:${g[0].at.toFixed(2)}s;--b:${(groups[k + 1] ? groups[k + 1][0].at : s.end).toFixed(2)}s">${
    g.map((w) => `<span class="w" style="--t:${w.at.toFixed(2)}s">${esc(w.w.replace(/[ً-ْ]/g, ''))}</span>`).join(' ')}</div>`).join('');
}

function pageHtml(dir, spec, slides) {
  const [W, H] = spec.size;
  const face = (family, pkg, subset, w) => `@font-face{font-family:${family};font-weight:${w};src:url(${url(require.resolve(`@fontsource/${pkg}/files/${pkg}-${subset}-${w}-normal.woff2`))})}`;
  const c = { bg: '#0f172a', text: '#f8fafc', accent: '#38bdf8', muted: '#94a3b8', ...spec.colors };
  return `<!doctype html><html lang="${spec.lang || 'en'}" dir="${spec.dir || 'ltr'}"><head><meta charset="utf-8"><style>
${face('Inter', 'inter', 'latin', 400)}${face('Inter', 'inter', 'latin', 800)}${face('Cairo', 'cairo', 'arabic', 400)}${face('Cairo', 'cairo', 'arabic', 800)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;overflow:hidden;background:${c.bg};color:${c.text};font-family:Inter,Cairo,sans-serif}
.sc{position:absolute;inset:0;opacity:0;animation:on 1ms linear var(--s) forwards, off 1ms linear var(--e) forwards}
@keyframes on{to{opacity:1}} @keyframes off{to{opacity:0}}
.slide{position:absolute;inset:${H * 0.09}px ${W * 0.07}px;display:flex;flex-direction:column;gap:${H * 0.035}px}
h1{font-size:${H * 0.075}px;font-weight:800;line-height:1.15;color:${c.text}}
h1::after{content:"";display:block;width:${W * 0.06}px;height:8px;margin-top:${H * 0.02}px;border-radius:4px;background:${c.accent}}
.sub{font-size:${H * 0.035}px;color:${c.muted}}
.body{flex:1;min-height:0;display:flex;gap:${W * 0.04}px;align-items:center}
ul{flex:1;list-style:none;display:flex;flex-direction:column;gap:${H * 0.03}px}
li{font-size:${H * 0.042}px;line-height:1.35;padding-inline-start:${H * 0.05}px;position:relative}
li::before{content:"";position:absolute;inset-inline-start:0;top:.45em;width:.5em;height:.5em;border-radius:50%;background:${c.accent}}
.media{flex:1;min-width:0;max-height:100%;object-fit:contain;border-radius:18px;box-shadow:0 20px 60px #0008}
.split .media{flex:1.2}
.cover{justify-content:center;align-items:center;text-align:center}.cover h1{font-size:${H * 0.1}px}.cover h1::after{margin-inline:auto}.cover .body{display:none}
${spec.captions ? `.slide{bottom:${H * 0.16}px}` : ''}
/* entrances: class + style="--t:<seconds>" (use them in your own html too) */
.up{animation:up .6s cubic-bezier(.2,.8,.2,1) var(--t) both} @keyframes up{from{transform:translateY(40px);opacity:0}}
.fade{animation:fade .6s ease var(--t) both} @keyframes fade{from{opacity:0}}
.pop{animation:pop .5s cubic-bezier(.3,1.5,.5,1) var(--t) both} @keyframes pop{from{transform:scale(0);opacity:0}}
.caps{position:absolute;left:10%;right:10%;bottom:${H * 0.05}px;height:${H * 0.08}px}
.line{position:absolute;inset:0;text-align:center;font-size:${H * 0.036}px;font-weight:800;opacity:0;
  animation:on 1ms linear var(--a) forwards, off 1ms linear var(--b) forwards}
.line .w{display:inline-block;margin:0 .1em;padding:.05em .2em;border-radius:8px;background:#000a;animation:lit .1s linear var(--t) forwards}
@keyframes lit{to{color:${c.accent}}}
${spec.css || ''}
</style></head><body>
${slides.map((s) => {
    const T = helpers(s, dir);
    return `<section class="sc" style="--s:${s.start}s;--e:${s.end}s">${slideHtml(s, T)}${spec.captions && s.words.length ? `<div class="caps">${captions(s)}</div>` : ''}</section>`;
  }).join('\n')}
<script>
// Show exactly the frame at <ms>: every CSS animation paused at that time, every clip on its frame.
window.seek = (ms, fps) => {
  for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; }
  const waits = [];
  for (const el of document.querySelectorAll('[data-frames]')) {
    const n = Math.min(+el.dataset.count, Math.max(1, Math.floor((ms / 1000 - el.dataset.from) * fps) + 1));
    const src = el.dataset.frames + '/' + String(n).padStart(5, '0') + '.jpg';
    if (el.getAttribute('src') !== src) { el.setAttribute('src', src); waits.push(el.decode().catch(() => {})); }
  }
  return Promise.all(waits);
};
</script></body></html>`;
}

async function openPage(dir, spec, slides, out) {
  const file = path.join(out, 'page.html');
  fs.writeFileSync(file, pageHtml(dir, spec, slides));
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: spec.size[0], height: spec.size[1] } });
  await page.goto(url(file), { waitUntil: 'load' }); // a real file (not setContent) so file:// images load
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.images].map((i) => i.decode().catch(() => {}))));
  return { browser, page };
}

async function renderFrames(page, spec, total, file) {
  const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(spec.fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', file], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((resolve, reject) => ff.on('close', (c) => (c ? reject(new Error(`ffmpeg exit ${c}`)) : resolve())));
  const write = (buf) => new Promise((resolve) => (ff.stdin.write(buf) ? resolve() : ff.stdin.once('drain', resolve)));
  const frames = Math.round(total * spec.fps);
  for (let f = 0; f < frames; f++) {
    await page.evaluate(([ms, fps]) => window.seek(ms, fps), [(f * 1000) / spec.fps, spec.fps]);
    await write(await page.screenshot({ type: 'jpeg', quality: 92 }));
    if (f % spec.fps === 0) process.stdout.write(`\rframes: ${(f / spec.fps).toFixed(0)}/${total.toFixed(0)} s`);
  }
  ff.stdin.end();
  await done;
  process.stdout.write('\n');
}

// Each voice at its slide time + optional music, quieter under the voice (ducking); all at -14 LUFS.
async function mix(dir, spec, slides, total, picture, file) {
  const said = slides.filter((s) => s.audio);
  const inputs = ['-i', picture, ...said.flatMap((s) => ['-i', s.audio])];
  const parts = said.map((s, k) => `[${k + 1}:a]adelay=${Math.round(s.voiceAt * 1000)}:all=1[v${k}]`);
  let f = said.length
    ? `${parts.join(';')};${said.map((_, k) => `[v${k}]`).join('')}amix=inputs=${said.length}:normalize=0,apad=whole_dur=${total}`
    : `anullsrc=r=48000:cl=stereo,atrim=0:${total}`;
  if (spec.music) {
    inputs.push('-stream_loop', '-1', '-i', path.join(dir, spec.music));
    f += `,asplit=2[voice][key];[${said.length + 1}:a]atrim=0:${total},volume=${spec.musicVolume ?? 0.25},afade=t=out:st=${Math.max(0, total - 2)}:d=2[bed];`
      + '[bed][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=900[duck];[voice][duck]amix=inputs=2:normalize=0';
  }
  f += ',loudnorm=I=-14:TP=-1.5:LRA=11[a]';
  await run(FFMPEG, ['-y', '-loglevel', 'error', ...inputs, '-filter_complex', f, '-map', '0:v', '-map', '[a]',
    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-t', String(total), '-movflags', '+faststart', file]);
}

(async () => {
  const [name, flag, arg] = process.argv.slice(2);
  if (!name) { console.log('usage: node render.js <project> [--stills | --frame <seconds>]'); process.exit(1); }
  const dir = path.resolve('projects', name);
  const out = path.join(dir, 'out');
  fs.mkdirSync(out, { recursive: true });
  const spec = { size: [1920, 1080], fps: 30, ...require(path.join(dir, 'video.js')) };
  const slides = await timeline(dir, spec, out);
  const total = slides.at(-1).end;
  const { browser, page } = await openPage(dir, spec, slides, out);
  try {
    if (flag === '--stills' || flag === '--frame') {
      const times = flag === '--frame' ? [[+arg, 'frame.jpg']] : slides.map((s, k) => [s.end - 0.3, `still-${k + 1}.jpg`]);
      for (const [t, f] of times) {
        await page.evaluate(([ms, fps]) => window.seek(ms, fps), [t * 1000, spec.fps]);
        await page.screenshot({ path: path.join(out, f), type: 'jpeg' });
      }
      console.log(`pictures → ${out}`);
      return;
    }
    const picture = path.join(out, 'picture.mp4');
    await renderFrames(page, spec, total, picture);
    await mix(dir, spec, slides, total, picture, path.join(out, 'video.mp4'));
    console.log(`${total.toFixed(1)} s → ${path.join(out, 'video.mp4')}`);
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e.message); process.exit(1); });
```

### `align_words.py` (word timing)

Uses Meta's MMS forced-alignment model (via `torchaudio`), on text romanized by `uroman`, so it works for
English, French, Arabic and most languages. CPU only. First run downloads the model (~1.2 GB) to `~/.cache/torch`.

```python
# Time of every word in a recording whose text we already know (forced alignment), for voices that don't report word
# times themselves (Gemini). Meta's MMS aligner (torchaudio MMS_FA, ~1.2 GB, downloaded once to ~/.cache/torch),
# on uroman-romanized text, CPU only.
# Usage: .venv/bin/python src/align_words.py <ffmpeg> <audio>  < text   →  JSON [{"t": start, "d": length, "w": word}]
# Words = the text split on spaces, punctuation stripped (harakat kept), same shape as src/tts_words.py prints.
import json
import re
import subprocess
import sys

import numpy as np
import torch
import torchaudio
import uroman

SR = 16000


def main(ffmpeg, audio):
    words = [w for w in (re.sub(r"[^\wً-ْٰ]", "", t) for t in sys.stdin.read().split()) if w]
    pcm = subprocess.run([ffmpeg, "-v", "error", "-i", audio, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    wave = torch.from_numpy(np.frombuffer(pcm, np.int16).astype(np.float32) / 32768).unsqueeze(0)

    bundle = torchaudio.pipelines.MMS_FA
    model, tokenizer, aligner = bundle.get_model(with_star=False), bundle.get_tokenizer(), bundle.get_aligner()
    roman = uroman.Uroman()
    # Romanized, only letters the model knows; a word with none left (rare) gets its time from its neighbours.
    keep = set(bundle.get_dict())
    latin = ["".join(c for c in roman.romanize_string(w).lower() if c in keep and c != "-") for w in words]
    idx = [k for k, r in enumerate(latin) if r]

    with torch.inference_mode():
        emission, _ = model(wave)
        spans = aligner(emission[0], tokenizer([latin[k] for k in idx]))
    step = wave.size(1) / emission.size(1) / SR
    times = {k: (s[0].start * step, s[-1].end * step) for k, s in zip(idx, spans)}
    out = []
    for k, w in enumerate(words):
        if k not in times:  # squeeze it in between its neighbours
            prev = out[-1]["t"] + out[-1]["d"] if out else 0.0
            nxt = next((times[j][0] for j in range(k + 1, len(words)) if j in times), prev)
            times[k] = (prev, max(prev, nxt))
        t0, t1 = times[k]
        out.append({"t": round(t0, 3), "d": round(t1 - t0, 3), "w": w})
    print(json.dumps(out, ensure_ascii=False))


main(*sys.argv[1:3])
```

### `tts.js` (optional: Gemini voice for every slide)

```js
// Gemini voice for every slide of projects/<name>/video.js that has `text` and an `audio` file not made yet.
// Usage: node tts.js <name> [voice]     (key GEMINI_API_KEY in .env; free tier ≈ 10 calls/day, 3/minute)
require('dotenv').config({ quiet: true });
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');
const { promisify } = require('util');
const FFMPEG = require('ffmpeg-static');

const run = promisify(execFile);
const MODEL = process.env.GEMINI_TTS_MODEL || 'gemini-3.8-flash-tts'; // check the current TTS model name in the Gemini docs
// Notes for the "director" (never spoken), then the transcript (the only part that is read).
// Without this exact layout, Gemini reads the notes aloud too.
const NOTES = `### DIRECTOR'S NOTES
Style: a clear, friendly presenter, confident and warm, like a good product demo.
Pace: natural, short pauses at commas and full stops.`;

async function speak(text, file, voice) {
  const body = {
    contents: [{ parts: [{ text: `${NOTES}\n\n#### TRANSCRIPT\n${text}` }] }],
    generationConfig: { responseModalities: ['AUDIO'], speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: voice } } } },
  };
  let res;
  for (let attempt = 1; ; attempt++) {
    res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`, {
      method: 'POST', headers: { 'x-goog-api-key': process.env.GEMINI_API_KEY, 'Content-Type': 'application/json' }, body: JSON.stringify(body),
    });
    if (res.status < 500 || attempt === 3) break; // 5xx now and then: retry; 429 = daily quota used, stop
    await new Promise((r) => setTimeout(r, 3000 * attempt));
  }
  const data = await res.json();
  if (!res.ok) throw new Error(`Gemini TTS ${res.status}: ${data.error?.message || 'no message'}`);
  const audio = data.candidates?.[0]?.content?.parts?.find((p) => p.inlineData)?.inlineData;
  if (!audio) throw new Error('Gemini returned no audio');
  // 24 kHz 16-bit mono PCM → mp3, silence trimmed at both ends
  const pcm = file.replace(/\.\w+$/, '.pcm');
  fs.writeFileSync(pcm, Buffer.from(audio.data, 'base64'));
  const trim = 'silenceremove=start_periods=1:start_threshold=-45dB';
  await run(FFMPEG, ['-y', '-loglevel', 'error', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', pcm,
    '-af', `${trim},areverse,${trim},areverse`, '-b:a', '128k', file]);
  fs.unlinkSync(pcm);
}

(async () => {
  const [name, voice = 'Charon'] = process.argv.slice(2);
  if (!name) { console.log('usage: node tts.js <project> [voice]'); process.exit(1); }
  if (!process.env.GEMINI_API_KEY) throw new Error('GEMINI_API_KEY missing in .env');
  const dir = path.resolve('projects', name);
  const todo = require(path.join(dir, 'video.js')).slides.filter((s) => s.audio && s.text && !fs.existsSync(path.join(dir, s.audio)));
  for (const [k, s] of todo.entries()) {
    if (k) await new Promise((r) => setTimeout(r, 21e3)); // stay under 3 calls per minute
    const file = path.join(dir, s.audio);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    await speak(s.text, file, voice);
    console.log(`✓ ${s.audio}`);
  }
  console.log(todo.length ? 'done — listen to every file before rendering' : 'nothing to voice (all audio files exist)');
})().catch((e) => { console.error(e.message); process.exit(1); });
```

Usage: `npm i dotenv`, put `GEMINI_API_KEY=...` in `.env`, then `node tts.js my-demo` (voices only the slides
whose `audio` file doesn't exist yet), or `node tts.js my-demo Kore` for another voice.

---

## 9. Remotion instead (optional)

[Remotion](https://www.remotion.dev) builds the video with React components and has a live preview with a
timeline (Remotion Studio). Good if you already know React.

```bash
npx create-video@latest        # pick a template (e.g. "Hello World" or "Blank")
npm run dev                    # opens Remotion Studio in the browser (live preview)
npx remotion render            # → out/video.mp4
```

- Animations use `useCurrentFrame()` + `interpolate()` / `spring()`; slides are `<Sequence from={…} durationInFrames={…}>`.
- Voice: `<Audio src={staticFile('voice/1.mp3')} />` inside each slide's `Sequence`. The word times from
  `align_words.py` (save its JSON in `public/`) work the same way: `frame = seconds * fps`.
- **License:** free for individuals and companies with up to 3 people; bigger companies need a paid
  company license. Check [remotion.dev/license](https://www.remotion.dev/license) before using it at work.

---

## 10. What makes a presentation video good

- **First 5 seconds:** say what the viewer gets ("In 90 seconds: what Taskly does and how to start").
- **One idea per slide**, ≤ 3 bullets, ≤ 6 words each. The voice explains; the screen shows the keywords.
- **Show, don't list:** a screen recording of the real thing beats a bullet about it. Zoom/crop recordings so
  text is readable on a phone.
- **Keep it moving:** a change on screen every 3–6 s (new bullet, new slide, the clip). Long static slides lose people.
- **Readable:** titles ≥ 70 px and body ≥ 40 px at 1080p; strong contrast; captions on for social media
  (most people watch muted).
- **Sound:** voice clear and loud (−14 LUFS overall), music low and calm, no music in the demo parts if it fights the voice.
- **End with one action:** "Try it free at …", a QR code or the link, held 3–4 s.
- **Length:** product demo 60–120 s; social post 30–60 s; class/pitch presentation up to 5–10 min.
- **Honest:** real numbers with a source, real screen recordings, no fake UI.
- **No AI-drawn text:** if you use AI images, ask for no text in them and put titles in with code (AI-drawn
  letters come out wrong).

## 11. Check before sharing

- [ ] Watched the whole `video.mp4` once with sound and once muted (captions readable?)
- [ ] Every bullet appears on its word, nothing appears before it's said
- [ ] No typos on screen (screen text ≠ voice text: proofread it separately)
- [ ] Screen recordings: no private data (emails, tokens, notifications) visible
- [ ] Music license OK; credit it in the description if the license asks
- [ ] Thumbnail: `--frame` at a strong moment, or a designed cover slide

## 12. Troubleshooting

| Problem | Fix |
|---|---|
| `Executable doesn't exist … chromium` | `npx playwright install chromium` (or set `CHROMIUM_PATH`) |
| `"word" is not said in: …` | The cue word isn't in `text`, or `text` doesn't match the audio. Use a word that's really in the line |
| Bullets appear at the wrong moment | `text` must be exactly what's said; delete `voice/N.mp3.words.json` to re-time that slide |
| Arabic text shows in the wrong order | `lang: 'ar', dir: 'rtl'` in `video.js` |
| Font missing / boxes instead of letters | `npm i @fontsource/inter @fontsource/cairo`; another language needs its own `@fontsource` font in `pageHtml` |
| Images don't show | Paths are relative to the project folder (`art/x.png`); check the file name's case |
| `edge-tts` 403 | `.venv/bin/pip install -U edge-tts` |
| Gemini `429` | Free daily quota used: wait until tomorrow |
| Out of memory | Close Chrome/other apps; render one video at a time |
| Render is slow | `--stills` while designing; render the full video only at the end; lower `fps` to 25 |
