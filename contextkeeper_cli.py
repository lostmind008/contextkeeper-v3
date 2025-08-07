#!/usr/bin/env python3
"""
File: /Users/sumitm1/contextkeeper-pro-v3/contextkeeper/contextkeeper_cli.py
Project: ContextKeeper v3.0
Purpose: Main CLI entry point for ContextKeeper Pro - interactive and command-line interface
Dependencies: Click, Flask API server, all command modules
Dependents: User interaction, shell scripts, automation tools
Created: 2025-08-06
Modified: 2025-08-06

PLANNING CONTEXT:
This is the main CLI entry point for ContextKeeper v3.0, providing a unified interface
for all operations including server management, project operations, queries, sacred layer
management, and system utilities. Uses Click framework for robust command handling.

TODO FROM PLANNING:
- [x] Main CLI structure with Click
- [x] Command group organization
- [x] Interactive menu system
- [x] Integration with existing Flask API server
- [x] Proper error handling and user feedback
- [ ] Shell completion support
- [ ] Configuration file support
- [ ] Plugin system for extensions
"""

import click
import sys
import os
import signal
import requests
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from cli.commands.server import server_commands
    from cli.commands.project import project_commands
    from cli.commands.query import query_commands
    from cli.commands.sacred import sacred_commands
    from cli.commands.utils import utils_commands
except ImportError as e:
    click.echo(f"❌ Import error: {e}", err=True)
    click.echo("Make sure you're running from the ContextKeeper directory", err=True)
    sys.exit(1)

# === NAVIGATION ===
# Previous: N/A - This is the main CLI entry point
# Next: cli/commands/* - Individual command modules
# Children: All command modules handle specific functionality
# Parent: rag_agent.py - Flask API server that this CLI communicates with


# Version information
__version__ = "3.0.0"
__author__ = "ContextKeeper Team"


