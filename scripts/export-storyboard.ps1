param(
 [Parameter(Mandatory=$true)][string]$Storyboard,
 [Parameter(Mandatory=$true)][string]$OutputDirectory,
 [int]$Width=1600,
 [int]$Height=900
)
$ErrorActionPreference='Stop'
$source=(Resolve-Path -LiteralPath $Storyboard).Path
$destination=[IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Force -Path $destination | Out-Null
$application=$null; $presentation=$null
try {
 $application=[Activator]::CreateInstance([Type]::GetTypeFromProgID('PowerPoint.Application'))
 $presentation=$application.Presentations.Open($source,-1,0,0)
 $count=$presentation.Slides.Count
 $presentation.Export($destination,'PNG',$Width,$Height)
 Write-Output "Exported $count read-only storyboard slides to $destination"
} finally {
 if($null -ne $presentation){$presentation.Close()}
 if($null -ne $application -and $application.Presentations.Count -eq 0){$application.Quit()}
}
