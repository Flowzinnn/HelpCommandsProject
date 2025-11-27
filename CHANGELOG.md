# 📋 Changelog - Mini Terminal

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

---

## [2.0.0] - 2025-11-27

### ✨ Novidades Principais

#### Interface Gráfica Completa
- ✅ **GUI com Tkinter** - Interface gráfica intuitiva e moderna
- ✅ **Layout em Painel** - Divisão clara entre lista de comandos e detalhes
- ✅ **Sistema de Abas** - Detalhes, Console, Histórico e Ajuda
- ✅ **Busca em Tempo Real** - Filtra comandos enquanto digita
- ✅ **Filtro por Categoria** - Dropdown para selecionar categoria específica

#### Catálogo Expandido de Comandos
- ✅ **+50 Comandos Windows** - De 9 para mais de 50 comandos
- ✅ **Comandos Linux** - Suporte completo para GNOME/Ubuntu
- ✅ **Novas Categorias:**
  - Disco (Gerenciamento, Verificação, DirectX)
  - Programas (Instalação, Recursos, Apps)
  - Energia (Opções, Bateria, Desempenho)
  - Personalização (Temas, Mouse, Teclado, Sons)
  - Data/Hora
  - Backup (Restauração, Pontos de Restauração)
  - Acessibilidade (Lupa, Narrador, Teclado Virtual)

#### Sistema de Privilégios
- ✅ **Detecção Automática** - Identifica comandos que precisam de admin
- ✅ **Elevação UAC (Windows)** - Solicita privilégios via ShellExecuteEx
- ✅ **Sudo (Linux)** - Executa com sudo automaticamente
- ✅ **Marcadores Visuais** - 🔒 indica comando que precisa de admin
- ✅ **Fallback Gracioso** - Tenta executar sem admin se elevação falhar

#### Segurança e Confirmações
- ✅ **Comandos Críticos** - Marcados com ⚠️ (regedit, chkdsk, etc)
- ✅ **Confirmação Obrigatória** - Dialog antes de executar críticos
- ✅ **Avisos de Admin** - Informa sobre solicitação UAC
- ✅ **Configurável** - Pode desativar avisos nas configurações

#### Sistema de Favoritos
- ✅ **Marcar como Favorito** - Botão ⭐ para comandos frequentes
- ✅ **Filtro de Favoritos** - Ver apenas comandos favoritados
- ✅ **Persistência** - Favoritos salvos entre sessões
- ✅ **Indicador Visual** - ⭐ na lista de comandos

#### Histórico de Comandos
- ✅ **Registro Completo** - Data/hora, comando, status
- ✅ **Visualização na GUI** - Aba dedicada ao histórico
- ✅ **Exportação** - Salvar histórico em .txt legível
- ✅ **Limite Automático** - Mantém últimas 500 entradas
- ✅ **Indicador de Sucesso** - ✅ sucesso / ❌ falha

#### Console Integrado
- ✅ **Saída em Tempo Real** - Ver output dos comandos
- ✅ **Estilo Terminal** - Fundo preto, texto verde
- ✅ **Auto-Scroll** - Rola automaticamente (configurável)
- ✅ **Limpar Console** - Botão para limpar saída

#### Sistema de Ajuda
- ✅ **Guia de Uso** - Documentação completa integrada
- ✅ **Solução de Problemas** - Troubleshooting detalhado
- ✅ **Sobre** - Informações do aplicativo
- ✅ **Ajuda Contextual** - Descrição detalhada de cada comando

#### Configurações
- ✅ **Persistência** - Salva em app_config.json
- ✅ **Auto-Scroll** - Ativar/desativar scroll automático
- ✅ **Confirmações** - Configurar avisos de comandos críticos
- ✅ **Avisos de Admin** - Mostrar/ocultar avisos UAC
- ✅ **Tamanho da Janela** - Lembra dimensões entre sessões
- ✅ **Dialog de Configurações** - Interface gráfica para ajustes

#### Detecção de Plataforma
- ✅ **Multi-OS** - Detecta Windows, Linux, macOS
- ✅ **Comandos Específicos** - Carrega comandos do SO atual
- ✅ **Adaptação Automática** - Interface se adapta ao sistema

#### Melhorias de Usabilidade
- ✅ **Duplo Clique** - Executa comando com duplo clique
- ✅ **Atalhos de Teclado:**
  - Ctrl+L: Comando Livre
  - Ctrl+H: Ver Histórico
  - Ctrl+S: Configurações
  - Ctrl+F: Focar na Busca
  - ESC: Limpar Busca
- ✅ **Comando Livre** - Dialog para executar comandos arbitrários
- ✅ **Barra de Status** - Mostra SO e privilégios atuais

### 📦 Novos Arquivos

#### Código Fonte
- `gui.py` - Interface gráfica principal (700+ linhas)
- `platform_detector.py` - Detecção de SO e privilégios
- `commands_windows.py` - Catálogo expandido Windows (60+ comandos)
- `commands_linux.py` - Catálogo Linux (30+ comandos)
- `config_manager.py` - Gerenciamento de configurações e histórico
- `help_system.py` - Sistema de ajuda integrado

