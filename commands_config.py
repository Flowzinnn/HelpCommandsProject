from typing import List
from models import Command
from commands_windows import get_windows_commands


def get_all_commands() -> List[Command]:
    """
    Retorna a lista de comandos do Windows.
    """
    return get_windows_commands()
