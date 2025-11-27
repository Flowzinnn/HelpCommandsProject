@echo off
REM ============================================
REM  Mini Terminal - Inicializador Windows
REM ============================================

echo.
echo ========================================
echo   MINI TERMINAL - PAINEL DE CONTROLE
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao esta instalado ou nao esta no PATH
    echo.
    echo Baixe Python em: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python detectado
python --version
echo.

REM Verificar Tkinter
python -m tkinter >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Tkinter pode nao estar disponivel
    echo Tentando executar mesmo assim...
    echo.
) else (
    echo [OK] Tkinter disponivel
    echo.
)

REM Perguntar modo de execução
echo Como deseja executar?
echo.
echo [1] Interface Grafica (GUI) - Recomendado
echo [2] Modo Terminal (linha de comando)
echo [3] GUI como Administrador
echo.
set /p choice="Escolha (1-3): "

if "%choice%"=="1" (
    echo.
    echo Iniciando interface grafica...
    python main.py
) else if "%choice%"=="2" (
    echo.
    echo Iniciando modo terminal...
    python main.py --terminal
) else if "%choice%"=="3" (
    echo.
    echo Solicitando privilegios administrativos...
    powershell -Command "Start-Process python -ArgumentList 'main.py' -Verb RunAs"
) else (
    echo.
    echo Opcao invalida! Executando GUI padrao...
    python main.py
)

echo.
pause
