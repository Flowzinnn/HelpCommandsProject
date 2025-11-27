import platform
import sys
from enum import Enum
from typing import Tuple


class OSType(Enum):
    """Tipos de sistemas operacionais suportados."""
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    UNKNOWN = "unknown"


def detectar_sistema() -> Tuple[OSType, str]:
    """
    Detecta o sistema operacional atual.
    
    Returns:
        Tupla (OSType, versão_detalhada)
    """
    sistema = platform.system().lower()
    versao = platform.version()
    
    if sistema == "windows":
        return OSType.WINDOWS, f"Windows {platform.release()} ({versao})"
    elif sistema == "linux":
        return OSType.LINUX, f"Linux {platform.release()} ({versao})"
    elif sistema == "darwin":
        return OSType.MACOS, f"macOS {platform.mac_ver()[0]}"
    else:
        return OSType.UNKNOWN, f"{sistema} {versao}"


def eh_windows() -> bool:
    """Verifica se está rodando no Windows."""
    return detectar_sistema()[0] == OSType.WINDOWS


def eh_linux() -> bool:
    """Verifica se está rodando no Linux."""
    return detectar_sistema()[0] == OSType.LINUX


def eh_admin() -> bool:
    """
    Verifica se o programa está sendo executado com privilégios administrativos.
    
    Returns:
        True se está como admin/root, False caso contrário.
    """
    try:
        if eh_windows():
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            import os
            return os.geteuid() == 0
    except Exception:
        return False
