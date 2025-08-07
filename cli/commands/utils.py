"""
Utility commands for ContextKeeper CLI.

Handles system utilities, debugging, and maintenance tasks.
"""

import click
import sys
import json
import requests
import os
from pathlib import Path
from datetime import datetime

# Add the parent directory to sys.path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def get_server_url():
    """Get the server URL for API calls."""
    return "http://localhost:5556"


def call_api(endpoint: str, method: str = 'GET', data: dict = None):
    """Make API call to the server."""
    url = f"{get_server_url()}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
        return response
    except requests.exceptions.RequestException as e:
        click.echo(f"❌ Server connection error: {e}", err=True)
        click.echo("💡 Make sure the server is running: contextkeeper server start", err=True)
        return None


@click.group()
def utils_commands():
    """Utility and maintenance commands."""
    pass


@utils_commands.command('version')
def show_version():
    """Show ContextKeeper version information."""
    try:
        from cli import __version__
        click.echo(f"ContextKeeper Pro v{__version__}")
    except ImportError:
        click.echo("ContextKeeper Pro v3.0.0")
    
    # Try to get version from server
    response = call_api('/version')
    if response and response.status_code == 200:
        server_data = response.json()
        click.echo(f"Server version: {server_data.get('version', 'Unknown')}")
        click.echo(f"API version: {server_data.get('api_version', 'Unknown')}")
        
        # Show component versions
        components = server_data.get('components', {})
        if components:
            click.echo("\nComponent versions:")
            for component, version in components.items():
                click.echo(f"  {component}: {version}")
    else:
        click.echo("Server version: Not available (server not running)")
    
    # Show Python and system info
    import platform
    click.echo(f"\nPython version: {platform.python_version()}")
    click.echo(f"Platform: {platform.system()} {platform.release()}")
    click.echo(f"Architecture: {platform.machine()}")


@utils_commands.command('health')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed health information')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def system_health(verbose, output_json):
    """Check system health and diagnostics."""
    response = call_api('/health')
    
    if not response:
        click.echo("❌ Server health check failed - server not running", err=True)
        return
        
    if response.status_code != 200:
        click.echo("❌ Server returned error status", err=True)
        return
        
    health_data = response.json()
    
    if output_json:
        click.echo(json.dumps(health_data, indent=2))
        return
        
    status = health_data.get('status', 'unknown')
    status_icon = {'healthy': '✅', 'warning': '⚠️', 'error': '❌'}.get(status, '❓')
    
    click.echo(f"🏥 ContextKeeper Health Check")
    click.echo()
    click.echo(f"Overall Status: {status_icon} {status.upper()}")
    
    # Basic metrics
    uptime = health_data.get('uptime', 'Unknown')
    memory_usage = health_data.get('memory_usage', 'Unknown')
    active_projects = health_data.get('active_projects', 0)
    
    click.echo(f"Uptime: {uptime}")
    click.echo(f"Memory Usage: {memory_usage}")
    click.echo(f"Active Projects: {active_projects}")
    
    if verbose:
        click.echo()
        
        # Database health
        db_health = health_data.get('database', {})
        if db_health:
            click.echo("📊 Database Health:")
            click.echo(f"  Status: {db_health.get('status', 'unknown')}")
            click.echo(f"  Collections: {db_health.get('collections', 0)}")
            click.echo(f"  Total chunks: {db_health.get('total_chunks', 0)}")
            click.echo(f"  Disk usage: {db_health.get('disk_usage', 'unknown')}")
        
        # API health
        api_health = health_data.get('api', {})
        if api_health:
            click.echo()
            click.echo("🌐 API Health:")
            click.echo(f"  Status: {api_health.get('status', 'unknown')}")
            click.echo(f"  Requests per minute: {api_health.get('requests_per_minute', 0)}")
            click.echo(f"  Average response time: {api_health.get('avg_response_time', 0)}ms")
            click.echo(f"  Error rate: {api_health.get('error_rate', 0)}%")
        
        # Sacred layer health
        sacred_health = health_data.get('sacred_layer', {})
        if sacred_health:
            click.echo()
            click.echo("🏛️  Sacred Layer Health:")
            click.echo(f"  Status: {sacred_health.get('status', 'unknown')}")
            click.echo(f"  Active decisions: {sacred_health.get('active_decisions', 0)}")
            click.echo(f"  Pending approvals: {sacred_health.get('pending_approvals', 0)}")
            click.echo(f"  Drift alerts: {sacred_health.get('drift_alerts', 0)}")
        
        # System resources
        resources = health_data.get('system_resources', {})
        if resources:
            click.echo()
            click.echo("💻 System Resources:")
            click.echo(f"  CPU usage: {resources.get('cpu_usage', 'unknown')}%")
            click.echo(f"  Memory usage: {resources.get('memory_usage', 'unknown')}%")
            click.echo(f"  Disk usage: {resources.get('disk_usage', 'unknown')}%")
            click.echo(f"  Network status: {resources.get('network_status', 'unknown')}")


