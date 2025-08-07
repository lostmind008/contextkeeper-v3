#!/usr/bin/env python3
"""
File: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/cli/interactive/menu.py
Project: ContextKeeper v3
Purpose: Interactive menu system for CLI
Dependencies: rich, prompt_toolkit, commands modules
Dependents: Main CLI entry point
Created: 2025-08-06
Modified: 2025-08-06

PLANNING CONTEXT:
- Beautiful interactive menu with keyboard navigation
- Submenus for each major feature area
- Context-aware options based on state
- Quick actions and shortcuts

TODO FROM PLANNING:
- [x] Main menu with all feature areas
- [x] Submenus for project, sacred, query operations
- [x] Context display in menu header
- [ ] Add keyboard shortcuts (Ctrl+P for projects, etc.)
- [ ] Add command history and autocomplete
"""

import sys
import os
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime
from pathlib import Path
import logging

# Rich for beautiful menus
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.columns import Columns
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Warning: 'rich' not installed. Using basic menu.")

# Prompt toolkit for advanced input
try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter, PathCompleter
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False

# === NAVIGATION ===
# Previous: [../commands/project.py] - Uses command implementations
# Next: [../cli.py] - Called from main CLI entry
# Parent: [../../cli/] - Part of CLI package

logger = logging.getLogger(__name__)

console = Console() if RICH_AVAILABLE else None


