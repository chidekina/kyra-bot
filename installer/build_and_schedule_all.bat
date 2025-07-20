@echo off
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

REM Agenda a tarefa do monitor para rodar diariamente às 10h
echo Agendando tarefa do monitor...
set MONITOR_EXE=%~dp0dist\monitor.exe
schtasks /create /tn "ClearwaveEnvio" /tr "%MONITOR_EXE%" /sc daily /st 10:00

REM Mensagem final
echo Executáveis gerados na pasta dist\
pause

python3 --version