"""
Mini Terminal - Painel de Controle de Suporte
Aplicação GUI moderna para executar comandos do Windows de forma organizada.
"""

if __name__ == "__main__":
    try:
        from gui_modern import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"ERRO: Não foi possível importar a interface gráfica: {e}")
        print("Certifique-se de que o CustomTkinter está instalado.")
        print("Execute: pip install customtkinter")
        input("Pressione Enter para sair...")
    except Exception as e:
        print(f"ERRO ao iniciar a aplicação: {e}")
        input("Pressione Enter para sair...")
