# test_app.py

"""Test Application Module for OrangeHRM.

Contains the Selenium test script steps that are executed on
each browser to validate the OrangeHRM demo application.
Uses explicit waits for high stability on Single Page Applications (SPAs).
"""

import time
import logging
# pyrefly: ignore [missing-import]
from selenium.webdriver.common.by import By
# pyrefly: ignore [missing-import]
from selenium.webdriver.support.ui import WebDriverWait
# pyrefly: ignore [missing-import]
from selenium.webdriver.support import expected_conditions as EC
import config

# Set up clean logging format
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] (%(threadName)s) %(message)s")

def run_test(driver, browser_name):
    """Executes the test flow on the provided webdriver instance.
    
    Workflow:
    1. Navigate to OrangeHRM target login URL
    2. Input username & password (Admin / admin123)
    3. Click login
    4. Verify dashboard header loads successfully
    5. Perform a business action: navigate to "My Info" section
    6. Click user profile dropdown and log out cleanly
    
    Args:
        driver: The remote webdriver instance.
        browser_name: Name of the browser (for logging).
        
    Returns:
        dict: {"success": True/False, "message": "Result description"}
    """
    # Increased wait timeout to 15 seconds to handle OrangeHRM loading speeds
    wait = WebDriverWait(driver, 15)
    
    try:
        logging.info(f"[{browser_name.upper()}] Step 1: Navigating to {config.APP_URL}...")
        driver.get(config.APP_URL)
        
        # 2. Enter credentials (wait for the SPA page to finish loading)
        logging.info(f"[{browser_name.upper()}] Step 2: Entering OrangeHRM credentials...")
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.clear()
        username_field.send_keys(config.USERNAME)
        password_field.clear()
        password_field.send_keys(config.PASSWORD)
        
        # 3. Click Login
        logging.info(f"[{browser_name.upper()}] Step 3: Clicking Login...")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # 4. Validate login succeeded (checking OrangeHRM dashboard topbar)
        logging.info(f"[{browser_name.upper()}] Step 4: Validating Dashboard breadcrumb...")
        breadcrumb_module = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb-module"))
        )
        
        if "Dashboard" not in breadcrumb_module.text:
            raise AssertionError(f"Expected 'Dashboard' breadcrumb but got: '{breadcrumb_module.text}'")
            
        logging.info(f"[{browser_name.upper()}] SUCCESS: Logged in and verified Dashboard module!")
        
        # 5. Perform business action: Navigate to "My Info" menu item on the left panel
        logging.info(f"[{browser_name.upper()}] Step 5: Navigating to 'My Info' left-panel page...")
        my_info_menu = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='viewMyDetails']"))
        )
        my_info_menu.click()
        
        # Wait until the Personal Details container form is visible
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".orangehrm-edit-employee"))
        )
        logging.info(f"[{browser_name.upper()}] SUCCESS: Loaded PIM/My Details profile page successfully.")
        
        time.sleep(2)  # Short sleep for visual feedback during parallel runs
        
        # 6. Click Profile Dropdown and Logout
        logging.info(f"[{browser_name.upper()}] Step 6: Opening Profile Dropdown...")
        profile_dropdown = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-userdropdown-tab"))
        )
        profile_dropdown.click()
        
        logging.info(f"[{browser_name.upper()}] Step 7: Clicking Logout link...")
        logout_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='logout']"))
        )
        logout_link.click()
        
        # Confirm logout redirected back to the login page successfully
        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        logging.info(f"[{browser_name.upper()}] SUCCESS: Logged out successfully and returned to login screen.")
        
        return {"success": True, "message": "All steps passed successfully."}
        
    except Exception as e:
        error_msg = f"Test failed: {str(e)}"
        logging.error(f"[{browser_name.upper()}] ERROR: {error_msg}")
        return {"success": False, "message": error_msg}

