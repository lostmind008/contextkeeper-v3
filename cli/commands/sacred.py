"""
Sacred layer commands for ContextKeeper CLI.

Handles sacred architectural decisions, approvals, and drift detection.
"""

import click
import sys
import json
import requests
from pathlib import Path

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
            response = requests.get(url, timeout=15)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=15)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=15)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
        return response
    except requests.exceptions.RequestException as e:
        click.echo(f"❌ Server connection error: {e}", err=True)
        click.echo("💡 Make sure the server is running: contextkeeper server start", err=True)
        return None


@click.group()
def sacred_commands():
    """Sacred layer architectural governance commands."""
    pass


@sacred_commands.command('status')
@click.option('--project', help='Show status for specific project')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def sacred_status(project, output_json):
    """Show sacred layer status and architectural decisions."""
    endpoint = '/sacred/status'
    if project:
        endpoint += f'?project_id={project}'
        
    response = call_api(endpoint)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error getting sacred status: {error}", err=True)
        return
        
    status = response.json()
    
    if output_json:
        click.echo(json.dumps(status, indent=2))
        return
        
    click.echo("🏛️  Sacred Layer Status")
    click.echo()
    
    # Overall health
    health = status.get('health', 'unknown')
    health_icon = {'healthy': '🟢', 'warning': '🟡', 'critical': '🔴'}.get(health, '❓')
    click.echo(f"Health: {health_icon} {health.upper()}")
    
    # Active decisions
    decisions = status.get('active_decisions', [])
    click.echo(f"Active Decisions: {len(decisions)}")
    
    # Pending approvals
    pending = status.get('pending_approvals', [])
    if pending:
        click.echo(f"Pending Approvals: ⏳ {len(pending)}")
    
    # Drift alerts
    drift_alerts = status.get('drift_alerts', [])
    if drift_alerts:
        click.echo(f"Drift Alerts: ⚠️ {len(drift_alerts)}")
    
    click.echo()
    
    # Show recent decisions
    if decisions:
        click.echo("📋 Recent Sacred Decisions:")
        for i, decision in enumerate(decisions[:5], 1):
            title = decision.get('title', 'Untitled')
            status_text = decision.get('status', 'unknown')
            timestamp = decision.get('created_at', 'Unknown time')
            click.echo(f"  {i}. {title} [{status_text}] ({timestamp})")
        click.echo()
    
    # Show pending approvals
    if pending:
        click.echo("⏳ Pending Approvals:")
        for i, approval in enumerate(pending[:5], 1):
            title = approval.get('title', 'Untitled')
            requester = approval.get('requester', 'Unknown')
            click.echo(f"  {i}. {title} (requested by {requester})")
        click.echo()
    
    # Show drift alerts
    if drift_alerts:
        click.echo("⚠️  Drift Alerts:")
        for i, alert in enumerate(drift_alerts[:5], 1):
            description = alert.get('description', 'Unknown drift')
            severity = alert.get('severity', 'medium')
            click.echo(f"  {i}. {description} [severity: {severity}]")
        click.echo()


@sacred_commands.command('decisions')
@click.option('--project', help='Filter by project ID')
@click.option('--status', type=click.Choice(['active', 'approved', 'rejected', 'pending']), 
              help='Filter by decision status')
@click.option('--limit', default=20, help='Maximum number of decisions to show')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def list_decisions(project, status, limit, output_json):
    """List sacred architectural decisions."""
    params = {'limit': limit}
    if project:
        params['project_id'] = project
    if status:
        params['status'] = status
        
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    endpoint = f'/sacred/decisions?{query_string}'
    
    response = call_api(endpoint)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error listing decisions: {error}", err=True)
        return
        
    data = response.json()
    decisions = data.get('decisions', [])
    
    if output_json:
        click.echo(json.dumps(decisions, indent=2))
        return
        
    if not decisions:
        click.echo("📋 No sacred decisions found")
        if status:
            click.echo(f"   (filtered by status: {status})")
        return
        
    click.echo(f"📋 Found {len(decisions)} sacred decision{'s' if len(decisions) != 1 else ''}:")
    click.echo()
    
    for i, decision in enumerate(decisions, 1):
        decision_id = decision.get('id', 'Unknown')
        title = decision.get('title', 'Untitled')
        status_text = decision.get('status', 'unknown')
        timestamp = decision.get('created_at', 'Unknown')
        project_name = decision.get('project_name', 'Unknown project')
        
        status_icon = {
            'active': '🟢',
            'approved': '✅',
            'rejected': '❌',
            'pending': '⏳'
        }.get(status_text, '❓')
        
        click.echo(f"{i:2}. {status_icon} {title}")
        click.echo(f"    ID: {decision_id}")
        click.echo(f"    Project: {project_name}")
        click.echo(f"    Status: {status_text}")
        click.echo(f"    Created: {timestamp}")
        
        # Show brief description if available
        description = decision.get('description', '').strip()
        if description:
            desc_preview = description[:80] + '...' if len(description) > 80 else description
            click.echo(f"    Description: {desc_preview}")
            
        click.echo()