def check_server_connection():
    """Check if the ContextKeeper server is running."""
    try:
        response = requests.get('http://localhost:5556/health', timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def show_interactive_menu():
    """Show the interactive menu when no command is provided."""
    click.clear()
    click.echo("🤖 " + click.style("ContextKeeper Pro v3.0", bold=True, fg='cyan'))
    click.echo("   " + click.style("AI-Powered Development Context Management", fg='white', dim=True))
    click.echo()
    
    # Check server status
    server_running = check_server_connection()
    server_status = "🟢 Running" if server_running else "🔴 Stopped"
    click.echo(f"Server Status: {server_status}")
    click.echo()
    
    # Main menu options
    menu_options = [
        ("1", "🚀 Server Management", "Start, stop, restart the ContextKeeper server"),
        ("2", "📁 Project Management", "Create, list, focus, and manage projects"),
        ("3", "🔍 Query & Search", "Ask questions and search your codebase"),
        ("4", "🏛️  Sacred Layer", "Architectural decisions and drift detection"),
        ("5", "🔧 System Utils", "Health checks, backups, configuration"),
        ("6", "❓ Help", "Show detailed help and documentation"),
        ("q", "👋 Quit", "Exit ContextKeeper CLI")
    ]
    
    click.echo(click.style("Available Commands:", bold=True))
    for key, title, description in menu_options:
        click.echo(f"  {click.style(key, fg='yellow', bold=True)}) {click.style(title, bold=True)} - {description}")
    
    click.echo()
    
    # Quick actions if server is running
    if server_running:
        click.echo(click.style("Quick Actions:", bold=True))
        click.echo("  " + click.style("contextkeeper query ask", fg='green') + " - Ask a quick question")
        click.echo("  " + click.style("contextkeeper project list", fg='green') + " - List all projects")
        click.echo("  " + click.style("contextkeeper sacred status", fg='green') + " - Check sacred layer status")
        click.echo()
    
    # Handle user input
    try:
        choice = click.prompt("Select an option", type=str).strip().lower()
        
        if choice == '1':
            handle_server_menu()
        elif choice == '2':
            handle_project_menu()
        elif choice == '3':
            handle_query_menu()
        elif choice == '4':
            handle_sacred_menu()
        elif choice == '5':
            handle_utils_menu()
        elif choice == '6':
            show_help_menu()
        elif choice in ['q', 'quit', 'exit']:
            click.echo("👋 Goodbye!")
            sys.exit(0)
        else:
            click.echo("❌ Invalid option. Please try again.", err=True)
            click.pause()
            show_interactive_menu()
            
    except (KeyboardInterrupt, EOFError):
        click.echo("\n👋 Goodbye!")
        sys.exit(0)


def handle_server_menu():
    """Handle server management submenu."""
    click.clear()
    click.echo("🚀 " + click.style("Server Management", bold=True, fg='cyan'))
    click.echo()
    
    server_running = check_server_connection()
    status = "🟢 Running" if server_running else "🔴 Stopped"
    click.echo(f"Current Status: {status}")
    click.echo()
    
    options = [
        ("1", "Start Server", not server_running),
        ("2", "Stop Server", server_running),
        ("3", "Restart Server", server_running),
        ("4", "Show Status", True),
        ("5", "Show Logs", server_running),
        ("b", "Back to Main Menu", True)
    ]
    
    for key, title, enabled in options:
        if enabled:
            click.echo(f"  {key}) {title}")
        else:
            click.echo(f"  {click.style(key, dim=True)}) {click.style(title, dim=True)} (not available)")
    
    choice = click.prompt("\nSelect an option", type=str).strip().lower()
    
    if choice == '1' and not server_running:
        os.system('contextkeeper server start')
    elif choice == '2' and server_running:
        os.system('contextkeeper server stop')
    elif choice == '3' and server_running:
        os.system('contextkeeper server restart')
    elif choice == '4':
        os.system('contextkeeper server status')
    elif choice == '5' and server_running:
        os.system('contextkeeper server logs')
    elif choice == 'b':
        show_interactive_menu()
        return
    
    click.pause()
    show_interactive_menu()


def handle_project_menu():
    """Handle project management submenu."""
    click.clear()
    click.echo("📁 " + click.style("Project Management", bold=True, fg='cyan'))
    click.echo()
    
    if not check_server_connection():
        click.echo("❌ Server is not running. Please start it first.", err=True)
        click.pause()
        show_interactive_menu()
        return
    
    options = [
        ("1", "List Projects", "contextkeeper project list"),
        ("2", "Create Project", None),  # Special handling
        ("3", "Focus Project", None),   # Special handling
        ("4", "Project Info", None),    # Special handling
        ("5", "Ingest Project", "contextkeeper project ingest"),
        ("6", "Archive Project", None), # Special handling
        ("b", "Back to Main Menu", None)
    ]
    
    for key, title, command in options:
        click.echo(f"  {key}) {title}")
    
    choice = click.prompt("\nSelect an option", type=str).strip().lower()
    
    if choice == '1':
        os.system('contextkeeper project list')
    elif choice == '2':
        name = click.prompt("Project name")
        path = click.prompt("Project path")
        description = click.prompt("Description (optional)", default="")
        cmd = f'contextkeeper project create "{name}" "{path}"'
        if description:
            cmd += f' --description "{description}"'
        os.system(cmd)
    elif choice == '3':
        project_id = click.prompt("Project ID")
        os.system(f'contextkeeper project focus {project_id}')
    elif choice == '4':
        project_id = click.prompt("Project ID")
        os.system(f'contextkeeper project info {project_id}')
    elif choice == '5':
        os.system('contextkeeper project ingest')
    elif choice == '6':
        project_id = click.prompt("Project ID to archive")
        os.system(f'contextkeeper project archive {project_id}')
    elif choice == 'b':
        show_interactive_menu()
        return
        
    click.pause()
    show_interactive_menu()


def handle_query_menu():
    """Handle query and search submenu."""
    click.clear()
    click.echo("🔍 " + click.style("Query & Search", bold=True, fg='cyan'))
    click.echo()
    
    if not check_server_connection():
        click.echo("❌ Server is not running. Please start it first.", err=True)
        click.pause()
        show_interactive_menu()
        return
    
    options = [
        ("1", "Ask Question", None),           # Special handling
        ("2", "Interactive Query Session", "contextkeeper query ask --interactive"),
        ("3", "Search Code", None),            # Special handling
        ("4", "Query History", "contextkeeper query history"),
        ("5", "Query Statistics", "contextkeeper query stats"),
        ("b", "Back to Main Menu", None)
    ]
    
    for key, title, command in options:
        click.echo(f"  {key}) {title}")
    
    choice = click.prompt("\nSelect an option", type=str).strip().lower()
    
    if choice == '1':
        question = click.prompt("Your question")
        os.system(f'contextkeeper query ask "{question}"')
    elif choice == '2':
        os.system('contextkeeper query ask --interactive')
    elif choice == '3':
        term = click.prompt("Search term")
        os.system(f'contextkeeper query search "{term}"')
    elif choice == '4':
        os.system('contextkeeper query history')
    elif choice == '5':
        os.system('contextkeeper query stats')
    elif choice == 'b':
        show_interactive_menu()
        return
        
    click.pause()
    show_interactive_menu()


def handle_sacred_menu():
    """Handle sacred layer submenu."""
    click.clear()
    click.echo("🏛️  " + click.style("Sacred Layer Management", bold=True, fg='cyan'))
    click.echo()
    
    if not check_server_connection():
        click.echo("❌ Server is not running. Please start it first.", err=True)
        click.pause()
        show_interactive_menu()
        return
    
    options = [
        ("1", "Sacred Status", "contextkeeper sacred status"),
        ("2", "List Decisions", "contextkeeper sacred decisions"),
        ("3", "Create Decision", None),        # Special handling
        ("4", "Check Drift", "contextkeeper sacred drift"),
        ("5", "Approve Decision", None),       # Special handling
        ("b", "Back to Main Menu", None)
    ]
    
    for key, title, command in options:
        click.echo(f"  {key}) {title}")
    
    choice = click.prompt("\nSelect an option", type=str).strip().lower()
    
    if choice == '1':
        os.system('contextkeeper sacred status')
    elif choice == '2':
        os.system('contextkeeper sacred decisions')
    elif choice == '3':
        title = click.prompt("Decision title")
        os.system(f'contextkeeper sacred create "{title}"')
    elif choice == '4':
        os.system('contextkeeper sacred drift')
    elif choice == '5':
        decision_id = click.prompt("Decision ID")
        os.system(f'contextkeeper sacred approve {decision_id}')
    elif choice == 'b':
        show_interactive_menu()
        return
        
    click.pause()
    show_interactive_menu()


def handle_utils_menu():
    """Handle system utilities submenu."""
    click.clear()
    click.echo("🔧 " + click.style("System Utilities", bold=True, fg='cyan'))
    click.echo()
    
    options = [
        ("1", "System Health", "contextkeeper utils health"),
        ("2", "Version Info", "contextkeeper utils version"),
        ("3", "Configuration", "contextkeeper utils config --show"),
        ("4", "System Cleanup", "contextkeeper utils cleanup --dry-run"),
        ("5", "Create Backup", None),          # Special handling
        ("6", "Run Tests", "contextkeeper utils test"),
        ("b", "Back to Main Menu", None)
    ]
    
    for key, title, command in options:
        click.echo(f"  {key}) {title}")
    
    choice = click.prompt("\nSelect an option", type=str).strip().lower()
    
    if choice == '1':
        os.system('contextkeeper utils health --verbose')
    elif choice == '2':
        os.system('contextkeeper utils version')
    elif choice == '3':
        os.system('contextkeeper utils config --show')
    elif choice == '4':
        if click.confirm("Run actual cleanup (not dry-run)?"):
            os.system('contextkeeper utils cleanup --all')
        else:
            os.system('contextkeeper utils cleanup --all --dry-run')
    elif choice == '5':
        backup_path = click.prompt("Backup path (optional)", default="")
        cmd = 'contextkeeper utils backup'
        if backup_path:
            cmd += f' "{backup_path}"'
        if click.confirm("Compress backup?"):
            cmd += ' --compress'
        os.system(cmd)
    elif choice == '6':
        if click.confirm("Run full tests (slower) instead of quick tests?"):
            os.system('contextkeeper utils test --verbose')
        else:
            os.system('contextkeeper utils test --quick')
    elif choice == 'b':
        show_interactive_menu()
        return
        
    click.pause()
    show_interactive_menu()


def show_help_menu():
    """Show help and documentation."""
    click.clear()
    click.echo("❓ " + click.style("ContextKeeper Help", bold=True, fg='cyan'))
    click.echo()
    
    click.echo(click.style("Common Commands:", bold=True))
    click.echo()
    
    commands = [
        ("Server Management:", [
            "contextkeeper server start       - Start the RAG agent server",
            "contextkeeper server stop        - Stop the server",
            "contextkeeper server status      - Check server status",
        ]),
        ("Project Management:", [
            "contextkeeper project list       - List all projects",
            "contextkeeper project create     - Create a new project",
            "contextkeeper project focus      - Set active project",
            "contextkeeper project ingest     - Index project files",
        ]),
        ("Querying:", [
            "contextkeeper query ask         - Ask a question",
            "contextkeeper query search      - Search for code",
            "contextkeeper query ask -i      - Interactive session",
        ]),
        ("Sacred Layer:", [
            "contextkeeper sacred status     - Check architectural health",
            "contextkeeper sacred decisions  - List decisions",
            "contextkeeper sacred drift      - Check for drift",
        ]),
        ("Utilities:", [
            "contextkeeper utils health      - System health check",
            "contextkeeper utils version     - Show version info",
            "contextkeeper utils backup      - Create backup",
        ])
    ]
    
    for category, command_list in commands:
        click.echo(click.style(category, bold=True, fg='yellow'))
        for cmd in command_list:
            click.echo(f"  {cmd}")
        click.echo()
    
    click.echo(click.style("Getting Help:", bold=True))
    click.echo("  contextkeeper --help                - Main help")
    click.echo("  contextkeeper <command> --help      - Command-specific help")
    click.echo("  contextkeeper <command> <sub> --help - Subcommand help")
    click.echo()
    
    click.echo(click.style("Configuration:", bold=True))
    click.echo("  Default server port: 5556")
    click.echo("  Configuration files: ./config/")
    click.echo("  Logs: ./logs/")
    click.echo("  Projects: ./projects/")
    click.echo()
    
    click.pause()
    show_interactive_menu()


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version information')
@click.pass_context
def main(ctx, version):
    """
    ContextKeeper Pro v3.0 - AI-Powered Development Context Management
    
    A sophisticated RAG (Retrieval Augmented Generation) system that helps developers
    understand, navigate, and maintain complex codebases through natural language queries
    and intelligent context management.
    
    Features:
    • Multi-project knowledge management with isolation
    • Sacred architectural layer with drift detection
    • Real-time file watching and incremental updates
    • Advanced search and query capabilities
    • Interactive dashboard and CLI interface
    
    If no command is provided, an interactive menu will be displayed.
    Use 'contextkeeper --help' to see all available commands.
    """
    
    if version:
        click.echo(f"ContextKeeper Pro v{__version__}")
        click.echo(f"Author: {__author__}")
        sys.exit(0)
    
    # If no subcommand was invoked, show interactive menu
    if ctx.invoked_subcommand is None:
        show_interactive_menu()


# Add command groups to main CLI
main.add_command(server_commands, name='server')
main.add_command(project_commands, name='project')
main.add_command(query_commands, name='query')
main.add_command(sacred_commands, name='sacred')
main.add_command(utils_commands, name='utils')


# Common aliases for convenience
@main.command('start')
@click.pass_context
def start_alias(ctx):
    """Quick alias for 'contextkeeper server start'."""
    ctx.invoke(server_commands.commands['start'])


@main.command('stop')
@click.pass_context
def stop_alias(ctx):
    """Quick alias for 'contextkeeper server stop'."""
    ctx.invoke(server_commands.commands['stop'])


@main.command('ask')
@click.argument('question', required=False)
@click.pass_context
def ask_alias(ctx, question):
    """Quick alias for 'contextkeeper query ask'."""
    if question:
        ctx.invoke(query_commands.commands['ask'], question=question)
    else:
        ctx.invoke(query_commands.commands['ask'], interactive=True)


@main.command('ls')
@click.pass_context
def list_alias(ctx):
    """Quick alias for 'contextkeeper project list'."""
    ctx.invoke(project_commands.commands['list'])


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    click.echo("\n👋 Goodbye!")
    sys.exit(0)


if __name__ == '__main__':
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        main()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        click.echo("💡 Please report this issue if it persists", err=True)
        sys.exit(1)