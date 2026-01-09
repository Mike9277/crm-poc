@echo off
REM Script per avviare il frontend React
REM Richiede Node.js installato localmente

REM Aggiungi Node.js al PATH
set PATH=%PATH%;C:\Program Files\nodejs

cd /d "%~dp0frontend"

echo Controllando se node_modules esiste...
if not exist node_modules (
    echo Installando dipendenze npm...
    call npm install --no-audit --no-fund --prefer-offline
) else (
    echo node_modules trovato, skipping install
)

echo.
echo Avviando Vite dev server...
echo Frontend sara disponibile su: http://localhost:5173
echo API URL: http://localhost:8000/api
echo.
call npm run dev

npm run dev

pause
