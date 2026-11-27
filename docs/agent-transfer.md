# Install Digital Lab Studio on Windows — 2026-11-11

The x64 Windows installer is the simplest handoff for colleagues. It embeds the reusable snapshot and portable Node.js and Python. Per-user setup downloads hash-checked FFmpeg, installs locked npm packages, checks project assets and prepares Remotion’s rendering browser. It needs internet for setup. The launcher listens on 127.0.0.1:3235 and keeps logs in the app folder. See START_HERE.md for the studio, project, terminal and optional narration shortcuts.

The default project folder is `%LOCALAPPDATA%\Programs\Digital Lab Studio\project`. Setup reuses an existing project folder so colleagues keep their changes. An uninstall keeps the project folder. For a fresh copy, choose a separate installation directory. Optional narration tooling uses a project-local Python virtual environment and model downloads on first use. The recipient supplies their own Gemini credential and uses their own Codex account.

Rebuild the unsigned EXE from the source project with Python 3.12 and the Inno Setup 7 compiler. Use a build cache outside the source project.

```powershell
python scripts/windows/build-installer.py --iscc "C:\path\to\ISCC.exe" --work-dir "../DigitalLabSetupBuild" --output-dir "../DigitalLabSetupRelease"
```

The builder reuses the same snapshot selection as the ZIP, checks pinned Node/Python downloads and writes an EXE checksum. The FFmpeg archive is fetched from its distributor during installation. [Inno Setup compiler](https://jrsoftware.org/isdl.php) · [Node.js release checksums](https://nodejs.org/download/release/v22.23.3/SHASUMS256.txt) · [Python runtime](https://www.nuget.org/packages/python/3.12.10) · [FFmpeg release builds](https://www.gyan.dev/ffmpeg/builds/)

## Reuse from another user or account — 2026-11-11

Use START_HERE.md for recipient setup and NEXT_AGENT_PROMPT.md for the first Codex message. Sign in with the receiving account and open the extracted folder as the primary Codex project folder. A ChatGPT Project can use AGENTS.md and docs/production-runbook.md for storyboard review and scene planning. Render from the local project.

Build the reusable kit with the project's Python interpreter. Choose a destination and ZIP outside the source workspace.

```powershell
python scripts/build-transfer.py --reusable --destination "../Digital-Lab-Codex-Kit" --archive "../Digital-Lab-Codex-Kit.zip"
```

The reusable kit retains the application, scene plans, timelines, audio caches, both skills, visual references and one finished 2AC like-terms lesson. It omits the original PPTX decks and full-length source reference video. Attach a new deck when commissioning a new video. Share the kit privately with authorized Digital Lab collaborators. A second build can use `--refresh` on a marked destination of the same transfer type. Cached renders work without API credentials. See the latest PROJECT_HANDOFF.md entry for verification and environment details.

## Earlier full private transfer — 2026-11-05

The user requested a project containing the skills and detailed video-generation workflow. Created a separate local project at C:/Users/EDITO/Desktop/Digital-Lab-Codex-Project, with a private portable ZIP alongside it. This creates a transferable project folder; it does not create/message another Codex chat or publish a repository. Open that folder in the receiving Codex and paste NEXT_AGENT_PROMPT.md. START_HERE.md gives installation and first-render instructions; docs/production-runbook.md supplies the complete workflow and its boundaries. AGENTS.md carries the saved user contract and handoff-maintenance requirements.

Included snapshot: application source, package lock, all current plans/timelines, the complete digital-lab-project and presentation-video skills/references, exact target/question artwork, original and paced cached audio/alignment receipts, four source decks with extracted mathematics/notes/slide previews, independent ASR evidence, original N1 reference video and four selected final example exports. Cached renders require no TTS calls. The packaging manifest records actual paths, sizes and SHA-256 hashes; user-renamed PPCM/prime MP4 names are preserved and documented rather than silently asserting historical names still exist.

Excluded: API keys, .env files, private folders, DPAPI bundles, node_modules, .next, Python/model caches and duplicate obsolete exports. Source media stays ignored by Git and is included only for this private handoff. The archive builder uses an explicit file selection, rejects private/symlink/credential-shaped content, verifies destination hashes and ZIP integrity, and writes a separate ZIP SHA-256 file. It does not recursively remove directories. Refresh is allowed only for a marked generated snapshot.

Portability fixes in source: Gemini key lookup resolves CODEX_HOME or the current user's home, supports securely provided GEMINI_API_KEY before any DPAPI attempt, locates the current profile's bundled PowerShell or normal Windows PowerShell, and supports GEMINI_POWERSHELL_EXE. Unix/new-machine generation uses the environment credential; the originating encrypted bundle is not copied. Speech-review caches use Path.home() instead of requiring USERPROFILE. A read-only model-list probe passed with the existing credential provider; no new voice was generated for the transfer.

New helpers: scripts/doctor.mjs checks Node/FFmpeg/ffprobe, installed packages, exact question hash and all 38 timeline audio references, optionally Python video imports; inspect-storyboard.py extracts text, OMML, geometry and notes; export-storyboard.ps1 exports a PPTX read-only to PNG; install-project-skills.ps1 copies only the bundled skill resources with preflight conflict detection, dry-run and explicit update options; verify-transfer.py checks the snapshot manifest; build-transfer.py produces the snapshot/ZIP/checksum. requirements-video.txt records the working Python versions. The generic renderer now accepts --out=<fresh-directory> for sequential batch jobs without colliding with earlier outputs.

Verified on the same Windows workstation in a separate project folder with newly installed JavaScript dependencies: npm ci installed 264 packages from the existing lockfile; all 14 tests and typecheck passed; Next production build passed; the generic renderer downloaded its own fresh 131 MB headless browser and rendered the fractions opening via --still/--out. The resulting PNG was visually inspected. Full desktop/mobile UI checks passed from the separate project's production server. The preflight found both approved assets and all 38 timeline audio references. Snapshot file integrity passed. Python tool imports passed in the existing Python environment (not a newly provisioned Python environment). Source inspection and PowerPoint export read the 28-slide fractions deck successfully. Skill install/dry-run/identical-file handling passed; a differing-file test refused overwrite and preserved the existing file; explicit UpdateExisting then passed. The installer initially exposed a legacy Get-FileHash availability issue; replaced it with .NET SHA-256 and retested successfully.

No Linux/macOS, alternate-font, new-account credential or fresh Python-environment certification is claimed. Model/browser downloads require network on first use; Python alignment/ASR models and installed dependencies are not inside the ZIP. The source videos are the existing delivered artifacts, not newly rendered full lessons for this transfer. Broad automatic interpretation, Manim workers, persistent queues and comprehensive pronunciation/pixel-fidelity checks remain pending. No new deployment, remote publication or GitHub sync occurred; the matching local codex-skills directory is still not a Git repository.

Rebuild privately after a future verified change using scripts/build-transfer.py with --destination outside the source workspace, --reference-video when the original source is elsewhere, --archive <zip-path> and --refresh only for an existing marked snapshot. Maintain both skill copies and the project handoff first. Runtime/test extras installed in the destination are not added to the archive because selection is explicit. Run python scripts/verify-transfer.py in the receiving folder before editing.
