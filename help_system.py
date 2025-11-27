from typing import Dict, List
from models import Command


class HelpSystem:
    """Sistema de ajuda e documentação da aplicação."""
    
    @staticmethod
    def get_guia_uso() -> str:
        """Retorna o guia de uso da aplicação."""
        return r"""
═══════════════════════════════════════════════════════════════════
                    GUIA DE USO - HELP COMMANDS
═══════════════════════════════════════════════════════════════════

📌 SOBRE
--------
O Help Commands é uma ferramenta de suporte técnico que permite executar
comandos do sistema de forma rápida e organizada. Ideal para:
  • Suporte remoto
  • Acesso rápido a configurações do sistema
  • Cenários onde o usuário tem dificuldade de acessar ferramentas
  • Manutenção e diagnóstico de sistemas

🎯 FUNCIONALIDADES PRINCIPAIS
-----------------------------
1. EXECUÇÃO DE COMANDOS PRÉ-DEFINIDOS
   - Catálogo com mais de 50 comandos do Windows
   - Comandos organizados por categoria
   - Descrição detalhada de cada comando
   - Indicação de comandos que requerem privilégios admin

2. BUSCA E FILTRO
   - Busque comandos por nome, categoria ou descrição
   - Filtro rápido para encontrar o que precisa

3. FAVORITOS
   - Marque comandos mais usados como favoritos
   - Acesso rápido aos comandos preferidos
   - Favoritos salvos entre sessões

4. HISTÓRICO
   - Registro completo de todos os comandos executados
   - Data/hora de execução
   - Status de sucesso/falha
   - Exportação para arquivo de texto

5. COMANDO LIVRE
   - Execute qualquer comando do Windows manualmente
   - Opção de executar com privilégios administrativos
   - Histórico também salvo

6. ELEVAÇÃO DE PRIVILÉGIOS
   - Detecção automática de comandos que precisam de admin
   - Solicitação UAC quando necessário
   - Fallback gracioso quando elevação falha

7. SEGURANÇA
   - Confirmação antes de executar comandos críticos (regedit, etc)
   - Logs de todas as operações
   - Avisos claros sobre privilégios necessários

🔧 COMO USAR
------------
1. Navegue pelas categorias ou use a busca
2. Clique em um comando para ver detalhes
3. Clique "Executar" para rodar o comando
4. Veja a saída no console integrado
5. Use ⭐ para marcar favoritos

⚙️ CONFIGURAÇÕES
---------------
- Tema: Claro ou Escuro
- Auto-scroll: Rola automaticamente o console
- Confirmação: Pede confirmação em comandos críticos
- Avisos: Mostra avisos sobre privilégios admin

📝 ATALHOS
----------
- Ctrl+F: Focar na busca
- Ctrl+H: Ver histórico
- Ctrl+L: Comando livre
- Ctrl+S: Configurações
- ESC: Limpar busca

🛡️ SEGURANÇA
------------
- NUNCA execute comandos que você não entende
- Comandos críticos têm confirmação extra
- Todos os comandos são registrados em log
- Use com responsabilidade em ambientes de produção

💡 DICAS
--------
• Use favoritos para comandos frequentes
• Verifique o histórico para auditar ações
• Exporte o histórico antes de limpar
• Leia a descrição antes de executar comandos desconhecidos
• Comandos marcados com 🔒 precisam de admin
• Comandos marcados com ⚠️ são críticos

═══════════════════════════════════════════════════════════════════
"""
    
    @staticmethod
    def get_troubleshooting() -> str:
        """Retorna guia de solução de problemas."""
        return r"""
═══════════════════════════════════════════════════════════════════
                    SOLUÇÃO DE PROBLEMAS
═══════════════════════════════════════════════════════════════════

❌ COMANDO NÃO EXECUTA
----------------------
Problema: Clico em Executar mas nada acontece
Solução:
  1. Verifique se você tem privilégios necessários
  2. Se comando pede admin, aceite a solicitação UAC
  3. Veja o console de saída para mensagens de erro
  4. Verifique o log: mini_terminal_suporte.log

❌ ERRO "ACESSO NEGADO"
-----------------------
Problema: Mensagem de acesso negado ao executar
Solução:
  1. Comando provavelmente precisa de admin
  2. Execute o Mini Terminal como Administrador
  3. Clique com botão direito > "Executar como administrador"
  4. Tente novamente

❌ COMANDO ENCONTRADO MAS NÃO FUNCIONA
--------------------------------------
Problema: Comando existe mas não abre a ferramenta
Solução:
  1. Ferramenta pode não estar disponível na sua versão do Windows
     (ex: gpedit.msc não existe no Windows Home)
  2. Verifique se componente está instalado
  3. Consulte documentação do Windows para alternativas

❌ BUSCA NÃO ENCONTRA NADA
--------------------------
Problema: Digito na busca mas não acha comandos
Solução:
  1. Verifique a ortografia
  2. Tente termos mais genéricos (ex: "rede" ao invés de "adaptador")
  3. Limpe a busca (ESC) e navegue por categorias
  4. Use parte do nome do comando

❌ JANELA DO UAC NÃO APARECE
----------------------------
Problema: Comando precisa de admin mas UAC não aparece
Solução:
  1. UAC pode estar desabilitado no sistema
  2. Execute o Mini Terminal como administrador desde o início
  3. Verifique configurações de UAC: control userpasswords2

❌ HISTÓRICO NÃO SALVA
----------------------
Problema: Executo comandos mas histórico fica vazio
Solução:
  1. Verifique permissões de escrita na pasta
  2. Verifique se command_history.json existe
  3. Pode haver erro ao salvar - veja console
  4. Execute aplicação com privilégios adequados

❌ FAVORITOS NÃO SALVAM
-----------------------
Problema: Marco favoritos mas somem ao fechar
Solução:
  1. Similar ao histórico - problema de permissões
  2. Verifique se app_config.json existe
  3. Não feche aplicação abruptamente

❌ INTERFACE ESTÁ LENTA
-----------------------
Problema: Aplicação demora a responder
Solução:
  1. Histórico muito grande - limpe comandos antigos
  2. Muitos comandos na busca - seja mais específico
  3. Reinicie a aplicação

❌ LOGS OCUPANDO MUITO ESPAÇO
-----------------------------
Problema: mini_terminal_suporte.log está grande
Solução:
  1. É seguro deletar o arquivo (será recriado)
  2. Ou mova para backup
  3. Configure rotação de logs se necessário

🆘 AINDA COM PROBLEMAS?
----------------------
1. Verifique o arquivo de log: mini_terminal_suporte.log
2. Execute como administrador
3. Reinicie o computador
4. Reinstale a aplicação

═══════════════════════════════════════════════════════════════════
"""
    
    @staticmethod
    def get_sobre() -> str:
        """Retorna informações sobre a aplicação."""
        return r"""
═══════════════════════════════════════════════════════════════════
                    SOBRE - HELP COMMANDS
═══════════════════════════════════════════════════════════════════

📱 INFORMAÇÕES
--------------
Nome: Help Commands - Painel de Suporte Técnico
Versão: 3.2.0
Plataforma: Windows
Interface: Tkinter GUI

📋 DESCRIÇÃO
------------
Ferramenta desenvolvida para facilitar o acesso rápido a comandos
e configurações do sistema operacional, especialmente útil em
cenários de suporte técnico remoto onde o usuário final pode ter
dificuldades de acesso.

✨ RECURSOS
-----------
• Mais de 50 comandos pré-configurados para Windows
• Suporte multiplataforma (Windows/Linux)
• Interface gráfica intuitiva
• Sistema de busca e filtros
• Favoritos personalizáveis
• Histórico completo de execuções
• Elevação automática de privilégios
• Confirmação de comandos críticos
• Sistema de ajuda integrado
• Exportação de histórico
• Logging completo
• Configurações persistentes

🔧 TECNOLOGIAS
--------------
• Python 3.8+
• Tkinter (Interface Gráfica)
• Subprocess (Execução de comandos)
• JSON (Configurações e histórico)
• Logging (Auditoria)

📦 COMANDOS INCLUÍDOS
--------------------
• Sistema: Painel de Controle, Serviços, Registro, etc
• Rede: Conexões, IP, Firewall, DNS, etc
• Usuários: Contas, Permissões, Credenciais
• Programas: Instalação, Desinstalação, Recursos
• Disco: Gerenciamento, Partições, Limpeza
• Energia: Planos, Bateria, Desempenho
• Ferramentas: Terminal, Editores, Calculadora
• Backup: Restauração, Pontos de Restauração
• Acessibilidade: Lupa, Teclado Virtual, Narrador
• E muito mais...

🛡️ SEGURANÇA
------------
• Todos os comandos são registrados em log
• Confirmação obrigatória para comandos críticos
• Avisos claros sobre necessidade de privilégios
• Código fonte aberto e auditável
• Sem conexões de rede
• Sem coleta de dados

📄 LICENÇA
----------
Este é um projeto de código aberto desenvolvido para fins educacionais
e de suporte técnico. Use com responsabilidade.

⚠️ AVISO LEGAL
-------------
O uso desta ferramenta é de sua inteira responsabilidade. Execute
apenas comandos que você compreende totalmente. Alguns comandos
podem fazer alterações permanentes no sistema.

═══════════════════════════════════════════════════════════════════

Programado e desenvolvido em Python por Nicolas Wolf para atender
demandas de suporte técnico.

═══════════════════════════════════════════════════════════════════
"""
    
    @staticmethod
    def get_command_help(cmd: Command) -> str:
        """Retorna ajuda detalhada para um comando específico."""
        help_text = f"""
┌───────────────────────────────────────────────────────────────────┐
  DETALHES DO COMANDO
└───────────────────────────────────────────────────────────────────┘

📌 NOME
   {cmd.name}

🔑 TECLA DE ATALHO
   [{cmd.key}]

📂 CATEGORIA
   {cmd.category}

💻 COMANDO
   {cmd.command}

📝 DESCRIÇÃO
   {cmd.description}

"""
        if cmd.requires_admin:
            help_text += "🔒 PRIVILÉGIOS\n   Este comando REQUER privilégios administrativos\n\n"
        else:
            help_text += "👤 PRIVILÉGIOS\n   Este comando NÃO requer privilégios administrativos\n\n"
        
        if cmd.is_critical:
            help_text += "⚠️  ATENÇÃO\n   Este é um comando CRÍTICO que pode fazer alterações\n   permanentes no sistema. Use com cautela!\n\n"
        
        help_text += "───────────────────────────────────────────────────────────────────\n"
        
        return help_text
    
    @staticmethod
    def get_categorias_help() -> Dict[str, str]:
        """Retorna descrições das categorias."""
        return {
            "Sistema": "Comandos relacionados a configurações gerais do sistema, serviços, informações de hardware e gerenciamento do Windows.",
            "Rede": "Ferramentas para diagnóstico e configuração de rede, conexões, IP, DNS, firewall e conectividade.",
            "Usuário": "Gerenciamento de contas de usuário, permissões, senhas, grupos e políticas de segurança.",
            "Internet": "Configurações de navegação, proxy, opções do Internet Explorer e conectividade web.",
            "Ferramentas": "Utilitários diversos como terminal, editores de texto, calculadora e ferramentas de captura.",
            "Disco": "Gerenciamento de discos, partições, formatação, verificação de erros e diagnóstico de hardware.",
            "Programas": "Instalação, desinstalação e gerenciamento de aplicativos e recursos do Windows.",
            "Energia": "Configurações de energia, bateria, planos de energia e monitoramento de desempenho.",
            "Personalização": "Temas, aparência, sons, mouse, teclado e configurações visuais do sistema.",
            "Data/Hora": "Ajustes de data, hora, fuso horário e sincronização com servidores de tempo.",
            "Backup": "Backup de arquivos, restauração do sistema e pontos de restauração.",
            "Acessibilidade": "Ferramentas de acessibilidade como narrador, lupa, teclado virtual e alto contraste.",
        }
