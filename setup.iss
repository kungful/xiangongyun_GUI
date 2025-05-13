[Setup]
AppName=XGC
AppVersion=1.0
AppId={{XGC_AppId}}
DefaultDirName={pf}\XGC
DefaultGroupName=XGC
UninstallDisplayIcon={app}\main.exe
Compression=lzma
SolidCompression=yes
OutputDir=.
OutputBaseFilename=仙宫云windows版
SetupIconFile=app.ico
PrivilegesRequired=admin
CloseApplications=yes
CloseApplicationsFilter=main.exe
UsePreviousAppDir=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\XGC"; Filename: "{app}\main.exe"
Name: "{commondesktop}\XGC"; Filename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "Run application"; Flags: postinstall nowait skipifsilent

[UninstallRun]
Filename: "{uninstallexe}"; Parameters: "/SILENT"
