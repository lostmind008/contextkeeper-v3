#!/usr/bin/env python3
"""
Test script to add analytics import to rag_agent.py
"""

def main():
    # Read the file
    with open('rag_agent.py', 'r') as f:
        content = f.read()
    
    # Check if analytics import already exists
    if "from analytics import" in content:
        print("Analytics import already exists!")
        return
    
    # Find the position to add the import
    import_line = "from enhanced_drift_sacred import SacredDriftDetector, add_sacred_drift_endpoint"
    if import_line in content:
        print("Found enhanced_drift_sacred import line")
        # Add analytics import after it
        new_import = "from analytics import SacredMetricsCalculator, AnalyticsService"
        content = content.replace(
            import_line,
            import_line + "\n" + new_import
        )
        
        # Write the modified content back
        with open('rag_agent.py', 'w') as f:
            f.write(content)
        
        print("Analytics import added successfully!")
    else:
        print("Could not find enhanced_drift_sacred import line")

if __name__ == "__main__":
    main()