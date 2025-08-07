"""
Project management commands for ContextKeeper CLI.

Handles creating, listing, focusing, and managing projects.
"""

import click
import sys
import json
import requests
from pathlib import Path
from typing import Optional

# Add the parent directory to sys.path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from src.core.project_manager import ProjectManager, ProjectStatus
except ImportError as e:
    click.echo(f"❌ Import error: {e}", err=True)
    click.echo("Make sure you're running from the ContextKeeper directory", err=True)
    sys.exit(1)


def get_server_url():
    """Get the server URL for API calls."""
    return "http://localhost:5556"


def call_api(endpoint: str, method: str = 'GET', data: Optional[dict] = None):
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
def project_commands():
    """Project management commands."""
    pass


@project_commands.command('list')
@click.option('--status', type=click.Choice(['active', 'paused', 'archived', 'all']), 
              default='all', help='Filter projects by status')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def list_projects(status, output_json):
    """List all projects."""
    response = call_api('/projects')
    if not response:
        return
        
    if response.status_code != 200:
        click.echo(f"❌ Error listing projects: {response.text}", err=True)
        return
        
    data = response.json()
    projects = data.get('projects', [])
    
    if status != 'all':
        projects = [p for p in projects if p.get('status', '').lower() == status.lower()]
    
    if output_json:
        click.echo(json.dumps(projects, indent=2))
        return
        
    if not projects:
        click.echo("📁 No projects found")
        if status != 'all':
            click.echo(f"   (filtered by status: {status})")
        return
    
    click.echo(f"📁 Found {len(projects)} project{'s' if len(projects) != 1 else ''}:")
    click.echo()
    
    for project in projects:
        status_icon = {
            'active': '🟢',
            'paused': '🟡', 
            'archived': '🔒'
        }.get(project.get('status', 'unknown').lower(), '❓')
        
        click.echo(f"{status_icon} {project.get('name', 'Unknown')}")
        click.echo(f"   ID: {project.get('id', 'Unknown')}")
        click.echo(f"   Path: {project.get('root_path', 'Unknown')}")
        click.echo(f"   Status: {project.get('status', 'Unknown')}")
        
        if project.get('description'):
            click.echo(f"   Description: {project.get('description')}")
            
        # Show some stats
        chunks = project.get('chunks', 0)
        files = project.get('files', 0)
        if chunks or files:
            click.echo(f"   📊 {files} files, {chunks} chunks indexed")
            
        click.echo()


@project_commands.command('create')
@click.argument('name')
@click.argument('path')
@click.option('--description', help='Project description')
@click.option('--watch-dirs', multiple=True, help='Additional directories to watch (can specify multiple)')
@click.option('--auto-ingest', is_flag=True, default=True, help='Automatically ingest project files')
def create_project(name, path, description, watch_dirs, auto_ingest):
    """Create a new project.
    
    NAME is the project name
    PATH is the root path of the project
    """
    path = str(Path(path).resolve())
    
    if not Path(path).exists():
        click.echo(f"❌ Path does not exist: {path}", err=True)
        return
        
    data = {
        'name': name,
        'root_path': path,
        'description': description or f"Project created for {name}",
        'watch_dirs': list(watch_dirs) if watch_dirs else [path]
    }
    
    response = call_api('/projects', method='POST', data=data)
    if not response:
        return
        
    if response.status_code == 201:
        project_data = response.json()
        project_id = project_data.get('id')
        click.echo(f"✅ Created project '{name}' with ID: {project_id}")
        click.echo(f"📁 Root path: {path}")
        
        if auto_ingest:
            click.echo("📚 Starting automatic ingestion...")
            ingest_data = {'path': path, 'project_id': project_id}
            ingest_response = call_api('/ingest', method='POST', data=ingest_data)
            
            if ingest_response and ingest_response.status_code == 200:
                ingest_result = ingest_response.json()
                chunks = ingest_result.get('chunks', 0)
                click.echo(f"✅ Ingested {chunks} chunks")
            else:
                click.echo("⚠️  Auto-ingestion failed - you can run 'contextkeeper project ingest' later")
                
    elif response.status_code == 400:
        error = response.json().get('error', 'Unknown error')
        click.echo(f"❌ Error creating project: {error}", err=True)
    else:
        click.echo(f"❌ Unexpected error: {response.text}", err=True)


