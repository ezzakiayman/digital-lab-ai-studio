param([string]$Destination,[switch]$UpdateExisting,[switch]$DryRun)
$ErrorActionPreference='Stop'
if(-not $Destination){
 $codexRoot=$env:CODEX_HOME
 if(-not $codexRoot){$codexRoot=Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex'}
 $Destination=Join-Path $codexRoot 'skills'
}
$projectRoot=Split-Path $PSScriptRoot -Parent
function Get-SkillDigest([string]$FilePath){
 $algorithm=[Security.Cryptography.SHA256]::Create()
 try {return [Convert]::ToBase64String($algorithm.ComputeHash([IO.File]::ReadAllBytes($FilePath)))}
 finally {$algorithm.Dispose()}
}
$copies=@()
foreach($skillName in @('digital-lab-project','presentation-video')){
 $sourceRoot=Join-Path (Join-Path $projectRoot 'skill') $skillName
 foreach($file in Get-ChildItem -LiteralPath $sourceRoot -Recurse -File){
  $relative=$file.FullName.Substring($sourceRoot.Length).TrimStart('\','/')
  if($relative -match '(^|[\\/])(private|\.env)([\\/]|$)'){throw 'Private content is not an installable skill resource'}
  $target=Join-Path (Join-Path $Destination $skillName) $relative
  if(Test-Path -LiteralPath $target){
   $same=(Get-SkillDigest $target) -eq (Get-SkillDigest $file.FullName)
   if(-not $same -and -not $UpdateExisting){throw "Existing skill differs: $target. Review it before using -UpdateExisting."}
  }
  $copies+=@{Source=$file.FullName;Target=$target}
 }
}
foreach($copy in $copies){
 if(-not $DryRun){
  New-Item -ItemType Directory -Force -Path (Split-Path $copy.Target -Parent) | Out-Null
  Copy-Item -LiteralPath $copy.Source -Destination $copy.Target -Force
 }
}
Write-Output "Validated $($copies.Count) skill files for $Destination; dry run: $DryRun"
