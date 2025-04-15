import os
import re
import sys
from pathlib import Path

def fix_relative_paths_in_file(file_path, workspace_root):
    """Fix relative paths in HTML file based on its depth in the directory structure."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Calculate the file's depth in the directory structure
        rel_path = os.path.relpath(file_path, workspace_root)
        path_depth = len(Path(rel_path).parts) - 1
        
        # If the file is in the root directory, no changes needed
        if path_depth == 0:
            return False
            
        # Path prefix to navigate up to the root directory
        path_prefix = '../' * path_depth
        
        modified = False
        new_content = content
        
        # Fix 1: Fix malformed URLs like https://./index.html/
        malformed_url_pattern = re.compile(r'href=["\']https?://\./(.*?)["\']')
        def fix_malformed_url(match):
            nonlocal modified
            path = match.group(1)
            # Remove any trailing slash after html
            if path.endswith('/') and path.lower().endswith('.html/'):
                path = path[:-1]
            # Convert to a proper relative URL with correct depth
            fixed_url = f'href="{path_prefix}{path}"'
            modified = True
            print(f"  Fixed malformed URL: {match.group(0)} -> {fixed_url}")
            return fixed_url
            
        new_content = malformed_url_pattern.sub(fix_malformed_url, new_content)
        
        # Fix 2: Fix incorrect relative paths for images
        # This matches "./assets/images/" and changes it to the correct depth
        incorrect_img_pattern = re.compile(r'(src|srcset)=["\']\./assets/images/([^"\']+)["\']')
        def fix_incorrect_img_path(match):
            nonlocal modified
            attr = match.group(1)
            img_path = match.group(2)
            # Make path relative based on file depth
            fixed_path = f'{attr}="{path_prefix}assets/images/{img_path}"'
            modified = True
            print(f"  Fixed incorrect image path: {match.group(0)} -> {fixed_path}")
            return fixed_path
            
        new_content = incorrect_img_pattern.sub(fix_incorrect_img_path, new_content)
        
        # Fix 3: Also fix href attributes pointing to images
        incorrect_href_pattern = re.compile(r'href=["\']\./assets/images/([^"\']+)["\']')
        def fix_incorrect_href_path(match):
            nonlocal modified
            img_path = match.group(1)
            # Make path relative based on file depth
            fixed_path = f'href="{path_prefix}assets/images/{img_path}"'
            modified = True
            print(f"  Fixed incorrect href path: {match.group(0)} -> {fixed_path}")
            return fixed_path
            
        new_content = incorrect_href_pattern.sub(fix_incorrect_href_path, new_content)
        
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
    """Scan all HTML files in the workspace and fix relative paths."""
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
                
                if fix_relative_paths_in_file(file_path, workspace_root):
                    total_files_modified += 1

    print(f"\nFinished.")
    print(f"Total HTML files processed: {total_files_processed}")
    print(f"Total HTML files modified: {total_files_modified}")

if __name__ == "__main__":
    # Use current directory as the workspace root
    scan_and_fix_files(".") 