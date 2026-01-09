@echo off
REM ================================
REM   CRM POC - Startup Script
REM ================================

echo ================================
echo    CRM POC - Startup Script
echo ================================
echo.

REM Aggiungi Node.js al PATH
set PATH=%PATH%;C:\Program Files\nodejs

REM ================================
REM 1. Start Docker (Backend + MySQL)
REM ================================
echo [1/2] Starting Backend and MySQL with Docker...
echo.

REM Stop e rimuovi container esistenti
docker-compose down

REM Build e avvia backend e mysql
docker-compose up --build -d mysql backend

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak > nul

REM Verifica che i container siano avviati
docker-compose ps | findstr "backend" > nul
if %errorlevel% equ 0 (
    echo [OK] Backend is running
) else (
    echo [ERROR] Backend failed to start
    echo.
    echo Showing backend logs:
    docker-compose logs backend
    pause
    exit /b 1
)

docker-compose ps | findstr "mysql" > nul
if %errorlevel% equ 0 (
    echo [OK] MySQL is running
) else (
    echo [ERROR] MySQL failed to start
    echo.
    echo Showing mysql logs:
    docker-compose logs mysql
    pause
    exit /b 1
)

echo.

REM ================================
REM 2. Ottieni IP locale
REM ================================
echo [2/2] Detecting local IP address...

REM Estrai l'IP locale
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4" ^| findstr /v "127.0.0.1"') do (
    set LOCAL_IP=%%a
    goto :ip_found
)
:ip_found
REM Rimuovi spazi iniziali
set LOCAL_IP=%LOCAL_IP:~1%

if "%LOCAL_IP%"=="" (
    set LOCAL_IP=localhost
)

echo Local IP detected: %LOCAL_IP%
echo.

REM ================================
REM 3. Start Frontend
REM ================================
cd /d "%~dp0frontend"

echo Controllando se node_modules esiste...
if not exist node_modules (
    echo Installando dipendenze npm...
    call npm install --no-audit --no-fund --prefer-offline
) else (
    echo node_modules trovato, skipping install
)

echo.
echo ================================
echo     CRM POC is ready!
echo ================================
echo Backend API:  http://localhost:8000/api
echo Frontend:     http://%LOCAL_IP%:5173
echo MySQL:        localhost:3306
echo ================================
echo.
echo Avviando Vite dev server...
echo.

REM Avvia il frontend con host esposto
call npm run dev -- --host %LOCAL_IP%

pause