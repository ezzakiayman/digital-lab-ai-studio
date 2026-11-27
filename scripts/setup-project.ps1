param([switch]$InstallSkills)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
foreach($command in @('node','npm','python','ffmpeg','ffprobe')){
 if(-not (Get-Command $command -ErrorAction SilentlyContinue)){throw "Install $command and open a new terminal. See docs/github-reuse.md."}
}
if([int]((& node -p 'process.versions.node.split(".")[0]')) -lt 22){throw 'Node.js 22 or newer is required.'}
& npm ci
if($LASTEXITCODE -ne 0){throw 'npm ci failed'}
& node scripts/doctor.mjs --portable
if($LASTEXITCODE -ne 0){throw 'Portable preflight failed'}
if($InstallSkills){& (Join-Path $PSScriptRoot 'install-project-skills.ps1')}
Write-Output 'Ready. Run npm run dev for the studio or npm run render:demo for a credential-free 1080p example.'
