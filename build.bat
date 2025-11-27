@echo off
echo ========================================
echo   COMPILANDO HELPCOMMANDS (MODERNO)
echo ========================================
echo.

REM Limpar builds anteriores
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Instalando dependencias...
pip install customtkinter pyinstaller

echo.
echo Compilando executavel com requisicao de admin...
echo NOTA: CustomTkinter sera incluido no executavel
pyinstaller HelpCommands.spec

echo.
echo ========================================
if exist "dist\HelpCommands.exe" (
    echo [OK] Executavel criado com sucesso!
    echo.
    echo Localizacao: dist\HelpCommands.exe
    echo NOTA: Este executavel sempre solicitara privilegios de administrador
    echo.
    explorer dist
) else (
    echo [ERRO] Falha ao criar executavel
)
echo ========================================
pause
