import os
import re
import sys

# CDN base URL pattern (adjust if needed, captures the domain part)
CDN_DOMAIN = "cdn.prod.website-files.com"
# Regex to find the full CDN path up to the filename
# It handles potential variations in the path structure before the filename
cdn_base_pattern = re.compile(r'https?://' + re.escape(CDN_DOMAIN) + r'/[^\"\'\s]+/')

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

def get_relative_image_path(base_filename, path_to_root, assets_folder="assets/images"):
     """Constructs the full relative path to the image."""
     # If path_to_root is '.', the image path starts from the current dir
     if path_to_root == '.':
         return f"{assets_folder}/{base_filename}"
     else:
         return f"{path_to_root}/{assets_folder}/{base_filename}"

def replace_cdn_urls_in_html(html_content, file_path, workspace_root):
    """Replaces CDN image URLs in src and srcset attributes with relative paths."""
    modified_content = html_content
    modified = False
    path_to_root = calculate_relative_path(file_path, workspace_root)

    # --- Function to process a single URL ---
    def process_url(url):
        nonlocal modified
        try:
            base_filename = url.split('?')[0].split('/')[-1] # Get filename, ignore query params
            file_ext = os.path.splitext(base_filename)[1].lower()

            if file_ext in IMAGE_EXTENSIONS:
                relative_img_path = get_relative_image_path(base_filename, path_to_root)
                # Basic check: Does the local file potentially exist? (Case-insensitive check helpful)
                # Note: This is a simple check; a more robust check would list assets/images once.
                # We'll rely on the export being complete for now.
                # print(f"    Replacing: {url} -> {relative_img_path}") # Verbose logging
                modified = True
                return relative_img_path
        except Exception as e:
            print(f"    WARN: Error processing URL {url} in {file_path}: {e}", file=sys.stderr)
        return None # Return None if not an image or error

    # --- Replace in src attributes ---
    # Pattern: src="<CDN_URL>"
    src_pattern = re.compile(r'src=["\'](https?://' + re.escape(CDN_DOMAIN) + r'/[^\"\']+)["\']', re.IGNORECASE)
    def replace_src_match(match):
        url = match.group(1)
        new_path = process_url(url)
        if new_path:
            print(f"  [src] Replaced {url.split('/')[-1]} with {new_path}")
            return f'src="{new_path}"'
        return match.group(0) # Return original if not replaced

    modified_content = src_pattern.sub(replace_src_match, modified_content)

    # --- Replace in srcset attributes ---
    # Pattern: srcset="<URL1> 500w, <URL2> 1080w, ..."
    srcset_pattern = re.compile(r'srcset=["\']([^\"\']+)["\']', re.IGNORECASE)
    def replace_srcset_match(match):
        srcset_value = match.group(1)
        parts = srcset_value.split(',')
        new_parts = []
        set_modified = False
        logged_set = False # Log only once per srcset

        for part in parts:
            part = part.strip()
            if not part: continue
            url_part = part.split(None, 1) # Split URL from descriptor like "500w"
            url = url_part[0]
            descriptor = url_part[1] if len(url_part) > 1 else ""

            if CDN_DOMAIN in url:
                new_path = process_url(url)
                if new_path:
                    new_parts.append(f"{new_path} {descriptor}".strip())
                    set_modified = True
                    if not logged_set:
                         print(f"  [srcset] Replaced {url.split('/')[-1]} (and possibly others) with relative paths")
                         logged_set = True
                else:
                    new_parts.append(part) # Keep original if processing failed
            else:
                new_parts.append(part) # Keep original if not a CDN URL

        if set_modified:
            return f'srcset="{", ".join(new_parts)}"'
        return match.group(0) # Return original if no changes in this srcset

    modified_content = srcset_pattern.sub(replace_srcset_match, modified_content)

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