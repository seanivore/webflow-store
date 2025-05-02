#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_full_site_home_button(file_path):
    """Fix only the Full Site > Home Page navigation button, preserving all attributes and styles."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Super specific pattern to match exact href attribute for Home Page link
        # Using a more surgical approach to only replace the href attribute value
        pattern = re.compile(r'(<a\s+)href="[^"]*"(\s+id="[^"]*"\s+class="[^"]*"[^>]*>Home Page</a>)')
        
        if pattern.search(content):
            def fix_link(match):
                print(f"  Fixed 'Home Page' link in {file_path} -> ../../../index.html")
                return f'{match.group(1)}href="../../../index.html"{match.group(2)}'
                
            new_content = pattern.sub(fix_link, content)
            
            # Check if we actually made changes
            if new_content != content:
                # For verification, check if the replacement was successful
                if '../../../index.html' in new_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    return True
                else:
                    print(f"  Warning: Replacement pattern matched but href change not found in {file_path}")
            else:
                print(f"  No changes needed for {file_path}")
            
        return False
        
    except Exception as e:
        print(f"ERROR processing {file_path}: {e}")
        return False

def process_directory():
    """Process all HTML files in the lookbook directory."""
    target_dir = "./fashion/lookbook"
    total_processed = 0
    total_fixed = 0
    
    print(f"Scanning directory: {target_dir}")
    for file_path in Path(target_dir).glob('**/*.html'):
        total_processed += 1
        if fix_full_site_home_button(str(file_path)):
            total_fixed += 1
            
    print(f"\nFixed 'Full Site > Home Page' button in {total_fixed} of {total_processed} HTML files.")
    print(f"Confirm all links now correctly point to ../../../index.html")

if __name__ == "__main__":
    process_directory() 