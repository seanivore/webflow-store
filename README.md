# AI Print Store - Webflow Export

## Overview
This repository contains a complete Webflow export for the AI Print Store - a collection of over 30+ different art movements beautifully and accurately reproduced as single-edition prints. The site is configured to be hosted at [ai-print-store.august.style](https://ai-print-store.august.style/).

## Site Structure
- **HTML Files**: All pages exported from Webflow with proper relative paths
- **Assets**: Images and other media files in the `assets/` directory
- **CSS/JS**: Webflow-generated styling and scripts

## Path Fixing Scripts
This project includes several utility scripts to fix common path issues in Webflow exports:

### replace_image_paths.py
Fixes relative paths for images, ensuring they work properly across the site. The script handles:
- Correct relative path calculation based on file depth
- Proper regex pattern matching for image extensions
- Replacement in both `src` and `href` attributes

### fix_nested_image_paths.py
Dedicated script for dealing with nested directory structures:
- Calculates proper path depth for each HTML file
- Fixes malformed URLs like `https://./index.html/`
- Updates relative paths for deeply nested files
- Handles both image and link paths

### fix_navigation_links.py
Fixes navigation issues in deeply nested directories:
- Corrects home links in the original print series (`/understand-trends/buy-historic-artwork/original-print-series/`) 
- Fixes navigation in the lookbook section (`/fashion/lookbook/`)
- Fixes absolute file paths that incorrectly point to `file:///Users/seanivore/Development/index.html/`
- Ensures About, Contact, and other main navigation links point to the correct locations
- Replaces incorrect paths like `fashion/lookbook/index.html` with proper `../../../index.html` paths

### fix_lookbook_navigation.py
Specialized script for the complex navigation in the lookbook section:
- Precisely targets each navigation button by its text content
- Fixes "Full Site" dropdown menu links (Home Page, Print Shop, Lookbook Cover)
- Fixes "Made Simple" dropdown menu links (How To Buy the Looks, Table of Contents)
- Fixes "Trend Watch" dropdown menu links (Season Trends, Art History Inspired Looks, Zodiac Inspired Outfits)
- Addresses unique path issues for each button with specific patterns and transformations

## How to Test Locally
1. Open any HTML file directly in your browser
   - Example: Open `index.html` in Chrome to view the home page
   - Navigate through the site using the links

2. Alternative: Run a local web server:
   ```
   python3 -m http.server 8000
   ```
   Then visit [http://localhost:8000](http://localhost:8000) in your browser

## Deployment
The site is configured to deploy to [ai-print-store.august.style](https://ai-print-store.august.style/) using:
- `CNAME` file for custom domain configuration
- `_config.yml` for site metadata and settings

## Troubleshooting Common Issues

### Missing Images
If images are not displaying correctly:
1. Check browser console for 404 errors
2. Verify the paths in the HTML source
3. Run the path fixing scripts if needed:
   ```
   python3 replace_image_paths.py
   ```

### Navigation Issues
If links are not working properly:
1. Ensure relative paths are correct
2. For deeply nested pages, run:
   ```
   python3 fix_nested_image_paths.py
   ```
3. For specific navigation menu issues in deep directories:
   ```
   python3 fix_navigation_links.py
   ```
4. For complex lookbook navigation buttons:
   ```
   python3 fix_lookbook_navigation.py
   ```

### CSS/Style Issues
Webflow exports include all necessary CSS. If styles aren't applying:
1. Ensure the browser can access the CSS files
2. Check for path issues to stylesheets
3. Verify that you're viewing via an appropriate protocol (http:// rather than file://)

## Content Statistics
- Total HTML files: Over 1,100
- Image assets: Nearly 3,000 files
- Art movements represented: 30+
- Site structure: Home, categories, product detail pages, and more

## License
All content is proprietary and copyright protected. 