
# Main Entry Point.

# Orchestrates the entire Browser Release Validation workflow:
# 1. Detect installed browser versions.
# 2. Identify which browsers have changed/updated since the last run.
# 3. If changes are detected (or if it's the first run), run parallel tests via Selenium Server.
# 4. Save results to results/report.txt and update stored_versions.json.


import os
import datetime
import version_checker
import browser_runner

REPORT_DIR = "results"
REPORT_FILE = os.path.join(REPORT_DIR, "report.txt")

def ensure_report_directory():
    """Ensure the results directory exists."""
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

def write_report(results, installed_versions):
    """Generate and write a beautiful plain-text report of the execution results."""
    ensure_report_directory()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = [
        " ",
        "      BROWSER RELEASE VALIDATION REPORT           ",
        f"      Executed At: {timestamp}                   ",
        "",
        "Installed Browser Versions Under Test:",
        f"  - Chrome:  {installed_versions.get('chrome', 'Not Found')}",
        f"  - Firefox: {installed_versions.get('firefox', 'Not Found')}",
        f"  - Edge:    {installed_versions.get('edge', 'Not Found')}\n",
        "Test Results Summary:",
        "--------------------------------------------------"
    ]
    
    all_passed = True
    for browser, res in results.items():
        status = "PASS" if res.get("success") else "FAIL"
        if not res.get("success"):
            all_passed = False
        report_lines.append(f"  {browser.upper():<10} -> {status:<6} | Details: {res.get('message')}")
        
    report_lines.append("--------------------------------------------------")
    overall = "SUCCESS: All tested browsers passed!" if all_passed else "WARNING: Some browser tests failed!"
    report_lines.append(overall)
    report_lines.append("==================================================\n")
    
    # Write to file
    with open(REPORT_FILE, "a") as f:
        f.write("\n".join(report_lines) + "\n")
        
    # Also print to terminal for immediate feedback
    print("\n" + "\n".join(report_lines))

def main():
    print("==================================================")
    print("      Starting Browser Release Validation System   ")
    print("==================================================")
    
    # 1. Check for browser version updates
    changed_browsers, installed = version_checker.check_for_browser_updates()
    
    if not changed_browsers:
        print("\n[INFO] No browser updates detected since the last run.")
        print("[INFO] All browser versions match stored records. Exiting.")
        return
        
    print(f"\n[TRIGGER] Detected updates/changes in: {', '.join([b.upper() for b in changed_browsers])}")
    print("[TRIGGER] Launching parallel verification tests on all updated browsers...")
    
    # 2. Run parallel Selenium Server Remote tests
    results = browser_runner.run_parallel_tests(changed_browsers)
    
    # 3. Generate Report
    write_report(results, installed)
    
    # 4. If all tests on updated browsers passed, update stored versions
    all_passed = all(res.get("success") for res in results.values())
    if all_passed:
        print("\n[SUCCESS] All updated browser validation tests passed. Saving new versions.")
        version_checker.save_stored_versions(installed)
    else:
        print("\n[ALERT] Some tests failed. Stored versions not updated to trigger re-test next run.")

if __name__ == "__main__":
    main()
