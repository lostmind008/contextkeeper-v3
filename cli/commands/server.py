"""
Server management commands for ContextKeeper CLI.

Handles starting, stopping, and monitoring the RAG agent server.
"""

import click
import asyncio
import signal
import sys
from pathlib import Path

# Add the parent directory to sys.path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from rag_agent import ProjectKnowledgeAgent, CONFIG, main as rag_main
    from src.core.project_manager import ProjectManager
except ImportError as e:
    click.echo(f"❌ Import error: {e}", err=True)
    click.echo("Make sure you're running from the ContextKeeper directory", err=True)
    sys.exit(1)


@click.group()
def server_commands():
    """Server management commands."""
    pass


@server_commands.command('start')
@click.option('--port', default=5556, help='Port to run server on (default: 5556)')
@click.option('--daemon', is_flag=True, help='Run server in background')
@click.option('--watch', is_flag=True, help='Enable file watching (default: True)')
def start_server(port, daemon, watch):
    """Start the ContextKeeper RAG agent server.
    
    This starts the Flask API server that handles all RAG operations,
    project management, and sacred layer interactions.
    """
    click.echo("🚀 Starting ContextKeeper RAG Agent Server...")
    click.echo(f"📡 Server will run on port {port}")
    
    if daemon:
        click.echo("🔄 Running in daemon mode...")
        # For daemon mode, we'd need proper process management
        # This is a simplified implementation
        click.echo("⚠️  Daemon mode not fully implemented yet - running normally")
    
    try:
        # Override the default port in CONFIG if specified
        if port != 5556:
            CONFIG['api_port'] = port
            
        # Use the existing main function from rag_agent.py
        # But we need to modify sys.argv to simulate command line args
        original_argv = sys.argv[:]
        sys.argv = ['rag_agent.py', 'server']
        
        if not watch:
            click.echo("📁 File watching disabled")
            # We'd need to modify the CONFIG for this
            
        # Run the server
        asyncio.run(rag_main())
        
    except KeyboardInterrupt:
        click.echo("\n🛑 Server stopped by user")
    except Exception as e:
        click.echo(f"❌ Error starting server: {e}", err=True)
        sys.exit(1)
    finally:
        sys.argv = original_argv


@server_commands.command('stop')
def stop_server():
    """Stop the ContextKeeper server."""
    import requests
    
    try:
        # Try to gracefully shutdown via API
        response = requests.post('http://localhost:5556/shutdown', timeout=5)
        if response.status_code == 200:
            click.echo("✅ Server stopped gracefully")
        else:
            click.echo("⚠️  Server may not have stopped properly")
    except requests.exceptions.RequestException:
        click.echo("❌ Could not connect to server - it may already be stopped")
        
    # Also try to find and kill the process
    import psutil
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and any('rag_agent' in str(cmd) for cmd in proc.info['cmdline']):
                proc.terminate()
                click.echo(f"🔪 Terminated process {proc.info['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


@server_commands.command('status')
def server_status():
    """Check server status and health."""
    import requests
    
    try:
        response = requests.get('http://localhost:5556/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            click.echo("✅ Server is running")
            click.echo(f"📊 Status: {data.get('status', 'Unknown')}")
            click.echo(f"⏱️  Uptime: {data.get('uptime', 'Unknown')}")
            click.echo(f"📁 Active projects: {data.get('active_projects', 'Unknown')}")
            click.echo(f"💾 Memory usage: {data.get('memory_usage', 'Unknown')}")
        else:
            click.echo("❌ Server responded with error status")
    except requests.exceptions.RequestException:
        click.echo("❌ Server is not running or not accessible")
        click.echo("💡 Use 'contextkeeper server start' to start it")


@server_commands.command('restart')
@click.option('--port', default=5556, help='Port to run server on (default: 5556)')
def restart_server(port):
    """Restart the ContextKeeper server."""
    click.echo("🔄 Restarting ContextKeeper server...")
    
    # Stop first
    ctx = click.get_current_context()
    ctx.invoke(stop_server)
    
    # Wait a moment
    import time
    time.sleep(2)
    
    # Start again
    ctx.invoke(start_server, port=port, daemon=False, watch=True)


@server_commands.command('logs')
@click.option('--follow', '-f', is_flag=True, help='Follow log output')
@click.option('--lines', '-n', default=50, help='Number of lines to show')
def show_logs(follow, lines):
    """Show server logs."""
    import requests
    
    try:
        # Try to get logs via API first
        response = requests.get(f'http://localhost:5556/logs?lines={lines}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            for log_line in data.get('logs', []):
                click.echo(log_line)
                
            if follow:
                click.echo("📡 Following logs... (Ctrl+C to stop)")
                # Simple implementation - in production we'd use websockets
                while True:
                    try:
                        import time
                        time.sleep(1)
                        response = requests.get('http://localhost:5556/logs?lines=1', timeout=5)
                        if response.status_code == 200:
                            new_logs = response.json().get('logs', [])
                            for log_line in new_logs:
                                click.echo(log_line)
                    except KeyboardInterrupt:
                        break
                    except requests.exceptions.RequestException:
                        click.echo("❌ Lost connection to server")
                        break
        else:
            click.echo("❌ Could not retrieve logs from server")
    except requests.exceptions.RequestException:
        click.echo("❌ Server is not running - no logs available")
        click.echo("💡 Check local log files in ./logs/ directory")