#!/usr/bin/env python3
"""Debug script to find correct Kiro IDE sources"""

import requests
import re
from bs4 import BeautifulSoup

def debug_kiro_sources():
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    
    print("=== Finding Correct Kiro IDE Sources ===\n")
    
    # Check if the GitHub repo exists
    print("1. Checking GitHub repo existence...")
    try:
        resp = requests.get("https://github.com/kirodotdev/Kiro", headers=headers, timeout=10)
        print(f"GitHub repo status: {resp.status_code}")
        if resp.status_code == 404:
            print("   -> Repo doesn't exist or is private")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Check downloads page content
    print("2. Analyzing downloads page content...")
    try:
        resp = requests.get("https://kiro.dev/downloads/", headers=headers, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Look for download links
            links = soup.find_all('a', href=True)
            download_links = [link for link in links if any(ext in link['href'].lower() 
                            for ext in ['.appimage', '.tar.gz', '.deb', '.rpm'])]
            
            print(f"Found {len(download_links)} download links:")
            for link in download_links[:10]:  # Show first 10
                href = link['href']
                text = link.get_text(strip=True)
                print(f"  {href} -> '{text}'")
            
            # Look for version numbers in the page
            version_patterns = [
                r'version[:\s]+(\d+\.\d+\.\d+)',
                r'v(\d+\.\d+\.\d+)',
                r'(\d+\.\d+\.\d+)',
                r'kiro[_-](\d+\.\d+\.\d+)',
                r'ide[_-](\d+\.\d+\.\d+)'
            ]
            
            print(f"\nSearching for version patterns in page text...")
            for pattern in version_patterns:
                matches = re.findall(pattern, resp.text, re.IGNORECASE)
                if matches:
                    print(f"  Pattern '{pattern}': {list(set(matches))[:5]}")
                    
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Check AWS bucket structure
    print("3. Exploring AWS bucket structure...")
    try:
        # Try to list versions from the bucket
        base_url = "https://desktop-release.q.us-east-1.amazonaws.com"
        
        # Try some common version patterns
        test_versions = ["0.8.0", "0.9.0", "0.10.0", "0.11.0", "0.12.0"]
        
        for version in test_versions:
            appimage_url = f"{base_url}/{version}/kiro-ide-{version}-stable-linux-x64.AppImage"
            try:
                resp = requests.head(appimage_url, timeout=3)
                if resp.status_code == 200:
                    print(f"  Found IDE version {version}: {appimage_url}")
                    break
            except:
                pass
        
        # Try to get version list from manifest or other endpoints
        manifest_url = f"{base_url}/latest/manifest.json"
        resp = requests.get(manifest_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f"\nManifest data keys: {list(data.keys())}")
            if 'packages' in data:
                print(f"Packages: {len(data['packages'])}")
                for pkg in data['packages'][:3]:
                    print(f"  Package: {pkg}")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_kiro_sources()