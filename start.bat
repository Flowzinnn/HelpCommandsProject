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
    echo A aplicacao pode nao funcionar corretamente.
    echo.
    pause
) else (
    echo [OK] Tkinter disponivel
    echo.
)

REM Perguntar modo de execução
echo Como deseja executar?
echo.
echo [1] Executar Normalmente
echo [2] Executar como Administrador
echo.
set /p choice="Escolha (1-2): "

if "%choice%"=="2" (
    echo.
    echo Solicitando privilegios administrativos...
    powershell -Command "Start-Process python -ArgumentList 'main.py' -Verb RunAs"
) else (
    echo.
    echo Iniciando interface grafica...
    python main.py
)

echo.
pause