@project_commands.command('focus')
@click.argument('project_id')
def focus_project(project_id):
    """Set the active/focused project."""
    data = {'project_id': project_id}
    response = call_api('/projects/focus', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code == 200:
        project_data = response.json()
        click.echo(f"✅ Focused on project: {project_data.get('name', project_id)}")
        click.echo(f"📁 Path: {project_data.get('root_path', 'Unknown')}")
    else:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error focusing project: {error}", err=True)


@project_commands.command('info')
@click.argument('project_id')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def project_info(project_id, output_json):
    """Show detailed information about a project."""
    response = call_api(f'/projects/{project_id}')
    
    if not response:
        return
        
    if response.status_code != 200:
        click.echo(f"❌ Project not found: {project_id}", err=True)
        return
        
    project = response.json()
    
    if output_json:
        click.echo(json.dumps(project, indent=2))
        return
        
    click.echo(f"📁 Project: {project.get('name', 'Unknown')}")
    click.echo(f"   ID: {project.get('id', 'Unknown')}")
    click.echo(f"   Status: {project.get('status', 'Unknown')}")
    click.echo(f"   Root Path: {project.get('root_path', 'Unknown')}")
    click.echo(f"   Description: {project.get('description', 'No description')}")
    click.echo(f"   Created: {project.get('created_at', 'Unknown')}")
    click.echo(f"   Modified: {project.get('modified_at', 'Unknown')}")
    
    watch_dirs = project.get('watch_dirs', [])
    if watch_dirs:
        click.echo(f"   Watch Dirs: {', '.join(watch_dirs)}")
        
    # Stats
    click.echo()
    click.echo("📊 Statistics:")
    click.echo(f"   Files indexed: {project.get('files', 0)}")
    click.echo(f"   Chunks: {project.get('chunks', 0)}")
    click.echo(f"   Last ingestion: {project.get('last_ingestion', 'Never')}")
    
    # Recent activity
    activities = project.get('recent_activities', [])
    if activities:
        click.echo()
        click.echo("📈 Recent Activity:")
        for activity in activities[:5]:  # Show last 5
            click.echo(f"   • {activity}")


@project_commands.command('ingest')
@click.argument('project_id', required=False)
@click.option('--path', help='Specific path to ingest (optional)')
@click.option('--force', is_flag=True, help='Force re-ingestion of all files')
def ingest_project(project_id, path, force):
    """Ingest files for a project."""
    if not project_id:
        # Try to get the currently focused project
        response = call_api('/projects/current')
        if response and response.status_code == 200:
            project_data = response.json()
            project_id = project_data.get('id')
            click.echo(f"📁 Using current project: {project_data.get('name', 'Unknown')}")
        else:
            click.echo("❌ No project specified and no current project set", err=True)
            click.echo("💡 Use: contextkeeper project focus <project_id>", err=True)
            return
            
    data = {
        'project_id': project_id,
        'force': force
    }
    
    if path:
        data['path'] = str(Path(path).resolve())
        
    click.echo("📚 Starting ingestion...")
    response = call_api('/ingest', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code == 200:
        result = response.json()
        chunks = result.get('chunks', 0)
        files = result.get('files', 0)
        click.echo(f"✅ Ingestion complete: {files} files, {chunks} chunks")
        
        if result.get('skipped'):
            click.echo(f"⏭️  Skipped {result['skipped']} unchanged files")
            
    else:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Ingestion failed: {error}", err=True)


@project_commands.command('delete')
@click.argument('project_id')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def delete_project(project_id, force):
    """Delete a project and all its data."""
    if not force:
        # Get project info first
        response = call_api(f'/projects/{project_id}')
        if response and response.status_code == 200:
            project = response.json()
            project_name = project.get('name', 'Unknown')
            click.echo(f"⚠️  You are about to delete project: {project_name}")
            click.echo(f"   ID: {project_id}")
            click.echo("   This will remove all indexed data and cannot be undone!")
            
            if not click.confirm("Are you sure you want to continue?"):
                click.echo("❌ Deletion cancelled")
                return
        else:
            click.echo(f"⚠️  Project {project_id} not found or inaccessible")
            if not click.confirm("Delete anyway?"):
                click.echo("❌ Deletion cancelled")
                return
                
    response = call_api(f'/projects/{project_id}', method='DELETE')
    
    if not response:
        return
        
    if response.status_code == 200:
        click.echo(f"✅ Project {project_id} deleted successfully")
    else:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error deleting project: {error}", err=True)


@project_commands.command('archive')
@click.argument('project_id')
def archive_project(project_id):
    """Archive a project (stops watching but keeps data)."""
    data = {'status': 'archived'}
    response = call_api(f'/projects/{project_id}/status', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code == 200:
        click.echo(f"✅ Project {project_id} archived")
        click.echo("📦 Data preserved but file watching stopped")
    else:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error archiving project: {error}", err=True)


@project_commands.command('activate')
@click.argument('project_id')
def activate_project(project_id):
    """Activate an archived or paused project."""
    data = {'status': 'active'}
    response = call_api(f'/projects/{project_id}/status', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code == 200:
        click.echo(f"✅ Project {project_id} activated")
        click.echo("👁️  File watching resumed")
    else:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error activating project: {error}", err=True)