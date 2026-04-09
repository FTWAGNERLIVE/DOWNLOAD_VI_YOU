@echo off
echo ==========================================
echo Instalando dependencias extras...
echo ==========================================
pip install pywebview pyinstaller pillow

echo.
echo ==========================================
echo Gerando o icone profissional YDL...
python convert_icon.py

echo.
echo Limpando cache antigo para forcar o novo icone...
if exist "YouDL.spec" del "YouDL.spec"
if exist "build" rmdir /s /q "build"

echo.
echo ==========================================
echo Construindo o aplicativo YouDL...
echo Isso pode levar alguns minutos...
python -m PyInstaller --name "YouDL" --noconsole --icon=icon.ico --add-data "web/templates;web/templates" --clean desktop.py

echo.
echo ==========================================
echo Concluido! Seu aplicativo esta dentro da pasta 'dist'
echo ==========================================
pause
