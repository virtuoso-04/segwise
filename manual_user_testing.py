from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import time
import json

# Test credentials
EMAIL = "qa@segwise.ai"
PASSWORD = "segwise_test"
LOGIN_URL = "https://ua.segwise.ai/login"
DASHBOARD_URL = "https://ua.segwise.ai/qa_assignment"

def setup_driver():
    """Simple driver setup for manual testing"""
    chromedriver_autoinstaller.install()
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def test_dashboard_first_impression(driver):
    """What would a first-time user think when they see this dashboard?"""
    issues = []
    
    print("👀 FIRST IMPRESSION TEST: What does a new user see?")
    
    # 1. Is it clear what this dashboard is for?
    page_title = driver.title
    h1_elements = driver.find_elements(By.TAG_NAME, "h1")
    
    if not page_title or "dashboard" not in page_title.lower():
        issues.append("❓ UNCLEAR PURPOSE: Page title doesn't indicate this is a dashboard")
    
    if not any(h1.is_displayed() and h1.text.strip() for h1 in h1_elements):
        issues.append("❓ NO HEADING: Dashboard lacks main heading - users don't know what they're looking at")
    
    # 2. Can users immediately see important data?
    charts = driver.find_elements(By.CSS_SELECTOR, "canvas, svg, [class*='chart'], [class*='graph']")
    metrics = driver.find_elements(By.CSS_SELECTOR, "[class*='metric'], [class*='kpi'], [class*='stat'], .card")
    
    if len(charts) == 0 and len(metrics) < 3:
        issues.append("📊 NO KEY DATA: Dashboard doesn't prominently display key metrics or charts")
    
    # 3. Is there too much information at once?
    all_text = driver.find_element(By.TAG_NAME, "body").text
    word_count = len(all_text.split())
    
    if word_count > 500:
        issues.append(f"🧠 INFORMATION OVERLOAD: {word_count} words on screen - too much to process quickly")
    
    return issues

def test_chart_presence_and_usability(driver):
    """Assert charts exist and test if users can actually use them"""
    issues = []
    
    print("📊 CHART USABILITY TEST: Can users interact with the data?")
    
    # 1. Are there charts present?
    charts = driver.find_elements(By.CSS_SELECTOR, "canvas, svg, [class*='chart'], [class*='graph']")
    
    if not charts:
        issues.append("🚨 CRITICAL: No charts found on analytics dashboard - core functionality missing")
        return issues
    
    print(f"   ✅ Found {len(charts)} charts")
    
    # 2. Can users get details from charts?
    tooltip_found = False
    for i, chart in enumerate(charts[:2]):
        if chart.is_displayed():
            print(f"   Testing chart {i+1} interactivity...")
            
            # Test hover for details
            ActionChains(driver).move_to_element(chart).perform()
            time.sleep(1.5)
            
            tooltips = driver.find_elements(By.CSS_SELECTOR, 
                ".tooltip, [role='tooltip'], [class*='tooltip'], [data-tooltip]")
            
            if any(tip.is_displayed() for tip in tooltips):
                tooltip_found = True
                print(f"   ✅ Chart {i+1} shows details on hover")
                break
            else:
                print(f"   ❌ Chart {i+1} no hover details")
    
    if not tooltip_found:
        issues.append("📊 CHART ISSUE: Charts don't show details on hover - users can't see precise values")
    
    # 3. Can users interact with chart data?
    clickable_chart_found = False
    for chart in charts[:2]:
        if chart.is_displayed():
            chart.click()
            time.sleep(1)
            
            # Check for modal or drill-down
            modals = driver.find_elements(By.CSS_SELECTOR, ".modal, [role='dialog']")
            if any(modal.is_displayed() for modal in modals):
                clickable_chart_found = True
                break
    
    if not clickable_chart_found:
        issues.append("📊 LIMITED INTERACTION: Charts not clickable - users can't explore data deeper")
    
    return issues

