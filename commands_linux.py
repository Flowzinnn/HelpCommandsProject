from typing import List
from models import Command


def get_linux_commands() -> List[Command]:
    """
    Retorna comandos específicos do Linux.
    """
    return [
        # ========== SISTEMA ==========
        Command(
            key="1",
            name="Configurações do Sistema (GNOME)",
            command="gnome-control-center",
            category="Sistema",
            description="Abre o painel de configurações do GNOME (equivalente ao Painel de Controle).",
            requires_admin=False,
        ),
        Command(
            key="2",
            name="Informações do Sistema",
            command="gnome-system-monitor",
            category="Sistema",
            description="Monitor de sistema com processos, recursos e discos.",
            requires_admin=False,
        ),
        Command(
            key="3",
            name="Gerenciador de Serviços (systemd)",
            command="systemctl status",
            category="Sistema",
            description="Lista status de todos os serviços do sistema.",
            requires_admin=False,
        ),
        Command(
            key="4",
            name="Informações de Hardware",
            command="lshw -short",
            category="Sistema",
            description="Lista informações resumidas de hardware do sistema.",
            requires_admin=True,
        ),
        Command(
            key="5",
            name="Uso de Disco",
            command="df -h",
            category="Sistema",
            description="Mostra uso de espaço em disco de todas as partições montadas.",
            requires_admin=False,
        ),
        Command(
            key="6",
            name="Processos em Execução",
            command="ps aux",
            category="Sistema",
            description="Lista todos os processos em execução no sistema.",
            requires_admin=False,
        ),
        Command(
            key="7",
            name="Top - Monitor de Processos",
            command="gnome-terminal -- top",
            category="Sistema",
            description="Monitor interativo de processos e uso de recursos em tempo real.",
            requires_admin=False,
        ),

        # ========== REDE ==========
        Command(
            key="R1",
            name="Configurações de Rede",
            command="nm-connection-editor",
            category="Rede",
            description="Editor de conexões do NetworkManager.",
            requires_admin=False,
        ),
        Command(
            key="R2",
            name="Teste de Conexão (ping)",
            command="ping -c 4 8.8.8.8",
            category="Rede",
            description="Testa conectividade com a internet (4 pacotes).",
            requires_admin=False,
        ),
        Command(
            key="R3",
            name="Configuração de Rede (ifconfig)",
            command="ifconfig",
            category="Rede",
            description="Exibe configuração de todas as interfaces de rede.",
            requires_admin=False,
        ),
        Command(
            key="R4",
            name="Configuração de Rede (ip addr)",
            command="ip addr show",
            category="Rede",
            description="Exibe endereços IP de todas as interfaces (comando moderno).",
            requires_admin=False,
        ),
        Command(
            key="R5",
            name="Firewall (UFW Status)",
            command="sudo ufw status",
            category="Rede",
            description="Mostra status e regras do firewall UFW.",
            requires_admin=True,
        ),
        Command(
            key="R6",
            name="Conexões Ativas (netstat)",
            command="netstat -tulpn",
            category="Rede",
            description="Lista portas em escuta e conexões ativas.",
            requires_admin=True,
        ),

        # ========== USUÁRIOS ==========
        Command(
            key="U1",
            name="Gerenciamento de Usuários",
            command="gnome-control-center user-accounts",
            category="Usuário",
            description="Gerencia contas de usuário do sistema.",
            requires_admin=False,
        ),
        Command(
            key="U2",
            name="Listar Usuários",
            command="cat /etc/passwd",
            category="Usuário",
            description="Lista todos os usuários do sistema.",
            requires_admin=False,
        ),
        Command(
            key="U3",
            name="Usuários Logados",
            command="who",
            category="Usuário",
            description="Mostra usuários atualmente logados no sistema.",
            requires_admin=False,
        ),

        # ========== PROGRAMAS ==========
        Command(
            key="P1",
            name="Gerenciador de Software",
            command="gnome-software",
            category="Programas",
            description="Loja de aplicativos do GNOME para instalar e remover programas.",
            requires_admin=False,
        ),
        Command(
            key="P2",
            name="Atualizar Sistema (APT)",
            command="gnome-terminal -- bash -c 'sudo apt update && sudo apt upgrade; exec bash'",
            category="Programas",
            description="Atualiza lista de pacotes e instala atualizações (Debian/Ubuntu).",
            requires_admin=True,
        ),
        Command(
            key="P3",
            name="Listar Pacotes Instalados",
            command="dpkg -l",
            category="Programas",
            description="Lista todos os pacotes instalados no sistema (Debian/Ubuntu).",
            requires_admin=False,
        ),

        # ========== FERRAMENTAS ==========
        Command(
            key="T1",
            name="Terminal",
            command="gnome-terminal",
            category="Ferramentas",
            description="Abre um novo terminal GNOME.",
            requires_admin=False,
        ),
        Command(
            key="T2",
            name="Editor de Texto (gedit)",
            command="gedit",
            category="Ferramentas",
            description="Editor de texto simples do GNOME.",
            requires_admin=False,
        ),
        Command(
            key="T3",
            name="Gerenciador de Arquivos",
            command="nautilus",
            category="Ferramentas",
            description="Abre o gerenciador de arquivos Nautilus.",
            requires_admin=False,
        ),
        Command(
            key="T4",
            name="Calculadora",
            command="gnome-calculator",
            category="Ferramentas",
            description="Calculadora do GNOME.",
            requires_admin=False,
        ),
        Command(
            key="T5",
            name="Screenshot",
            command="gnome-screenshot -i",
            category="Ferramentas",
            description="Ferramenta de captura de tela interativa.",
            requires_admin=False,
        ),

        # ========== DISCOS ==========
        Command(
            key="D1",
            name="Utilitário de Discos",
            command="gnome-disks",
            category="Disco",
            description="Gerencia partições, formatação e montagem de discos.",
            requires_admin=False,
        ),
        Command(
            key="D2",
            name="Uso de Disco por Pasta",
            command="gnome-terminal -- bash -c 'du -h --max-depth=1 /home; exec bash'",
            category="Disco",
            description="Mostra uso de disco na pasta home por subpasta.",
            requires_admin=False,
        ),

        # ========== ENERGIA ==========
        Command(
            key="E1",
            name="Configurações de Energia",
            command="gnome-control-center power",
            category="Energia",
            description="Configura suspensão, desligamento de tela e bateria.",
            requires_admin=False,
        ),

        # ========== LOGS E DIAGNÓSTICO ==========
        Command(
            key="L1",
            name="Logs do Sistema (journalctl)",
            command="gnome-terminal -- journalctl -xe",
            category="Logs",
            description="Visualiza logs do sistema com journalctl.",
            requires_admin=False,
        ),
        Command(
            key="L2",
            name="Logs do Sistema (dmesg)",
            command="gnome-terminal -- dmesg",
            category="Logs",
            description="Exibe mensagens do kernel e boot.",
            requires_admin=False,
        ),
    ]
