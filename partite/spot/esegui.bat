@echo off
setlocal

REM Avvia server HTTP in background con Python e salva il PID
start "" /B cmd /c "python -m http.server 8080 >nul 2>&1"
set "pid_file=server_pid.txt"

REM Salva il PID del server HTTP
for /f "tokens=2 delims==; " %%A in ('wmic process where "CommandLine like '%%http.server%%'" get ProcessId /value ^| find "="') do (
    echo %%A > %pid_file%
)

timeout /t 2 >nul
start "" http://localhost:8080/search.html

echo.
echo Premi un tasto per terminare il server HTTP e chiudere...
pause >nul

REM Chiude il server HTTP
for /f %%P in (%pid_file%) do taskkill /PID %%P >nul 2>&1
del %pid_file%

echo Server terminato.