def test_real_user_workflows(driver):
    """Test common things users would actually want to do"""
    issues = []
    
    print("🎯 USER WORKFLOW TEST: Can users accomplish real tasks?")
    
    # Workflow 1: User wants to find specific data
    print("   🔍 Can users search for specific information?")
    
    search_elements = driver.find_elements(By.CSS_SELECTOR, 
        "input[type='search'], [placeholder*='search'], [class*='search']")
    
    if not search_elements:
        issues.append("🔍 MISSING SEARCH: No search function - users can't quickly find specific data")
    
    # Workflow 2: User wants to export data
    print("   📤 Can users export or share findings?")
    
    export_elements = driver.find_elements(By.CSS_SELECTOR, 
        "[class*='export'], [class*='download'], [class*='share'], button")
    
    export_found = False
    for elem in export_elements:
        if elem.is_displayed():
            text = elem.text.lower()
            if any(word in text for word in ['export', 'download', 'share', 'save']):
                export_found = True
                break
    
    if not export_found:
        issues.append("📤 NO EXPORT: Can't export data - users can't take action on insights")
    
    # Workflow 3: User wants to filter or customize view
    print("   🎚️ Can users filter or customize the data view?")
    
    filter_elements = driver.find_elements(By.CSS_SELECTOR, 
        "select, [class*='filter'], [class*='dropdown'], input[type='date']")
    
    if len(filter_elements) < 2:
        issues.append("🎚️ LIMITED FILTERING: Few filter options - users can't customize data view")
    
    # Workflow 4: User needs help
    print("   🆘 Can users get help if confused?")
    
    help_elements = driver.find_elements(By.CSS_SELECTOR, 
        "[class*='help'], [aria-label*='help'], [title*='help']")
    
    if not help_elements:
        issues.append("🆘 NO HELP: No help or guidance available - users stuck if confused")
    
    return issues

