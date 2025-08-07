"""
Query commands for ContextKeeper CLI.

Handles asking questions and searching through project knowledge.
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
            response = requests.get(url, timeout=30)  # Longer timeout for queries
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
        return response
    except requests.exceptions.RequestException as e:
        click.echo(f"❌ Server connection error: {e}", err=True)
        click.echo("💡 Make sure the server is running: contextkeeper server start", err=True)
        return None


@click.group()
def query_commands():
    """Query and search commands."""
    pass


@query_commands.command('ask')
@click.argument('question', required=False)
@click.option('--project', help='Project ID to query (uses current project if not specified)')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
@click.option('--context', default=5, help='Number of context chunks to include (default: 5)')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive query session')
def ask_question(question, project, output_json, context, interactive):
    """Ask a question about your code.
    
    QUESTION is the question to ask (optional if using --interactive)
    """
    
    if interactive:
        click.echo("🤖 Interactive ContextKeeper Query Session")
        click.echo("Type 'exit', 'quit', or press Ctrl+C to end session")
        click.echo("Type 'help' for available commands")
        click.echo()
        
        # Get current project if not specified
        current_project = None
        if not project:
            response = call_api('/projects/current')
            if response and response.status_code == 200:
                project_data = response.json()
                current_project = project_data.get('name', 'Unknown')
                project = project_data.get('id')
                click.echo(f"📁 Using current project: {current_project}")
            else:
                click.echo("⚠️  No current project set - queries will search all projects")
        
        click.echo()
        
        while True:
            try:
                user_input = click.prompt("🔍 Query", type=str).strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    click.echo("👋 Goodbye!")
                    break
                    
                if user_input.lower() in ['help', 'h']:
                    click.echo("Available commands:")
                    click.echo("  help, h     - Show this help")
                    click.echo("  exit, quit  - End session")
                    click.echo("  project     - Show current project")
                    click.echo("  switch <id> - Switch to different project")
                    click.echo("  context <n> - Set context chunks (current: {})".format(context))
                    click.echo()
                    continue
                    
                if user_input.lower() == 'project':
                    if current_project:
                        click.echo(f"📁 Current project: {current_project} ({project})")
                    else:
                        click.echo("❌ No current project set")
                    continue
                    
                if user_input.lower().startswith('switch '):
                    new_project_id = user_input[7:].strip()
                    # Try to get project info
                    response = call_api(f'/projects/{new_project_id}')
                    if response and response.status_code == 200:
                        project_data = response.json()
                        project = new_project_id
                        current_project = project_data.get('name', 'Unknown')
                        click.echo(f"✅ Switched to project: {current_project}")
                    else:
                        click.echo(f"❌ Project not found: {new_project_id}")
                    continue
                    
                if user_input.lower().startswith('context '):
                    try:
                        new_context = int(user_input[8:].strip())
                        context = new_context
                        click.echo(f"✅ Context chunks set to: {context}")
                    except ValueError:
                        click.echo("❌ Invalid context number")
                    continue
                
                if not user_input:
                    continue
                
                # Process the query
                _process_query(user_input, project, output_json, context)
                click.echo()
                
            except (KeyboardInterrupt, EOFError):
                click.echo("\n👋 Goodbye!")
                break
                
        return
    
    # Non-interactive mode
    if not question:
        click.echo("❌ Question required in non-interactive mode", err=True)
        click.echo("💡 Use --interactive for interactive mode or provide a question", err=True)
        return
        
    _process_query(question, project, output_json, context)


def _process_query(question: str, project_id: str = None, output_json: bool = False, context: int = 5):
    """Process a single query."""
    data = {
        'question': question,
        'context_limit': context
    }
    
    if project_id:
        data['project_id'] = project_id
    
    click.echo("🔍 Searching knowledge base...")
    response = call_api('/query', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Query failed: {error}", err=True)
        return
        
    result = response.json()
    
    if output_json:
        click.echo(json.dumps(result, indent=2))
        return
        
    # Format the response nicely
    click.echo("🤖 Answer:")
    click.echo()
    answer = result.get('answer', 'No answer provided')
    
    # Word wrap the answer for better readability
    import textwrap
    wrapped_answer = textwrap.fill(answer, width=80, initial_indent='  ', subsequent_indent='  ')
    click.echo(wrapped_answer)
    
    # Show context sources if available
    context_sources = result.get('context_sources', [])
    if context_sources:
        click.echo()
        click.echo("📚 Sources:")
        for i, source in enumerate(context_sources[:context], 1):
            file_path = source.get('file_path', 'Unknown file')
            relevance = source.get('relevance_score', 0.0)
            click.echo(f"  {i}. {file_path} (relevance: {relevance:.2f})")
            
            # Show a snippet if available
            snippet = source.get('content', '').strip()
            if snippet:
                snippet_preview = snippet[:200] + '...' if len(snippet) > 200 else snippet
                click.echo(f"     \"{snippet_preview}\"")
    
    # Show query statistics
    stats = result.get('statistics', {})
    if stats:
        click.echo()
        click.echo("📊 Query Stats:")
        search_time = stats.get('search_time', 0)
        llm_time = stats.get('llm_time', 0)
        total_time = stats.get('total_time', 0)
        chunks_searched = stats.get('chunks_searched', 0)
        
        click.echo(f"  Search time: {search_time:.2f}s")
        click.echo(f"  LLM time: {llm_time:.2f}s") 
        click.echo(f"  Total time: {total_time:.2f}s")
        click.echo(f"  Chunks searched: {chunks_searched}")


@query_commands.command('search')
@click.argument('term')
@click.option('--project', help='Project ID to search in (uses current project if not specified)')
@click.option('--type', 'file_type', help='Filter by file type (e.g., py, js, md)')
@click.option('--limit', default=10, help='Maximum number of results (default: 10)')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def search_code(term, project, file_type, limit, output_json):
    """Search for specific terms in the codebase.
    
    TERM is the search term or phrase
    """
    data = {
        'term': term,
        'limit': limit
    }
    
    if project:
        data['project_id'] = project
    
    if file_type:
        data['file_type'] = file_type
        
    response = call_api('/search', method='POST', data=data)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Search failed: {error}", err=True)
        return
        
    results = response.json()
    
    if output_json:
        click.echo(json.dumps(results, indent=2))
        return
        
    matches = results.get('matches', [])
    if not matches:
        click.echo(f"🔍 No results found for: {term}")
        return
        
    click.echo(f"🔍 Found {len(matches)} result{'s' if len(matches) != 1 else ''} for: {term}")
    click.echo()
    
    for i, match in enumerate(matches, 1):
        file_path = match.get('file_path', 'Unknown file')
        relevance = match.get('relevance_score', 0.0)
        content = match.get('content', '').strip()
        
        click.echo(f"{i}. {file_path} (relevance: {relevance:.2f})")
        
        # Show context around the match
        if content:
            # Highlight the search term (simple case-insensitive replacement)
            import re
            highlighted = re.sub(
                f'({re.escape(term)})', 
                f'**\\1**', 
                content, 
                flags=re.IGNORECASE
            )
            
            # Show a preview
            preview = highlighted[:300] + '...' if len(highlighted) > 300 else highlighted
            click.echo(f"   {preview}")
        
        click.echo()


@query_commands.command('history')
@click.option('--limit', default=20, help='Number of recent queries to show (default: 20)')
@click.option('--project', help='Filter by project ID')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def query_history(limit, project, output_json):
    """Show recent query history."""
    params = {'limit': limit}
    if project:
        params['project_id'] = project
        
    # Build query string
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    endpoint = f'/query/history?{query_string}'
    
    response = call_api(endpoint)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error getting history: {error}", err=True)
        return
        
    history = response.json()
    
    if output_json:
        click.echo(json.dumps(history, indent=2))
        return
        
    queries = history.get('queries', [])
    if not queries:
        click.echo("📝 No query history found")
        return
        
    click.echo(f"📝 Recent {len(queries)} queries:")
    click.echo()
    
    for i, query in enumerate(queries, 1):
        timestamp = query.get('timestamp', 'Unknown time')
        question = query.get('question', 'Unknown question')
        project_name = query.get('project_name', 'All projects')
        
        # Truncate long questions
        if len(question) > 60:
            question = question[:57] + '...'
            
        click.echo(f"{i:2}. [{timestamp}] {question}")
        click.echo(f"    Project: {project_name}")
        click.echo()


@query_commands.command('stats')
@click.option('--project', help='Show stats for specific project')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def query_stats(project, output_json):
    """Show query and search statistics."""
    endpoint = '/stats'
    if project:
        endpoint += f'?project_id={project}'
        
    response = call_api(endpoint)
    
    if not response:
        return
        
    if response.status_code != 200:
        error = response.json().get('error', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
        click.echo(f"❌ Error getting stats: {error}", err=True)
        return
        
    stats = response.json()
    
    if output_json:
        click.echo(json.dumps(stats, indent=2))
        return
        
    click.echo("📊 ContextKeeper Statistics")
    click.echo()
    
    # Query stats
    query_stats = stats.get('queries', {})
    click.echo("🔍 Query Statistics:")
    click.echo(f"   Total queries: {query_stats.get('total', 0)}")
    click.echo(f"   Queries today: {query_stats.get('today', 0)}")
    click.echo(f"   Average response time: {query_stats.get('avg_response_time', 0):.2f}s")
    click.echo(f"   Most active project: {query_stats.get('most_active_project', 'N/A')}")
    click.echo()
    
    # Knowledge base stats
    kb_stats = stats.get('knowledge_base', {})
    click.echo("📚 Knowledge Base Statistics:")
    click.echo(f"   Total projects: {kb_stats.get('total_projects', 0)}")
    click.echo(f"   Total files indexed: {kb_stats.get('total_files', 0)}")
    click.echo(f"   Total chunks: {kb_stats.get('total_chunks', 0)}")
    click.echo(f"   Database size: {kb_stats.get('db_size', 'Unknown')}")
    click.echo()
    
    # Recent activity
    recent = stats.get('recent_activity', [])
    if recent:
        click.echo("📈 Recent Activity:")
        for activity in recent[:5]:
            click.echo(f"   • {activity}")
        click.echo()