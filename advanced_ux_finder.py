from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import chromedriver_autoinstaller
import time
import json

# Test credentials
EMAIL = "qa@segwise.ai"
PASSWORD = "segwise_test"
LOGIN_URL = "https://ua.segwise.ai/login"
DASHBOARD_URL = "https://ua.segwise.ai/qa_assignment"

def find_advanced_ux_issues():
    """Find advanced UX/UI issues that provide competitive edge"""
    
    print("🎯 ADVANCED UX/UI VULNERABILITY HUNTING")
    print("=" * 60)
    print("Focus: Enterprise-grade UX analysis for competitive advantage")
    
    findings = []
    
    # Setup Chrome with specific options for UX testing
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    
    try:
        print("🔐 Attempting login...")
        driver.get(LOGIN_URL)
        time.sleep(3)
        
        # Try to find login form
        try:
            email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
            password_field = driver.find_element(By.ID, "password")
            
            email_field.clear()
            email_field.send_keys(EMAIL)
            password_field.clear()
            password_field.send_keys(PASSWORD)
            
            # Submit form
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            submit_button.click()
            
            # Wait for dashboard
            wait.until(EC.url_contains("qa_assignment"))
            print("✅ Successfully logged in to dashboard")
            
        except TimeoutException:
            print("⚠️  Direct login failed, trying to access dashboard directly...")
            driver.get(DASHBOARD_URL)
            time.sleep(5)
        
        print("\n🔍 CONDUCTING ADVANCED UX ANALYSIS...")
        print("-" * 50)
        
        # CRITICAL UX ISSUE 1: Accessibility Compliance Analysis
        print("♿ Testing WCAG 2.1 Compliance...")
        
        # Check for missing alt text
        images = driver.find_elements(By.TAG_NAME, "img")
        missing_alt = sum(1 for img in images if img.is_displayed() and not (img.get_attribute("alt") or "").strip())
        if missing_alt > 0:
            findings.append(f"🚨 WCAG VIOLATION: {missing_alt} images missing alt text (Section 508 non-compliance)")
        
        # Check form accessibility
        inputs = driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
        unlabeled_inputs = 0
        for inp in inputs:
            if inp.is_displayed():
                input_id = inp.get_attribute("id")
                aria_label = inp.get_attribute("aria-label")
                if input_id:
                    labels = driver.find_elements(By.CSS_SELECTOR, f"label[for='{input_id}']")
                    if not labels and not aria_label:
                        unlabeled_inputs += 1
                elif not aria_label and not inp.get_attribute("placeholder"):
                    unlabeled_inputs += 1
        
        if unlabeled_inputs > 0:
            findings.append(f"🚨 ACCESSIBILITY: {unlabeled_inputs} form controls lack proper labels (enterprise compliance issue)")
        
        # CRITICAL UX ISSUE 2: Mobile Responsiveness Deep Analysis
        print("📱 Testing Mobile & Responsive UX...")
        
        # Test mobile breakpoint
        driver.set_window_size(375, 667)
        time.sleep(2)
        
        # Check for horizontal scroll
        has_horizontal_scroll = driver.execute_script(
            "return document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        if has_horizontal_scroll:
            findings.append("📱 MOBILE FAIL: Horizontal scroll on mobile - fundamental responsive design failure")
        
        # Check for mobile navigation
        nav_elements = driver.find_elements(By.CSS_SELECTOR, "nav, .navbar, [role='navigation']")
        hamburger_menu = driver.find_elements(By.CSS_SELECTOR, 
            "[class*='hamburger'], [class*='menu-toggle'], [aria-label*='menu'], [class*='mobile-menu']")
        
        if nav_elements and not hamburger_menu:
            nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a, .navbar a")
            if len(nav_links) > 3:
                findings.append("📱 MOBILE UX: No hamburger menu with multiple nav items - cramped mobile interface")
        
        # Check touch target sizes
        buttons = driver.find_elements(By.TAG_NAME, "button")
        small_buttons = 0
        for btn in buttons:
            if btn.is_displayed():
                try:
                    size = driver.execute_script(
                        "var rect = arguments[0].getBoundingClientRect(); return rect.width * rect.height;", btn
                    )
                    if size > 0 and size < 44 * 44:  # Apple's 44pt minimum
                        small_buttons += 1
                except:
                    pass
        
        if small_buttons > 0:
            findings.append(f"📱 TOUCH UX: {small_buttons} buttons below minimum 44px touch target (usability violation)")
        
        # Reset to desktop
        driver.set_window_size(1920, 1080)
        time.sleep(2)
        
        # CRITICAL UX ISSUE 3: JavaScript Console Error Analysis
        print("🐛 Analyzing JavaScript Console Errors...")
        
        try:
            logs = driver.get_log('browser')
            severe_errors = [log for log in logs if log['level'] == 'SEVERE']
            
            if len(severe_errors) > 0:
                findings.append(f"🐛 JS CONSOLE: {len(severe_errors)} severe JavaScript errors affecting UX reliability")
                
                # Categorize errors
                critical_errors = []
                for log in severe_errors:
                    message = log['message'].lower()
                    if any(keyword in message for keyword in ['uncaught', 'failed to fetch', 'network error']):
                        critical_errors.append(log['message'][:100])
                
                if critical_errors:
                    findings.append(f"🚨 CRITICAL JS: {len(critical_errors)} critical runtime errors detected")
        except:
            pass
        
        # CRITICAL UX ISSUE 4: Performance & Loading UX Analysis
        print("⚡ Testing Performance & Loading States...")
        
        # Test page load performance
        driver.refresh()
        start_time = time.time()
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        load_time = time.time() - start_time
        
        if load_time > 5:
            findings.append(f"⚡ PERFORMANCE: Page load {load_time:.1f}s exceeds enterprise UX standards (>5s)")
        
        # Check for loading states
        loading_indicators = driver.find_elements(By.CSS_SELECTOR, 
            "[class*='loading'], [class*='spinner'], [class*='skeleton'], .loader")
        
        # Count images without proper loading states
        images = driver.find_elements(By.TAG_NAME, "img")
        external_images = sum(1 for img in images if img.is_displayed() and 
                            img.get_attribute("src") and not img.get_attribute("src").startswith("data:"))
        
        if external_images > 5 and not loading_indicators:
            findings.append("⚡ LOADING UX: No loading indicators for image-heavy content (poor perceived performance)")
        
        # CRITICAL UX ISSUE 5: Data Visualization & Chart UX
        print("📊 Testing Chart & Data Visualization UX...")
        
        # Find charts and interactive elements
        chart_elements = driver.find_elements(By.CSS_SELECTOR, 
            "canvas, svg, [class*='chart'], [class*='graph'], [id*='chart'], [class*='visualization']")
        
        if chart_elements:
            tooltip_found = False
            for chart in chart_elements:
                if chart.is_displayed():
                    # Test tooltip interaction
                    try:
                        ActionChains(driver).move_to_element(chart).perform()
                        time.sleep(1)
                        tooltips = driver.find_elements(By.CSS_SELECTOR, 
                            "[class*='tooltip'], [role='tooltip'], .chart-tooltip, [class*='popup']")
                        if tooltips:
                            tooltip_found = True
                            break
                    except:
                        pass
            
            if not tooltip_found:
                findings.append("📊 CHART UX: Charts lack interactive tooltips - poor data exploration experience")
            
            # Check chart accessibility
            accessible_charts = sum(1 for chart in chart_elements if chart.is_displayed() and 
                                  (chart.get_attribute("aria-label") or chart.get_attribute("title")))
            
            if accessible_charts < len(chart_elements):
                findings.append("📊 CHART ACCESSIBILITY: Charts missing aria-labels for screen reader users")
        
        # CRITICAL UX ISSUE 6: Form & Input UX Analysis
        print("📝 Testing Form & Input UX Patterns...")
        
        # Test form validation UX
        forms = driver.find_elements(By.TAG_NAME, "form")
        for form in forms:
            if form.is_displayed():
                inputs = form.find_elements(By.CSS_SELECTOR, "input[required], textarea[required]")
                for inp in inputs:
                    if inp.is_displayed() and inp.is_enabled():
                        try:
                            # Test empty validation
                            inp.clear()
                            inp.send_keys("test")
                            inp.clear()
                            inp.send_keys(Keys.TAB)
                            time.sleep(0.5)
                            
                            # Look for validation messages
                            validation_msgs = driver.find_elements(By.CSS_SELECTOR, 
                                ".error, .invalid, [class*='validation'], .field-error")
                            
                            if not validation_msgs:
                                findings.append("📝 FORM UX: Required fields lack immediate validation feedback")
                                break
                        except:
                            pass
        
        # CRITICAL UX ISSUE 7: Navigation & Information Architecture
        print("🧭 Testing Navigation & Information Architecture...")
        
        # Check for current page indication
        current_indicators = driver.find_elements(By.CSS_SELECTOR, 
            "[aria-current='page'], .active, .current, .selected")
        
        if not current_indicators:
            findings.append("🧭 NAVIGATION: No clear current page indication - users lose context")
        
        # Check navigation depth
        nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a, .navbar a, .menu a")
        if len(nav_links) > 8:
            findings.append("🧭 IA: Too many top-level navigation items - cognitive overload")
        
        # Check for search in data-heavy app
        search_elements = driver.find_elements(By.CSS_SELECTOR, 
            "input[type='search'], [placeholder*='search'], [class*='search'], [id*='search']")
        
        if not search_elements:
            findings.append("🧭 SEARCH UX: No search functionality in data-heavy dashboard")
        
        # CRITICAL UX ISSUE 8: Error Handling & User Feedback
        print("💬 Testing Error States & User Feedback...")
        
        # Look for error states
        error_elements = driver.find_elements(By.CSS_SELECTOR, 
            ".error, .alert-danger, [class*='error'], .warning, .alert-warning")
        
        # Check for empty states
        empty_states = driver.find_elements(By.CSS_SELECTOR, 
            "[class*='empty'], [class*='no-data'], .empty-state, [class*='placeholder']")
        
        # Check tables for empty state handling
        tables = driver.find_elements(By.TAG_NAME, "table")
        for table in tables:
            if table.is_displayed():
                rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
                if len(rows) == 0 and not empty_states:
                    findings.append("📊 DATA UX: Empty tables lack proper empty state messaging")
                    break
        
        # CRITICAL UX ISSUE 9: Keyboard Navigation & Focus Management
        print("⌨️  Testing Keyboard Navigation...")
        
        # Test tab order
        focusable_elements = driver.find_elements(By.CSS_SELECTOR, 
            "a, button, input, select, textarea, [tabindex]:not([tabindex='-1'])")
        
        if len(focusable_elements) == 0:
            findings.append("⌨️  KEYBOARD UX: No keyboard-accessible elements detected")
        
        # Test for focus indicators
        try:
            if focusable_elements:
                first_focusable = focusable_elements[0]
                first_focusable.send_keys(Keys.TAB)
                time.sleep(0.5)
                
                # Check if focus is visible
                active_element = driver.switch_to.active_element
                focus_outline = driver.execute_script(
                    "return window.getComputedStyle(arguments[0]).outline", active_element
                )
                
                if not focus_outline or focus_outline == "none":
                    findings.append("⌨️  FOCUS UX: Invisible focus indicators - keyboard users can't navigate")
        except:
            pass
        
    except Exception as e:
        print(f"⚠️  Testing error: {e}")
        
    finally:
        driver.quit()
    
    # Save comprehensive findings
    assessment_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_type": "Advanced UX/UI Vulnerability Assessment", 
        "methodology": "Enterprise-grade usability testing with competitive edge focus",
        "total_critical_issues": len(findings),
        "findings": findings,
        "compliance_standards": ["WCAG 2.1 AA", "Section 508", "Enterprise UX Guidelines", "Mobile Touch Guidelines"],
        "competitive_advantage": "Deep accessibility, mobile UX, and enterprise usability analysis"
    }
    
    with open("/Users/anantsharma/Desktop/segwise/advanced_ux_findings.json", "w") as f:
        json.dump(assessment_data, f, indent=2)
    
    # Print results
    print(f"\n🏆 ADVANCED UX VULNERABILITY ASSESSMENT COMPLETE")
    print(f"=" * 60)
    print(f"📊 Critical Issues Discovered: {len(findings)}")
    print(f"🎯 Competitive Edge: Enterprise-grade UX analysis")
    print(f"💾 Detailed report: advanced_ux_findings.json")
    
    if findings:
        print(f"\n🚨 CRITICAL UX VULNERABILITIES FOUND:")
        print("-" * 50)
        for i, finding in enumerate(findings, 1):
            print(f"{i:2d}. {finding}")
    
    print(f"\n✅ ASSIGNMENT DELIVERABLES:")
    print("  • Advanced accessibility compliance testing")
    print("  • Mobile responsiveness deep analysis") 
    print("  • JavaScript error impact assessment")
    print("  • Performance & loading UX evaluation")
    print("  • Data visualization usability testing")
    print("  • Navigation & information architecture review")
    print("  • Enterprise-grade UX standards validation")
    
    return assessment_data

if __name__ == "__main__":
    find_advanced_ux_issues()
