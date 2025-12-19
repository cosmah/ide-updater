import requests
import re

def check_cursor():
    # User provided: https://cursor.com/download
    # But usually downloaders are direct. Let's check the main download endpoint often typical for these sites.
    # Often it is https://downloader.cursor.com/linux/appImage/x64 like VS Code.
    # Let's try to fetch the page provided by user to see if it has a link.
    url = "https://cursor.com/download"
    print(f"Checking Cursor: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        
        # Look for direct download links in the HTML
        # e.g. https://downloader.cursor.com/...
        matches = re.findall(r'https://[^"]*cursor[^"]*\.AppImage', r.text, re.IGNORECASE)
        if matches:
            print("Found AppImage links:", matches[:2])
        
        # Also let's try the direct downloader link again with .com
        direct_url = "https://downloader.cursor.com/linux/appImage/x64"
        print(f"Checking direct: {direct_url}")
        r2 = requests.head(direct_url, allow_redirects=True, headers=headers, timeout=5)
        print(f"Direct Status: {r2.status_code}")
        print(f"Direct Final URL: {r2.url}")
        if r2.status_code == 200:
             print("Headers:", r2.headers)

    except Exception as e:
        print(f"Cursor Error: {e}")

def check_kiro():
    url = "https://kiro.dev/downloads/"
    print(f"\nChecking Kiro: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        
        # Look for AppImage link
        # Extract <a href="..."> that contains .AppImage
        matches = re.findall(r'href="([^"]*\.AppImage)"', r.text, re.IGNORECASE)
        if matches:
            print(f"Found Kiro AppImages: {matches}")
        
        # Look for version text
        # e.g. "Version 0.1.0" or "v0.1.0"
        v_matches = re.findall(r'v?(\d+\.\d+\.\d+)', r.text)
        if v_matches:
            print(f"Possible versions: {v_matches[:3]}")

    except Exception as e:
        print(f"Kiro Error: {e}")

if __name__ == "__main__":
    check_cursor()
    check_kiro()
