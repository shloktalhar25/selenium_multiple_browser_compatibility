# config.py

"""Configuration module for Browser Release Validation System.

Define constants for:
- Selenium Server URL
- Application URL to test
- Credentials for login
- Paths to driver executables if using local drivers (optional)
"""

# Selenium Server URL (default standalone)
SELENIUM_SERVER_URL = "http://localhost:4444"

# Application under test (OrangeHRM Demo Live Website)
APP_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

# Credentials for the OrangeHRM Demo site
USERNAME = "Admin"
PASSWORD = "admin123"


# Optional: paths to driver binaries if you prefer local drivers instead of remote.
# Leave empty to let Selenium Server manage drivers automatically in standalone mode.
CHROME_DRIVER_PATH = ""
FIREFOX_DRIVER_PATH = ""
EDGE_DRIVER_PATH = ""

# Headless mode toggle (True to hide browser windows, False to show them)
HEADLESS = False


