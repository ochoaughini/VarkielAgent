#!/usr/bin/env python3
"""
Script to add operational risk warnings to Python files in the Varkiel Agent project.
"""

import os
import re
from pathlib import Path

# Warning text to add to each Python file
WARNING = """
⚠️ OPERATIONAL RISK WARNING ⚠️

This file contains experimental AI safety research code that includes intentional security patterns.

DANGER: This code is NOT production-ready and includes intentionally vulnerable patterns
for research purposes only. It must NEVER be deployed without proper OS-level isolation
(e.g., Docker containers with appropriate security profiles, seccomp, namespaces).

This code is provided AS-IS for research into AI safety, adversarial prompt containment,
and execution analysis. All unsafe patterns are intentionally exposed for research purposes.
"""

def add_warning_to_file(file_path):
    """Add warning to the top of a Python file."""
    try:
        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            
            # Check if warning already exists
            if "OPERATIONAL RISK WARNING" in content:
                print(f"⚠️  Warning already exists in {file_path}")
                return False
                
            # Find the first docstring (handles both """ and ''' style docstrings)
            docstring_match = re.search(r'^\s*(""".*?"""|\'\'\'.*?\'\'\')', 
                                     content, re.DOTALL)
            
            if docstring_match:
                # Insert warning before the first docstring
                new_content = content[:docstring_match.start()] + f'"""{WARNING}"""\n\n' + content[docstring_match.start():]
            else:
                # If no docstring found, add warning at the top
                new_content = f'"""{WARNING}"""\n\n' + content
            
            # Write the new content back to the file
            f.seek(0)
            f.write(new_content)
            f.truncate()
            print(f"✅ Added warning to {file_path}")
            return True
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def main():
    # Get all Python files in the project
    project_root = Path(__file__).parent
    python_files = list(project_root.glob('**/*.py'))
    
    print(f"Found {len(python_files)} Python files to process...")
    
    success_count = 0
    for py_file in python_files:
        if add_warning_to_file(py_file):
            success_count += 1
    
    print(f"\n✅ Successfully added warnings to {success_count}/{len(python_files)} files")
    if success_count < len(python_files):
        print("⚠️  Some files may already have warnings or encountered errors")

if __name__ == "__main__":
    main()
