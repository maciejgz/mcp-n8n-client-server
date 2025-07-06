@echo off
echo ================================
echo MCP Mix Server - Quick Start
echo ================================

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

:MENU
echo.
echo Wybierz opcje:
echo 1. Zainstaluj zaleznosci
echo 2. Uruchom serwer HTTP (dla n8n)
echo 3. Uruchom serwer MCP (standardowy)
echo 4. Uruchom testy
echo 5. Zbuduj Docker
echo 6. Uruchom Docker
echo 7. Zatrzymaj Docker
echo 8. Pokaz logi Docker
echo 9. Wyjscie
echo.

set /p choice="Twoj wybor (1-9): "

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto HTTP_SERVER
if "%choice%"=="3" goto MCP_SERVER
if "%choice%"=="4" goto TEST
if "%choice%"=="5" goto BUILD_DOCKER
if "%choice%"=="6" goto RUN_DOCKER
if "%choice%"=="7" goto STOP_DOCKER
if "%choice%"=="8" goto LOGS_DOCKER
if "%choice%"=="9" goto EXIT

echo Nieprawidlowy wybor!
goto MENU

:INSTALL
echo.
echo Instalowanie zaleznosci...
pip install -r requirements.txt
if %ERRORLEVEL% EQU 0 (
    echo Zaleznosci zainstalowane pomyslnie!
) else (
    echo Blad podczas instalacji zaleznosci!
)
pause
goto MENU

:HTTP_SERVER
echo.
echo Uruchamianie serwera HTTP dla n8n na porcie 8000...
echo Nacisnij Ctrl+C aby zatrzymac
python start.py --http
pause
goto MENU

:MCP_SERVER
echo.
echo Uruchamianie standardowego serwera MCP...
echo Nacisnij Ctrl+C aby zatrzymac
python start.py
pause
goto MENU

:TEST
echo.
echo Uruchamianie testow...
echo Upewnij sie, ze serwer HTTP jest uruchomiony na porcie 8000
python test_server.py
pause
goto MENU

:BUILD_DOCKER
echo.
echo Budowanie kontenera Docker...
docker build -t mix-server .
if %ERRORLEVEL% EQU 0 (
    echo Kontener zbudowany pomyslnie!
) else (
    echo Blad podczas budowania kontenera!
)
pause
goto MENU

:RUN_DOCKER
echo.
echo Uruchamianie kontenera Docker...
echo Zatrzymywanie i usuwanie istniejacego kontenera...
docker stop mix-server-container 2>nul
docker rm mix-server-container 2>nul
docker run -d --name mix-server-container -p 8000:8000 --rm mix-server
if %ERRORLEVEL% EQU 0 (
    echo Kontener uruchomiony na porcie 8000!
    echo URL: http://localhost:8000
) else (
    echo Blad podczas uruchamiania kontenera!
)
pause
goto MENU

:STOP_DOCKER
echo.
echo Zatrzymywanie kontenera Docker...
docker stop mix-server-container
if %ERRORLEVEL% EQU 0 (
    echo Kontener zatrzymany!
) else (
    echo Blad podczas zatrzymywania kontenera (moze nie byl uruchomiony)!
)
pause
goto MENU

:LOGS_DOCKER
echo.
echo Logi kontenera Docker:
docker logs mix-server-container
pause
goto MENU

:EXIT
echo.
echo Dziekujemy za korzystanie z MCP Mix Server!
exit /b 0