@sacred_commands.command('create')
@click.argument('title')
@click.option('--description', prompt='Description', help='Detailed description of the decision')
@click.option('--category', type=click.Choice(['architecture', 'design', 'process', 'technology']),
              default='architecture', help='Category of decision')
@click.option('--project', help='Project ID (uses current project if not specified)')
@click.option('--priority', type=click.Choice(['low', 'medium', 'high', 'critical']),
              default='medium', help='Priority level')
def create_decision(title, description, category, project, priority):
    """Create a new sacred architectural decision.
    
    TITLE is the decision title/summary
    """
    if not project:
        # Try to get current project
        response = call_api('/projects/current')
        if response and response.status_code == 200:
            project_data = response.json()
            project = project_data.get('id')
            click.echo(f"📁 Using current project: {project_data.get('name', 'Unknown')}")
        else:
            click.echo("❌ No project specified and no current project set", err=True)
            click.echo("💡 Use: contextkeeper project focus <project_id>", err=True)
            return
            
    data = {
        'title': title,
        'description': description,
        'category': category,
        'project_id': project,
        'priority': priority
    }
    
    response = call_api('/sacred/decisions', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code == 201:
        decision = response.json()
        decision_id = decision.get('id')
        click.echo(f"✅ Sacred decision created with ID: {decision_id}")
        click.echo(f"📋 Title: {title}")
        click.echo(f"🏷️  Category: {category}")
        click.echo(f"⚡ Priority: {priority}")
        click.echo("⏳ Status: Pending approval")
    else:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error creating decision: {error}", err=True)


@sacred_commands.command('approve')
@click.argument('decision_id')
@click.option('--comment', help='Approval comment')
def approve_decision(decision_id, comment):
    """Approve a pending sacred decision."""
    data = {
        'action': 'approve',
        'comment': comment
    }
    
    response = call_api(f'/sacred/decisions/{decision_id}/approve', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code == 200:
        click.echo(f"✅ Decision {decision_id} approved")
        if comment:
            click.echo(f"💬 Comment: {comment}")
    else:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error approving decision: {error}", err=True)


@sacred_commands.command('reject')
@click.argument('decision_id')
@click.option('--reason', prompt='Rejection reason', help='Reason for rejection')
def reject_decision(decision_id, reason):
    """Reject a pending sacred decision."""
    data = {
        'action': 'reject',
        'reason': reason
    }
    
    response = call_api(f'/sacred/decisions/{decision_id}/approve', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code == 200:
        click.echo(f"❌ Decision {decision_id} rejected")
        click.echo(f"💬 Reason: {reason}")
    else:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error rejecting decision: {error}", err=True)


@sacred_commands.command('drift')
@click.option('--project', help='Check drift for specific project')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
@click.option('--fix', is_flag=True, help='Automatically fix detected drift where possible')
def check_drift(project, output_json, fix):
    """Check for architectural drift between decisions and implementation."""
    params = {}
    if project:
        params['project_id'] = project
    if fix:
        params['fix'] = 'true'
        
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()]) if params else ''
    endpoint = f'/sacred/drift/check{"?" + query_string if query_string else ""}'
    
    click.echo("🔍 Checking for architectural drift...")
    response = call_api(endpoint, method='POST')
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error checking drift: {error}", err=True)
        return
        
    result = response.json()
    
    if output_json:
        click.echo(json.dumps(result, indent=2))
        return
        
    drift_items = result.get('drift_detected', [])
    
    if not drift_items:
        click.echo("✅ No architectural drift detected")
        return
        
    click.echo(f"⚠️  Found {len(drift_items)} drift issue{'s' if len(drift_items) != 1 else ''}:")
    click.echo()
    
    for i, drift in enumerate(drift_items, 1):
        description = drift.get('description', 'Unknown drift')
        severity = drift.get('severity', 'medium')
        decision_id = drift.get('decision_id', 'Unknown')
        file_path = drift.get('file_path', 'Unknown file')
        
        severity_icon = {
            'low': '🟡',
            'medium': '🟠', 
            'high': '🔴',
            'critical': '💥'
        }.get(severity, '❓')
        
        click.echo(f"{i}. {severity_icon} {description}")
        click.echo(f"   Decision: {decision_id}")
        click.echo(f"   File: {file_path}")
        click.echo(f"   Severity: {severity}")
        
        # Show suggested fix if available
        suggested_fix = drift.get('suggested_fix')
        if suggested_fix:
            click.echo(f"   💡 Suggested fix: {suggested_fix}")
            
        auto_fixed = drift.get('auto_fixed', False)
        if auto_fixed:
            click.echo("   ✅ Automatically fixed")
            
        click.echo()
        
    if fix:
        fixed_count = sum(1 for drift in drift_items if drift.get('auto_fixed', False))
        click.echo(f"🔧 Automatically fixed {fixed_count}/{len(drift_items)} drift issues")


@sacred_commands.command('info')
@click.argument('decision_id')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def decision_info(decision_id, output_json):
    """Show detailed information about a sacred decision."""
    response = call_api(f'/sacred/decisions/{decision_id}')
    
    if not response:
        return
        
    if response.status_code != 200:
        click.echo(f"❌ Decision not found: {decision_id}", err=True)
        return
        
    decision = response.json()
    
    if output_json:
        click.echo(json.dumps(decision, indent=2))
        return
        
    click.echo(f"📋 Sacred Decision: {decision.get('title', 'Untitled')}")
    click.echo(f"   ID: {decision.get('id', 'Unknown')}")
    click.echo(f"   Status: {decision.get('status', 'Unknown')}")
    click.echo(f"   Category: {decision.get('category', 'Unknown')}")
    click.echo(f"   Priority: {decision.get('priority', 'Unknown')}")
    click.echo(f"   Project: {decision.get('project_name', 'Unknown')}")
    click.echo(f"   Created: {decision.get('created_at', 'Unknown')}")
    click.echo(f"   Modified: {decision.get('modified_at', 'Unknown')}")
    
    description = decision.get('description', '').strip()
    if description:
        click.echo()
        click.echo("📝 Description:")
        # Word wrap the description
        import textwrap
        wrapped = textwrap.fill(description, width=80, initial_indent='   ', subsequent_indent='   ')
        click.echo(wrapped)
    
    # Show approval history
    approvals = decision.get('approval_history', [])
    if approvals:
        click.echo()
        click.echo("📋 Approval History:")
        for approval in approvals:
            action = approval.get('action', 'unknown')
            timestamp = approval.get('timestamp', 'unknown')
            approver = approval.get('approver', 'unknown')
            comment = approval.get('comment', '')
            
            action_icon = {'approve': '✅', 'reject': '❌'}.get(action, '❓')
            click.echo(f"   {action_icon} {action.upper()} by {approver} ({timestamp})")
            if comment:
                click.echo(f"      Comment: {comment}")
    
    # Show related files
    related_files = decision.get('related_files', [])
    if related_files:
        click.echo()
        click.echo("📁 Related Files:")
        for file_path in related_files:
            click.echo(f"   • {file_path}")
    
    # Show drift status
    drift_status = decision.get('drift_status', {})
    if drift_status:
        click.echo()
        drift_detected = drift_status.get('drift_detected', False)
        if drift_detected:
            click.echo("⚠️  Drift Status: DRIFT DETECTED")
            last_check = drift_status.get('last_check', 'unknown')
            click.echo(f"   Last checked: {last_check}")
        else:
            click.echo("✅ Drift Status: No drift detected")