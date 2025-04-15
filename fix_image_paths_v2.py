import os
import re
import sys
from pathlib import Path

def fix_all_paths_in_file(file_path, workspace_root):
    """Fix all problematic paths in the HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        modified = False
        new_content = content
        
        # Fix 1: Fix malformed URLs like https://./index.html/
        malformed_url_pattern = re.compile(r'href=["\']https?://\./(.*?)["\']')
        def fix_malformed_url(match):
            nonlocal modified
            path = match.group(1)
            # Convert to a proper relative URL
            fixed_url = f'href="./{path}"'
            modified = True
            print(f"  Fixed malformed URL: {match.group(0)} -> {fixed_url}")
            return fixed_url
            
        new_content = malformed_url_pattern.sub(fix_malformed_url, new_content)
        
        # Fix 2: Convert absolute paths back to relative for file:// protocol compatibility
        # Change /assets/images/ back to ./assets/images/
        absolute_img_pattern = re.compile(r'(src|srcset)=["\'](/assets/images/[^"\']+)["\']')
        def fix_absolute_img_path(match):
            nonlocal modified
            attr = match.group(1)
            img_path = match.group(2)
            # Make path relative for file:// protocol
            fixed_path = f'{attr}="./assets/images/{os.path.basename(img_path)}"'
            modified = True
            print(f"  Fixed absolute image path: {match.group(0)} -> {fixed_path}")
            return fixed_path
            
        new_content = absolute_img_pattern.sub(fix_absolute_img_path, new_content)
        
        # Fix 3: Normalize any other image paths to ensure consistency
        inconsistent_img_pattern = re.compile(r'(src|srcset)=["\']((?:\.\./)+assets/images/[^"\']+)["\']')
        def normalize_img_path(match):
            nonlocal modified
            attr = match.group(1)
            img_path = match.group(2)
            basename = os.path.basename(img_path)
            # Normalize to ./assets/images/filename.ext format
            fixed_path = f'{attr}="./assets/images/{basename}"'
            modified = True
            print(f"  Normalized image path: {match.group(0)} -> {fixed_path}")
            return fixed_path
            
        new_content = inconsistent_img_pattern.sub(normalize_img_path, new_content)
        
        # If we made changes, write back to the file
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
        
    except Exception as e:
        print(f"  ERROR processing {file_path}: {e}", file=sys.stderr)
        return False

def scan_and_fix_files(workspace_root):
    """Scan all HTML files in the workspace and fix paths."""
    total_files_processed = 0
    total_files_modified = 0

    print(f"Starting path fixing from root: {os.path.abspath(workspace_root)}")

    for dirpath, dirnames, filenames in os.walk(workspace_root):
        # Skip .git directory
        if '.git' in dirnames:
            dirnames.remove('.git')
        if '.git' in dirpath.split(os.sep):
            continue
            
        for filename in filenames:
            if filename.lower().endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                print(f"Processing: {file_path}")
                total_files_processed += 1
                
                if fix_all_paths_in_file(file_path, workspace_root):
                    total_files_modified += 1

    print(f"\nFinished.")
    print(f"Total HTML files processed: {total_files_processed}")
    print(f"Total HTML files modified: {total_files_modified}")

if __name__ == "__main__":
    scan_and_fix_files(".") 