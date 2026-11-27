# Démarrage depuis GitHub

Pour le dépôt privé et un autre compte, suivre **docs/github-reuse.md**. Le clone GitHub contient les sources, les deux compétences et une démonstration silencieuse ; les médias de production et les anciens installateurs mentionnés ci-dessous ne sont pas inclus.

# Start here · Digital Lab AI Studio

This folder carries the Digital Lab workflow to another user or account. It contains the Next.js studio, the Remotion renderer, editable JSON timelines, approved Digital Lab artwork, cached narration and two Codex skills. You can start a fresh chat with these files.

## Windows installer

Run Digital-Lab-Studio-Setup-x64.exe on an Intel or AMD x64 PC with Windows 10 version 1809 or later, or Windows 11. Use an internet connection for FFmpeg, JavaScript packages and the rendering browser. Setup installs into your Windows profile and opens the studio. To reopen it later, use **Digital Lab Studio** in the Start menu.

Use **Digital Lab Project for Codex** to find the installed project folder and open that folder in Codex with your account. Paste NEXT_AGENT_PROMPT.md into the new chat. In a PowerShell terminal inside the installed project, run `. .\scripts\use-windows-runtime.ps1` to load the supplied runtime for that session. The **Digital Lab Tools** shortcut opens an already configured terminal.

Use **Install Narration Tools** from the Start menu if you need to prepare, align or review new voice-over. It downloads Python speech dependencies into the project. Speech models are downloaded on first use. New Google narration also requires your own `GEMINI_API_KEY`. Use the cached sample to try previewing or rendering immediately.

Setup can be run again if a download fails. See setup.log in the install folder for the error. The installed project and your work stay on disk after uninstall.

## Produce videos from the ZIP

1. Extract the ZIP. Sign in to Codex with the receiving account, open the extracted folder as the project’s primary folder, and start a chat there.
2. Paste the contents of NEXT_AGENT_PROMPT.md into the chat. For a new video, attach or copy your storyboard PPTX into the project and tell Codex which video to produce.
3. Install Node.js (tested with 22.18.0), Python 3.12 and FFmpeg with ffprobe on PATH. Windows is the verified environment for the Arial and Cambria Math charter. PowerPoint is used by the optional Windows script for slide preview exports.
4. From the project root, verify the files and try a cached lesson. The first Remotion render can download a headless browser.

```powershell
python scripts/verify-transfer.py
npm ci
node scripts/doctor.mjs
npm run render:storyboards -- --stills like-terms
```

Use `npm run dev` for the studio and `npm run render:storyboards -- like-terms` to render the 2AC lesson on like terms to MP4. In the reusable kit, you can also open the finished sample at `outputs/n2-sem2-vdp2/P1_MATHS_N2_SEM2_VDP2.mp4`.

## New narration and new lessons

Cached narration works without a key. For new Google Gemini Kore voice, configure your own `GEMINI_API_KEY` in the environment available to the rendering agent. Keep the key out of chat, project files and shared archives. Follow [the production runbook](docs/production-runbook.md) for the speech dependencies, source review, editing, alignment, reflection pauses and export checks. Every new storyboard needs a reviewed scene plan.

The bundled skills can be read directly from `skill/`. To make them available to other Codex projects on Windows, run `powershell -NoProfile -File scripts/install-project-skills.ps1`. It checks for conflicting installed copies. Start a fresh Codex chat after installation.

## Use the workflow in ChatGPT

For storyboard review and scene planning, create a ChatGPT Project and add AGENTS.md, docs/production-runbook.md and the storyboard you want to work on. Use the local Codex project for the Remotion preview and 1080p export.

> Review the attached storyboard using the Digital Lab rules in AGENTS.md. Flag any mismatch between the stated objective and the mathematics taught. Create a scene-by-scene plan with the source slide numbers, on-screen text and formulas, French narration, motion cues and reflection pauses.

## Share with a colleague

Send the ZIP privately to a colleague authorized to use the Digital Lab assets. The reusable kit contains one finished example and the pronunciation reference. It omits the original storyboard decks, the full-length source reference video, credentials, dependency folders and model caches. The previous full private snapshot has a wider media selection. TRANSFER_MANIFEST.json records which files are included. Older handoff entries may refer to artifacts on the original workstation.