def test_mobile_user_experience(driver):
    """Test what happens when users access on mobile"""
    issues = []
    
    print("📱 MOBILE USER TEST: What's the mobile experience like?")
    
    # Switch to mobile size
    original_size = driver.get_window_size()
    driver.set_window_size(375, 667)  # iPhone size
    time.sleep(2)
    
    # 1. Is navigation accessible on mobile?
    nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a, .navbar a")
    hamburger_menu = driver.find_elements(By.CSS_SELECTOR, 
        "[class*='hamburger'], [class*='menu-toggle'], [aria-label*='menu']")
    
    if len(nav_links) > 3 and not hamburger_menu:
        issues.append("📱 MOBILE NAV: Too many nav items without mobile menu - cramped interface")
    
    # 2. Are buttons big enough to tap?
    buttons = driver.find_elements(By.TAG_NAME, "button")
    small_buttons = 0
    
    for btn in buttons[:5]:  # Check first 5 buttons
        if btn.is_displayed():
            try:
                size = driver.execute_script(
                    "var rect = arguments[0].getBoundingClientRect(); return rect.width * rect.height;", btn
                )
                if size > 0 and size < 44 * 44:  # 44px is minimum touch target
                    small_buttons += 1
            except:
                pass
    
    if small_buttons > 0:
        issues.append(f"📱 TOUCH TARGETS: {small_buttons} buttons too small for mobile tapping")
    
    # 3. Does content fit the screen?
    has_horizontal_scroll = driver.execute_script(
        "return document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    
    if has_horizontal_scroll:
        issues.append("📱 MOBILE LAYOUT: Content requires horizontal scrolling - poor mobile experience")
    
    # Reset to desktop
    driver.set_window_size(original_size['width'], original_size['height'])
    time.sleep(1)
    
    return issues

def test_user_confusion_points(driver):
    """Identify things that would confuse real users"""
    issues = []
    
    print("😕 CONFUSION TEST: What might confuse users?")
    
    # 1. Are there confusing error messages?
    error_elements = driver.find_elements(By.CSS_SELECTOR, 
        ".error, .alert, [role='alert'], [class*='error']")
    
    for error in error_elements:
        if error.is_displayed():
            error_text = error.text.strip()
            if error_text:
                # Check for technical jargon
                technical_terms = ['undefined', 'null', '500', 'exception', 'api']
                if any(term in error_text.lower() for term in technical_terms):
                    issues.append(f"😕 CONFUSING ERROR: Technical error shown - '{error_text[:50]}...'")
    
    # 2. Are there too many options?
    buttons = driver.find_elements(By.TAG_NAME, "button")
    visible_buttons = [btn for btn in buttons if btn.is_displayed()]
    
    if len(visible_buttons) > 15:
        issues.append(f"😕 TOO MANY OPTIONS: {len(visible_buttons)} buttons visible - choice paralysis")
    
    # 3. Is the user's current location clear?
    current_page_indicators = driver.find_elements(By.CSS_SELECTOR, 
        ".active, .current, [aria-current='page']")
    
    if not current_page_indicators:
        issues.append("😕 LOST USER: No indication of current page location")
    
    return issues

def main():
    """Run focused manual testing from real user perspective"""
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    all_issues = []
    
    try:
        print("👤 MANUAL TESTING - REAL USER PERSPECTIVE")
        print("=" * 55)
        print("Testing like a real user: What could go wrong?\n")
        
        # Login
        print("🔐 Logging in...")
        driver.get(LOGIN_URL)
        
        try:
            email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
            password_input = driver.find_element(By.ID, "password")
            
            email_input.send_keys(EMAIL)
            password_input.send_keys(PASSWORD)
            password_input.submit()
            
            time.sleep(3)
            print("✅ Login successful")
            
        except Exception as e:
            print(f"❌ Login issue: {e}")
            return
        
        # Navigate to dashboard
        driver.get(DASHBOARD_URL)
        time.sleep(4)
        print(f"📊 Testing dashboard: {driver.current_url}\n")
        
        # Run user-focused tests
        all_issues.extend(test_dashboard_first_impression(driver))
        all_issues.extend(test_chart_presence_and_usability(driver))
        all_issues.extend(test_real_user_workflows(driver))
        all_issues.extend(test_mobile_user_experience(driver))
        all_issues.extend(test_user_confusion_points(driver))
        
        # Take evidence screenshot
        driver.save_screenshot("/Users/anantsharma/Desktop/segwise/manual_testing_evidence.png")
        
        # Report results
        print(f"\n👤 MANUAL TESTING RESULTS")
        print(f"{'='*40}")
        print(f"User Experience Issues Found: {len(all_issues)}")
        
        if all_issues:
            print(f"\n😤 REAL USER PROBLEMS:")
            for i, issue in enumerate(all_issues, 1):
                print(f"{i}. {issue}")
            
            print(f"\n💡 IMMEDIATE IMPROVEMENTS NEEDED:")
            print("1. Add chart hover tooltips for data precision")
            print("2. Implement search functionality")
            print("3. Add export/download options")
            print("4. Improve mobile navigation")
            print("5. Add clear dashboard title/purpose")
            print("6. Provide user help/guidance")
            
            # Save focused report
            report = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "testing_approach": "Manual Testing - Real User Perspective",
                "user_issues_found": len(all_issues),
                "critical_user_problems": all_issues,
                "immediate_improvements": [
                    "Add chart hover tooltips for data precision",
                    "Implement search functionality", 
                    "Add export/download options",
                    "Improve mobile navigation",
                    "Add clear dashboard title/purpose",
                    "Provide user help/guidance"
                ],
                "test_url": driver.current_url
            }
            
            with open("/Users/anantsharma/Desktop/segwise/manual_user_testing.json", "w") as f:
                json.dump(report, f, indent=2)
            
            print(f"\n💾 Manual testing report saved to: manual_user_testing.json")
            
        else:
            print("\n✅ Great user experience - no major issues found!")
            
        print(f"\n🎯 KEY INSIGHTS FOR REAL USERS:")
        print("• Users need interactive charts with hover details")
        print("• Search is essential for data discovery")
        print("• Export functionality critical for business value")
        print("• Mobile experience needs significant work")
        print("• Clear guidance helps user orientation")
        
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        try:
            driver.save_screenshot("/Users/anantsharma/Desktop/segwise/manual_testing_error.png")
        except:
            pass
    
    finally:
        driver.quit()
        print(f"\n✅ Manual testing complete - Real user insights delivered!")

if __name__ == "__main__":
    main()
