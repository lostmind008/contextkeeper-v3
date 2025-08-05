#!/usr/bin/env python3
"""
Comprehensive Project Indexing Fix
==================================

This script addresses the issue where project proj_736df3fd80a4 only contains
JSON files with base64 encoded image data, providing no meaningful context.

The fix includes:
1. Better content filtering (exclude binary/base64 content)
2. Enhanced project indexing with meaningful content only
3. Improved file type detection
4. Content quality validation

Usage:
    python fix_project_indexing.py --project proj_736df3fd80a4 --reindex
"""

import os
import sys
import json
import base64
import mimetypes
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import requests
import argparse

class ProjectIndexingFixer:
    """Fixes project indexing issues with better content filtering"""
    
    def __init__(self, agent_url: str = "http://localhost:5556"):
        self.agent_url = agent_url
        self.excluded_dirs = {
            'node_modules', '.git', '__pycache__', '.pytest_cache',
            'venv', '.venv', 'env', '.env', 'site-packages',
            '.next', 'dist', 'build', '.DS_Store'
        }
        self.excluded_extensions = {
            '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
            '.exe', '.bin', '.dat', '.db', '.sqlite', '.sqlite3',
            '.log', '.tmp', '.temp', '.cache', '.pid'
        }
        self.image_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
            '.webp', '.svg', '.ico', '.heic', '.heif'
        }
        self.binary_extensions = self.image_extensions.union({
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.tar', '.gz', '.7z', '.rar', '.dmg', '.iso'
        })
    
    def is_base64_content(self, content: str) -> bool:
        """Check if content is primarily base64 encoded data"""
        if len(content) < 100:  # Too short to be meaningful base64
            return False
        
        # Check for base64 patterns
        base64_indicators = [
            'data:image/',
            'base64,',
            '"data":"data:',
            'iVBORw0KGgo',  # PNG signature in base64
            '/9j/',          # JPEG signature in base64
            'UklGR',         # RIFF (WebP/WAV) signature in base64
        ]
        
        for indicator in base64_indicators:
            if indicator in content:
                return True
        
        # Check if majority of content looks like base64
        lines = content.split('\n')
        base64_like_lines = 0
        
        for line in lines:
            line = line.strip()
            if len(line) > 50:  # Only check substantial lines
                try:
                    # Count characters that are valid base64
                    valid_chars = sum(1 for c in line if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
                    if valid_chars / len(line) > 0.9:  # 90% base64 characters
                        base64_like_lines += 1
                except:
                    continue
        
        # If more than 50% of substantial lines look like base64
        substantial_lines = [l for l in lines if len(l.strip()) > 50]
        if substantial_lines and base64_like_lines / len(substantial_lines) > 0.5:
            return True
        
        return False
    
    def is_meaningful_content(self, file_path: str, content: str) -> Tuple[bool, str]:
        """
        Determine if file content is meaningful for indexing
        Returns (is_meaningful, reason)
        """
        file_ext = Path(file_path).suffix.lower()
        
        # Skip binary files
        if file_ext in self.binary_extensions:
            return False, f"Binary file type: {file_ext}"
        
        # Skip empty files
        if not content.strip():
            return False, "Empty file"
        
        # Skip very small files (likely not meaningful)
        if len(content.strip()) < 50:
            return False, "File too small"
        
        # Skip base64 content
        if self.is_base64_content(content):
            return False, "Contains base64/binary data"
        
        # Check for JSON files with only data/metadata
        if file_ext == '.json':
            try:
                data = json.loads(content)
                if isinstance(data, dict):
                    # Skip if it's just metadata/data without descriptive content
                    keys = set(data.keys())
                    data_keys = {'data', 'image', 'base64', 'src', 'url', 'path', 'file'}
                    if keys.issubset(data_keys) or any(k in str(data) for k in ['data:image', 'base64,']):
                        return False, "JSON contains only data/metadata"
                    
                    # Look for meaningful text content
                    text_content = json.dumps(data, indent=2)
                    if len([word for word in text_content.split() if len(word) > 3]) < 10:
                        return False, "JSON lacks meaningful text"
            except:
                pass  # Not valid JSON, continue with other checks
        
        # Look for code patterns
        code_indicators = [
            'function ', 'def ', 'class ', 'import ', 'from ', 'const ', 'let ', 'var ',
            'if ', 'for ', 'while ', 'return ', 'export ', 'module.exports',
            '#!/', '#include', 'namespace ', 'using ', 'public class'
        ]
        
        has_code = any(indicator in content for indicator in code_indicators)
        
        # Look for documentation patterns
        doc_indicators = [
            '# ', '## ', '### ', '/**', '/*', '*/', '///', 'TODO:', 'FIXME:',
            'README', 'documentation', 'description', 'overview', 'getting started'
        ]
        
        has_docs = any(indicator.lower() in content.lower() for indicator in doc_indicators)
        
        # Look for configuration patterns
        config_indicators = [
            'version', 'name', 'description', 'dependencies', 'scripts', 'config',
            'settings', 'environment', 'api_key', 'database', 'server', 'port'
        ]
        
        has_config = any(indicator.lower() in content.lower() for indicator in config_indicators)
        
        # Must have at least one meaningful pattern
        if has_code or has_docs or has_config:
            return True, "Contains meaningful content"
        
        # Check word density
        words = content.split()
        meaningful_words = [w for w in words if len(w) > 3 and not w.isdigit()]
        if len(meaningful_words) > 20:
            return True, "Sufficient meaningful text"
        
        return False, "No meaningful patterns detected"
    
    def get_project_info(self, project_id: str) -> Optional[Dict]:
        """Get project information from API"""
        try:
            response = requests.get(f"{self.agent_url}/projects")
            if response.status_code == 200:
                data = response.json()
                for project in data.get('projects', []):
                    if project['id'] == project_id:
                        return project
        except Exception as e:
            print(f"Error getting project info: {e}")
        return None
    
    def scan_project_content(self, project_path: str) -> Dict:
        """Scan project directory and analyze content quality"""
        results = {
            'total_files': 0,
            'meaningful_files': 0,
            'skipped_files': 0,
            'file_analysis': [],
            'recommendations': []
        }
        
        if not os.path.exists(project_path):
            results['error'] = f"Project path does not exist: {project_path}"
            return results
        
        for root, dirs, files in os.walk(project_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)
                
                results['total_files'] += 1
                
                # Skip excluded extensions
                if Path(file).suffix.lower() in self.excluded_extensions:
                    results['skipped_files'] += 1
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    is_meaningful, reason = self.is_meaningful_content(file_path, content)
                    
                    file_info = {
                        'path': relative_path,
                        'size': len(content),
                        'meaningful': is_meaningful,
                        'reason': reason
                    }
                    
                    results['file_analysis'].append(file_info)
                    
                    if is_meaningful:
                        results['meaningful_files'] += 1
                    else:
                        results['skipped_files'] += 1
                        
                except Exception as e:
                    results['skipped_files'] += 1
                    results['file_analysis'].append({
                        'path': relative_path,
                        'error': str(e),
                        'meaningful': False,
                        'reason': f"Read error: {e}"
                    })
        
        # Generate recommendations
        if results['meaningful_files'] == 0:
            results['recommendations'].append("No meaningful content found. Consider:")
            results['recommendations'].append("1. Add README.md with project description")
            results['recommendations'].append("2. Add code files (.py, .js, .md, etc.)")
            results['recommendations'].append("3. Add configuration files")
            results['recommendations'].append("4. Exclude binary/image directories from indexing")
        elif results['meaningful_files'] < 5:
            results['recommendations'].append("Limited meaningful content found. Consider:")
            results['recommendations'].append("1. Add more documentation")
            results['recommendations'].append("2. Include source code files")
            results['recommendations'].append("3. Add project configuration files")
        
        return results
    
    def reindex_project(self, project_id: str) -> Dict:
        """Reindex project with better content filtering"""
        project_info = self.get_project_info(project_id)
        if not project_info:
            return {'error': f'Project {project_id} not found'}
        
        project_path = project_info.get('root_path')
        if not project_path:
            return {'error': f'No root path found for project {project_id}'}
        
        # First, analyze current content
        analysis = self.scan_project_content(project_path)
        
        # If no meaningful content, suggest fixes
        if analysis['meaningful_files'] == 0:
            return {
                'status': 'no_meaningful_content',
                'analysis': analysis,
                'action_required': True,
                'message': 'Project contains no meaningful content for indexing'
            }
        
        # TODO: Implement actual reindexing API call
        # For now, return analysis with instructions
        return {
            'status': 'analysis_complete',
            'analysis': analysis,
            'action_required': analysis['meaningful_files'] < 5,
            'message': f'Found {analysis["meaningful_files"]} meaningful files out of {analysis["total_files"]} total'
        }

def main():
    parser = argparse.ArgumentParser(description='Fix project indexing issues')
    parser.add_argument('--project', '-p', required=True, help='Project ID to fix')
    parser.add_argument('--reindex', '-r', action='store_true', help='Attempt to reindex project')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    fixer = ProjectIndexingFixer()
    
    print(f"🔍 Analyzing project: {args.project}")
    print("=" * 50)
    
    result = fixer.reindex_project(args.project)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    analysis = result.get('analysis', {})
    
    print(f"📊 Analysis Results:")
    print(f"   Total files: {analysis.get('total_files', 0)}")
    print(f"   Meaningful files: {analysis.get('meaningful_files', 0)}")
    print(f"   Skipped files: {analysis.get('skipped_files', 0)}")
    print()
    
    if args.verbose and analysis.get('file_analysis'):
        print("📝 File Analysis:")
        for file_info in analysis['file_analysis']:
            status = "✅" if file_info['meaningful'] else "❌"
            print(f"   {status} {file_info['path']} - {file_info['reason']}")
        print()
    
    if analysis.get('recommendations'):
        print("💡 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"   {rec}")
        print()
    
    if result['action_required']:
        print("⚠️  Action Required:")
        print("   This project needs meaningful content to provide useful chat responses.")
        print("   See recommendations above.")
    else:
        print("✅ Project has sufficient meaningful content for indexing.")

if __name__ == "__main__":
    main()