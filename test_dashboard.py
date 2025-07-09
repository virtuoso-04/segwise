#!/usr/bin/env python3
"""
Segwise Dashboard Test Script
============================

Automation Task (Basic) - Assignment Requirements:
- Opens a login page
- Logs in with test credentials  
- Navigates to a dashboard
- Asserts presence of a specific chart or metric

Requirements: pip install selenium chromedriver-autoinstaller
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time

# Test Configuration
EMAIL = "qa@segwise.ai"
PASSWORD = "segwise_test"
BASE_URL = "https://ua.segwise.ai"

def setup_driver():
    """Initialize Chrome WebDriver with basic settings"""
    chromedriver_autoinstaller.install()
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def test_login(driver):
    """Test 1: Login functionality"""
    print("Testing Login...")
    
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 10)
    
    # Find and fill login form
    email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    
    email_input.clear()
    email_input.send_keys(EMAIL)
    password_input.clear()
    password_input.send_keys(PASSWORD)
    
    # Submit login
    password_input.submit()
    time.sleep(3)
    
    # Verify login success
    if "login" not in driver.current_url.lower():
        print("PASS: Login successful")
        return True
    else:
        print("FAIL: Login failed")
        return False

def test_dashboard_loading(driver):
    """Test 2: Dashboard page loading"""
    print("Testing Dashboard Loading...")
    
    driver.get(f"{BASE_URL}/qa_assignment")
    time.sleep(3)
    
    page_title = driver.title
    print(f"Page title: {page_title}")
    
    if page_title and "segwise" in page_title.lower():
        print("PASS: Dashboard loaded successfully")
        return True
    else:
        print("WARNING: Dashboard may not have loaded correctly")
        return False

def test_chart_presence(driver):
    """Test 3: Chart elements presence"""
    print("Testing Chart Presence...")
    
    # Look for chart elements
    charts = driver.find_elements(By.CSS_SELECTOR, "canvas, svg, [class*='chart']")
    headings = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3")
    
    print(f"Found {len(charts)} chart elements")
    print(f"Found {len(headings)} heading elements")
    
    if len(charts) > 0:
        print("PASS: Charts detected on dashboard")
        return True
    else:
        print("WARNING: No chart elements found")
        return False

def test_chart_interaction(driver):
    """Test 4: Chart interactivity (tooltip test)"""
    print("Testing Chart Interaction...")
    
    charts = driver.find_elements(By.CSS_SELECTOR, "canvas, svg")
    
    if charts:
        try:
            # Try to hover over first chart
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(driver).move_to_element(charts[0]).perform()
            time.sleep(2)
            
            # Check if any tooltip or popup appeared
            tooltips = driver.find_elements(By.CSS_SELECTOR, "[class*='tooltip'], [class*='popup']")
            
            if tooltips:
                print("PASS: Chart interaction working - tooltip detected")
                return True
            else:
                print("WARNING: No tooltips detected on chart hover")
                return False
                
        except Exception as e:
            print(f"WARNING: Chart interaction test failed: {e}")
            return False
    else:
        print("WARNING: No charts available for interaction testing")
        return False

def test_navigation(driver):
    """Test 5: Basic navigation functionality"""
    print("Testing Navigation...")
    
    # Look for navigation elements
    nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a, [role='navigation'] a")
    buttons = driver.find_elements(By.TAG_NAME, "button")
    
    print(f"Found {len(nav_links)} navigation links")
    print(f"Found {len(buttons)} interactive buttons")
    
    if len(nav_links) > 0 or len(buttons) > 0:
        print("PASS: Navigation elements present")
        return True
    else:
        print("WARNING: Limited navigation elements found")
        return False

def run_tests():
    """Main test runner"""
    print("Starting Segwise Dashboard Tests")
    print("=" * 50)
    
    driver = setup_driver()
    test_results = []
    
    try:
        # Run all tests
        test_results.append(("Login", test_login(driver)))
        test_results.append(("Dashboard Loading", test_dashboard_loading(driver)))
        test_results.append(("Chart Presence", test_chart_presence(driver)))
        test_results.append(("Chart Interaction", test_chart_interaction(driver)))
        test_results.append(("Navigation", test_navigation(driver)))
        
        # Print summary
        print("\n" + "=" * 50)
        print("TEST SUMMARY:")
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "PASS" if result else "FAIL"
            print(f"{test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\nResults: {passed}/{total} tests passed")
        
        if passed == total:
            print("All tests passed!")
        elif passed >= total * 0.7:
            print("Most tests passed - minor issues detected")
        else:
            print("Multiple test failures - investigation needed")
            
    except Exception as e:
        print(f"Test suite failed: {e}")
        
        # Save screenshot for debugging
        try:
            driver.save_screenshot("test_failure_screenshot.png")
            print("Screenshot saved: test_failure_screenshot.png")
        except:
            pass
            
    finally:
        driver.quit()
        print("Test completed - browser closed")

if __name__ == "__main__":
    run_tests()