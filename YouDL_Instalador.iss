[Setup]
; INFORMACOES GERAIS
AppName=YouDL
AppVersion=1.0.0
AppPublisher=YouDL Oficial
DefaultDirName={autopf}\YouDL
DefaultGroupName=YouDL
UninstallDisplayIcon={app}\YouDL.exe

; EXECUTAVEL DE SAIDA E VISUAL
OutputBaseFilename=Instalar_YouDL
OutputDir=.
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=lowest
SetupIconFile=icon.ico
WizardSmallImageFile=wizard_small.bmp
WizardImageFile=wizard_large.bmp

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na Area de Trabalho"; GroupDescription: "Atalhos adicionais:"

[Files]
; Copia tudo da sua pasta de build para a maquina da pessoa
Source: "dist\YouDL\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Cria atalhos e busca sozinho o icone rosa embuitido no sistema
Name: "{autodesktop}\YouDL"; Filename: "{app}\YouDL.exe"; Tasks: desktopicon
Name: "{group}\YouDL"; Filename: "{app}\YouDL.exe"
Name: "{group}\Desinstalar YouDL"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\YouDL.exe"; Description: "Iniciar o YouDL agora"; Flags: nowait postinstall skipifsilent
