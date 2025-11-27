import json
import os
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime


CONFIG_FILE = "app_config.json"
HISTORY_FILE = "command_history.json"


@dataclass
class AppConfig:
    """Configurações da aplicação."""
    theme: str = "dark"
    auto_scroll_console: bool = True
    confirm_critical: bool = True
    show_admin_warnings: bool = True
    favorites: List[str] = None
    window_width: int = 1200
    window_height: int = 800
    
    def __post_init__(self):
        if self.favorites is None:
            self.favorites = []


@dataclass
class CommandHistoryEntry:
    """Entrada no histórico de comandos."""
    timestamp: str
    command_key: str
    command_name: str
    command_text: str
    success: bool
    is_free_command: bool = False


class ConfigManager:
    """Gerencia configurações e histórico da aplicação."""
    
    def __init__(self):
        self.config = self.carregar_config()
        self.history: List[CommandHistoryEntry] = self.carregar_historico()
    
    def carregar_config(self) -> AppConfig:
        """Carrega configurações do arquivo JSON."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return AppConfig(**data)
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")
        
        return AppConfig()
    
    def salvar_config(self) -> None:
        """Salva configurações no arquivo JSON."""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.config), f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def save_config(self) -> None:
        """Alias para salvar_config (compatibilidade)."""
        self.salvar_config()
    
    def carregar_historico(self) -> List[CommandHistoryEntry]:
        """Carrega histórico de comandos do arquivo JSON."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [CommandHistoryEntry(**entry) for entry in data]
            except Exception as e:
                print(f"Erro ao carregar histórico: {e}")
        
        return []
    
    def salvar_historico(self) -> None:
        """Salva histórico de comandos no arquivo JSON."""
        try:
            # Limitar histórico a últimas 500 entradas
            historico_limitado = self.history[-500:]
            
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(
                    [asdict(entry) for entry in historico_limitado],
                    f,
                    indent=4,
                    ensure_ascii=False
                )
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
    
    def adicionar_ao_historico(
        self,
        command_key: str,
        command_name: str,
        command_text: str,
        success: bool = True,
        is_free_command: bool = False
    ) -> None:
        """Adiciona um comando ao histórico."""
        entry = CommandHistoryEntry(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            command_key=command_key,
            command_name=command_name,
            command_text=command_text,
            success=success,
            is_free_command=is_free_command
        )
        self.history.append(entry)
        self.salvar_historico()
    
    def adicionar_favorito(self, command_key: str) -> None:
        """Adiciona um comando aos favoritos."""
        if command_key not in self.config.favorites:
            self.config.favorites.append(command_key)
            self.salvar_config()
    
    def remover_favorito(self, command_key: str) -> None:
        """Remove um comando dos favoritos."""
        if command_key in self.config.favorites:
            self.config.favorites.remove(command_key)
            self.salvar_config()
    
    def eh_favorito(self, command_key: str) -> bool:
        """Verifica se um comando está nos favoritos."""
        return command_key in self.config.favorites
    
    def exportar_historico_txt(self, filepath: str) -> bool:
        """Exporta histórico para arquivo de texto legível."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("HISTÓRICO DE COMANDOS - HELP COMMANDS\n")
                f.write("=" * 80 + "\n\n")
                
                for entry in self.history:
                    f.write(f"Data/Hora: {entry.timestamp}\n")
                    f.write(f"Comando: [{entry.command_key}] {entry.command_name}\n")
                    f.write(f"Comando executado: {entry.command_text}\n")
                    f.write(f"Status: {'✓ Sucesso' if entry.success else '✗ Falha'}\n")
                    if entry.is_free_command:
                        f.write(f"Tipo: Comando Livre\n")
                    f.write("-" * 80 + "\n\n")
            
            return True
        except Exception as e:
            print(f"Erro ao exportar histórico: {e}")
            return False
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Retorna histórico em formato de dicionário."""
        return [
            {
                "timestamp": entry.timestamp,
                "command_key": entry.command_key,
                "command_name": entry.command_name,
                "status": "sucesso" if entry.success else "erro"
            }
            for entry in self.history
        ]
    
    def add_to_history(self, command_key: str, command_name: str, status: str) -> None:
        """Adiciona entrada ao histórico (formato simplificado)."""
        self.adicionar_ao_historico(
            command_key=command_key,
            command_name=command_name,
            command_text=command_name,
            success=(status == "sucesso"),
            is_free_command=False
        )
    
    def clear_history(self) -> None:
        """Limpa todo o histórico."""
        self.history = []
        self.salvar_historico()
