#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_navigation_links(file_path):
    """Fix navigation links in deeply nested pages."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        modified = False
        new_content = content
        
        # Fix 1: Fix home links that add the directory path to the home link
        # This pattern looks for links to index.html/ or incorrect paths to home
        bad_home_pattern = re.compile(r'href=["\'](?:\.{0,2}/)*(?:fashion/lookbook/|understand-trends/buy-historic-artwork/original-print-series/)?index\.html/?["\']')
        def fix_home_link(match):
            nonlocal modified
            modified = True
            return 'href="../../../index.html"'
            
        new_content = bad_home_pattern.sub(fix_home_link, new_content)
        
        # Fix 2: Fix absolute file paths that point to Development/index.html
        absolute_home_pattern = re.compile(r'href=["\']file:///Users/seanivore/Development/(?:webflow-store/)?index\.html/?["\']')
        def fix_absolute_home_link(match):
            nonlocal modified
            modified = True
            return 'href="../../../index.html"'
            
        new_content = absolute_home_pattern.sub(fix_absolute_home_link, new_content)
        
        # Fix 3: Fix home text links that might be different
        home_text_pattern = re.compile(r'href=["\'](?:\.{0,2}/)*(?:fashion/lookbook/|understand-trends/buy-historic-artwork/original-print-series/)?["\']>Home</a>')
        def fix_home_text_link(match):
            nonlocal modified
            modified = True
            return 'href="../../../index.html">Home</a>'
            
        new_content = home_text_pattern.sub(fix_home_text_link, new_content)
        
        # Fix 4: Fix links in navigation menus for About, Contact, etc.
        nav_links_pattern = re.compile(r'href=["\'](?:\.{0,2}/)*(?:fashion/lookbook/|understand-trends/buy-historic-artwork/original-print-series/)?(about|contact|shop)\.html/?["\']')
        def fix_nav_link(match):
            nonlocal modified
            page = match.group(1)
            modified = True
            return f'href="../../../{page}.html"'
            
        new_content = nav_links_pattern.sub(fix_nav_link, new_content)
        
        # If we made changes, write back to the file
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed navigation links in: {file_path}")
            return True
        return False
        
    except Exception as e:
        print(f"ERROR processing {file_path}: {e}")
        return False

def process_directory(target_dir):
    """Process all HTML files in the specified directory."""
    total_processed = 0
    total_fixed = 0
    
    print(f"Scanning directory: {target_dir}")
    for file_path in Path(target_dir).glob('**/*.html'):
        total_processed += 1
        if fix_navigation_links(str(file_path)):
            total_fixed += 1
            
    print(f"\nFixed navigation links in {total_fixed} of {total_processed} HTML files.")

if __name__ == "__main__":
    # Fix navigation in the original print series
    print("Fixing navigation in original print series...")
    process_directory("./understand-trends/buy-historic-artwork/original-print-series")
    
    # Fix navigation in the lookbook section
    print("\nFixing navigation in lookbook section...")
    process_directory("./fashion/lookbook") 