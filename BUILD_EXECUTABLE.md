# 📦 Como Criar Executável Standalone

Este guia mostra como transformar o Mini Terminal em um executável independente (.exe no Windows ou binário no Linux) que pode ser distribuído sem precisar do Python instalado.

---

## 🪟 Windows - Criar .EXE

### Método 1: PyInstaller (Recomendado)

#### 1. Instalar PyInstaller
```powershell
pip install pyinstaller
```

#### 2. Criar Executável Básico
```powershell
pyinstaller --onefile --windowed --name="MiniTerminal" main.py
```

**Opções:**
- `--onefile` - Cria um único arquivo .exe
- `--windowed` - Remove janela de console (apenas GUI)
- `--name="MiniTerminal"` - Nome do executável

#### 3. Criar Executável com Ícone
```powershell
pyinstaller --onefile --windowed --name="MiniTerminal" --icon=icon.ico main.py
```

#### 4. Executável Completo (Incluir Todos os Arquivos)
```powershell
pyinstaller --onefile ^
    --windowed ^
    --name="MiniTerminal" ^
    --icon=icon.ico ^
    --add-data "README.md;." ^
    main.py
```

#### 5. Localização do Executável
O arquivo `MiniTerminal.exe` estará em:
```
dist/MiniTerminal.exe
```

---

### Método 2: Auto-Py-To-Exe (Interface Gráfica)

#### 1. Instalar Auto-Py-To-Exe
```powershell
pip install auto-py-to-exe
```

#### 2. Iniciar Interface
```powershell
auto-py-to-exe
```

#### 3. Configurar na Interface
- **Script Location:** `main.py`
- **Onefile:** One File
- **Console Window:** Window Based
- **Icon:** Selecione seu ícone (opcional)
- Clique em **CONVERT .PY TO .EXE**

---

## 🐧 Linux - Criar Binário

### Usando PyInstaller

#### 1. Instalar PyInstaller
```bash
pip3 install pyinstaller
```

#### 2. Criar Binário
```bash
pyinstaller --onefile --windowed --name="MiniTerminal" main.py
```

#### 3. Tornar Executável
```bash
chmod +x dist/MiniTerminal
```

#### 4. Executar
```bash
./dist/MiniTerminal
```

---

## 📋 Arquivo .spec Customizado

Para builds mais avançados, crie um arquivo `MiniTerminal.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MiniTerminal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = Apenas GUI, True = Com console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Remova se não tiver ícone
)
```

Depois compile com:
```powershell
pyinstaller MiniTerminal.spec
```

---

## 🎨 Criar Ícone (Opcional)

### Online (Fácil)
1. Acesse https://convertio.co/png-ico/
2. Faça upload de uma imagem PNG
3. Converta para ICO
4. Salve como `icon.ico` na pasta do projeto

### Com Python (PIL)
```python
from PIL import Image

img = Image.open('logo.png')
img.save('icon.ico', format='ICO', sizes=[(256, 256)])
```

---

## 📦 Distribuir o Executável

### Windows
1. Copie `dist/MiniTerminal.exe` para onde quiser
2. Não precisa de Python instalado
3. Pode distribuir por:
   - USB/Pendrive
   - Email (se não for muito grande)
   - Cloud (Google Drive, Dropbox)
   - Rede local

### Criar Instalador (NSIS - Opcional)
Para criar um instalador profissional:

1. Baixe NSIS: https://nsis.sourceforge.io/
2. Crie script `installer.nsi`:

```nsis
!define APP_NAME "Mini Terminal"
!define COMP_NAME "Suporte Técnico"
!define VERSION "2.0.0"
!define INSTALLER_NAME "MiniTerminal_Setup.exe"

OutFile "${INSTALLER_NAME}"
InstallDir "$PROGRAMFILES\${APP_NAME}"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File "dist\MiniTerminal.exe"
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\MiniTerminal.exe"
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\MiniTerminal.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\MiniTerminal.exe"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    RMDir "$INSTDIR"
SectionEnd
```

