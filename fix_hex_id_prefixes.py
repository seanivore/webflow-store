import os
import re
from pathlib import Path

# Get all HTML files in the project
html_files = list(Path('.').glob('**/*.html'))
assets_dir = Path('assets')
fixed_count = 0
verified_file_paths = {}  # Cache for verified file paths

print(f"Starting to fix image path ID prefixes in {len(html_files)} HTML files...")

# Pre-scan assets directory to build a map of filenames to their actual paths
filename_to_path = {}
for file_path in assets_dir.glob('**/*'):
    if file_path.is_file():
        filename_to_path[file_path.name] = str(file_path.relative_to('.'))

print(f"Found {len(filename_to_path)} asset files")

for html_file in html_files:
    folder_depth = len(html_file.parts) - 1
    path_prefix = '../' * folder_depth if folder_depth > 0 else ''
    
    print(f"Processing {html_file} (depth: {folder_depth})")
    
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    file_fixed_count = 0
    
    # Function to find the correct path for a filename
    def get_correct_path(filename):
        if filename in filename_to_path:
            return filename_to_path[filename]
        return None
    
    # Fix src attributes with hex ID prefixes
    def fix_src_path(match):
        # Use file_fixed_count from outer scope
        prefix = match.group(1)
        path_part = match.group(2) or ''
        hex_id = match.group(3)
        real_filename = match.group(4)
        
        correct_path = get_correct_path(real_filename)
        if correct_path:
            # Increment counter outside the function
            if folder_depth > 0:
                # Need to add ../ for depth
                return f'{prefix}{path_prefix}{correct_path}"'
            else:
                # In root directory, can use the path directly
                return f'{prefix}{correct_path}"'
        return match.group(0)
    
    # Fix src attributes for assets/images/
    content_fixed = re.sub(
        r'(src=")([\/\.]*)assets/images/([0-9a-f]+)_([^"/]+)"',
        fix_src_path,
        content
    )
    # Count changes
    if content_fixed != content:
        file_fixed_count += content_fixed.count('src="') - content.count('src="')
        content = content_fixed
    
    # Fix src attributes for any asset path
    content_fixed = re.sub(
        r'(src=")([\/\.]*)assets/[^"]+/([0-9a-f]+)_([^"/]+)"',
        fix_src_path,
        content
    )
    # Count changes
    if content_fixed != content:
        file_fixed_count += content_fixed.count('src="') - content.count('src="')
        content = content_fixed
    
    # Fix background-image URLs
    def fix_bg_image(match):
        prefix = match.group(1)
        path_part = match.group(2) or ''
        hex_id = match.group(3)
        real_filename = match.group(4)
        suffix = match.group(5)
        
        correct_path = get_correct_path(real_filename)
        if correct_path:
            if folder_depth > 0:
                return f'{prefix}{path_prefix}{correct_path}{suffix}'
            else:
                return f'{prefix}{correct_path}{suffix}'
        return match.group(0)
    
    # Fix background-image for assets/images/
    content_fixed = re.sub(
        r'(background-image:\s*url\([\'"]?)([\/\.]*)assets/images/([0-9a-f]+)_([^\'"\)]+)([\'"]?\))',
        fix_bg_image,
        content
    )
    # Count changes
    if content_fixed != content:
        file_fixed_count += content_fixed.count('background-image') - content.count('background-image')
        content = content_fixed
    
    # Fix background-image for any asset path
    content_fixed = re.sub(
        r'(background-image:\s*url\([\'"]?)([\/\.]*)assets/[^\)]+/([0-9a-f]+)_([^\'"\)]+)([\'"]?\))',
        fix_bg_image,
        content
    )
    # Count changes
    if content_fixed != content:
        file_fixed_count += content_fixed.count('background-image') - content.count('background-image')
        content = content_fixed
    
    # Fix srcset attributes
    def fix_srcset(match):
        prefix = match.group(1)
        path_part = match.group(2) or ''
        hex_id = match.group(3)
        real_filename = match.group(4)
        
        correct_path = get_correct_path(real_filename)
        if correct_path:
            if folder_depth > 0:
                return f'{prefix}{path_prefix}{correct_path}'
            else:
                return f'{prefix}{correct_path}'
        return match.group(0)
    
    # Fix srcset for assets/images/
    content_fixed = re.sub(
        r'(srcset=")([\/\.]*)assets/images/([0-9a-f]+)_([^ ",]+)',
        fix_srcset,
        content
    )
    # Count changes
    if content_fixed != content:
        file_fixed_count += content_fixed.count('srcset="') - content.count('srcset="')
        content = content_fixed
    
    # Fix srcset for any asset path
    content_fixed = re.sub(
        r'(srcset=")([\/\.]*)assets/[^"]+/([0-9a-f]+)_([^ ",]+)',
        fix_srcset,
        content
    )
    # Count changes
    if content_fixed != content:
        file_fixed_count += content_fixed.count('srcset="') - content.count('srcset="')
        content = content_fixed
    
    # If content was modified, write it back to the file
    if content != original_content:
        fixed_count += file_fixed_count
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Fixed {file_fixed_count} image paths in {html_file}")
    else:
        print(f"  No changes needed in {html_file}")

print(f"\nFixed {fixed_count} image path references with hex ID prefixes!")
print("Run your local server to verify all images are loading correctly.") 