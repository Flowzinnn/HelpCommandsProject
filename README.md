# Mini Terminal - Painel de Controle de Suporte

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Ferramenta de suporte técnico com interface gráfica** para execução rápida de comandos do sistema Windows/Linux. Ideal para cenários de suporte remoto onde o usuário tem dificuldade de acessar configurações.

---

## 🎯 Funcionalidades

✅ **+50 comandos pré-configurados** organizados por categoria  
✅ **Interface gráfica intuitiva** com Tkinter  
✅ **Suporte multiplataforma** (Windows/Linux)  
✅ **Sistema de busca e filtros** avançados  
✅ **Favoritos personalizáveis**  
✅ **Histórico completo** de execuções com exportação  
✅ **Elevação automática de privilégios** (UAC/sudo)  
✅ **Confirmação de comandos críticos**  
✅ **Console integrado** com saída em tempo real  
✅ **Sistema de ajuda** completo  
✅ **Logging de auditoria**  
✅ **Configurações persistentes**  

---

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Tkinter (já incluído na maioria das instalações Python)

### Clonar/Baixar o Projeto
```bash
# Apenas extraia os arquivos em uma pasta
```

### Verificar Dependências
```bash
python --version  # Deve ser 3.8+
python -m tkinter  # Deve abrir uma janela de teste
```

---

## 🚀 Como Usar

### Modo GUI (Padrão)
```bash
python main.py
```

### Modo Terminal (Legado)
```bash
python main.py --terminal
```

### Executar como Administrador (Windows)
Clique com botão direito em `main.py` → **Executar como administrador**

Ou via PowerShell:
```powershell
Start-Process python -ArgumentList "main.py" -Verb RunAs
```

---

## 📂 Estrutura do Projeto

```
terminal python/
├── main.py                    # Ponto de entrada (GUI ou terminal)
├── gui.py                     # Interface gráfica principal
├── models.py                  # Modelos de dados (Command)
├── commands_config.py         # Carregador de comandos multiplataforma
├── commands_windows.py        # +50 comandos do Windows
├── commands_linux.py          # Comandos do Linux
├── executor.py                # Executor de comandos com elevação
├── platform_detector.py       # Detecção de SO e privilégios
├── config_manager.py          # Gerenciamento de config e histórico
├── help_system.py             # Sistema de ajuda integrado
├── requirements.txt           # Dependências (apenas Python stdlib)
└── README.md                  # Esta documentação
```

**Arquivos gerados em runtime:**
- `app_config.json` - Configurações do usuário
- `command_history.json` - Histórico de comandos
- `mini_terminal_suporte.log` - Log de auditoria

---

## 🎮 Interface Gráfica

### Painel Principal
- **Lista de comandos** organizada por categoria
- **Busca em tempo real** por nome, comando ou descrição
- **Filtro por categoria**
- **Marcadores visuais**: ⭐ Favorito | 🔒 Requer Admin | ⚠️ Crítico

### Abas
1. **📋 Detalhes** - Informações completas do comando selecionado
2. **💻 Console** - Saída de execução em tempo real
3. **📜 Histórico** - Todos os comandos executados
4. **❓ Ajuda** - Guia de uso e troubleshooting

### Menu
- **Arquivo** → Comando Livre, Exportar Histórico, Sair
- **Ferramentas** → Limpar Console, Ver Histórico, Configurações
- **Ajuda** → Guia de Uso, Solução de Problemas, Sobre

---

## 📖 Comandos Incluídos

### Windows (Exemplos)
| Categoria | Comandos |
|-----------|----------|
| **Sistema** | Painel de Controle, Serviços, Registro, Gerenciador de Tarefas, msconfig, gpedit |
| **Rede** | Conexões, ipconfig, ping, DNS flush, Firewall, netstat |
| **Usuários** | Contas, Grupos Locais, Políticas de Segurança, Credenciais |
| **Disco** | Gerenciamento de Disco, chkdsk, DirectX Diagnostic |
| **Programas** | Adicionar/Remover, Recursos do Windows |
| **Energia** | Opções de Energia, Relatório de Bateria, Monitor de Desempenho |
| **Backup** | Backup e Restauração, Pontos de Restauração |