3. Compile:
```powershell
makensis installer.nsi
```

---

## ⚙️ Otimização do Executável

### Reduzir Tamanho

#### 1. Usar UPX (Compressor)
```powershell
# Baixe UPX: https://upx.github.io/
pyinstaller --onefile --windowed --upx-dir="C:\upx" main.py
```

#### 2. Excluir Módulos Desnecessários
```powershell
pyinstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy main.py
```

### Desempenho

#### Usar --onedir para Startup Mais Rápido
```powershell
pyinstaller --onedir --windowed main.py
```
Cria uma pasta com o executável e DLLs (startup mais rápido, mas mais arquivos)

---

## 🔐 Assinatura Digital (Opcional - Windows)

Para evitar avisos do SmartScreen:

### 1. Obter Certificado
- Compre de CA confiável (Digicert, Sectigo, etc)
- Ou use certificado self-signed (para uso interno)

### 2. Assinar com SignTool
```powershell
signtool sign /f certificado.pfx /p senha /t http://timestamp.digicert.com dist\MiniTerminal.exe
```

---

## 🐛 Troubleshooting

### Erro: "Failed to execute script"
**Solução:** Compile sem `--windowed` para ver erros:
```powershell
pyinstaller --onefile --console main.py
```

### Antivírus Bloqueia o .exe
**Solução:** 
1. Adicione exceção no antivírus
2. Ou assine digitalmente o executável

### Executável Muito Grande (>50MB)
**Solução:**
1. Use `--onedir` ao invés de `--onefile`
2. Use UPX para comprimir
3. Exclua módulos desnecessários

### Tkinter Não Funciona no Executável
**Solução:** Adicione ao .spec:
```python
hiddenimports=['tkinter', '_tkinter']
```

---

## 📊 Comparação de Métodos

| Método | Tamanho | Velocidade | Facilidade | Recomendado |
|--------|---------|------------|------------|-------------|
| PyInstaller --onefile | ~15-25MB | Médio | Fácil | ✅ SIM |
| PyInstaller --onedir | ~30-40MB | Rápido | Fácil | Para uso local |
| Auto-Py-To-Exe | ~15-25MB | Médio | Muito Fácil | Para iniciantes |
| NSIS Installer | Variável | - | Médio | Para distribuição |

---

## 📝 Checklist de Distribuição

Antes de distribuir o executável:

- [ ] Testou em máquina limpa (sem Python)?
- [ ] Funciona sem privilégios admin?
- [ ] Funciona COM privilégios admin?
- [ ] Testou em Windows 10 e 11?
- [ ] Ícone está correto?
- [ ] Versão está atualizada?
- [ ] README incluído?
- [ ] Antivírus não bloqueia?
- [ ] Tamanho razoável (<30MB)?

---

## 🚀 Script Completo de Build

Salve como `build.bat`:

```batch
@echo off
echo ========================================
echo   COMPILANDO MINI TERMINAL
echo ========================================
echo.

REM Limpar builds anteriores
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

echo Instalando PyInstaller...
pip install pyinstaller

echo.
echo Compilando executavel...
pyinstaller --onefile ^
    --windowed ^
    --name="MiniTerminal" ^
    --icon=icon.ico ^
    main.py

echo.
echo ========================================
if exist "dist\MiniTerminal.exe" (
    echo [OK] Executavel criado com sucesso!
    echo.
    echo Localizacao: dist\MiniTerminal.exe
    echo.
    explorer dist
) else (
    echo [ERRO] Falha ao criar executavel
)
echo ========================================
pause
```

Execute:
```powershell
.\build.bat
```

---

**✅ Pronto!** Agora você tem um executável standalone do Mini Terminal que pode ser distribuído para qualquer computador Windows sem precisar do Python instalado.
