#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_full_site_home_button(file_path):
    """Fix only the Full Site > Home Page navigation button."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Pattern specifically for the "Home Page" link in the Full Site dropdown
        # Using contextual markup to ensure we only target this specific button
        home_pattern = re.compile(r'<div[^>]*class="lb-nav-link-wrap-tier-2[^>]*>.*?Full.*?Site.*?</div>.*?<nav[^>]*class="lb-sub-menu-home[^>]*>.*?<a[^>]*href="[^"]*"[^>]*>Home Page</a>', re.DOTALL)
        
        if home_pattern.search(content):
            # More specific pattern to capture the href attribute
            specific_link_pattern = re.compile(r'(<div[^>]*class="lb-nav-link-wrap-tier-2[^>]*>.*?Full.*?Site.*?</div>.*?<nav[^>]*class="lb-sub-menu-home[^>]*>.*?<a[^>]*href=")[^"]*(".*?>Home Page</a>)', re.DOTALL)
            
            def fix_home_link(match):
                print(f"  Fixed 'Home Page' link in Full Site menu -> ../../../index.html")
                return f'{match.group(1)}../../../index.html{match.group(2)}'
                
            new_content = specific_link_pattern.sub(fix_home_link, content)
            
            # Only write if changes were made
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
            
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

if __name__ == "__main__":
    process_directory() 