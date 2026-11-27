param(
    [ValidateSet('Install','Studio','Tools','VoiceTools')]
    [string]$Action = 'Studio',
    [string]$Archive,
    [ValidateRange(1024,65535)]
    [int]$Port = 3235,
    [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'
$appRoot = Split-Path -Parent $PSScriptRoot
$project = Join-Path $appRoot 'project'
$runtime = Join-Path $appRoot 'runtime'
$nodeRoot = Join-Path $runtime 'node'
$pythonRoot = Join-Path $runtime 'python'
$ffmpegRoot = Join-Path $runtime 'ffmpeg'
$node = Join-Path $nodeRoot 'node.exe'
$python = Join-Path $pythonRoot 'python.exe'
$npm = Join-Path $nodeRoot 'node_modules\npm\bin\npm-cli.js'
$env:Path = "$nodeRoot;$pythonRoot;$ffmpegRoot\bin;$env:Path"
$env:PYTHONUTF8 = '1'
$env:NEXT_TELEMETRY_DISABLED = '1'
$env:NO_PROXY = "$env:NO_PROXY,localhost,127.0.0.1"

function Invoke-Checked([string]$Program, [string[]]$Arguments) {
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$(Split-Path -Leaf $Program) returned exit code $LASTEXITCODE."
    }
}

function Get-Sha256([string]$File) {
    $stream = [IO.File]::OpenRead((Resolve-Path -LiteralPath $File).Path)
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try {
        return [BitConverter]::ToString($algorithm.ComputeHash($stream)).Replace('-', '')
    }
    finally {
        $algorithm.Dispose()
        $stream.Dispose()
    }
}

function Remove-SetupStage([string]$Stage, [string]$Parent) {
    $directory = Get-Item -LiteralPath $Stage -ErrorAction SilentlyContinue
    if ($directory -and $directory.Parent.FullName -eq (Resolve-Path -LiteralPath $Parent).Path -and
        -not ($directory.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        Remove-Item -LiteralPath $directory.FullName -Recurse -Force
    }
}

function Initialize-Project {
    if (Test-Path -LiteralPath $project -PathType Container) {
        return
    }
    if (-not $Archive) {
        throw 'The project archive is missing. Run Digital Lab Studio Setup again.'
    }

    $stage = Join-Path $appRoot ('.project-' + [guid]::NewGuid())
    try {
        [IO.Compression.ZipFile]::ExtractToDirectory($Archive, $stage)
        $stagedProject = Join-Path $stage 'project'
        Invoke-Checked $python @((Join-Path $stagedProject 'scripts\verify-transfer.py'))
        Move-Item -LiteralPath $stagedProject -Destination $project
    }
    finally {
        Remove-SetupStage $stage $appRoot
    }
}

function Install-FFmpeg {
    if ((Test-Path -LiteralPath (Join-Path $ffmpegRoot 'bin\ffmpeg.exe')) -and
        (Test-Path -LiteralPath (Join-Path $ffmpegRoot 'bin\ffprobe.exe'))) {
        return
    }

    $zipName = 'ffmpeg-8.1.2-essentials_build.zip'
    $expected = 'db580001caa24ac104c8cb856cd113a87b0a443f7bdf47d8c12b1d740584a2ec'
    $stage = Join-Path $runtime ('.ffmpeg-' + [guid]::NewGuid())
    New-Item -ItemType Directory -Path $stage | Out-Null
    try {
        $zip = Join-Path $stage $zipName
        Write-Host 'Downloading FFmpeg and ffprobe.'
        $sources = @(
            "https://github.com/GyanD/codexffmpeg/releases/download/8.1.2/$zipName",
            "https://www.gyan.dev/ffmpeg/builds/packages/$zipName"
        )
        foreach ($url in $sources) {
            & "$env:SystemRoot\System32\curl.exe" --fail --location --silent --show-error `
                --connect-timeout 20 --speed-limit 1024 --speed-time 25 --max-time 600 $url -o $zip
            if ($LASTEXITCODE -eq 0) { break }
        }
        if ($LASTEXITCODE -ne 0) { throw 'FFmpeg could not be downloaded. Check the network and run Setup again.' }
        if ((Get-Sha256 $zip) -ne $expected) {
            throw 'FFmpeg download checksum mismatch.'
        }
        [IO.Compression.ZipFile]::ExtractToDirectory($zip, $stage)
        $extracted = Join-Path $stage 'ffmpeg-8.1.2-essentials_build'
        foreach ($exe in @('ffmpeg.exe','ffprobe.exe')) {
            if (-not (Test-Path -LiteralPath (Join-Path $extracted "bin\$exe") -PathType Leaf)) {
                throw "The FFmpeg archive is missing $exe."
            }
        }
        if (Test-Path -LiteralPath $ffmpegRoot) {
            throw "The FFmpeg folder is incomplete: $ffmpegRoot. Move it aside before retrying."
        }
        [IO.Directory]::Move($extracted, $ffmpegRoot)
    }
    finally {
        Remove-SetupStage $stage $runtime
    }
}

function Install-Studio {
    Start-Transcript -Path (Join-Path $appRoot 'setup.log') | Out-Null
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        Initialize-Project
        Install-FFmpeg
        Set-Location -LiteralPath $project

        $receipt = Join-Path $runtime 'npm-lock.sha256'
        $lockHash = Get-Sha256 'package-lock.json'
        $installedHash = if (Test-Path -LiteralPath $receipt) { Get-Content -LiteralPath $receipt }
        if ($installedHash -ne $lockHash -or -not (Test-Path -LiteralPath 'node_modules\next\package.json')) {
            Write-Host 'Installing locked JavaScript packages.'
            Invoke-Checked $node @($npm,'ci','--no-audit','--no-fund','--fetch-retries=2')
            Set-Content -LiteralPath $receipt -Value $lockHash -Encoding ASCII
        }
        Invoke-Checked $node @('scripts/doctor.mjs')
        Write-Host 'Checking the Remotion rendering browser.'
        Invoke-Checked $node @('-e', "require('@remotion/renderer').ensureBrowser().then(s=>{if(!s.path) throw Error(s.type)}).catch(e=>{console.error(e);process.exitCode=1})")
    }
    catch {
        Write-Host $_.Exception.Message
        throw
    }
    finally {
        Stop-Transcript | Out-Null
    }
}

function Test-StudioResponse([string]$Address) {
    try {
        $response = Invoke-WebRequest -Uri $Address -UseBasicParsing -TimeoutSec 2
        if ($response.Content -notmatch '<title>Digital Lab .* AI Studio</title>') {
            throw "Port $Port is already in use by another application."
        }
        return $true
    }
    catch [System.Net.WebException] {
        return $false
    }
}

function Open-Studio {
    Set-Location -LiteralPath $project
    if (-not (Test-Path -LiteralPath 'node_modules\next\dist\bin\next')) {
        throw 'The studio dependencies are missing. Run Digital Lab Studio Setup again.'
    }
    $address = "http://127.0.0.1:$Port/"
    if (-not (Test-StudioResponse $address)) {
        $logs = Join-Path $appRoot 'logs'
        New-Item -ItemType Directory -Path $logs -Force | Out-Null
        $server = Start-Process -FilePath $node -ArgumentList @(
            'node_modules/next/dist/bin/next','dev','--hostname','127.0.0.1','--port',"$Port"
        ) -WorkingDirectory $project -WindowStyle Hidden -PassThru `
            -RedirectStandardOutput (Join-Path $logs 'studio.log') `
            -RedirectStandardError (Join-Path $logs 'studio-error.log')

        $deadline = [DateTime]::UtcNow.AddSeconds(60)
        do {
            Start-Sleep -Milliseconds 500
            if ($server.HasExited) { throw "Studio stopped. See $logs\studio-error.log." }
            if (Test-StudioResponse $address) { break }
        } while ([DateTime]::UtcNow -lt $deadline)
        if (-not (Test-StudioResponse $address)) {
            throw "The studio took too long to start. See $logs\studio.log."
        }
    }
    if (-not $NoBrowser) {
        Start-Process $address
    }
    Write-Host "Digital Lab Studio is ready at $address"
}

try {
    switch ($Action) {
        'Install' { Install-Studio }
        'Studio' { Open-Studio }
        'Tools' {
            Set-Location -LiteralPath $project
            if (Test-Path -LiteralPath '.venv\Scripts\python.exe') {
                $env:Path = "$(Join-Path $project '.venv\Scripts');$env:Path"
            }
            Write-Host "Digital Lab project: $project"
            Write-Host 'Open START_HERE.md for setup and NEXT_AGENT_PROMPT.md for Codex.'
            Write-Host 'Render the included sample: npm.cmd run render:storyboards -- like-terms'
        }
        'VoiceTools' {
            Set-Location -LiteralPath $project
            Invoke-Checked $python @('-m','venv','.venv')
            $voicePython = Join-Path $project '.venv\Scripts\python.exe'
            Invoke-Checked $voicePython @('-m','pip','install','-r','requirements-video.txt')
            Invoke-Checked $node @('scripts/doctor.mjs','--full','--python',$voicePython)
            Write-Host 'Narration tools are ready. See START_HERE.md for credentials and the production workflow.'
        }
    }
}
catch {
    if ($Action -eq 'Studio' -and -not $NoBrowser) {
        Add-Type -AssemblyName System.Windows.Forms
        [Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Digital Lab Studio') | Out-Null
    }
    Write-Error -Message $_.Exception.Message -ErrorAction Continue
    if ($Action -in @('Install','Studio')) {
        exit 1
    }
}
