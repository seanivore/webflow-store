import os
import re
import sys
from pathlib import Path

# --- REMOVED CDN Patterns ---
# CDN_DOMAIN = "cdn.prod.website-files.com"
# cdn_base_pattern = re.compile(r'https?://' + re.escape(CDN_DOMAIN) + r'/[^\"\'\s]+/')

# Pattern to find the hex prefix (start of filename)
hex_prefix_pattern = re.compile(r'^[0-9a-f]+_')

# List of image extensions to target
IMAGE_EXTENSIONS = {'.webp', '.png', '.jpg', '.jpeg', '.gif', '.svg'}

def calculate_relative_path(file_path, root_dir):
    """Calculates the relative path prefix to get from file_path to root_dir."""
    file_dir = os.path.dirname(file_path)
    # Calculate path from file_dir up to root_dir
    path_to_root = os.path.relpath(root_dir, start=file_dir)
    # Convert to forward slashes for web paths
    path_to_root = path_to_root.replace("\\\\", "/")
    # If the file is in the root, path_to_root will be '.', adjust if needed for concatenation
    if path_to_root == '.':
        return '.' # Return '.' which means "current directory" relative path
    else:
        return path_to_root

def get_relative_image_path(base_filename, root_prefix, assets_folder="assets/images"):
    """Constructs the full relative path to the image using root_prefix."""
    return f"{root_prefix}{assets_folder}/{base_filename}"

def replace_cdn_urls_in_html(html_content, file_path, workspace_root):
    """Replaces *incorrectly* generated relative image URLs by removing the hex prefix."""
    modified_content = html_content
    modified = False
    relative_file_path = Path(os.path.relpath(file_path, workspace_root))
    folder_depth = len(relative_file_path.parts) - 1
    root_prefix = '../' * folder_depth

    # --- Function to process an existing relative path ---
    def process_existing_relative_path(path_match):
        nonlocal modified
        full_path = path_match.group(1) # e.g., ../assets/images/HEX_filename.webp
        path_parts = full_path.split('/')
        original_base_filename = path_parts[-1]

        # Check if it has the hex prefix
        if hex_prefix_pattern.match(original_base_filename):
            base_filename = hex_prefix_pattern.sub('', original_base_filename)
            file_ext = os.path.splitext(base_filename)[1].lower()

            if file_ext in IMAGE_EXTENSIONS:
                # Reconstruct the *correct* relative path using the *current* file's depth
                correct_relative_path = get_relative_image_path(base_filename, root_prefix)
                if full_path != correct_relative_path:
                    print(f"    Correcting: {original_base_filename} -> {base_filename} (Path: {correct_relative_path})")
                    modified = True
                    return correct_relative_path
                else:
                    # Path might already be correct if depth = 0 and no prefix was removed
                    # print(f"    Skipping already correct path: {full_path}")
                    pass
            else:
                print(f"    WARN: Non-image extension found in existing path: {original_base_filename} in {file_path}", file=sys.stderr)
        # else: # Path doesn't have the hex prefix, assume it's correct or unrelated
            # print(f"    Skipping path without hex prefix: {full_path}")
        return None # Indicate no replacement needed for this specific match

    # --- Regex to find existing potentially incorrect relative paths ---
    # Matches variations like: ../assets/images/..., ./assets/images/..., assets/images/...
    # Ensures it only captures paths ending with known image extensions.
    # It captures the full relative path in group 1.
    relative_path_pattern = re.compile(r'([.\\\/]*assets/images/[^\"\'\\s?#]+\.(?:webp|png|jpg|jpeg|gif|svg))', re.IGNORECASE)

    # --- Replace in src attributes ---
    # Explicitly define the combined pattern for src
    src_pattern = re.compile(r'src=[\"\']([.\\\/]*assets/images/[^\"\'\\s?#]+\.(?:webp|png|jpg|jpeg|gif|svg))[\"\']', re.IGNORECASE)
    def replace_src_match(match):
        corrected_path = process_existing_relative_path(match)
        if corrected_path:
            return f'src="' + corrected_path + '"'
        return match.group(0) # Return original if not corrected

    modified_content = src_pattern.sub(replace_src_match, modified_content)

    # --- Replace in srcset attributes ---
    srcset_pattern = re.compile(r'srcset=[\"\']([^\"\']+)[\"\']', re.IGNORECASE)
    def replace_srcset_match(match):
        srcset_value = match.group(1)
        parts = srcset_value.split(',')
        new_parts = []
        set_modified = False
        logged_set = False

        for part in parts:
            part = part.strip()
            if not part: continue
            url_part = part.split(None, 1) # Split URL from descriptor
            url = url_part[0]
            descriptor = url_part[1] if len(url_part) > 1 else ""

            # Check if this url matches our relative path pattern
            path_match = relative_path_pattern.match(url)
            if path_match:
                corrected_path = process_existing_relative_path(path_match)
                if corrected_path:
                    new_parts.append(f"{corrected_path} {descriptor}".strip())
                    set_modified = True
                    if not logged_set:
                        print(f"  [srcset] Corrected {path_match.group(2).split('_')[-1]} (and possibly others) to relative paths")
                        logged_set = True
                else:
                    new_parts.append(part) # Keep original if processing decided not to change
            else:
                new_parts.append(part) # Keep non-matching URLs

        if set_modified:
            nonlocal modified
            modified = True # Ensure overall modified flag is set
            return f'srcset="' + ", ".join(new_parts) + '"'
        return match.group(0) # Return original if no changes in this srcset

    modified_content = srcset_pattern.sub(replace_srcset_match, modified_content)

    # --- Replace in href attributes ---
    # Explicitly define the combined pattern for href
    href_pattern = re.compile(r'href=[\"\']([.\\\/]*assets/images/([0-9a-f]+_[^\"\'\\s?#]+\.(?:webp|png|jpg|jpeg|gif|svg)))[\"\']', re.IGNORECASE)
    def replace_href_match(match):
        corrected_path = process_existing_relative_path(match)
        if corrected_path:
            return f'href="' + corrected_path + '"'
        return match.group(0) # Return original if not corrected

    modified_content = href_pattern.sub(replace_href_match, modified_content)

    return modified_content, modified

# --- Main Execution ---
if __name__ == "__main__":
    workspace_root = "." # Assumes script is run from webflow-store directory
    total_files_processed = 0
    total_files_modified = 0

    print(f"Starting image path replacement from root: {os.path.abspath(workspace_root)}")

    for dirpath, dirnames, filenames in os.walk(workspace_root):
        # Skip .git directory explicitly
        if '.git' in dirnames:
            dirnames.remove('.git')
        if '.git' in dirpath.split(os.sep):
            continue
        # Skip this script itself
        if 'replace_image_paths.py' in filenames and dirpath == workspace_root :
             filenames.remove('replace_image_paths.py')
        if 'filter_scripts.py' in filenames and dirpath == workspace_root :
             filenames.remove('filter_scripts.py')


        for filename in filenames:
            if filename.lower().endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                print(f"Processing: {file_path}")
                total_files_processed += 1
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    new_content, modified = replace_cdn_urls_in_html(content, file_path, workspace_root)

                    if modified:
                        total_files_modified += 1
                        # print(f"  -> Modifying file.") # Less verbose output
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                    # else:
                        # print(f"  -> No changes needed.") # Less verbose output

                except Exception as e:
                    print(f"  ERROR processing {file_path}: {e}", file=sys.stderr)

    print(f"\nFinished.")
    print(f"Total HTML files processed: {total_files_processed}")
    print(f"Total HTML files modified: {total_files_modified}") 