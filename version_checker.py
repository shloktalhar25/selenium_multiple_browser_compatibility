# version_checker.py

"""Version Checker Module.

Detects current installed versions of Chrome, Firefox, and Edge on Windows,
compares them with last saved versions in stored_versions.json,
and determines if tests need to run.
"""

import os
import json
import subprocess
import shutil

# Standard installation paths for browsers on Windows
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

FIREFOX_PATHS = [
    r"C:\Program Files\Mozilla Firefox\firefox.exe",
    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
]

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

VERSION_FILE = "stored_versions.json"

def get_executable_version(file_path):
    """Retrieve the product version of an executable on Windows using PowerShell."""
    if not file_path or not os.path.exists(file_path):
        return None
    try:
        # PowerShell command to extract the exact file version info
        cmd = f"(Get-Item '{file_path}').VersionInfo.ProductVersion"
        output = subprocess.check_output(["powershell", "-Command", cmd], text=True).strip()
        if output:
            return output
    except Exception as e:
        print(f"Error checking version for {file_path}: {e}")
    return None

def find_browser_executable(paths):
    """Find the first existing browser executable from a list of standard paths."""
    for path in paths:
        if os.path.exists(path):
            return path
    return None

def get_installed_versions():
    """Retrieve current installed versions of all 3 browsers."""
    versions = {}
    
    # 1. Chrome
    chrome_exe = find_browser_executable(CHROME_PATHS)
    if chrome_exe:
        versions["chrome"] = get_executable_version(chrome_exe)
    else:
        versions["chrome"] = "Not Found"
        
    # 2. Firefox
    firefox_exe = find_browser_executable(FIREFOX_PATHS)
    if firefox_exe:
        versions["firefox"] = get_executable_version(firefox_exe)
    else:
        versions["firefox"] = "Not Found"
        
    # 3. Edge
    edge_exe = find_browser_executable(EDGE_PATHS)
    if edge_exe:
        versions["edge"] = get_executable_version(edge_exe)
    else:
        versions["edge"] = "Not Found"
        
    return versions

def load_stored_versions():
    """Load previously stored browser versions from stored_versions.json."""
    if not os.path.exists(VERSION_FILE):
        return {}
    try:
        with open(VERSION_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading stored versions: {e}")
        return {}

def save_stored_versions(versions):
    """Save current browser versions to stored_versions.json."""
    try:
        with open(VERSION_FILE, "w") as f:
            json.dump(versions, f, indent=2)
    except Exception as e:
        print(f"Error saving versions: {e}")

def check_for_browser_updates():
    """Compare installed versions with stored versions.
    
    Returns:
        tuple: (changed_browsers, installed_versions)
            changed_browsers: List of browser names that were updated/changed
            installed_versions: Dict of current installed versions
    """
    installed = get_installed_versions()
    stored = load_stored_versions()
    
    changed = []
    print("\n--- Browser Version Check ---")
    for browser in ["chrome", "firefox", "edge"]:
        inst_ver = installed.get(browser)
        stor_ver = stored.get(browser)
        
        print(f"{browser.capitalize()}: Installed = {inst_ver} | Stored = {stor_ver}")
        
        if inst_ver != "Not Found":
            # If the version changed or was never recorded, mark it as changed
            if inst_ver != stor_ver:
                changed.append(browser)
                
    return changed, installed

if __name__ == "__main__":
    changed, installed = check_for_browser_updates()
    print(f"\nChanged browsers: {changed}")
    # Update stored versions
    save_stored_versions(installed)
