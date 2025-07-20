@echo off
REM Script para gerar executáveis do Clearwave (Instalador e Monitoramento)
REM Requisitos: Python 3.10+, PyInstaller instalado

REM Instala PyInstaller se não estiver instalado
pip show pyinstaller >nul 2>&1
IF ERRORLEVEL 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

REM Gera o executável da interface (instalador)
echo Gerando instalador (interface)...
pyinstaller --onefile --windowed ..\app\ui\interface.py

REM Gera o executável do monitoramento
echo Gerando monitoramento...
pyinstaller --onefile --console ..\app\core\monitor.py

REM Mensagem final
echo Executáveis gerados na pasta dist\
pause
