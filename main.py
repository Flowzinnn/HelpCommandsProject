import sys
from collections import defaultdict
from typing import Dict, List

from commands_config import get_all_commands
from executor import (
    configurar_logger,
    executar_comando,
    executar_comando_livre,
    indexar_por_key,
)
from models import Command


def agrupar_por_categoria(comandos: List[Command]) -> Dict[str, List[Command]]:
    """
    Agrupa os comandos por categoria para exibir no menu.
    """
    grupos: Dict[str, List[Command]] = defaultdict(list)
    for cmd in comandos:
        grupos[cmd.category].append(cmd)
    return grupos


def mostrar_menu(comandos: List[Command]) -> None:
    """
    Exibe o menu principal, agrupando comandos por categoria.
    """
    grupos = agrupar_por_categoria(comandos)

    print("\n======================================")
    print("   MINI TERMINAL - SUPORTE REMOTO")
    print("======================================")
    print("Comandos disponíveis:\n")

    for categoria, lista_cmds in grupos.items():
        print(f"--- {categoria} ---")
        for cmd in lista_cmds:
            print(f"[{cmd.key}] {cmd.name}  ->  {cmd.command}")
        print()

    print("[C] Comando livre (digitar manualmente)")
    print("[Q] Sair")
    print("======================================")


def loop_principal() -> None:
    """
    Loop principal da ferramenta de suporte.
    """
    configurar_logger()

    comandos = get_all_commands()
    index = indexar_por_key(comandos)

    while True:
        mostrar_menu(comandos)
        escolha = input("Escolha uma opção: ").strip().upper()

        if escolha == "Q":
            print("Encerrando o mini terminal. Até a próxima.")
            break

        if escolha == "C":
            comando_texto = input("Digite o comando do Windows: ").strip()
            if comando_texto:
                executar_comando_livre(comando_texto)
            else:
                print("Nenhum comando digitado.")
            continue

        cmd = index.get(escolha)
        if cmd is None:
            print("Opção inválida. Tente novamente.")
            continue

        executar_comando(cmd)


if __name__ == "__main__":
    # Verificar se deve rodar em modo GUI ou terminal
    if len(sys.argv) > 1 and sys.argv[1] == "--terminal":
        # Modo terminal (legado)
        print("Executando em modo terminal...")
        loop_principal()
    else:
        # Modo GUI (padrão)
        try:
            import tkinter as tk
            from gui import main as gui_main
            
            print("Iniciando interface gráfica...")
            gui_main()
        except ImportError:
            print("ERRO: Tkinter não está instalado.")
            print("Executando em modo terminal como fallback...")
            loop_principal()
        except Exception as e:
            print(f"ERRO ao iniciar GUI: {e}")
            print("Executando em modo terminal como fallback...")
            loop_principal()
