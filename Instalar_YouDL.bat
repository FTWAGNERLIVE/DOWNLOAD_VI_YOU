@echo off
title Instalador do YouDL
color 0b

echo ===================================================
echo               BEM-VINDO AO YouDL
echo             Assistente de Instalacao
echo ===================================================
echo.
echo Este programa instalara o YouDL e todas as suas 
echo dependencias no seu computador.
echo.

:: Define a pasta padrao no PC da pessoa
set "DEFAULT_DIR=%LOCALAPPDATA%\YouDL"

:ASK_PATH
echo Por padrao, o app sera instalado de forma secreta em:
echo [%DEFAULT_DIR%]
echo.
echo Se desejar instalar em outra pasta (ex: C:\Meus_Programas\YouDL), 
echo digite o caminho completo abaixo. 
echo.
echo (Se quiser manter a pasta padrao, APENAS APERTE ENTER)
set /p USER_DIR="Pasta Destino > "

:: Se o usuario nao digitou nada e so apertou enter, assume a default
if "%USER_DIR%"=="" set "USER_DIR=%DEFAULT_DIR%"

echo.
echo ===================================================
echo Preparando instalacao na pasta: 
echo %USER_DIR%
echo ===================================================
echo.

:: Criar a pasta escolhida (e ignora erro se ja existir)
if not exist "%USER_DIR%" mkdir "%USER_DIR%" 2>nul

echo [1/3] Copiando arquivos essenciais...
:: O comando XCOPY copia todo o app (da pasta dist\YouDL) para a pasta que o usuario escolheu
xcopy /E /I /Y "dist\YouDL\*" "%USER_DIR%\" >nul

if errorlevel 1 (
    color 4f
    echo.
    echo ERRO CRITICO: Nao encontramos os arquivos originais.
    echo Certifique-se de que voce rodou o 'build_app.bat' corretamente
    echo e de que a pasta 'dist/YouDL' existe ao lado deste instalador.
    echo.
    pause
    exit /b
)

echo [2/3] Apagando atalhos e atalhos repetidos antigos...
:: Apaga atalhos que tenham 'YouDL' no nome, limpando a tela do usuario
del "%USERPROFILE%\Desktop\YouDL*.lnk" 2>nul

echo [3/3] Criando o novo atalho com seu Icone YDL...
:: Usamos um micro-script invisivel do Windows para forcar a criacao de atalho elegante
set "VBS_SCRIPT=%TEMP%\create_shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = "%USERPROFILE%\Desktop\YouDL.lnk" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%USER_DIR%\YouDL.exe" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%USER_DIR%" >> "%VBS_SCRIPT%"
echo oLink.Description = "YouDL - Baixar Videos em 4K e MP3" >> "%VBS_SCRIPT%"
echo oLink.IconLocation = "%USER_DIR%\YouDL.exe, 0" >> "%VBS_SCRIPT%"
echo oLink.Save >> "%VBS_SCRIPT%"
cscript /nologo "%VBS_SCRIPT%"
del "%VBS_SCRIPT%"

echo.
color 0a
echo ===================================================
echo               INSTALACAO CONCLUIDA!
echo ===================================================
echo O aplicativo YouDL esta pronto para ser usado.
echo Va para a sua Area de Trabalho e confira o seu
echo lindo icone!
echo.
pause
