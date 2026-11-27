[Setup]
AppId=DigitalLabAIStudio
AppName=Digital Lab AI Studio
AppVersion=1.0
AppPublisher=Digital Lab
DefaultDirName={localappdata}\Programs\Digital Lab Studio
DefaultGroupName=Digital Lab Studio
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64os
ArchitecturesInstallIn64BitMode=x64os
MinVersion=10.0.17763
OutputDir={#OutputDir}
OutputBaseFilename=Digital-Lab-Studio-Setup-x64
Compression=lzma2/fast
SolidCompression=no
WizardStyle=modern
ExtraDiskSpaceRequired=2300000000

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"

[Files]
Source: "{#PayloadDir}\runtime\*"; DestDir: "{app}\runtime"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "windows-launcher.ps1"; DestDir: "{app}\launcher"; Flags: ignoreversion
Source: "{#PayloadDir}\project.zip"; Flags: dontcopy nocompression

[Icons]
Name: "{group}\Digital Lab Studio"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""{app}\launcher\windows-launcher.ps1"" -Action Studio"; WorkingDir: "{app}"
Name: "{group}\Digital Lab Project for Codex"; Filename: "{win}\explorer.exe"; Parameters: """{app}\project"""; WorkingDir: "{app}"
Name: "{group}\Digital Lab Tools"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -NoExit -ExecutionPolicy Bypass -File ""{app}\launcher\windows-launcher.ps1"" -Action Tools"; WorkingDir: "{app}"
Name: "{group}\Install Narration Tools"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -NoExit -ExecutionPolicy Bypass -File ""{app}\launcher\windows-launcher.ps1"" -Action VoiceTools"; WorkingDir: "{app}"
Name: "{userdesktop}\Digital Lab Studio"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""{app}\launcher\windows-launcher.ps1"" -Action Studio"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""{app}\launcher\windows-launcher.ps1"" -Action Studio"; Description: "Open Digital Lab Studio"; Flags: postinstall nowait skipifsilent runhidden; Check: SetupComplete

[Code]
var
  DependenciesReady: Boolean;

function SetupComplete: Boolean;
begin
  Result := DependenciesReady;
end;

function GetCustomSetupExitCode: Integer;
begin
  if DependenciesReady then
    Result := 0
  else
    Result := 10;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Arguments: String;
  ResultCode: Integer;
begin
  if CurStep <> ssPostInstall then
    exit;

  WizardForm.StatusLabel.Caption := 'Preparing the studio and downloading rendering tools...';
  WizardForm.ProgressGauge.Style := npbstMarquee;
  Arguments := '-NoProfile -ExecutionPolicy Bypass -File "' +
    ExpandConstant('{app}\launcher\windows-launcher.ps1') + '" -Action Install';

  if not DirExists(ExpandConstant('{app}\project')) then
  begin
    ExtractTemporaryFile('project.zip');
    Arguments := Arguments + ' -Archive "' + ExpandConstant('{tmp}\project.zip') + '"';
  end;

  DependenciesReady := Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'),
    Arguments, ExpandConstant('{app}'), SW_HIDE, ewWaitUntilTerminated, ResultCode)
    and (ResultCode = 0);
  if not DependenciesReady then
    SuppressibleMsgBox('Digital Lab setup could not finish. See setup.log in the installation folder, then run Setup again to resume.',
      mbError, MB_OK, IDOK);
end;
