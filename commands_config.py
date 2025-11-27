from typing import List
from models import Command
from platform_detector import detectar_sistema, OSType
from commands_windows import get_windows_commands
from commands_linux import get_linux_commands


def get_all_commands() -> List[Command]:
    """
    Retorna a lista de comandos apropriados para o sistema operacional atual.
    """
    os_type, _ = detectar_sistema()
    
    if os_type == OSType.WINDOWS:
        return get_windows_commands()
    elif os_type == OSType.LINUX:
        return get_linux_commands()
    else:
        # Fallback: retorna comandos básicos multiplataforma
        return [
            Command(
                key="1",
                name="Terminal/Prompt",
                command="cmd" if os_type == OSType.WINDOWS else "gnome-terminal",
                category="Sistema",
                description="Abre o terminal do sistema.",
                requires_admin=False,
            ),
        ]
