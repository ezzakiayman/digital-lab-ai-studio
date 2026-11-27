# Digital Lab VDP — local video generator (MVP)

This prototype reads a PowerPoint storyboard, extracts all slide text, groups the supplied negative-number comparison lesson into six reusable animated scenes, and exports an MP4 and editable JSON scene manifest. It does not use Higgsfield or upload media.

Run:

```bash
pip install -r requirements.txt
python generator.py --pptx ../upload/P1_MATHS_N1_SEM1_VDP4.pptx --out preview.mp4 --manifest scenes.json
```

Requires `ffmpeg`. Output is silent, 1280×720, 24 fps; narration text is preserved in `scenes.json`. For a truly automated production tool, the next stages are approved French TTS, word-aligned timing, automatic lesson interpretation for *other* mathematical topics, exact fonts/brand assets, and a batch UI. The current colors and styles are approximations from reference screenshots, **not pixel-verified copies** of the existing video.
