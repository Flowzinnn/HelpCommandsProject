import logging
import subprocess
import sys
from typing import Iterable, Dict, Optional, Callable
from models import Command
from platform_detector import eh_windows, eh_linux, eh_admin


LOG_FILE = "mini_terminal_suporte.log"


def configurar_logger() -> None:
    """
    Configura o logger básico para registrar execuções de comandos.
    """
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def indexar_por_key(comandos: Iterable[Command]) -> Dict[str, Command]:
    """
    Cria um dicionário {key: Command} para lookup rápido pelo código do menu.
    """
    return {cmd.key.upper(): cmd for cmd in comandos}


def executar_com_elevacao_windows(comando: str) -> bool:
    """
    Executa comando com elevação UAC no Windows usando ShellExecuteEx.
    
    Returns:
        True se executado com sucesso, False caso contrário.
    """
    try:
        import ctypes
        from ctypes import wintypes
        
        # Constantes do Windows
        SEE_MASK_NOCLOSEPROCESS = 0x00000040
        SW_SHOWNORMAL = 1
        
        class SHELLEXECUTEINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", wintypes.DWORD),
                ("fMask", ctypes.c_ulong),
                ("hwnd", wintypes.HWND),
                ("lpVerb", wintypes.LPCWSTR),
                ("lpFile", wintypes.LPCWSTR),
                ("lpParameters", wintypes.LPCWSTR),
                ("lpDirectory", wintypes.LPCWSTR),
                ("nShow", ctypes.c_int),
                ("hInstApp", wintypes.HINSTANCE),
                ("lpIDList", ctypes.c_void_p),
                ("lpClass", wintypes.LPCWSTR),
                ("hKeyClass", wintypes.HKEY),
                ("dwHotKey", wintypes.DWORD),
                ("hIconOrMonitor", wintypes.HANDLE),
                ("hProcess", wintypes.HANDLE),
            ]
        
        sei = SHELLEXECUTEINFO()
        sei.cbSize = ctypes.sizeof(sei)
        sei.fMask = SEE_MASK_NOCLOSEPROCESS
        sei.hwnd = None
        sei.lpVerb = "runas"  # Solicita elevação
        sei.lpFile = "cmd.exe"
        sei.lpParameters = f'/c "{comando}"'
        sei.lpDirectory = None
        sei.nShow = SW_SHOWNORMAL
        
        if not ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei)):
            raise ctypes.WinError()
        
        print(f"Comando executado com privilégios administrativos.")
        logging.info("Comando executado com elevação: %s", comando)
        return True
        
    except Exception as e:
        print(f"Erro ao executar com elevação: {e}")
        logging.error("Falha na elevação: %s", e)
        return False


def executar_com_sudo_linux(comando: str) -> bool:
    """
    Executa comando com sudo no Linux.
    
    Returns:
        True se executado com sucesso, False caso contrário.
    """
    try:
        comando_sudo = f"sudo {comando}"
        print(f"\n[EXECUTANDO COM SUDO] {comando_sudo}\n")
        
        resultado = subprocess.run(
            comando_sudo,
            shell=True,
            text=True,
        )
        
        if resultado.returncode == 0:
            print("Comando executado com sucesso.")
            logging.info("Comando sudo executado: %s", comando)
            return True
        else:
            print(f"Comando retornou código: {resultado.returncode}")
            logging.warning("Comando sudo retornou %s: %s", resultado.returncode, comando)
            return False
            
    except Exception as e:
        print(f"Erro ao executar com sudo: {e}")
        logging.error("Falha no sudo: %s", e)
        return False


def executar_comando(cmd: Command, confirmacao_callback: Optional[Callable[[Command], bool]] = None) -> None:
    """
    Executa um Command, solicitando elevação se necessário.
    
    Args:
        cmd: Comando a ser executado
        confirmacao_callback: Função opcional que retorna True se usuário confirmar comando crítico
    """
    # Verificar se comando crítico precisa de confirmação
    if cmd.is_critical and confirmacao_callback:
        if not confirmacao_callback(cmd):
            print("Execução cancelada pelo usuário.")
            logging.info("Execução cancelada: %s", cmd.name)
            return
    
    logging.info("Executando comando: %s (%s)", cmd.name, cmd.command)
    print(f"\n[EXECUTANDO] {cmd.name} -> {cmd.command}\n")
    
    # Verificar se precisa de privilégios administrativos
    if cmd.requires_admin and not eh_admin():
        print(f"⚠️  Este comando requer privilégios administrativos.")
        
        if eh_windows():
            print("Solicitando elevação via UAC...")
            if executar_com_elevacao_windows(cmd.command):
                return
            else:
                print("Falha na elevação. Executando sem privilégios...")
        elif eh_linux():
            print("Executando com sudo...")
            if executar_com_sudo_linux(cmd.command):
                return
            else:
                print("Falha no sudo. Tentando executar sem privilégios...")
    
    # Execução normal
    try:
        resultado = subprocess.run(
            cmd.command,
            shell=True,
            text=True,
            capture_output=True,
        )

        if resultado.stdout:
            print("Saída:")
            print(resultado.stdout)

        if resultado.stderr:
            print("Erros:")
            print(resultado.stderr)

        if resultado.returncode != 0:
            print(f"Código de retorno: {resultado.returncode}")
            logging.warning(
                "Comando retornou código %s: %s",
                resultado.returncode,
                cmd.command,
            )
        else:
            logging.info("Comando executado com sucesso: %s", cmd.name)

    except Exception as exc:
        print(f"Erro ao executar o comando: {exc}")
        logging.exception("Erro ao executar comando: %s", cmd.command)


def executar_comando_livre(comando_texto: str, requer_admin: bool = False) -> None:
    """
    Executa um comando arbitrário digitado pelo operador.
    
    Args:
        comando_texto: Comando a ser executado
        requer_admin: Se True, tenta executar com privilégios elevados
    """
    logging.info("Executando comando livre: %s", comando_texto)
    print(f"\n[EXECUTANDO LIVRE] {comando_texto}\n")
    
    # Elevação se solicitada
    if requer_admin and not eh_admin():
        print(f"⚠️  Executando com privilégios administrativos...")
        
        if eh_windows():
            executar_com_elevacao_windows(comando_texto)
            return
        elif eh_linux():
            executar_com_sudo_linux(comando_texto)
            return
    
    # Execução normal
    try:
        resultado = subprocess.run(
            comando_texto,
            shell=True,
            text=True,
            capture_output=True,
        )

        if resultado.stdout:
            print("Saída:")
            print(resultado.stdout)

        if resultado.stderr:
            print("Erros:")
            print(resultado.stderr)

        if resultado.returncode != 0:
            print(f"Código de retorno: {resultado.returncode}")
            logging.warning(
                "Comando livre retornou código %s: %s",
                resultado.returncode,
                comando_texto,
            )

    except Exception as exc:
        print(f"Erro ao executar o comando livre: {exc}")
        logging.exception("Erro ao executar comando livre: %s", comando_texto)
