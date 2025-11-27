import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from typing import List, Dict, Optional
import threading
from datetime import datetime

from models import Command
from commands_config import get_all_commands
from executor import executar_comando, executar_comando_livre, configurar_logger, indexar_por_key
from config_manager import ConfigManager
from help_system import HelpSystem
from collections import defaultdict
import ctypes


class HelpCommandsGUI:
    """Interface gráfica principal do Help Commands."""
    
    def __init__(self, root: tk.Tk):
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
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        self.selected_command: Optional[Command] = None
        
        # Configurar janela
        self._setup_window()
        self._create_widgets()
        self._apply_theme()
        
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
        self.root.minsize(900, 600)
        
        # Salvar tamanho ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _create_widgets(self):
        """Cria todos os widgets da interface."""
        
        # ========== BARRA DE TÍTULO E STATUS ==========
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🖥️ MINI TERMINAL - PAINEL DE CONTROLE",
            font=("Segoe UI", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Status do sistema
        status_text = f"Sistema: {self.os_version} | Privilégios: {'🔒 Admin' if self.is_admin else '👤 Usuário'}"
        status_label = tk.Label(
            title_frame,
            text=status_text,
            font=("Segoe UI", 9),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        status_label.pack(side=tk.RIGHT, padx=20)
        
        # ========== CONTAINER PRINCIPAL ==========
        main_container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=5)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ========== PAINEL ESQUERDO (Lista de Comandos) ==========
        left_panel = tk.Frame(main_container, width=400)
        main_container.add(left_panel, minsize=350)
        
        # Barra de ferramentas
        toolbar = tk.Frame(left_panel, height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Busca
        search_frame = tk.Frame(toolbar)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(search_frame, text="🔍 Buscar:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 10))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind("<Escape>", lambda e: self.search_var.set(""))
        
        # Botões
        btn_frame = tk.Frame(toolbar)
        btn_frame.pack(side=tk.RIGHT, padx=(5, 0))
        
        tk.Button(
            btn_frame,
            text="⭐ Favoritos",
            command=self.toggle_favoritos_filter,
            font=("Segoe UI", 9),
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            btn_frame,
            text="🔄 Limpar",
            command=lambda: self.search_var.set(""),
            font=("Segoe UI", 9),
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        # Filtro por categoria
        filter_frame = tk.Frame(left_panel)
        filter_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(0, 5))
        
        tk.Label(filter_frame, text="Categoria:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.category_var = tk.StringVar(value="Todas")
        categorias = ["Todas"] + sorted(set(cmd.category for cmd in self.comandos))
        category_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.category_var,
            values=categorias,
            state="readonly",
            font=("Segoe UI", 9),
            width=20
        )
        category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        category_combo.bind("<<ComboboxSelected>>", lambda e: self.update_command_list())
        
        # Lista de comandos
        list_frame = tk.Frame(left_panel)
        list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.command_listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            activestyle="none"
        )
        self.command_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.command_listbox.yview)
        
        self.command_listbox.bind("<<ListboxSelect>>", self.on_command_selected)
        self.command_listbox.bind("<Double-Button-1>", lambda e: self.executar_comando_selecionado())
        
        # ========== PAINEL DIREITO ==========
        right_panel = tk.Frame(main_container)
        main_container.add(right_panel, minsize=500)
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # === ABA: Detalhes do Comando ===
        details_tab = tk.Frame(self.notebook)
        self.notebook.add(details_tab, text="📋 Detalhes")
        
        # Área de detalhes
        details_scroll_frame = tk.Frame(details_tab)
        details_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.details_text = scrolledtext.ScrolledText(
            details_scroll_frame,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#f8f9fa"
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        action_frame = tk.Frame(details_tab)
        action_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        self.btn_execute = tk.Button(
            action_frame,
            text="▶️ EXECUTAR COMANDO",
            command=self.executar_comando_selecionado,
            font=("Segoe UI", 11, "bold"),
            bg="#27ae60",
            fg="white",
            height=2,
            state=tk.DISABLED
        )
        self.btn_execute.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.btn_favorite = tk.Button(
            action_frame,
            text="⭐ Favorito",
            command=self.toggle_favorite,
            font=("Segoe UI", 10),
            height=2,
            state=tk.DISABLED,
            width=12
        )
        self.btn_favorite.pack(side=tk.LEFT, padx=5)
        
        # === ABA: Console de Saída ===
        console_tab = tk.Frame(self.notebook)
        self.notebook.add(console_tab, text="💻 Console")
        
        console_toolbar = tk.Frame(console_tab)
        console_toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Button(
            console_toolbar,
            text="🗑️ Limpar Console",
            command=self.clear_console,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        self.console_text = scrolledtext.ScrolledText(
            console_tab,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="#00ff00",
            insertbackground="white"
        )
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # === ABA: Histórico ===
        history_tab = tk.Frame(self.notebook)
        self.notebook.add(history_tab, text="📜 Histórico")
        
        history_toolbar = tk.Frame(history_tab)
        history_toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Button(
            history_toolbar,
            text="🔄 Atualizar",
            command=self.update_history,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            history_toolbar,
            text="💾 Exportar",
            command=self.exportar_historico,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            history_toolbar,
            text="🗑️ Limpar",
            command=self.limpar_historico,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        self.history_text = scrolledtext.ScrolledText(
            history_tab,
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # === ABA: Ajuda ===
        help_tab = tk.Frame(self.notebook)
        self.notebook.add(help_tab, text="❓ Ajuda")
        
        help_buttons = tk.Frame(help_tab)
        help_buttons.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Button(
            help_buttons,
            text="📖 Guia de Uso",
            command=lambda: self.show_help("guia"),
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            help_buttons,
            text="🔧 Solução de Problemas",
            command=lambda: self.show_help("troubleshooting"),
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            help_buttons,
            text="ℹ️ Sobre",
            command=lambda: self.show_help("sobre"),
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        self.help_text = scrolledtext.ScrolledText(
            help_tab,
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.help_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Mostrar guia inicial
        self.show_help("guia")
        
        # ========== BARRA DE MENU ==========
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Comando Livre...", command=self.show_free_command_dialog, accelerator="Ctrl+L")
        file_menu.add_separator()
        file_menu.add_command(label="Exportar Histórico...", command=self.exportar_historico)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.on_closing, accelerator="Alt+F4")
        
        # Menu Ferramentas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
        tools_menu.add_command(label="Limpar Console", command=self.clear_console)
        tools_menu.add_command(label="Ver Histórico", command=lambda: self.notebook.select(2), accelerator="Ctrl+H")
        tools_menu.add_separator()
        tools_menu.add_command(label="Configurações...", command=self.show_settings_dialog, accelerator="Ctrl+S")
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Guia de Uso", command=lambda: self.show_help("guia"))
        help_menu.add_command(label="Solução de Problemas", command=lambda: self.show_help("troubleshooting"))
        help_menu.add_separator()
        help_menu.add_command(label="Sobre", command=lambda: self.show_help("sobre"))
        
        # Atalhos de teclado
        self.root.bind("<Control-l>", lambda e: self.show_free_command_dialog())
        self.root.bind("<Control-h>", lambda e: self.notebook.select(2))
        self.root.bind("<Control-s>", lambda e: self.show_settings_dialog())
        self.root.bind("<Control-f>", lambda e: search_entry.focus())
    
    def _apply_theme(self):
        """Aplica o tema configurado."""
        theme = self.config_manager.config.theme
        
        if theme == "dark":
            # Tema Escuro
            bg_color = "#2b2b2b"
            fg_color = "#ffffff"
            secondary_bg = "#363636"
            button_bg = "#404040"
            highlight_bg = "#505050"
            entry_bg = "#363636"
            text_bg = "#1e1e1e"
        else:
            # Tema Claro (padrão)
            bg_color = "#f0f0f0"
            fg_color = "#000000"
            secondary_bg = "#ffffff"
            button_bg = "#e0e0e0"
            highlight_bg = "#d0d0d0"
            entry_bg = "#ffffff"
            text_bg = "#ffffff"
        
        # Aplicar cores à janela principal
        self.root.configure(bg=bg_color)
        
        # Atualizar todos os frames e widgets
        for widget in self.root.winfo_children():
            self._apply_theme_recursive(widget, bg_color, fg_color, secondary_bg, 
                                       button_bg, highlight_bg, entry_bg, text_bg)
    
    def _apply_theme_recursive(self, widget, bg_color, fg_color, secondary_bg, 
                               button_bg, highlight_bg, entry_bg, text_bg):
        """Aplica tema recursivamente a todos os widgets."""
        try:
            widget_type = widget.winfo_class()
            
            if widget_type == "Frame":
                widget.configure(bg=bg_color)
            elif widget_type == "Label":
                widget.configure(bg=bg_color, fg=fg_color)
            elif widget_type == "Button":
                # Manter cores específicas de botões importantes
                if widget.cget("bg") not in ["#27ae60", "#e74c3c", "#3498db"]:
                    widget.configure(bg=button_bg, fg=fg_color)
            elif widget_type == "Entry":
                widget.configure(bg=entry_bg, fg=fg_color, 
                               insertbackground=fg_color)
            elif widget_type == "Listbox":
                widget.configure(bg=secondary_bg, fg=fg_color, 
                               selectbackground=highlight_bg)
            elif widget_type == "Text":
                widget.configure(bg=text_bg, fg=fg_color, 
                               insertbackground=fg_color)
            elif widget_type == "Checkbutton":
                widget.configure(bg=bg_color, fg=fg_color, 
                               selectcolor=secondary_bg)
            elif widget_type == "Radiobutton":
                widget.configure(bg=bg_color, fg=fg_color, 
                               selectcolor=secondary_bg)
            elif widget_type == "Toplevel":
                widget.configure(bg=bg_color)
            
            # Recursivamente aplicar aos filhos
            for child in widget.winfo_children():
                self._apply_theme_recursive(child, bg_color, fg_color, secondary_bg,
                                           button_bg, highlight_bg, entry_bg, text_bg)
        except:
            pass
    
    def update_command_list(self, filter_text: str = ""):
        """Atualiza a lista de comandos baseado nos filtros."""
        # Filtrar por categoria
        categoria_selecionada = self.category_var.get()
        if categoria_selecionada == "Todas":
            comandos = self.comandos.copy()
        else:
            comandos = [cmd for cmd in self.comandos if cmd.category == categoria_selecionada]
        
        # Filtrar por busca
        if filter_text:
            filter_lower = filter_text.lower()
            comandos = [
                cmd for cmd in comandos
                if (filter_lower in cmd.name.lower() or
                    filter_lower in cmd.command.lower() or
                    filter_lower in cmd.description.lower() or
                    filter_lower in cmd.category.lower())
            ]
        
        self.comandos_filtrados = comandos
        
        # Atualizar listbox
        self.command_listbox.delete(0, tk.END)
        
        for cmd in comandos:
            # Formatação da linha
            fav_marker = "⭐" if self.config_manager.eh_favorito(cmd.key) else "  "
            admin_marker = "🔒" if cmd.requires_admin else "  "
            critical_marker = "⚠️ " if cmd.is_critical else "  "
            
            line = f"{fav_marker} {admin_marker} {critical_marker} [{cmd.key:4}] {cmd.name}"
            self.command_listbox.insert(tk.END, line)
    
    def on_search_changed(self, *args):
        """Callback quando o texto de busca muda."""
        self.update_command_list(self.search_var.get())
    
    def on_command_selected(self, event):
        """Callback quando um comando é selecionado na lista."""
        selection = self.command_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < len(self.comandos_filtrados):
            self.selected_command = self.comandos_filtrados[index]
            self.show_command_details()
            self.btn_execute.config(state=tk.NORMAL)
            self.btn_favorite.config(state=tk.NORMAL)
            self.update_favorite_button()
    
    def show_command_details(self):
        """Mostra os detalhes do comando selecionado."""
        if not self.selected_command:
            return
        
        help_text = self.help_system.get_command_help(self.selected_command)
        
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, help_text)
        self.details_text.config(state=tk.DISABLED)
    
    def executar_comando_selecionado(self):
        """Executa o comando atualmente selecionado."""
        if not self.selected_command:
            return
        
        cmd = self.selected_command
        
        # Confirmação para comandos críticos
        if cmd.is_critical and self.config_manager.config.confirm_critical:
            response = messagebox.askyesno(
                "⚠️ Comando Crítico",
                f"Este é um comando CRÍTICO:\n\n{cmd.name}\n\n"
                f"Pode fazer alterações permanentes no sistema.\n\n"
                f"Deseja realmente executar?",
                icon="warning"
            )
            if not response:
                self.log_to_console(f"❌ Execução cancelada: {cmd.name}\n")
                return
        
        # Aviso sobre privilégios
        if cmd.requires_admin and not self.is_admin and self.config_manager.config.show_admin_warning:
            messagebox.showinfo(
                "🔒 Privilégios Administrativos",
                "Este comando requer privilégios administrativos.\n\n"
                "Uma solicitação UAC será exibida."
            )
        
        # Log
        self.log_to_console(f"\n{'='*60}\n")
        self.log_to_console(f"▶️ Executando: [{cmd.key}] {cmd.name}\n")
        self.log_to_console(f"Comando: {cmd.command}\n")
        self.log_to_console(f"{'='*60}\n\n")
        
        # Selecionar aba do console
        self.notebook.select(1)
        
        # Executar em thread separada
        def execute_thread():
            try:
                # Callback para confirmação
                def confirm_callback(c):
                    return True  # Já confirmamos acima
                
                executar_comando(cmd, confirm_callback)
                
                # Adicionar ao histórico
                self.config_manager.adicionar_ao_historico(
                    cmd.key,
                    cmd.name,
                    cmd.command,
                    success=True
                )
                
                self.root.after(0, lambda: self.log_to_console(f"\n✅ Comando concluído\n"))
            except Exception as e:
                self.root.after(0, lambda: self.log_to_console(f"\n❌ Erro: {e}\n"))
                self.config_manager.adicionar_ao_historico(
                    cmd.key,
                    cmd.name,
                    cmd.command,
                    success=False
                )
        
        threading.Thread(target=execute_thread, daemon=True).start()
    
    def toggle_favorite(self):
        """Adiciona/remove comando dos favoritos."""
        if not self.selected_command:
            return
        
        cmd = self.selected_command
        if self.config_manager.eh_favorito(cmd.key):
            self.config_manager.remover_favorito(cmd.key)
        else:
            self.config_manager.adicionar_favorito(cmd.key)
        
        self.update_command_list(self.search_var.get())
        self.update_favorite_button()
    
    def update_favorite_button(self):
        """Atualiza o texto do botão de favoritos."""
        if not self.selected_command:
            return
        
        if self.config_manager.eh_favorito(self.selected_command.key):
            self.btn_favorite.config(text="⭐ Remover")
        else:
            self.btn_favorite.config(text="⭐ Favorito")
    
    def toggle_favoritos_filter(self):
        """Filtra apenas comandos favoritos."""
        favoritos = self.config_manager.config.favorites
        if not favoritos:
            messagebox.showinfo("Favoritos", "Você ainda não tem comandos favoritos!")
            return
        
        comandos_fav = [cmd for cmd in self.comandos if cmd.key in favoritos]
        self.comandos_filtrados = comandos_fav
        
        self.command_listbox.delete(0, tk.END)
        for cmd in comandos_fav:
            line = f"⭐ {'🔒' if cmd.requires_admin else '  '} {'⚠️ ' if cmd.is_critical else '  '} [{cmd.key:4}] {cmd.name}"
            self.command_listbox.insert(tk.END, line)
    
    def log_to_console(self, message: str):
        """Adiciona mensagem ao console."""
        self.console_text.insert(tk.END, message)
        if self.config_manager.config.auto_scroll:
            self.console_text.see(tk.END)
    
    def clear_console(self):
        """Limpa o console de saída."""
        self.console_text.delete(1.0, tk.END)
    
    def update_history(self):
        """Atualiza a exibição do histórico."""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        if not self.config_manager.history:
            self.history_text.insert(1.0, "Nenhum comando executado ainda.\n")
        else:
            for entry in reversed(self.config_manager.history[-50:]):  # Últimos 50
                status = "✅" if entry.success else "❌"
                text = f"{status} {entry.timestamp} - [{entry.command_key}] {entry.command_name}\n"
                text += f"   Comando: {entry.command_text}\n\n"
                self.history_text.insert(tk.END, text)
        
        self.history_text.config(state=tk.DISABLED)
    
    def exportar_historico(self):
        """Exporta o histórico para arquivo de texto."""
        if not self.config_manager.history:
            messagebox.showinfo("Exportar", "Não há histórico para exportar.")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de Texto", "*.txt"), ("Todos os arquivos", "*.*")],
            initialfile=f"historico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filepath:
            if self.config_manager.exportar_historico_txt(filepath):
                messagebox.showinfo("Exportar", f"Histórico exportado com sucesso!\n\n{filepath}")
            else:
                messagebox.showerror("Exportar", "Erro ao exportar histórico.")
    
    def limpar_historico(self):
        """Limpa o histórico de comandos."""
        response = messagebox.askyesno(
            "Limpar Histórico",
            "Tem certeza que deseja limpar todo o histórico?\n\nEsta ação não pode ser desfeita.",
            icon="warning"
        )
        if response:
            self.config_manager.history.clear()
            self.config_manager.salvar_historico()
            self.update_history()
            messagebox.showinfo("Limpar", "Histórico limpo com sucesso!")
    
    def show_help(self, tipo: str):
        """Mostra conteúdo de ajuda."""
        self.help_text.config(state=tk.NORMAL)
        self.help_text.delete(1.0, tk.END)
        
        if tipo == "guia":
            content = self.help_system.get_guia_uso()
        elif tipo == "troubleshooting":
            content = self.help_system.get_troubleshooting()
        elif tipo == "sobre":
            content = self.help_system.get_sobre()
        else:
            content = "Conteúdo não encontrado."
        
        self.help_text.insert(1.0, content)
        self.help_text.config(state=tk.DISABLED)
        
        # Selecionar aba de ajuda
        self.notebook.select(3)
    
    def show_free_command_dialog(self):
        """Mostra diálogo para executar comando livre."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Comando Livre")
        dialog.geometry("600x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Digite o comando do sistema que deseja executar:",
            font=("Segoe UI", 10)
        ).pack(padx=20, pady=(20, 10))
        
        command_entry = tk.Entry(dialog, font=("Consolas", 11))
        command_entry.pack(padx=20, pady=10, fill=tk.X)
        command_entry.focus()
        
        admin_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            dialog,
            text="🔒 Executar com privilégios administrativos",
            variable=admin_var,
            font=("Segoe UI", 9)
        ).pack(padx=20, pady=5)
        
        def execute():
            comando = command_entry.get().strip()
            if not comando:
                messagebox.showwarning("Comando Livre", "Digite um comando!")
                return
            
            dialog.destroy()
            
            # Log
            self.log_to_console(f"\n{'='*60}\n")
            self.log_to_console(f"▶️ Comando Livre: {comando}\n")
            self.log_to_console(f"{'='*60}\n\n")
            self.notebook.select(1)
            
            # Executar
            def exec_thread():
                try:
                    executar_comando_livre(comando, admin_var.get())
                    self.config_manager.adicionar_ao_historico(
                        "LIVRE",
                        "Comando Livre",
                        comando,
                        success=True,
                        is_free_command=True
                    )
                    self.root.after(0, lambda: self.log_to_console(f"\n✅ Comando concluído\n"))
                except Exception as e:
                    self.root.after(0, lambda: self.log_to_console(f"\n❌ Erro: {e}\n"))
            
            threading.Thread(target=exec_thread, daemon=True).start()
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="▶️ Executar",
            command=execute,
            font=("Segoe UI", 10, "bold"),
            bg="#27ae60",
            fg="white",
            width=15,
            height=2
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            command=dialog.destroy,
            font=("Segoe UI", 10),
            width=15,
            height=2
        ).pack(side=tk.LEFT, padx=5)
        
        command_entry.bind("<Return>", lambda e: execute())
        command_entry.bind("<Escape>", lambda e: dialog.destroy())
    
    def show_settings_dialog(self):
        """Mostra diálogo de configurações."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Configurações")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(
            dialog,
            text="⚙️ Configurações",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=20)
        
        config_frame = tk.Frame(dialog)
        config_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
        
        # Tema
        tk.Label(
            config_frame,
            text="🎨 Tema da Interface:",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))
        
        theme_var = tk.StringVar(value=self.config_manager.config.theme)
        theme_frame = tk.Frame(config_frame)
        theme_frame.pack(anchor=tk.W, padx=20, pady=5)
        
        tk.Radiobutton(
            theme_frame,
            text="☀️ Claro",
            variable=theme_var,
            value="light",
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            theme_frame,
            text="🌙 Escuro",
            variable=theme_var,
            value="dark",
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=10)
        
        # Separador
        ttk.Separator(config_frame, orient='horizontal').pack(fill='x', pady=15)
        
        # Auto-scroll
        auto_scroll_var = tk.BooleanVar(value=self.config_manager.config.auto_scroll)
        tk.Checkbutton(
            config_frame,
            text="Auto-scroll no console",
            variable=auto_scroll_var,
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W, pady=5)
        
        # Confirmação crítica
        confirm_var = tk.BooleanVar(value=self.config_manager.config.confirm_critical)
        tk.Checkbutton(
            config_frame,
            text="Confirmar comandos críticos",
            variable=confirm_var,
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W, pady=5)
        
        # Aviso admin
        admin_warning_var = tk.BooleanVar(value=self.config_manager.config.show_admin_warning)
        tk.Checkbutton(
            config_frame,
            text="Mostrar avisos de privilégios administrativos",
            variable=admin_warning_var,
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W, pady=5)
        
        def save():
            # Verificar se tema mudou
            theme_changed = theme_var.get() != self.config_manager.config.theme
            
            self.config_manager.config.theme = theme_var.get()
            self.config_manager.config.auto_scroll = auto_scroll_var.get()
            self.config_manager.config.confirm_critical = confirm_var.get()
            self.config_manager.config.show_admin_warning = admin_warning_var.get()
            self.config_manager.salvar_config()
            
            if theme_changed:
                self._apply_theme()
                messagebox.showinfo("Configurações", "Configurações salvas!\nO tema foi atualizado.")
            else:
                messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")
            
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="💾 Salvar",
            command=save,
            font=("Segoe UI", 10, "bold"),
            bg="#27ae60",
            fg="white",
            width=12,
            height=2
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            command=dialog.destroy,
            font=("Segoe UI", 10),
            width=12,
            height=2
        ).pack(side=tk.LEFT, padx=5)
    
    def on_closing(self):
        """Callback ao fechar a janela."""
        # Salvar tamanho da janela
        self.config_manager.config.window_width = self.root.winfo_width()
        self.config_manager.config.window_height = self.root.winfo_height()
        self.config_manager.salvar_config()
        
        self.root.destroy()


def main():
    """Função principal para iniciar a GUI."""
    root = tk.Tk()
    app = HelpCommandsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
