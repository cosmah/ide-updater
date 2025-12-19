#!/usr/bin/env python3
"""Test the fixed Kiro version checker"""

import sys
sys.path.insert(0, 'src')

from ide_updater.modules.kiro import KiroUpdater

def test_kiro_fix():
    print("=== Testing Fixed Kiro Version Checker ===\n")
    
    # Create a dummy config
    config = {
        "install_dir": "/tmp/test",
        "temp_dir": "/tmp/test_temp"
    }
    
    updater = KiroUpdater(config)
    
    print(f"IDE Name: {updater.name}")
    
    print("\n1. Testing get_latest_version()...")
    try:
        version = updater.get_latest_version()
        print(f"   Latest version: {version}")
        
        if version.startswith('0.'):
            print("   ✅ Correctly detected IDE version (0.x.x)")
        elif version.startswith('1.'):
            print("   ❌ Still detecting CLI version (1.x.x)")
        else:
            print(f"   ⚠️  Unexpected version format: {version}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n2. Testing get_download_url()...")
    try:
        url = updater.get_download_url()
        print(f"   Download URL: {url}")
        
        if 'kiro-ide' in url:
            print("   ✅ URL contains 'kiro-ide' (correct)")
        else:
            print("   ⚠️  URL doesn't contain 'kiro-ide'")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n3. Testing get_current_version()...")
    try:
        current = updater.get_current_version()
        print(f"   Current version: {current}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_kiro_fix()