#!/usr/bin/env python3
"""Debug script to test Kiro version detection"""

import requests
import re
from packaging.version import parse as parse_version

def debug_kiro_version():
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    
    print("=== Debugging Kiro Version Detection ===\n")
    
    # Method 1: GitHub releases API
    print("1. Trying GitHub releases API...")
    try:
        resp = requests.get("https://api.github.com/repos/kirodotdev/Kiro/releases", 
                           headers=headers, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            releases = resp.json()
            print(f"Found {len(releases)} releases")
            
            # Show first few releases
            for i, release in enumerate(releases[:5]):
                tag = release.get("tag_name", "")
                name = release.get("name", "")
                print(f"  Release {i+1}: tag='{tag}', name='{name}'")
                
                # Check if it's IDE version
                version_match = re.search(r'(\d+\.\d+\.\d+)', tag)
                if version_match:
                    version = version_match.group(1)
                    print(f"    Extracted version: {version}")
                    if version.startswith('0.'):
                        print(f"    -> IDE version candidate: {version}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Method 2: Downloads page
    print("2. Trying downloads page...")
    try:
        resp = requests.get("https://kiro.dev/downloads/", headers=headers, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            text = resp.text
            print(f"Page content length: {len(text)} chars")
            
            # Look for version patterns
            ide_versions = re.findall(r'kiro-ide-(\d+\.\d+\.\d+)', text, re.IGNORECASE)
            print(f"Found kiro-ide versions: {ide_versions}")
            
            all_versions = re.findall(r'(\d+\.\d+\.\d+)', text)
            ide_candidates = [v for v in set(all_versions) if v.startswith('0.')]
            print(f"All 0.x.x versions found: {ide_candidates}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Method 3: CLI manifest
    print("3. Trying CLI manifest...")
    try:
        url = "https://desktop-release.q.us-east-1.amazonaws.com/latest/manifest.json"
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            version = data.get("version", "unknown")
            print(f"CLI version from manifest: {version}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_kiro_version()