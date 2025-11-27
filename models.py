from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Command:
    """
    Representa um comando executável multiplataforma.

    Atributos:
        key: tecla/opção usada no menu (ex.: "1", "A").
        name: nome amigável exibido no menu.
        command: comando que será passado para o shell.
        category: categoria lógica (ex.: "Sistema", "Rede", "Usuário").
        description: descrição detalhada do que o comando faz.
        requires_admin: se True, exige privilégios administrativos.
        is_critical: se True, pede confirmação antes de executar.
    """
    key: str
    name: str
    command: str
    category: str
    description: str = "Sem descrição disponível."
    requires_admin: bool = False
    is_critical: bool = False