@utils_commands.command('config')
@click.option('--show', is_flag=True, help='Show current configuration')
@click.option('--set', 'set_config', nargs=2, metavar='KEY VALUE', help='Set configuration value')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def manage_config(show, set_config, output_json):
    """Manage ContextKeeper configuration."""
    if show:
        response = call_api('/config')
        
        if not response:
            return
            
        if response.status_code != 200:
            click.echo("❌ Error getting configuration", err=True)
            return
            
        config = response.json()
        
        if output_json:
            click.echo(json.dumps(config, indent=2))
            return
            
        click.echo("⚙️  ContextKeeper Configuration")
        click.echo()
        
        for category, settings in config.items():
            click.echo(f"{category.upper()}:")
            if isinstance(settings, dict):
                for key, value in settings.items():
                    # Hide sensitive values
                    if 'key' in key.lower() or 'password' in key.lower() or 'secret' in key.lower():
                        value = '***HIDDEN***'
                    click.echo(f"  {key}: {value}")
            else:
                click.echo(f"  {settings}")
            click.echo()
            
    elif set_config:
        key, value = set_config
        data = {'key': key, 'value': value}
        
        response = call_api('/config', method='POST', data=data)
        
        if not response:
            return
            
        if response.status_code == 200:
            click.echo(f"✅ Configuration updated: {key} = {value}")
        else:
            error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
            click.echo(f"❌ Error updating configuration: {error}", err=True)
    else:
        click.echo("💡 Use --show to view config or --set KEY VALUE to update", err=True)


