#!/usr/bin/env python3
"""
Setup script for ContextKeeper CLI.
Ensures all dependencies are available and sets up the CLI properly.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Need Python 3.8+")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_click():
    """Install Click if not available."""
    try:
        import click
        print("✅ Click library already available")
        return True
    except ImportError:
        print("📦 Installing Click library...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'click'])
            print("✅ Click installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Click. Please install manually: pip install click")
            return False

def install_requests():
    """Install requests if not available."""
    try:
        import requests
        print("✅ Requests library already available")
        return True
    except ImportError:
        print("📦 Installing requests library...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
            print("✅ Requests installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install requests. Please install manually: pip install requests")
            return False

def make_executable():
    """Make the CLI script executable."""
    cli_path = Path(__file__).parent / 'contextkeeper_cli.py'
    
    if cli_path.exists():
        # Make executable on Unix-like systems
        if os.name != 'nt':  # Not Windows
            try:
                os.chmod(cli_path, 0o755)
                print("✅ Made contextkeeper_cli.py executable")
            except OSError as e:
                print(f"⚠️  Could not make CLI executable: {e}")
        
        return True
    else:
        print("❌ contextkeeper_cli.py not found")
        return False

def create_alias_script():
    """Create a convenience script for easier access."""
    script_content = '''#!/usr/bin/env python3
"""Convenience wrapper for ContextKeeper CLI."""
import sys
from pathlib import Path

# Add the ContextKeeper directory to Python path
contextkeeper_dir = Path(__file__).parent
sys.path.insert(0, str(contextkeeper_dir))

if __name__ == '__main__':
    from contextkeeper_cli import main
    main()
'''
    
    script_path = Path(__file__).parent / 'contextkeeper'
    
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        if os.name != 'nt':
            os.chmod(script_path, 0o755)
        
        print("✅ Created 'contextkeeper' wrapper script")
        print("💡 You can now run: ./contextkeeper [commands]")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create wrapper script: {e}")
        return False

def test_cli():
    """Test that the CLI works."""
    print("\n🧪 Testing CLI...")
    
    try:
        from contextkeeper_cli import main
        print("✅ CLI imports successfully")
        
        # Test help command
        import click.testing
        runner = click.testing.CliRunner()
        result = runner.invoke(main, ['--help'])
        
        if result.exit_code == 0:
            print("✅ CLI help command works")
            return True
        else:
            print(f"❌ CLI help command failed: {result.output}")
            return False
            
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def main():
    """Run setup process."""
    print("🚀 ContextKeeper CLI Setup")
    print("=" * 40)
    
    setup_steps = [
        ("Checking Python version", check_python_version),
        ("Installing Click", install_click),
        ("Installing Requests", install_requests),
        ("Making CLI executable", make_executable),
        ("Creating wrapper script", create_alias_script),
        ("Testing CLI", test_cli),
    ]
    
    success_count = 0
    
    for step_name, step_func in setup_steps:
        print(f"\n{step_name}...")
        if step_func():
            success_count += 1
        else:
            print(f"❌ {step_name} failed")
    
    print("\n" + "=" * 40)
    print(f"📊 Setup Results: {success_count}/{len(setup_steps)} steps completed")
    
    if success_count == len(setup_steps):
        print("🎉 Setup completed successfully!")
        print("\n💡 Try these commands:")
        print("  python contextkeeper_cli.py --help")
        print("  python contextkeeper_cli.py")
        print("  ./contextkeeper --help")
        return 0
    else:
        print("⚠️  Setup completed with some issues. CLI may still work.")
        print("💡 Try: python contextkeeper_cli.py --help")
        return 1

if __name__ == '__main__':
    sys.exit(main())