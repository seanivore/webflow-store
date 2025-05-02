#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_lookbook_navigation(file_path):
    """Fix navigation links specifically in the lookbook section with focused corrections."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        modified = False
        new_content = content
        
        # First fix: Full Site > Home Page
        home_pattern = re.compile(r'<a[^>]*>Home Page</a>', re.IGNORECASE)
        home_matches = home_pattern.findall(new_content)
        
        if home_matches:
            home_link_pattern = re.compile(r'<a\s+href=["\']([^"\']+)["\'][^>]*>Home Page</a>', re.IGNORECASE)
            
            def fix_home_link(match):
                nonlocal modified
                modified = True
                print(f"  Fixed 'Home Page' link: {match.group(1)} -> ../../../index.html")
                return f'<a href="../../../index.html">Home Page</a>'
                
            new_content = home_link_pattern.sub(fix_home_link, new_content)
        
        # Second fix: Full Site > Print Shop
        print_shop_pattern = re.compile(r'<a[^>]*>Print Shop</a>', re.IGNORECASE)
        print_shop_matches = print_shop_pattern.findall(new_content)
        
        if print_shop_matches:
            print_shop_link_pattern = re.compile(r'<a\s+href=["\']([^"\']+)["\'][^>]*>Print Shop</a>', re.IGNORECASE)
            
            def fix_print_shop_link(match):
                nonlocal modified
                modified = True
                print(f"  Fixed 'Print Shop' link: {match.group(1)} -> ../../../art-movement-museum/buy-historic-prints.html")
                return f'<a href="../../../art-movement-museum/buy-historic-prints.html">Print Shop</a>'
                
            new_content = print_shop_link_pattern.sub(fix_print_shop_link, new_content)
        
        # Third fix: Full Site > Lookbook Cover
        lookbook_pattern = re.compile(r'<a[^>]*>Lookbook Cover</a>', re.IGNORECASE)
        lookbook_matches = lookbook_pattern.findall(new_content)
        
        if lookbook_matches:
            lookbook_link_pattern = re.compile(r'<a\s+href=["\']([^"\']+)["\'][^>]*>Lookbook Cover</a>', re.IGNORECASE)
            
            def fix_lookbook_link(match):
                nonlocal modified
                modified = True
                print(f"  Fixed 'Lookbook Cover' link: {match.group(1)} -> ./summer-2024-cover.html")
                return f'<a href="./summer-2024-cover.html">Lookbook Cover</a>'
                
            new_content = lookbook_link_pattern.sub(fix_lookbook_link, new_content)
        
        # Fourth fix: Made Simple > How To Buy the Looks
        buy_looks_pattern = re.compile(r'<a[^>]*>How To Buy the Looks</a>', re.IGNORECASE)
        buy_looks_matches = buy_looks_pattern.findall(new_content)
        
        if buy_looks_matches:
            buy_looks_link_pattern = re.compile(r'<a\s+href=["\']([^"\']+)["\'][^>]*>How To Buy the Looks</a>', re.IGNORECASE)
            
            def fix_buy_looks_link(match):
                nonlocal modified
                modified = True
                print(f"  Fixed 'How To Buy the Looks' link: {match.group(1)} -> ../../../index.html")
                return f'<a href="../../../index.html">How To Buy the Looks</a>'
                
            new_content = buy_looks_link_pattern.sub(fix_buy_looks_link, new_content)
        
        # Fifth fix: Made Simple > Table of Contents
        toc_pattern = re.compile(r'<a[^>]*>Table of Contents</a>', re.IGNORECASE)
        toc_matches = toc_pattern.findall(new_content)
        
        if toc_matches:
            toc_link_pattern = re.compile(r'<a\s+href=["\']([^"\']+)["\'][^>]*>Table of Contents</a>', re.IGNORECASE)
            
            def fix_toc_link(match):
                nonlocal modified
                modified = True
                print(f"  Fixed 'Table of Contents' link: {match.group(1)} -> ./summer-fall-2024-trend-table-of-contents.html")
                return f'<a href="./summer-fall-2024-trend-table-of-contents.html">Table of Contents</a>'
                
            new_content = toc_link_pattern.sub(fix_toc_link, new_content)
        
        # Sixth fix: Trend Watch > Season Trends
        season_trends_pattern = re.compile(r'<a[^>]*>Season Trends</a>', re.IGNORECASE)
        season_trends_matches = season_trends_pattern.findall(new_content)
        
        if season_trends_matches:
            season_trends_link_pattern = re.compile(r'<a\s+href=["\']([^"\']+)["\'][^>]*>Season Trends</a>', re.IGNORECASE)
            
            def fix_season_trends_link(match):
                nonlocal modified
                modified = True
                print(f"  Fixed 'Season Trends' link: {match.group(1)} -> ./trend-watch-big-changes.html")
                return f'<a href="./trend-watch-big-changes.html">Season Trends</a>'
                
            new_content = season_trends_link_pattern.sub(fix_season_trends_link, new_content)
        
        # Seventh fix: Trend Watch > Art History Inspired Looks
        art_history_pattern = re.compile(r'<a[^>]*>Art History Inspired Looks</a>', re.IGNORECASE)
        art_history_matches = art_history_pattern.findall(new_content)
        
        if art_history_matches:
            art_history_link_pattern = re.compile(r'<a\s+href=["\']([^"\']+)["\'][^>]*>Art History Inspired Looks</a>', re.IGNORECASE)
            
            def fix_art_history_link(match):
                nonlocal modified
                modified = True
                print(f"  Fixed 'Art History Inspired Looks' link: {match.group(1)} -> ./classic-art-history-prints-paired-with-fashion.html")
                return f'<a href="./classic-art-history-prints-paired-with-fashion.html">Art History Inspired Looks</a>'
                
            new_content = art_history_link_pattern.sub(fix_art_history_link, new_content)
        
        # Eighth fix: Trend Watch > Zodiac Inspired Outfits
        zodiac_pattern = re.compile(r'<a[^>]*>Zodiac Inspired Outfits</a>', re.IGNORECASE)
        zodiac_matches = zodiac_pattern.findall(new_content)
        
        if zodiac_matches:
            zodiac_link_pattern = re.compile(r'<a\s+href=["\']([^"\']+)["\'][^>]*>Zodiac Inspired Outfits</a>', re.IGNORECASE)
            
            def fix_zodiac_link(match):
                nonlocal modified
                modified = True
                print(f"  Fixed 'Zodiac Inspired Outfits' link: {match.group(1)} -> ./zodiac-inspired-photoshoot-images.html")
                return f'<a href="./zodiac-inspired-photoshoot-images.html">Zodiac Inspired Outfits</a>'
                
            new_content = zodiac_link_pattern.sub(fix_zodiac_link, new_content)
            
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

def process_directory():
    """Process all HTML files in the lookbook directory."""
    target_dir = "./fashion/lookbook"
    total_processed = 0
    total_fixed = 0
    
    print(f"Scanning directory: {target_dir}")
    for file_path in Path(target_dir).glob('**/*.html'):
        total_processed += 1
        if fix_lookbook_navigation(str(file_path)):
            total_fixed += 1
            
    print(f"\nFixed navigation links in {total_fixed} of {total_processed} HTML files.")

if __name__ == "__main__":
    process_directory() 