@utils_commands.command('cleanup')
@click.option('--dry-run', is_flag=True, help='Show what would be cleaned without actually doing it')
@click.option('--all', 'cleanup_all', is_flag=True, help='Clean all temporary data')
@click.option('--logs', is_flag=True, help='Clean old log files')
@click.option('--cache', is_flag=True, help='Clean cache files')
@click.option('--orphaned', is_flag=True, help='Clean orphaned project data')
def cleanup_system(dry_run, cleanup_all, logs, cache, orphaned):
    """Clean up temporary files and orphaned data."""
    if not any([cleanup_all, logs, cache, orphaned]):
        click.echo("❌ Specify what to clean: --all, --logs, --cache, or --orphaned", err=True)
        return
        
    data = {
        'dry_run': dry_run,
        'cleanup_all': cleanup_all,
        'logs': logs or cleanup_all,
        'cache': cache or cleanup_all,
        'orphaned': orphaned or cleanup_all
    }
    
    if dry_run:
        click.echo("🧹 Dry run - showing what would be cleaned...")
    else:
        click.echo("🧹 Starting cleanup...")
        
    response = call_api('/utils/cleanup', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Cleanup failed: {error}", err=True)
        return
        
    result = response.json()
    
    if dry_run:
        click.echo("📋 Would clean:")
    else:
        click.echo("✅ Cleaned:")
        
    for category, items in result.get('cleaned', {}).items():
        if items:
            click.echo(f"  {category.upper()}:")
            for item in items:
                click.echo(f"    • {item}")
                
    space_freed = result.get('space_freed', 0)
    if space_freed:
        click.echo(f"\n💾 Space freed: {space_freed}")


@utils_commands.command('backup')
@click.argument('backup_path', required=False)
@click.option('--project', help='Backup specific project only')
@click.option('--compress', is_flag=True, help='Compress the backup')
def backup_data(backup_path, project, compress):
    """Create a backup of ContextKeeper data."""
    if not backup_path:
        # Generate default backup path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"contextkeeper_backup_{timestamp}"
        if compress:
            backup_path += ".tar.gz"
        
    data = {
        'backup_path': backup_path,
        'project_id': project,
        'compress': compress
    }
    
    click.echo(f"💾 Creating backup to: {backup_path}")
    if project:
        click.echo(f"📁 Project: {project}")
        
    response = call_api('/utils/backup', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Backup failed: {error}", err=True)
        return
        
    result = response.json()
    
    click.echo(f"✅ Backup created successfully")
    click.echo(f"📁 Location: {result.get('backup_path', backup_path)}")
    click.echo(f"💾 Size: {result.get('size', 'Unknown')}")
    
    included = result.get('included', [])
    if included:
        click.echo("📋 Included:")
        for item in included:
            click.echo(f"  • {item}")


@utils_commands.command('restore')
@click.argument('backup_path')
@click.option('--project', help='Restore to specific project')
@click.option('--force', is_flag=True, help='Overwrite existing data')
def restore_data(backup_path, project, force):
    """Restore ContextKeeper data from backup."""
    if not os.path.exists(backup_path):
        click.echo(f"❌ Backup file not found: {backup_path}", err=True)
        return
        
    if not force:
        click.echo(f"⚠️  This will restore data from: {backup_path}")
        if project:
            click.echo(f"   Target project: {project}")
        else:
            click.echo("   This may overwrite existing data!")
            
        if not click.confirm("Continue with restore?"):
            click.echo("❌ Restore cancelled")
            return
            
    data = {
        'backup_path': backup_path,
        'project_id': project,
        'force': force
    }
    
    click.echo(f"📥 Restoring from: {backup_path}")
    response = call_api('/utils/restore', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Restore failed: {error}", err=True)
        return
        
    result = response.json()
    
    click.echo("✅ Restore completed successfully")
    
    restored = result.get('restored', [])
    if restored:
        click.echo("📋 Restored:")
        for item in restored:
            click.echo(f"  • {item}")


@utils_commands.command('export')
@click.argument('format_type', type=click.Choice(['json', 'csv', 'markdown']))
@click.argument('output_path')
@click.option('--project', help='Export specific project only')
@click.option('--include-content', is_flag=True, help='Include file content in export')
def export_data(format_type, output_path, project, include_content):
    """Export ContextKeeper data in various formats."""
    data = {
        'format': format_type,
        'output_path': output_path,
        'project_id': project,
        'include_content': include_content
    }
    
    click.echo(f"📤 Exporting to {format_type.upper()} format: {output_path}")
    if project:
        click.echo(f"📁 Project: {project}")
        
    response = call_api('/utils/export', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Export failed: {error}", err=True)
        return
        
    result = response.json()
    
    click.echo("✅ Export completed successfully")
    click.echo(f"📁 Output: {result.get('output_path', output_path)}")
    
    stats = result.get('statistics', {})
    if stats:
        click.echo("📊 Export statistics:")
        for key, value in stats.items():
            click.echo(f"  {key}: {value}")


@utils_commands.command('test')
@click.option('--quick', is_flag=True, help='Run quick tests only')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def run_tests(quick, verbose):
    """Run system tests and diagnostics."""
    click.echo("🧪 Running ContextKeeper system tests...")
    
    data = {
        'quick': quick,
        'verbose': verbose
    }
    
    response = call_api('/utils/test', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Tests failed to run: {error}", err=True)
        return
        
    result = response.json()
    
    # Show test results
    tests_run = result.get('tests_run', 0)
    tests_passed = result.get('tests_passed', 0)
    tests_failed = result.get('tests_failed', 0)
    
    click.echo(f"\n📊 Test Results:")
    click.echo(f"  Total tests: {tests_run}")
    click.echo(f"  Passed: ✅ {tests_passed}")
    click.echo(f"  Failed: ❌ {tests_failed}")
    
    if tests_failed > 0:
        click.echo(f"\n❌ {tests_failed} test(s) failed:")
        failures = result.get('failures', [])
        for failure in failures:
            click.echo(f"  • {failure}")
    else:
        click.echo("\n✅ All tests passed!")
        
    if verbose and 'details' in result:
        click.echo(f"\n📋 Test Details:")
        for detail in result['details']:
            click.echo(f"  {detail}")