import os
import re
from pathlib import Path

# Patterns to match problematic references in HTML files
patterns = [
    # Images with ./index.html- prefix
    (re.compile(r'(["\']\./assets/images/)(\.\/index\.html-)(.*?)(["\']\s*)', re.IGNORECASE), r'\1\3\4'),
    
    # Any asset with ./index.html- prefix
    (re.compile(r'(["\']\./assets/)(\.\/index\.html-)(.*?)(["\']\s*)', re.IGNORECASE), r'\1\3\4'),
    
    # Direct references to /assets/images/index.html-
    (re.compile(r'(["\'])/assets/images/index\.html-(.*?)(["\']\s*)', re.IGNORECASE), r'\1/assets/images/\2\3'),
    
    # Fix data-wf-domain attribute that might be incorrectly set to ./index.html
    (re.compile(r'data-wf-domain=["\']\.\/index\.html["\']', re.IGNORECASE), r'data-wf-domain="/"'),
    
    # Fix canonical links
    (re.compile(r'href=["\'](https?:\/\/)?\.\/index\.html\/?["\'](\s+rel=["\'](canonical|shortlink)["\'])', re.IGNORECASE), 
               r'href="https://augusthousellc.com/"\2'),
]

# Count of files processed and modified
total_files_processed = 0
total_files_modified = 0

print(f"Starting to fix HTML references...")

# Process all HTML files in the project
for html_file in Path('.').glob('**/*.html'):
    total_files_processed += 1
    
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        modified = False
        modified_content = content
        
        # Apply all patterns
        for pattern, replacement in patterns:
            new_content = pattern.sub(replacement, modified_content)
            if new_content != modified_content:
                modified = True
                modified_content = new_content
        
        if modified:
            total_files_modified += 1
            print(f"Fixing references in: {html_file}")
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
    
    except Exception as e:
        print(f"Error processing {html_file}: {e}")

print(f"\nCompleted! Processed {total_files_processed} HTML files, modified {total_files_modified} files.") 