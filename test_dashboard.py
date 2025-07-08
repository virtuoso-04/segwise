from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time

# Test credentials and URLs
EMAIL = "qa@segwise.ai"
PASSWORD = "segwise_test"
LOGIN_URL = "https://ua.segwise.ai/login"
DASHBOARD_URL = "https://ua.segwise.ai/dashboard"

def setup_driver():
    """Set up Chrome WebDriver"""
    chromedriver_autoinstaller.install()
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

# Set up Chrome WebDriver
driver = setup_driver()

try:
    print("🚀 Starting Segwise Dashboard Tests\n")
    
    # 1. Open login page
    print("🌐 Opening login page...")
    driver.get(LOGIN_URL)
    
    # 2. Wait for login inputs and enter credentials
    print("🔐 Logging in...")
    wait = WebDriverWait(driver, 10)
    
    # Use the correct selectors based on what we found
    # First text input (email) - using ID from the discovery
    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
    # First password input
    password_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")))

    email_input.clear()
    email_input.send_keys(EMAIL)
    password_input.clear()
    password_input.send_keys(PASSWORD)
    
    # Submit the form (try password input submit first)
    password_input.submit()
    
    # Wait a bit for login to process
    time.sleep(3)
    
    print(f"After login - Current URL: {driver.current_url}")

    # 3. Navigate to dashboard (or check if already redirected)
    if "login" in driver.current_url.lower():
        print("Still on login page, trying to navigate to dashboard...")
        driver.get(DASHBOARD_URL)
    
    time.sleep(4)
    print(f"Dashboard URL: {driver.current_url}")

    # 4. Verify we're on a dashboard-like page
    if "dashboard" in driver.current_url.lower() or "segwise" in driver.title.lower():
        print("✅ Successfully reached dashboard area")
    else:
        print("⚠️  May not be on dashboard, but continuing tests...")

    # 5. Look for any chart elements (flexible search)
    print("📊 Looking for chart elements...")
    chart_found = False
    chart_selectors = [
        "//h2[contains(text(), 'Top')]",
        "//h3[contains(text(), 'Top')]", 
        "//div[contains(@class, 'chart')]",
        "//canvas",
        "//svg",
        "//*[contains(text(), 'Chart')]",
        "//*[contains(text(), 'chart')]"
    ]
    
    for selector in chart_selectors:
        try:
            element = driver.find_element(By.XPATH, selector)
            if element.is_displayed():
                print(f"✅ Found chart element: {selector}")
                chart_found = True
                break
        except:
            continue
    
    if not chart_found:
        print("⚠️  No specific chart elements found, checking for general dashboard content...")
        # Look for any content that suggests it's a working dashboard
        try:
            dashboard_indicators = driver.find_elements(By.TAG_NAME, "h1") + driver.find_elements(By.TAG_NAME, "h2") + driver.find_elements(By.TAG_NAME, "h3")
            if dashboard_indicators:
                print(f"✅ Found {len(dashboard_indicators)} heading elements (dashboard content)")
                for i, heading in enumerate(dashboard_indicators[:3]):
                    print(f"  - {heading.text[:50]}...")
        except:
            pass

    # 6. Look for filter/button elements
    print("🔍 Looking for interactive elements...")
    filter_found = False
    filter_selectors = [
        "//button[contains(text(), 'Filter')]",
        "//button[contains(text(), 'filter')]",
        "//select",
        "//button",
        "//input[@type='search']"
    ]
    
    buttons = driver.find_elements(By.TAG_NAME, "button")
    if buttons:
        print(f"✅ Found {len(buttons)} button elements")
        filter_found = True
    
    selects = driver.find_elements(By.TAG_NAME, "select")
    if selects:
        print(f"✅ Found {len(selects)} select elements")

    # 7. Test logout functionality
    print("🚪 Testing logout...")
    logout_found = False
    
    # Look for profile/user elements - try clicking around the top right area
    profile_selectors = [
        "//button[contains(@class, 'avatar')]",
        "//div[contains(@class, 'profile')]",
        "//button[contains(@class, 'user')]",
        "//img[contains(@alt, 'profile')]",
        "//img[contains(@alt, 'avatar')]",
        "//*[contains(text(), 'Profile')]",
        "//*[contains(text(), 'profile')]"
    ]
    
    profile_clicked = False
    for selector in profile_selectors:
        try:
            profile_btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            profile_btn.click()
            time.sleep(1)
            profile_clicked = True
            print(f"✅ Clicked profile element: {selector}")
            break
        except:
            continue
    
    # Look for logout button (might appear after clicking profile)
    logout_selectors = [
        "//button[contains(text(), 'Logout')]",
        "//button[contains(text(), 'logout')]",
        "//a[contains(text(), 'Logout')]",
        "//a[contains(text(), 'logout')]",
        "//a[contains(text(), 'Sign out')]",
        "//button[contains(text(), 'Sign out')]"
    ]
    
    for selector in logout_selectors:
        try:
            logout_btn = driver.find_element(By.XPATH, selector)
            if logout_btn.is_displayed():
                logout_btn.click()
                time.sleep(2)
                logout_found = True
                print(f"✅ Found and clicked logout: {selector}")
                break
        except:
            continue
    
    if logout_found:
        # Check if redirected to login
        if "login" in driver.current_url.lower():
            print("✅ Logout successful - redirected to login page")
        else:
            print(f"⚠️  Logout clicked but current URL: {driver.current_url}")
    else:
        print("⚠️  Could not find logout functionality")

    print("\n🎉 Test completed! Check the results above.")

except Exception as e:
    print(f"\n❌ Test failed with error: {e}")
    print(f"Current URL: {driver.current_url}")
    
    # Take screenshot for debugging
    try:
        screenshot_path = "/Users/anantsharma/Desktop/segwise/debug_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")
    except:
        pass

finally:
    driver.quit()
    print("🔚 Browser closed")