class InteractiveMenu:
    """
    Interactive menu system for ContextKeeper CLI
    
    Features:
    - Hierarchical menu structure
    - Context-aware options
    - Beautiful formatting with rich
    - Keyboard navigation
    - Command history
    """
    
    def __init__(self, context):
        """Initialise menu with CLI context"""
        self.context = context
        self.api = context.get_api_client()
        self.running = True
        
        # Command history
        self.history_file = Path.home() / ".contextkeeper" / "cli_history"
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Import command modules
        self._load_commands()
        
        # Menu structure
        self.main_menu = self._build_main_menu()
        self.current_menu = self.main_menu
    
    def _load_commands(self):
        """Load command implementations"""
        from ..commands.project import ProjectCommands
        
        self.project_commands = ProjectCommands(self.context)
        
        # TODO: Load other command modules as they're created
        # from ..commands.sacred import SacredCommands
        # from ..commands.query import QueryCommands
        # self.sacred_commands = SacredCommands(self.context)
        # self.query_commands = QueryCommands(self.context)
    
    def _build_main_menu(self) -> Dict:
        """Build main menu structure"""
        return {
            'title': 'ContextKeeper v3 - Main Menu',
            'options': [
                {
                    'key': '1',
                    'label': 'Project Management',
                    'action': self._project_menu,
                    'description': 'Create, list, and manage projects'
                },
                {
                    'key': '2',
                    'label': 'Query & Chat',
                    'action': self._query_menu,
                    'description': 'Query knowledge base and chat'
                },
                {
                    'key': '3',
                    'label': 'Sacred Architecture',
                    'action': self._sacred_menu,
                    'description': 'Manage sacred architectural decisions'
                },
                {
                    'key': '4',
                    'label': 'Analytics & Reports',
                    'action': self._analytics_menu,
                    'description': 'View analytics and generate reports'
                },
                {
                    'key': '5',
                    'label': 'Settings',
                    'action': self._settings_menu,
                    'description': 'Configure CLI settings'
                },
                {
                    'key': 's',
                    'label': 'Status',
                    'action': self._show_status,
                    'description': 'Show current context and status'
                },
                {
                    'key': 'h',
                    'label': 'Help',
                    'action': self._show_help,
                    'description': 'Show help and documentation'
                },
                {
                    'key': 'q',
                    'label': 'Quit',
                    'action': self._quit,
                    'description': 'Exit ContextKeeper CLI'
                }
            ]
        }
    
    def run(self):
        """Run interactive menu loop"""
        self._clear_screen()
        self._show_welcome()
        
        while self.running:
            try:
                self._display_menu(self.current_menu)
                choice = self._get_choice()
                
                if choice:
                    self._handle_choice(choice, self.current_menu)
                    
            except KeyboardInterrupt:
                if self._confirm_quit():
                    break
            except Exception as e:
                self._error(f"Menu error: {e}")
                logger.error(f"Menu error: {e}", exc_info=True)
        
        self._show_goodbye()
    
    def _display_menu(self, menu: Dict):
        """Display menu with rich formatting"""
        self._clear_screen()
        self._show_header()
        
        if RICH_AVAILABLE:
            # Create menu panel
            menu_items = []
            for option in menu['options']:
                key_style = "bold cyan" if option['key'].isdigit() else "bold yellow"
                menu_items.append(
                    f"[{key_style}]{option['key']}[/{key_style}]. {option['label']}"
                    f"  [dim]{option.get('description', '')}[/dim]"
                )
            
            menu_text = "\n".join(menu_items)
            
            panel = Panel(
                menu_text,
                title=menu['title'],
                border_style="blue",
                padding=(1, 2)
            )
            console.print(panel)
        else:
            # Simple text menu
            print(f"\n{menu['title']}")
            print("-" * 50)
            for option in menu['options']:
                print(f"{option['key']}. {option['label']}")
            print("-" * 50)
    
    def _show_header(self):
        """Show menu header with context info"""
        if RICH_AVAILABLE:
            # Build header with context info
            header_parts = []
            
            # Logo/Title
            header_parts.append(Text("🎯 ContextKeeper v3", style="bold magenta"))
            
            # Current project
            if self.context.project.is_focused():
                project_text = Text(
                    f"Project: {self.context.project.project_name or self.context.project.project_id[:8]}",
                    style="green"
                )
                header_parts.append(project_text)
            else:
                header_parts.append(Text("No project focused", style="dim"))
            
            # API status
            try:
                if self.api.health_check():
                    header_parts.append(Text("API: ✓", style="green"))
                else:
                    header_parts.append(Text("API: ✗", style="red"))
            except:
                header_parts.append(Text("API: ?", style="yellow"))
            
            # Display header
            console.print(Columns(header_parts, equal=True, expand=True))
            console.print("─" * console.width, style="dim")
        else:
            print("\n=== ContextKeeper v3 ===")
            if self.context.project.is_focused():
                print(f"Project: {self.context.project.project_name}")
            print()
    
    def _get_choice(self) -> Optional[str]:
        """Get user menu choice"""
        if PROMPT_TOOLKIT_AVAILABLE and self.context.config.interactive_mode:
            # Use prompt_toolkit for better input
            try:
                choice = prompt(
                    "Choose option: ",
                    history=FileHistory(str(self.history_file)),
                    auto_suggest=AutoSuggestFromHistory()
                ).strip().lower()
                return choice
            except:
                pass
        
        # Fallback to simple input
        if RICH_AVAILABLE:
            choice = Prompt.ask("[bold]Choose option[/bold]").strip().lower()
        else:
            choice = input("Choose option: ").strip().lower()
        
        return choice
    
    def _handle_choice(self, choice: str, menu: Dict):
        """Handle menu choice"""
        for option in menu['options']:
            if choice == option['key'].lower():
                action = option['action']
                if callable(action):
                    action()
                elif isinstance(action, dict):
                    # Submenu
                    self.current_menu = action
                return
        
        self._error(f"Invalid choice: {choice}")
    
    # === Project Menu ===
    
    def _project_menu(self):
        """Project management submenu"""
        menu = {
            'title': 'Project Management',
            'options': [
                {
                    'key': '1',
                    'label': 'Create Project',
                    'action': self._create_project,
                    'description': 'Create new project'
                },
                {
                    'key': '2',
                    'label': 'List Projects',
                    'action': self._list_projects,
                    'description': 'Show all projects'
                },
                {
                    'key': '3',
                    'label': 'Focus Project',
                    'action': self._focus_project,
                    'description': 'Switch to different project'
                },
                {
                    'key': '4',
                    'label': 'Index Current Project',
                    'action': self._index_project,
                    'description': 'Index files in focused project'
                },
                {
                    'key': '5',
                    'label': 'Project Status',
                    'action': self._project_status,
                    'description': 'Show focused project status'
                },
                {
                    'key': 'b',
                    'label': 'Back',
                    'action': self._back_to_main,
                    'description': 'Return to main menu'
                }
            ]
        }
        
        while True:
            self._display_menu(menu)
            choice = self._get_choice()
            
            if choice == 'b':
                break
            
            self._handle_choice(choice, menu)
    
    def _create_project(self):
        """Create new project interactive"""
        self._clear_screen()
        
        if RICH_AVAILABLE:
            console.print(Panel("Create New Project", style="bold blue"))
            
            name = Prompt.ask("Project name")
            
            # Path with completion
            if PROMPT_TOOLKIT_AVAILABLE:
                path = prompt(
                    "Project path (press Tab for completion): ",
                    completer=PathCompleter(),
                    default=os.getcwd()
                )
            else:
                path = Prompt.ask("Project path", default=os.getcwd())
            
            description = Prompt.ask("Description (optional)", default="")
            
            if Confirm.ask(f"Create project '{name}' at {path}?"):
                self.project_commands.create(name, path, description or None)
                Prompt.ask("\nPress Enter to continue")
        else:
            print("\n=== Create New Project ===")
            name = input("Project name: ")
            path = input(f"Project path [{os.getcwd()}]: ") or os.getcwd()
            description = input("Description (optional): ")
            
            confirm = input(f"\nCreate project '{name}' at {path}? (y/n): ")
            if confirm.lower() == 'y':
                self.project_commands.create(name, path, description or None)
                input("\nPress Enter to continue")
    
    def _list_projects(self):
        """List all projects"""
        self._clear_screen()
        self.project_commands.list(show_stats=True)
        
        if RICH_AVAILABLE:
            Prompt.ask("\nPress Enter to continue")
        else:
            input("\nPress Enter to continue")
    
    def _focus_project(self):
        """Focus on a project"""
        self._clear_screen()
        
        # Show current projects
        projects = self.api.list_projects()
        
        if not projects:
            self._error("No projects available")
            return
        
        if RICH_AVAILABLE:
            # Display projects table
            table = Table(title="Available Projects")
            table.add_column("Index", style="cyan")
            table.add_column("ID", style="yellow")
            table.add_column("Name", style="magenta")
            table.add_column("Path", style="dim")
            
            for i, p in enumerate(projects, 1):
                table.add_row(str(i), p['id'][:8], p['name'], Path(p['path']).name)
            
            console.print(table)
            
            # Get choice
            choice = IntPrompt.ask(
                "Select project number (0 to cancel)",
                choices=[str(i) for i in range(len(projects) + 1)]
            )
            
            if choice > 0:
                selected = projects[choice - 1]
                self.project_commands.focus(selected['id'])
                Prompt.ask("\nPress Enter to continue")
        else:
            print("\nAvailable Projects:")
            for i, p in enumerate(projects, 1):
                print(f"{i}. {p['name']} ({p['id'][:8]})")
            
            choice = input("\nSelect project number (0 to cancel): ")
            if choice.isdigit() and int(choice) > 0:
                selected = projects[int(choice) - 1]
                self.project_commands.focus(selected['id'])
                input("\nPress Enter to continue")
    
    def _index_project(self):
        """Index current project"""
        if not self.context.project.is_focused():
            self._error("No project focused. Focus a project first.")
            return
        
        self._clear_screen()
        
        if RICH_AVAILABLE:
            console.print(Panel(
                f"Indexing Project: {self.context.project.project_name}",
                style="bold blue"
            ))
            
            use_defaults = Confirm.ask("Use default settings?", default=True)
            
            if use_defaults:
                self.project_commands.index()
            else:
                # Custom settings
                path = Prompt.ask("Path to index", default=self.context.project.project_path)
                file_types = Prompt.ask("File types (comma-separated)", 
                                       default=".py,.js,.ts,.md")
                exclude_dirs = Prompt.ask("Exclude dirs (comma-separated)",
                                         default="node_modules,__pycache__,.git")
                
                self.project_commands.index(
                    path=path,
                    file_types=file_types.split(','),
                    exclude_dirs=exclude_dirs.split(',')
                )
            
            Prompt.ask("\nPress Enter to continue")
        else:
            print(f"\nIndexing Project: {self.context.project.project_name}")
            self.project_commands.index()
            input("\nPress Enter to continue")
    
    def _project_status(self):
        """Show project status"""
        if not self.context.project.is_focused():
            self._error("No project focused")
            return
        
        self._clear_screen()
        self.project_commands.status(verbose=True)
        
        if RICH_AVAILABLE:
            Prompt.ask("\nPress Enter to continue")
        else:
            input("\nPress Enter to continue")
    
    # === Query Menu ===
    
    def _query_menu(self):
        """Query and chat submenu"""
        self._info("Query menu - Coming soon!")
        self._wait()
    
    # === Sacred Menu ===
    
    def _sacred_menu(self):
        """Sacred architecture submenu"""
        self._info("Sacred architecture menu - Coming soon!")
        self._wait()
    
    # === Analytics Menu ===
    
    def _analytics_menu(self):
        """Analytics and reports submenu"""
        self._info("Analytics menu - Coming soon!")
        self._wait()
    
    # === Settings Menu ===
    
    def _settings_menu(self):
        """Settings submenu"""
        self._clear_screen()
        
        if RICH_AVAILABLE:
            # Show current settings
            settings_text = (
                f"[bold]Current Settings:[/bold]\n\n"
                f"API URL: {self.context.config.api_url}\n"
                f"Output Format: {self.context.config.output_format}\n"
                f"Colour Output: {self.context.config.colour_output}\n"
                f"Interactive Mode: {self.context.config.interactive_mode}\n"
                f"Debug Mode: {self.context.config.debug_mode}\n"
                f"Log Level: {self.context.config.log_level}\n"
            )
            
            console.print(Panel(settings_text, title="Settings", border_style="blue"))
            
            if Confirm.ask("Change settings?"):
                # TODO: Implement settings editor
                self._info("Settings editor coming soon!")
            
            Prompt.ask("\nPress Enter to continue")
        else:
            print("\n=== Settings ===")
            print(f"API URL: {self.context.config.api_url}")
            print(f"Output Format: {self.context.config.output_format}")
            input("\nPress Enter to continue")
    
    # === Status & Help ===
    
    def _show_status(self):
        """Show current status"""
        self._clear_screen()
        
        summary = self.context.get_context_summary()
        
        if RICH_AVAILABLE:
            # Format status nicely
            status_text = (
                f"[bold]API:[/bold] {summary['api_url']}\n"
                f"[bold]Project:[/bold] {summary['current_project']['name'] or 'None'}\n"
                f"[bold]Project ID:[/bold] {summary['current_project']['id'] or 'None'}\n"
                f"[bold]Commands Run:[/bold] {summary['session']['commands_run']}\n"
                f"[bold]Output Format:[/bold] {summary['config']['output_format']}\n"
            )
            
            console.print(Panel(status_text, title="Current Status", border_style="green"))
            Prompt.ask("\nPress Enter to continue")
        else:
            print("\n=== Current Status ===")
            print(f"API: {summary['api_url']}")
            print(f"Project: {summary['current_project']['name'] or 'None'}")
            input("\nPress Enter to continue")
    
    def _show_help(self):
        """Show help information"""
        self._clear_screen()
        
        help_text = """
ContextKeeper CLI Help

Navigation:
- Use number keys to select menu options
- Press 'b' to go back to previous menu
- Press 'q' to quit
- Press Ctrl+C to cancel current operation

Quick Keys:
- s: Show status
- h: Show this help
- q: Quit

For more information, visit:
https://github.com/contextkeeper/docs
        """
        
        if RICH_AVAILABLE:
            console.print(Panel(help_text.strip(), title="Help", border_style="blue"))
            Prompt.ask("\nPress Enter to continue")
        else:
            print(help_text)
            input("\nPress Enter to continue")
    
    # === Utility Methods ===
    
    def _back_to_main(self):
        """Return to main menu"""
        self.current_menu = self.main_menu
    
    def _quit(self):
        """Quit application"""
        if self._confirm_quit():
            self.running = False
    
    def _confirm_quit(self) -> bool:
        """Confirm quit action"""
        if RICH_AVAILABLE:
            return Confirm.ask("Really quit?", default=False)
        else:
            response = input("\nReally quit? (y/n): ")
            return response.lower() == 'y'
    
    def _clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def _show_welcome(self):
        """Show welcome message"""
        if RICH_AVAILABLE:
            welcome = Panel(
                "[bold magenta]Welcome to ContextKeeper v3![/bold magenta]\n\n"
                "Your AI-powered development context management system\n"
                "Type 'h' for help or 'q' to quit",
                title="🎯 ContextKeeper",
                border_style="magenta"
            )
            console.print(welcome)
            console.print()
        else:
            print("\n=== Welcome to ContextKeeper v3 ===")
            print("Your AI-powered development context management system\n")
    
    def _show_goodbye(self):
        """Show goodbye message"""
        if RICH_AVAILABLE:
            console.print("\n[bold green]Thank you for using ContextKeeper![/bold green]")
            console.print("[dim]Your context has been saved.[/dim]\n")
        else:
            print("\nThank you for using ContextKeeper!")
            print("Your context has been saved.\n")
    
    def _info(self, message: str):
        """Display info message"""
        if RICH_AVAILABLE:
            console.print(f"[blue]ℹ[/blue]  {message}")
        else:
            print(f"INFO: {message}")
    
    def _error(self, message: str):
        """Display error message"""
        if RICH_AVAILABLE:
            console.print(f"[red]✗[/red] {message}", style="red")
        else:
            print(f"ERROR: {message}")
    
    def _wait(self):
        """Wait for user input"""
        if RICH_AVAILABLE:
            Prompt.ask("\nPress Enter to continue")
        else:
            input("\nPress Enter to continue")