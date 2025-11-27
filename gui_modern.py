"""
Interface gráfica moderna usando CustomTkinter para o Help Commands.
"""
import customtkinter as ctk
from typing import List, Dict, Optional
import threading
from datetime import datetime
import ctypes

from models import Command
from commands_config import get_all_commands
from executor import executar_comando, executar_comando_livre, configurar_logger, indexar_por_key
from config_manager import ConfigManager
from help_system import HelpSystem
from collections import defaultdict


# Configurações do CustomTkinter
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


class HelpCommandsGUI:
    """Interface gráfica moderna do Help Commands."""
    
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("Help Commands - Painel de Suporte Técnico")
        
        # Inicializar gerenciadores
        self.config_manager = ConfigManager()
        self.help_system = HelpSystem()
        configurar_logger()
        
        # Carregar comandos
        self.comandos = get_all_commands()
        self.index_comandos = indexar_por_key(self.comandos)
        self.comandos_filtrados = self.comandos.copy()
        
        # Detectar sistema
        import platform
        self.os_version = f"Windows {platform.release()}"
        self.is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
        # Variáveis de interface
        self.search_var = ctk.StringVar()
        self.selected_command: Optional[Command] = None
        self.selected_category = "Todos"
        
        # Configurar janela
        self._setup_window()
        self._create_widgets()
        
        # Atualizar lista inicial
        self.update_command_list()
    
    def _setup_window(self):
        """Configura a janela principal."""
        width = self.config_manager.config.window_width
        height = self.config_manager.config.window_height
        
        # Centralizar janela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(1000, 650)
        
        # Salvar tamanho ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _create_widgets(self):
        """Cria todos os widgets da interface moderna."""
        
        # ========== BARRA SUPERIOR ==========
        header_frame = ctk.CTkFrame(self.root, height=80, corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="🖥️ HELP COMMANDS",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(side="left", padx=30, pady=20)
        
        # Status
        status_text = f"Sistema: {self.os_version} | {'🔒 Admin' if self.is_admin else '👤 Usuário'}"
        status_label = ctk.CTkLabel(
            header_frame,
            text=status_text,
            font=ctk.CTkFont(size=12)
        )
        status_label.pack(side="right", padx=30)
        
        # ========== CONTAINER PRINCIPAL ==========
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ========== PAINEL ESQUERDO ==========
        left_panel = ctk.CTkFrame(main_container, width=380)
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # Barra de busca
        search_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=15)
        
        search_label = ctk.CTkLabel(search_frame, text="🔍 Buscar:", font=ctk.CTkFont(size=13, weight="bold"))
        search_label.pack(anchor="w", pady=(0, 5))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Digite para buscar comandos...",
            textvariable=self.search_var,
            height=40
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", lambda e: self.on_search_changed())
        
        # Filtro por categoria
        category_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        category_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        category_label = ctk.CTkLabel(category_frame, text="📂 Categoria:", font=ctk.CTkFont(size=13, weight="bold"))
        category_label.pack(anchor="w", pady=(0, 5))
        
        categorias = ["Todos"] + sorted(set(cmd.category for cmd in self.comandos))
        self.category_combo = ctk.CTkOptionMenu(
            category_frame,
            values=categorias,
            command=self.on_category_changed,
            height=35
        )
        self.category_combo.pack(fill="x")
        self.category_combo.set("Todos")
        
        # Lista de comandos
        commands_label = ctk.CTkLabel(left_panel, text="📋 Comandos:", font=ctk.CTkFont(size=13, weight="bold"))
        commands_label.pack(anchor="w", padx=15, pady=(0, 5))
        
        # Scrollable frame para comandos
        self.commands_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")
        self.commands_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # ========== PAINEL DIREITO ==========
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Tabs
        self.tabview = ctk.CTkTabview(right_panel)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Tab: Detalhes
        self.tab_details = self.tabview.add("📝 Detalhes")
        self._create_details_tab()
        
        # Tab: Console
        self.tab_console = self.tabview.add("💻 Console")
        self._create_console_tab()
        
        # Tab: Favoritos
        self.tab_favorites = self.tabview.add("⭐ Favoritos")
        self._create_favorites_tab()
        
        # Tab: Histórico
        self.tab_history = self.tabview.add("📜 Histórico")
        self._create_history_tab()
        
        # ========== BARRA DE AÇÕES INFERIOR ==========
        actions_frame = ctk.CTkFrame(self.root, height=70, corner_radius=0)
        actions_frame.pack(fill="x", side="bottom", padx=0, pady=0)
        actions_frame.pack_propagate(False)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        btn_frame.pack(expand=True)
        
        self.btn_execute = ctk.CTkButton(
            btn_frame,
            text="▶️ Executar Comando",
            command=self.execute_selected_command,
            height=45,
            width=180,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#27ae60",
            hover_color="#229954"
        )
        self.btn_execute.pack(side="left", padx=10)
        self.btn_execute.configure(state="disabled")
        
        self.btn_free_cmd = ctk.CTkButton(
            btn_frame,
            text="✏️ Comando Livre",
            command=self.show_free_command_dialog,
            height=45,
            width=180,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_free_cmd.pack(side="left", padx=10)
        
        self.btn_settings = ctk.CTkButton(
            btn_frame,
            text="⚙️ Configurações",
            command=self.show_settings,
            height=45,
            width=180,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_settings.pack(side="left", padx=10)
        
        self.btn_help = ctk.CTkButton(
            btn_frame,
            text="❓ Ajuda",
            command=lambda: self.show_help_dialog("guia"),
            height=45,
            width=180,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_help.pack(side="left", padx=10)
        
        self.btn_about = ctk.CTkButton(
            btn_frame,
            text="ℹ️ Sobre",
            command=lambda: self.show_help_dialog("sobre"),
            height=45,
            width=180,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_about.pack(side="left", padx=10)
    
    def _create_details_tab(self):
        """Cria a aba de detalhes do comando."""
        # Frame de informações
        info_frame = ctk.CTkFrame(self.tab_details, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        self.detail_title = ctk.CTkLabel(
            info_frame,
            text="Selecione um comando",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
        )
        self.detail_title.pack(fill="x", pady=(0, 10))
        
        # Frame de informações detalhadas
        self.detail_info_frame = ctk.CTkFrame(info_frame)
        self.detail_info_frame.pack(fill="both", expand=True)
        
        self.detail_text = ctk.CTkTextbox(
            self.detail_info_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.detail_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botões de ação na aba
        action_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(10, 0))
        
        self.btn_favorite = ctk.CTkButton(
            action_frame,
            text="⭐ Adicionar aos Favoritos",
            command=self.toggle_favorite,
            height=35,
            width=200
        )
        self.btn_favorite.pack(side="left", padx=5)
        self.btn_favorite.configure(state="disabled")
    
    def _create_console_tab(self):
        """Cria a aba do console."""
        console_frame = ctk.CTkFrame(self.tab_console, fg_color="transparent")
        console_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Textbox para console
        self.console_text = ctk.CTkTextbox(
            console_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word",
            fg_color="#1e1e1e"
        )
        self.console_text.pack(fill="both", expand=True)
        
        # Botão limpar console
        btn_clear = ctk.CTkButton(
            console_frame,
            text="🗑️ Limpar Console",
            command=self.clear_console,
            height=35,
            width=150
        )
        btn_clear.pack(pady=(10, 0))
        
        self.console_text.insert("1.0", "Console pronto. Execute comandos para ver a saída aqui.\n")
        self.console_text.configure(state="disabled")
    
    def _create_favorites_tab(self):
        """Cria a aba de favoritos."""
        self.favorites_frame = ctk.CTkScrollableFrame(self.tab_favorites)
        self.favorites_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.update_favorites_list()
    
    def _create_history_tab(self):
        """Cria a aba de histórico."""
        history_frame = ctk.CTkFrame(self.tab_history, fg_color="transparent")
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Textbox para histórico
        self.history_text = ctk.CTkTextbox(
            history_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        self.history_text.pack(fill="both", expand=True)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        btn_refresh = ctk.CTkButton(
            btn_frame,
            text="🔄 Atualizar",
            command=self.update_history_display,
            height=35,
            width=120
        )
        btn_refresh.pack(side="left", padx=5)
        
        btn_export = ctk.CTkButton(
            btn_frame,
            text="💾 Exportar",
            command=self.export_history,
            height=35,
            width=120
        )
        btn_export.pack(side="left", padx=5)
        
        btn_clear_history = ctk.CTkButton(
            btn_frame,
            text="🗑️ Limpar",
            command=self.clear_history,
            height=35,
            width=120,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        btn_clear_history.pack(side="left", padx=5)
        
        self.update_history_display()
    
    def update_command_list(self):
        """Atualiza a lista de comandos exibidos."""
        # Limpar lista atual
        for widget in self.commands_scroll.winfo_children():
            widget.destroy()
        
        # Filtrar comandos
        search_term = self.search_var.get().lower()
        
        for cmd in self.comandos_filtrados:
            if search_term:
                if not (search_term in cmd.name.lower() or 
                       search_term in cmd.description.lower() or
                       search_term in cmd.category.lower()):
                    continue
            
            self._create_command_button(cmd)
    
    def _create_command_button(self, cmd: Command):
        """Cria um botão para o comando."""
        # Frame do comando
        cmd_frame = ctk.CTkFrame(self.commands_scroll)
        cmd_frame.pack(fill="x", pady=5)
        
        # Indicadores
        indicators = ""
        if cmd.requires_admin:
            indicators += "🔒 "
        if cmd.is_critical:
            indicators += "⚠️ "
        if cmd.key in self.config_manager.config.favorites:
            indicators += "⭐ "
        
        # Botão do comando
        btn = ctk.CTkButton(
            cmd_frame,
            text=f"{indicators}{cmd.name}",
            command=lambda c=cmd: self.select_command(c),
            anchor="w",
            height=32,
            font=ctk.CTkFont(size=13)
        )
        btn.pack(fill="x", padx=5, pady=3)
    
    def select_command(self, cmd: Command):
        """Seleciona um comando e exibe seus detalhes."""
        self.selected_command = cmd
        
        # Atualizar detalhes
        self.detail_title.configure(text=cmd.name)
        
        details = f"""
╔══════════════════════════════════════════════════════════════╗
  INFORMAÇÕES DO COMANDO
╚══════════════════════════════════════════════════════════════╝

📌 Nome: {cmd.name}

🔑 Atalho: [{cmd.key}]

📂 Categoria: {cmd.category}

💻 Comando: {cmd.command}

📝 Descrição:
{cmd.description}

{"🔒 Requer Privilégios Administrativos" if cmd.requires_admin else "👤 Não Requer Privilégios Especiais"}

{"⚠️  ATENÇÃO: Comando Crítico - Use com Cautela!" if cmd.is_critical else ""}
"""
        
        self.detail_text.configure(state="normal")
        self.detail_text.delete("1.0", "end")
        self.detail_text.insert("1.0", details)
        self.detail_text.configure(state="disabled")
        
        # Atualizar botões
        self.btn_execute.configure(state="normal")
        self.btn_favorite.configure(state="normal")
        
        # Atualizar texto do botão de favorito
        if cmd.key in self.config_manager.config.favorites:
            self.btn_favorite.configure(text="⭐ Remover dos Favoritos")
        else:
            self.btn_favorite.configure(text="⭐ Adicionar aos Favoritos")
    
    def execute_selected_command(self):
        """Executa o comando selecionado."""
        if not self.selected_command:
            return
        
        cmd = self.selected_command
        
        # Confirmação para comandos críticos
        if cmd.is_critical:
            dialog = ctk.CTkInputDialog(
                text=f"⚠️ ATENÇÃO: '{cmd.name}' é um comando crítico!\n\nDigite 'CONFIRMAR' para executar:",
                title="Confirmação Necessária"
            )
            if dialog.get_input() != "CONFIRMAR":
                self.log_to_console("Execução cancelada pelo usuário.\n")
                return
        
        # Mudar para aba do console
        self.tabview.set("💻 Console")
        
        # Executar em thread separada
        def execute():
            self.log_to_console(f"\n{'='*60}\n")
            self.log_to_console(f"[EXECUTANDO] {cmd.name}\n")
            self.log_to_console(f"Comando: {cmd.command}\n")
            self.log_to_console(f"{'='*60}\n\n")
            
            try:
                # Executar comando (isso vai imprimir no console padrão)
                executar_comando(cmd)
                self.log_to_console("\n✅ Comando executado.\n")
                
                # Adicionar ao histórico
                self.config_manager.add_to_history(cmd.key, cmd.name, "sucesso")
                self.update_history_display()
                
            except Exception as e:
                self.log_to_console(f"\n❌ Erro: {str(e)}\n")
                self.config_manager.add_to_history(cmd.key, cmd.name, "erro")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def show_free_command_dialog(self):
        """Mostra diálogo para executar comando livre."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Comando Livre")
        dialog.geometry("600x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 600) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 300) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Conteúdo
        ctk.CTkLabel(
            dialog,
            text="✏️ Digite o comando do Windows:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        cmd_entry = ctk.CTkTextbox(dialog, height=100)
        cmd_entry.pack(fill="x", padx=20, pady=10)
        
        admin_var = ctk.BooleanVar()
        admin_check = ctk.CTkCheckBox(
            dialog,
            text="Executar como Administrador",
            variable=admin_var
        )
        admin_check.pack(pady=10)
        
        def execute():
            comando = cmd_entry.get("1.0", "end").strip()
            if comando:
                self.tabview.set("💻 Console")
                self.log_to_console(f"\n{'='*60}\n")
                self.log_to_console(f"[COMANDO LIVRE] {comando}\n")
                self.log_to_console(f"{'='*60}\n\n")
                
                try:
                    executar_comando_livre(comando, admin_var.get())
                    self.log_to_console("\n✅ Comando executado.\n")
                except Exception as e:
                    self.log_to_console(f"\n❌ Erro: {str(e)}\n")
                
                dialog.destroy()
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="▶️ Executar",
            command=execute,
            width=120,
            height=40,
            fg_color="#27ae60",
            hover_color="#229954"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=dialog.destroy,
            width=120,
            height=40
        ).pack(side="left", padx=10)
    
    def show_settings(self):
        """Mostra janela de configurações."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Configurações")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 500) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 400) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Título
        ctk.CTkLabel(
            dialog,
            text="⚙️ Configurações",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Frame de configurações
        settings_frame = ctk.CTkFrame(dialog)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tema
        theme_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(theme_frame, text="🎨 Tema:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        theme_var = ctk.StringVar(value=self.config_manager.config.theme)
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["light", "dark"],
            variable=theme_var
        )
        theme_menu.pack(fill="x", pady=(5, 0))
        
        # Confirmação de comandos críticos
        confirm_var = ctk.BooleanVar(value=self.config_manager.config.confirm_critical)
        confirm_check = ctk.CTkCheckBox(
            settings_frame,
            text="Confirmar comandos críticos",
            variable=confirm_var
        )
        confirm_check.pack(padx=20, pady=10, anchor="w")
        
        # Avisos de admin
        warnings_var = ctk.BooleanVar(value=self.config_manager.config.show_admin_warnings)
        warnings_check = ctk.CTkCheckBox(
            settings_frame,
            text="Mostrar avisos de privilégios",
            variable=warnings_var
        )
        warnings_check.pack(padx=20, pady=10, anchor="w")
        
        # Auto-scroll
        autoscroll_var = ctk.BooleanVar(value=self.config_manager.config.auto_scroll_console)
        autoscroll_check = ctk.CTkCheckBox(
            settings_frame,
            text="Auto-scroll no console",
            variable=autoscroll_var
        )
        autoscroll_check.pack(padx=20, pady=10, anchor="w")
        
        def save_settings():
            self.config_manager.config.theme = theme_var.get()
            self.config_manager.config.confirm_critical = confirm_var.get()
            self.config_manager.config.show_admin_warnings = warnings_var.get()
            self.config_manager.config.auto_scroll_console = autoscroll_var.get()
            self.config_manager.save_config()
            
            # Aplicar tema
            ctk.set_appearance_mode(theme_var.get())
            
            dialog.destroy()
        
        # Botões
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar",
            command=save_settings,
            width=120,
            height=40,
            fg_color="#27ae60",
            hover_color="#229954"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=dialog.destroy,
            width=120,
            height=40
        ).pack(side="left", padx=10)
    
    def show_help_dialog(self, tipo: str):
        """Mostra janela de ajuda."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Ajuda - Help Commands")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        
        # Centralizar
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 800) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 600) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Conteúdo
        if tipo == "guia":
            content = self.help_system.get_guia_uso()
            title = "📖 Guia de Uso"
        elif tipo == "sobre":
            content = self.help_system.get_sobre()
            title = "ℹ️ Sobre"
        else:
            content = self.help_system.get_troubleshooting()
            title = "🔧 Solução de Problemas"
        
        ctk.CTkLabel(
            dialog,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)
        
        text_box = ctk.CTkTextbox(
            dialog,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        text_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        text_box.insert("1.0", content)
        text_box.configure(state="disabled")
        
        ctk.CTkButton(
            dialog,
            text="✅ Fechar",
            command=dialog.destroy,
            width=120,
            height=40
        ).pack(pady=(0, 20))
    
    def toggle_favorite(self):
        """Adiciona/remove comando dos favoritos."""
        if not self.selected_command:
            return
        
        cmd = self.selected_command
        
        if cmd.key in self.config_manager.config.favorites:
            self.config_manager.config.favorites.remove(cmd.key)
            self.btn_favorite.configure(text="⭐ Adicionar aos Favoritos")
        else:
            self.config_manager.config.favorites.append(cmd.key)
            self.btn_favorite.configure(text="⭐ Remover dos Favoritos")
        
        self.config_manager.save_config()
        self.update_command_list()
        self.update_favorites_list()
    
    def update_favorites_list(self):
        """Atualiza a lista de favoritos."""
        for widget in self.favorites_frame.winfo_children():
            widget.destroy()
        
        favoritos = [cmd for cmd in self.comandos if cmd.key in self.config_manager.config.favorites]
        
        if not favoritos:
            ctk.CTkLabel(
                self.favorites_frame,
                text="Nenhum favorito ainda.\nClique em ⭐ para adicionar comandos aos favoritos!",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
        else:
            for cmd in favoritos:
                self._create_command_button_in_frame(cmd, self.favorites_frame)
    
    def _create_command_button_in_frame(self, cmd: Command, parent_frame):
        """Cria um botão para comando em um frame específico."""
        cmd_frame = ctk.CTkFrame(parent_frame)
        cmd_frame.pack(fill="x", pady=5, padx=10)
        
        indicators = ""
        if cmd.requires_admin:
            indicators += "🔒 "
        if cmd.is_critical:
            indicators += "⚠️ "
        
        btn = ctk.CTkButton(
            cmd_frame,
            text=f"{indicators}{cmd.name}",
            command=lambda c=cmd: self.select_command(c),
            anchor="w",
            height=50,
            font=ctk.CTkFont(size=13)
        )
        btn.pack(fill="x", padx=5, pady=5)
    
    def on_search_changed(self):
        """Callback quando a busca muda."""
        self.update_command_list()
    
    def on_category_changed(self, category: str):
        """Callback quando a categoria muda."""
        self.selected_category = category
        
        if category == "Todos":
            self.comandos_filtrados = self.comandos.copy()
        else:
            self.comandos_filtrados = [cmd for cmd in self.comandos if cmd.category == category]
        
        self.update_command_list()
    
    def log_to_console(self, message: str):
        """Adiciona mensagem ao console."""
        self.console_text.configure(state="normal")
        self.console_text.insert("end", message)
        if self.config_manager.config.auto_scroll_console:
            self.console_text.see("end")
        self.console_text.configure(state="disabled")
    
    def clear_console(self):
        """Limpa o console."""
        self.console_text.configure(state="normal")
        self.console_text.delete("1.0", "end")
        self.console_text.insert("1.0", "Console limpo.\n")
        self.console_text.configure(state="disabled")
    
    def update_history_display(self):
        """Atualiza a exibição do histórico."""
        history = self.config_manager.get_history()
        
        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", "end")
        
        if not history:
            self.history_text.insert("1.0", "Nenhum comando executado ainda.\n")
        else:
            self.history_text.insert("1.0", "═══════════════════════════════════════════════════════════\n")
            self.history_text.insert("end", "                    HISTÓRICO DE COMANDOS\n")
            self.history_text.insert("end", "═══════════════════════════════════════════════════════════\n\n")
            
            for i, entry in enumerate(reversed(history), 1):
                status_icon = "✅" if entry["status"] == "sucesso" else "❌"
                self.history_text.insert("end", f"{i}. {status_icon} {entry['command_name']}\n")
                self.history_text.insert("end", f"   📅 {entry['timestamp']}\n")
                self.history_text.insert("end", f"   🔑 Código: {entry['command_key']}\n")
                self.history_text.insert("end", "\n")
        
        self.history_text.configure(state="disabled")
    
    def export_history(self):
        """Exporta histórico para arquivo."""
        from tkinter import filedialog
        import json
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                history = self.config_manager.get_history()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("═══════════════════════════════════════════════════════════\n")
                    f.write("           HISTÓRICO DE COMANDOS - HELP COMMANDS\n")
                    f.write("═══════════════════════════════════════════════════════════\n\n")
                    
                    for entry in reversed(history):
                        f.write(f"Comando: {entry['command_name']}\n")
                        f.write(f"Data/Hora: {entry['timestamp']}\n")
                        f.write(f"Código: {entry['command_key']}\n")
                        f.write(f"Status: {entry['status']}\n")
                        f.write("-" * 60 + "\n\n")
                
                self.log_to_console(f"✅ Histórico exportado para: {filename}\n")
            except Exception as e:
                self.log_to_console(f"❌ Erro ao exportar histórico: {str(e)}\n")
    
    def clear_history(self):
        """Limpa o histórico."""
        dialog = ctk.CTkInputDialog(
            text="⚠️ Isso vai apagar todo o histórico!\n\nDigite 'CONFIRMAR' para continuar:",
            title="Confirmação"
        )
        
        if dialog.get_input() == "CONFIRMAR":
            self.config_manager.clear_history()
            self.update_history_display()
            self.log_to_console("🗑️ Histórico limpo.\n")
    
    def on_closing(self):
        """Callback ao fechar a janela."""
        # Salvar tamanho da janela
        self.config_manager.config.window_width = self.root.winfo_width()
        self.config_manager.config.window_height = self.root.winfo_height()
        self.config_manager.save_config()
        
        self.root.destroy()


def main():
    """Função principal para iniciar a GUI moderna."""
    root = ctk.CTk()
    app = HelpCommandsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
