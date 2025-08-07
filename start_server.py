#!/usr/bin/env python3
"""
Start the ContextKeeper server using the new src/ structure.
This is the main entry point for the application.
"""

import sys
import os

# Add the current directory to Python path so src can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Import and run the main application from the new location
    from src.core.rag_agent import main
    
    # Pass command line arguments to main
    sys.exit(main())