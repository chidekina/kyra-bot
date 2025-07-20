@echo off
schtasks /create /tn "ClearwaveEnvio" /tr "python C:\Clearwave\app\core\monitor.py" /sc daily /st 10:00