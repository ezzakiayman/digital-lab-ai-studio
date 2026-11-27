# Dot-source this script in a Codex PowerShell session opened in the installed project.
$digitalLabProject = Split-Path -Parent $PSScriptRoot
$digitalLabRuntime = Join-Path (Split-Path -Parent $digitalLabProject) 'runtime'
$digitalLabNode = Join-Path $digitalLabRuntime 'node'
$digitalLabPython = Join-Path $digitalLabRuntime 'python'
$digitalLabFFmpeg = Join-Path $digitalLabRuntime 'ffmpeg\bin'
if (-not (Test-Path -LiteralPath (Join-Path $digitalLabNode 'node.exe'))) {
    throw 'The bundled Windows runtime is unavailable. Use the normal ZIP setup in START_HERE.md.'
}
$env:Path = "$digitalLabNode;$digitalLabPython;$digitalLabFFmpeg;$env:Path"
$digitalLabVoice = Join-Path $digitalLabProject '.venv\Scripts'
if (Test-Path -LiteralPath (Join-Path $digitalLabVoice 'python.exe')) {
    $env:Path = "$digitalLabVoice;$env:Path"
}
$env:PYTHONUTF8 = '1'
