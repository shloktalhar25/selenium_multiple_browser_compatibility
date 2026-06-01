# Browser Runner Module.

# Initializes Selenium Remote webdrivers for requested browsers and executes
# tests in parallel using threading.


import threading
import logging
# pyrefly: ignore [missing-import]
from selenium import webdriver
# pyrefly: ignore [missing-import]
from selenium.webdriver.chrome.options import Options as ChromeOptions
# pyrefly: ignore [missing-import]
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# pyrefly: ignore [missing-import]
from selenium.webdriver.edge.options import Options as EdgeOptions
import config
import test_app

def get_browser_options(browser_name):
    """Retrieve webdriver options customized for the requested browser."""
    name = browser_name.lower()
    if name == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if config.HEADLESS:
            options.add_argument("--headless=new")
        return options
    elif name == "firefox":
        options = FirefoxOptions()
        if config.HEADLESS:
            options.add_argument("--headless")
        return options
    elif name == "edge":
        options = EdgeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if config.HEADLESS:
            options.add_argument("--headless=new")
        return options
    else:
        raise ValueError(f"Unsupported browser type: {browser_name}")


def execute_single_browser_test(browser_name, results):
    """Worker function to initialize driver, run the test flow, and cleanup."""
    logging.info(f"Starting test worker thread for {browser_name.upper()}...")
    driver = None
    try:
        options = get_browser_options(browser_name)
        
        # Connect to Selenium Server Standalone (Remote Mode)
        driver = webdriver.Remote(
            command_executor=config.SELENIUM_SERVER_URL,
            options=options
        )
        
        # Run the test flow
        result = test_app.run_test(driver, browser_name)
        results[browser_name] = result
        
    except Exception as e:
        error_msg = f"Failed to initialize remote connection to Selenium Server: {str(e)}"
        logging.error(f"[{browser_name.upper()}] Setup Error: {error_msg}")
        results[browser_name] = {"success": False, "message": error_msg}
        
    finally:
        if driver:
            try:
                logging.info(f"[{browser_name.upper()}] Closing driver...")
                driver.quit()
            except Exception as e:
                logging.warning(f"[{browser_name.upper()}] Exception while quitting driver: {e}")

def run_parallel_tests(browsers):
    """Runs functional tests in parallel across a list of browsers.
    
    Args:
        browsers (list): List of browser names to test, e.g. ["chrome", "firefox", "edge"]
        
    Returns:
        dict: Summary of results per browser.
    """
    threads = []
    results = {}
    
    for browser in browsers:
        # Create a dedicated thread for each browser to support parallel runs
        thread = threading.Thread(
            target=execute_single_browser_test,
            args=(browser, results),
            name=f"Thread-{browser.capitalize()}"
        )
        threads.append(thread)
        thread.start()
        
    # Wait for all test threads to complete execution
    for thread in threads:
        thread.join()
        
    return results
