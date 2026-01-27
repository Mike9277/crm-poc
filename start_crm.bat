@echo off
REM ================================
REM    CRM POC - Startup Script (FIXED)
REM ================================
echo ================================
echo    CRM POC - Startup Script
echo ================================
echo.

REM Aggiungi Node.js al PATH
set PATH=%PATH%;C:\Program Files\nodejs

REM ================================
REM 1. Start Docker (Backend + MySQL + Drupal)
REM ================================
echo [1/3] Pulling latest images and starting services...
echo.

REM Pull updates delle immagini e avvia i servizi
docker-compose pull
docker-compose up --build -d

echo.
echo Waiting for MySQL to be ready (3s)...
timeout /t 3 /nobreak > nul

REM ================================
REM 2. Drupal Maintenance & Recovery
REM ================================
echo [2/3] Repairing Drupal Cache and Locks...

REM Sblocco del cron nel caso fosse rimasto appeso
docker-compose exec drupal php -r "\$lock = \Drupal::lock(); if (\$lock->isLocked('cron')) { \$lock->release('cron'); echo 'Cron lock released.\n'; }" 2>nul

REM Pulizia cache "brutale" tramite database (usando il nome servizio 'mysql')
echo Cleaning Drupal cache tables...
docker-compose exec mysql mysql -u drupal -pdrupal drupal -e "DELETE FROM cache_container; DELETE FROM cache_bootstrap; DELETE FROM cache_discovery; DELETE FROM cache_config;" 2>nul

REM Tentativo di Cache Rebuild tramite il percorso corretto di Drush
echo Rebuilding Drupal registry...
docker-compose exec drupal /var/www/html/vendor/bin/drush cr

echo.

REM ================================
REM 3. Ottieni IP locale
REM ================================
echo [3/3] Detecting local IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4" ^| findstr /v "127.0.0.1"') do (
    set LOCAL_IP=%%a
    goto :ip_found
)

:ip_found
set LOCAL_IP=%LOCAL_IP:~1%
if "%LOCAL_IP%"=="" (
    set LOCAL_IP=localhost
)
echo Local IP detected: %LOCAL_IP%
echo.

REM ================================
REM 4. Start Frontend
REM ================================
echo Starting Frontend...
cd /d "%~dp0frontend"

if not exist node_modules (
    echo Installing npm dependencies...
    call npm install --no-audit --no-fund --prefer-offline
)

echo.
echo ================================
echo      CRM POC is ready!
echo ================================
echo Backend API:  http://localhost:8000/api
echo Frontend:     http://%LOCAL_IP%:5173
echo Drupal:       http://localhost:8080
echo ================================
echo.

call npm run dev -- --host %LOCAL_IP%

pause