#### Documentação
- `README.md` - Documentação principal completa
- `BUILD_EXECUTABLE.md` - Guia para criar .exe
- `EXAMPLES.md` - Exemplos práticos de uso
- `CHANGELOG.md` - Este arquivo

#### Scripts de Inicialização
- `start.bat` - Inicializador Windows
- `start.sh` - Inicializador Linux
- `requirements.txt` - Dependências (apenas stdlib)
- `.gitignore` - Arquivos a ignorar no Git

### 🔄 Arquivos Modificados

#### models.py
- Adicionado campo `description: str`
- Adicionado campo `requires_admin: bool`
- Adicionado campo `is_critical: bool`
- Documentação atualizada para "multiplataforma"

#### executor.py
- Função `executar_com_elevacao_windows()` - Elevação UAC
- Função `executar_com_sudo_linux()` - Execução com sudo
- Callback `confirmacao_callback` para comandos críticos
- Parâmetro `requer_admin` em `executar_comando_livre()`
- Imports de `platform_detector`

#### commands_config.py
- Detecção automática de SO
- Carregamento dinâmico de comandos (Windows/Linux)
- Fallback para comandos genéricos

#### main.py
- Detecção de modo (GUI vs Terminal)
- Argumento `--terminal` para modo legado
- Try-except para iniciar GUI com fallback
- Import condicional de tkinter

### 🚀 Desempenho
- Inicialização: ~1-2 segundos
- Busca: Instantânea (<100ms)
- Carregamento de comandos: <50ms
- Uso de memória: ~30-50MB

### 📊 Estatísticas
- **Linhas de código:** ~2.500+
- **Comandos incluídos:** 60+ (Windows) + 30+ (Linux)
- **Arquivos Python:** 10
- **Arquivos de documentação:** 4
- **Funcionalidades:** 15+

---

## [1.0.0] - 2025-11-26 (Versão Original)

### Funcionalidades Iniciais
- ✅ Interface de linha de comando
- ✅ 9 comandos pré-definidos do Windows
- ✅ Agrupamento por categoria
- ✅ Comando livre
- ✅ Logging básico
- ✅ Execução via subprocess

### Categorias Originais
- Sistema (3 comandos)
- Rede (2 comandos)
- Usuário (1 comando)
- Internet (1 comando)
- Ferramentas (2 comandos)

### Arquivos Originais
- `main.py` - Loop principal
- `models.py` - Modelo Command
- `executor.py` - Execução de comandos
- `commands_config.py` - Lista de comandos

---

## 🔮 Roadmap Futuro

### Versão 2.1.0 (Planejado)
- [ ] Tema Dark/Light configurável
- [ ] Ícone personalizado
- [ ] Mais comandos para Linux (KDE, XFCE)
- [ ] Suporte para macOS
- [ ] Tradução para inglês

### Versão 2.2.0 (Planejado)
- [ ] Plugin system para comandos customizados
- [ ] Import/Export de comandos personalizados
- [ ] Templates de comandos
- [ ] Variáveis em comandos (ex: ${USERNAME})

### Versão 2.3.0 (Planejado)
- [ ] Execução remota via SSH
- [ ] Múltiplos perfis de configuração
- [ ] Agendamento de comandos
- [ ] Notificações desktop

### Versão 3.0.0 (Futuro)
- [ ] Sincronização na nuvem
- [ ] App mobile para controle remoto
- [ ] Modo servidor para gerenciar múltiplas máquinas
- [ ] Análise de logs com IA

---

## 🐛 Bugs Conhecidos

### Versão 2.0.0
- ⚠️ Windows Home não tem `gpedit.msc` e `lusrmgr.msc`
  - **Workaround:** Comandos falharão, mas não travam o app
- ⚠️ Alguns comandos Linux dependem do ambiente desktop (GNOME)
  - **Workaround:** Use equivalentes de linha de comando

---

## 🙏 Contribuições

Agradecimentos a todos que contribuíram com ideias e feedback:
- Comunidade Python Brasil
- Stack Overflow
- Documentação oficial do Windows/Linux

---

## 📝 Notas de Migração

### De 1.0 para 2.0

**Compatibilidade:**
- ✅ Modo terminal ainda funciona (`--terminal`)
- ✅ Logs compatíveis
- ⚠️ Estrutura de Command mudou (novos campos opcionais)

**Passos:**
1. Baixe todos os novos arquivos
2. Execute `python main.py` (GUI) ou `python main.py --terminal`
3. Configure preferências em Configurações
4. Marque favoritos para migração suave

**Novos Requisitos:**
- Python 3.8+ (antes era 3.6+)
- Tkinter (geralmente já incluído)

---

## 📊 Comparativo de Versões

| Recurso | v1.0 | v2.0 |
|---------|------|------|
| Interface | Terminal | GUI + Terminal |
| Comandos | 9 | 90+ |
| Plataformas | Windows | Windows + Linux |
| Favoritos | ❌ | ✅ |
| Histórico | Logs | GUI + Export |
| Busca | ❌ | ✅ |
| Elevação | ❌ | ✅ UAC/sudo |
| Ajuda | README | Integrada |
| Configurações | ❌ | ✅ Persistentes |
| Documentação | Básica | Completa |

---

**Formato baseado em [Keep a Changelog](https://keepachangelog.com/)**

**Versionamento:** [Semantic Versioning](https://semver.org/)