### Linux (Exemplos)
| Categoria | Comandos |
|-----------|----------|
| **Sistema** | gnome-control-center, systemctl, df, ps, top |
| **Rede** | NetworkManager, ping, ifconfig, ufw, netstat |
| **Usuários** | Gerenciamento de Contas, who, /etc/passwd |
| **Programas** | APT, dpkg, GNOME Software |
| **Ferramentas** | Terminal, gedit, Nautilus, Screenshot |

---

## ⚙️ Configurações

Acesse via **Ferramentas → Configurações** (Ctrl+S)

- ✅ **Auto-scroll no console** - Rola automaticamente a saída
- ✅ **Confirmar comandos críticos** - Pede confirmação extra
- ✅ **Mostrar avisos de admin** - Alerta sobre UAC/sudo
- 💾 **Favoritos** - Salvos automaticamente
- 📐 **Tamanho da janela** - Persistido entre sessões

---

## 🔒 Segurança

### Privilégios Administrativos
- Detecção automática de comandos que requerem admin
- Solicitação UAC (Windows) ou sudo (Linux) quando necessário
- Fallback gracioso se elevação falhar

### Comandos Críticos
Comandos como `regedit`, `chkdsk`, `rstrui` são marcados como críticos e **sempre pedem confirmação** antes de executar.

### Auditoria
Todos os comandos são registrados em `mini_terminal_suporte.log`:
```
2025-11-27 10:30:15 [INFO] Executando comando: Painel de Controle (control)
2025-11-27 10:30:15 [INFO] Comando executado com sucesso: Painel de Controle
```

---

## 🛠️ Desenvolvimento

### Adicionar Novos Comandos (Windows)
Edite `commands_windows.py`:
```python
Command(
    key="NOVO1",
    name="Meu Comando",
    command="meucomando.exe",
    category="Ferramentas",
    description="Descrição do que faz",
    requires_admin=False,
    is_critical=False,
)
```

### Criar Executável Standalone
```bash
# Instalar PyInstaller
pip install pyinstaller

# Gerar executável
pyinstaller --onefile --windowed --name="MiniTerminal" --icon=icon.ico main.py

# Executável estará em dist/MiniTerminal.exe
```

---

## 📝 Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl+L` | Abrir Comando Livre |
| `Ctrl+H` | Ver Histórico |
| `Ctrl+S` | Configurações |
| `Ctrl+F` | Focar na Busca |
| `ESC` | Limpar Busca |
| `Enter` | Executar Comando Selecionado |
| `Alt+F4` | Sair |

---

## 🐛 Solução de Problemas

### Comando não executa
1. Verifique se tem privilégios necessários (🔒)
2. Aceite a solicitação UAC/sudo
3. Veja o console para mensagens de erro
4. Consulte `mini_terminal_suporte.log`

### Erro "Acesso Negado"
Execute o Mini Terminal como Administrador:
```powershell
Start-Process python -ArgumentList "main.py" -Verb RunAs
```

### Tkinter não encontrado
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Comando existe mas não funciona
- Ferramenta pode não estar disponível (ex: `gpedit.msc` não existe no Windows Home)
- Verifique se o componente está instalado no sistema

---

## 📄 Licença

Projeto de código aberto desenvolvido para fins educacionais e de suporte técnico.  
**Use com responsabilidade!**

---

## ⚠️ Aviso Legal

O uso desta ferramenta é de sua inteira responsabilidade. Execute apenas comandos que você compreende totalmente. Alguns comandos podem fazer alterações permanentes no sistema.

---

## 🙏 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Adicionar novos comandos
- Melhorar a interface
- Reportar bugs
- Sugerir funcionalidades

---

## 📧 Suporte

Para dúvidas ou problemas:
1. Consulte a **Ajuda integrada** (Ctrl+H)
2. Verifique a seção **Solução de Problemas** neste README
3. Consulte os logs em `mini_terminal_suporte.log`

---

**Desenvolvido com ❤️ para facilitar o trabalho de suporte técnico.**

---

### Status do Projeto
✅ **Versão 2.0.0** - Interface GUI completa  
✅ Suporte Windows/Linux  
✅ +50 comandos incluídos  
✅ Sistema de ajuda integrado  
✅ Histórico e favoritos  
✅ Configurações persistentes  

### Próximas Versões (Roadmap)
- [ ] Temas personalizados (Dark/Light)
- [ ] Mais comandos para Linux (KDE, XFCE)
- [ ] Suporte para macOS
- [ ] Plugin system para comandos customizados
- [ ] Execução remota via SSH
- [ ] Logs em tempo real na GUI
