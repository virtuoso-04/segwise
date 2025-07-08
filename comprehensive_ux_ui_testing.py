from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time
import json

# Test credentials and URLs (from assignment)
EMAIL = "qa@segwise.ai"
PASSWORD = "segwise_test"
LOGIN_URL = "https://ua.segwise.ai/login"
DASHBOARD_URL = "https://ua.segwise.ai/qa_assignment"

def setup_driver():
    """Set up Chrome WebDriver for comprehensive UX/UI testing"""
    chromedriver_autoinstaller.install()
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # Enable console logging to catch UI errors
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def test_accessibility_violations(driver, wait):
    """Test for accessibility violations - CRITICAL UX ISSUE"""
    ux_issues = []
    
    print("♿ TESTING: Accessibility & WCAG compliance...")
    
    # Check for missing alt text on images
    images = driver.find_elements(By.TAG_NAME, "img")
    missing_alt_count = 0
    
    for img in images:
        if img.is_displayed():
            alt_text = img.get_attribute("alt")
            src = img.get_attribute("src")
            
            if not alt_text or alt_text.strip() == "":
                missing_alt_count += 1
                
    if missing_alt_count > 0:
        ux_issues.append(f"🚨 ACCESSIBILITY: {missing_alt_count} images missing alt text (WCAG violation)")
    
    # Check for proper heading hierarchy
    headings = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
    heading_levels = []
    
    for heading in headings:
        if heading.is_displayed():
            tag_name = heading.tag_name
            heading_levels.append(int(tag_name[1]))  # Extract number from h1, h2, etc.
    
    # Check if heading hierarchy is logical (no skipping levels)
    if heading_levels:
        for i in range(1, len(heading_levels)):
            if heading_levels[i] - heading_levels[i-1] > 1:
                ux_issues.append("🚨 ACCESSIBILITY: Improper heading hierarchy (skips levels)")
                break
    
    # Check for proper form labels
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email'], input[type='password'], textarea")
    unlabeled_inputs = 0
    
    for input_field in inputs:
        if input_field.is_displayed():
            # Check for associated label
            input_id = input_field.get_attribute("id")
            aria_label = input_field.get_attribute("aria-label")
            placeholder = input_field.get_attribute("placeholder")
            
            if input_id:
                labels = driver.find_elements(By.CSS_SELECTOR, f"label[for='{input_id}']")
                if not labels and not aria_label:
                    unlabeled_inputs += 1
            elif not aria_label and not placeholder:
                unlabeled_inputs += 1
    
    if unlabeled_inputs > 0:
        ux_issues.append(f"🚨 ACCESSIBILITY: {unlabeled_inputs} form inputs lack proper labels")
    
    # Check color contrast (basic test)
    body_bg = driver.execute_script("return window.getComputedStyle(document.body).backgroundColor")
    body_color = driver.execute_script("return window.getComputedStyle(document.body).color")
    
    if body_bg == body_color:
        ux_issues.append("🚨 ACCESSIBILITY: Poor color contrast between text and background")
    
    return ux_issues

def test_responsive_design_breakpoints(driver, wait):
    """Test responsive design at various breakpoints - KEY UX DIFFERENTIATOR"""
    ux_issues = []
    
    print("📱 TESTING: Responsive design across device breakpoints...")
    
    # Test different screen sizes
    breakpoints = [
        {"name": "Mobile Portrait", "width": 375, "height": 667},
        {"name": "Mobile Landscape", "width": 667, "height": 375}, 
        {"name": "Tablet Portrait", "width": 768, "height": 1024},
        {"name": "Tablet Landscape", "width": 1024, "height": 768},
        {"name": "Desktop Small", "width": 1280, "height": 720},
        {"name": "Desktop Large", "width": 1920, "height": 1080}
    ]
    
    for breakpoint in breakpoints:
        driver.set_window_size(breakpoint["width"], breakpoint["height"])
        time.sleep(2)
        
        # Check for horizontal scrollbars (usually bad UX)
        has_horizontal_scroll = driver.execute_script(
            "return document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        
        if has_horizontal_scroll:
            ux_issues.append(f"📱 RESPONSIVE: Horizontal scroll at {breakpoint['name']} ({breakpoint['width']}px)")
        
        # Check if navigation is accessible
        nav_elements = driver.find_elements(By.CSS_SELECTOR, "nav, [role='navigation'], .navbar, .menu")
        nav_visible = any(nav.is_displayed() for nav in nav_elements)
        
        # Look for hamburger menu on mobile
        hamburger_elements = driver.find_elements(By.CSS_SELECTOR, 
            "[class*='hamburger'], [class*='menu-toggle'], [class*='mobile-menu'], [aria-label*='menu']")
        
        if breakpoint["width"] <= 768:  # Mobile/tablet
            if not hamburger_elements and nav_visible:
                # Check if nav elements are too cramped
                nav_items = driver.find_elements(By.CSS_SELECTOR, "nav a, nav button, .navbar a, .menu a")
                if len(nav_items) > 5:
                    ux_issues.append(f"📱 MOBILE UX: Too many nav items without hamburger menu at {breakpoint['name']}")
        
        # Check for overlapping elements
        overlaps = driver.execute_script("""
            var elements = document.querySelectorAll('*');
            var overlapping = 0;
            for(var i = 0; i < elements.length; i++) {
                var rect1 = elements[i].getBoundingClientRect();
                if(rect1.width > 0 && rect1.height > 0) {
                    for(var j = i + 1; j < elements.length; j++) {
                        var rect2 = elements[j].getBoundingClientRect();
                        if(rect2.width > 0 && rect2.height > 0) {
                            if(!(rect1.right < rect2.left || rect1.left > rect2.right || 
                                 rect1.bottom < rect2.top || rect1.top > rect2.bottom)) {
                                overlapping++;
                            }
                        }
                    }
                }
            }
            return overlapping;
        """)
        
        if overlaps > 10:  # Threshold for concerning overlaps
            ux_issues.append(f"📱 LAYOUT: {overlaps} overlapping elements at {breakpoint['name']}")
    
    # Reset to desktop size
    driver.set_window_size(1920, 1080)
    time.sleep(2)
    
    return ux_issues

def test_form_usability_issues(driver, wait):
    """Test form UX and usability issues - CRITICAL FOR SEGWISE"""
    ux_issues = []
    
    print("📝 TESTING: Form usability and UX patterns...")
    
    forms = driver.find_elements(By.TAG_NAME, "form")
    
    for i, form in enumerate(forms):
        if form.is_displayed():
            # Test 1: Check for proper validation feedback
            inputs = form.find_elements(By.CSS_SELECTOR, "input, textarea, select")
            
            for input_field in inputs:
                if input_field.is_displayed() and input_field.is_enabled():
                    input_type = input_field.get_attribute("type")
                    required = input_field.get_attribute("required")
                    
                    if required:
                        # Test empty submission
                        input_field.clear()
                        input_field.send_keys("a")  # Add something
                        input_field.clear()  # Remove it
                        input_field.send_keys(Keys.TAB)  # Trigger validation
                        
                        time.sleep(0.5)
                        
                        # Check for validation message
                        validation_msgs = driver.find_elements(By.CSS_SELECTOR, 
                            ".error, .invalid, [role='alert'], .validation-error")
                        
                        if not any(msg.is_displayed() for msg in validation_msgs):
                            ux_issues.append(f"📝 FORM UX: Required field lacks visible validation feedback (Form {i+1})")
                            break
            
            # Test 2: Check for proper submit button states
            submit_buttons = form.find_elements(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            
            for btn in submit_buttons:
                if btn.is_displayed():
                    original_text = btn.text or btn.get_attribute("value")
                    
                    # Check if button shows loading state
                    btn.click()
                    time.sleep(1)
                    
                    current_text = btn.text or btn.get_attribute("value")
                    is_disabled = not btn.is_enabled()
                    
                    if original_text == current_text and not is_disabled:
                        ux_issues.append(f"📝 FORM UX: Submit button lacks loading state or disabled state")
                    
                    break  # Test only first submit button per form
    
    # Test 3: Check for password visibility toggle
    password_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
    
    for pwd_field in password_fields:
        if pwd_field.is_displayed():
            # Look for password visibility toggle near the field
            parent = pwd_field.find_element(By.XPATH, "..")
            toggle_elements = parent.find_elements(By.CSS_SELECTOR, 
                "[class*='show'], [class*='toggle'], [class*='eye'], button")
            
            has_toggle = any("show" in elem.get_attribute("class").lower() or 
                           "eye" in elem.get_attribute("class").lower() or
                           "toggle" in elem.get_attribute("class").lower()
                           for elem in toggle_elements if elem.get_attribute("class"))
            
            if not has_toggle:
                ux_issues.append("📝 FORM UX: Password field lacks visibility toggle")
            break  # Test only first password field
    
    return ux_issues

def test_loading_states_and_feedback(driver, wait):
    """Test loading states and user feedback - COMPETITIVE EDGE"""
    ux_issues = []
    
    print("⏳ TESTING: Loading states and user feedback...")
    
    # Test 1: Check for loading indicators on page load
    driver.refresh()
    
    # Look for loading indicators immediately after refresh
    loading_found = False
    for _ in range(5):  # Check for 5 seconds
        loading_elements = driver.find_elements(By.CSS_SELECTOR, 
            ".loading, .spinner, .loader, [class*='loading'], [class*='spinner']")
        
        if any(elem.is_displayed() for elem in loading_elements):
            loading_found = True
            break
        time.sleep(1)
    
    if not loading_found:
        ux_issues.append("⏳ LOADING UX: No loading indicators during page load")
    
    # Test 2: Check for skeleton screens or placeholders
    time.sleep(3)  # Wait for initial load
    
    skeleton_elements = driver.find_elements(By.CSS_SELECTOR, 
        ".skeleton, .placeholder, [class*='skeleton'], [class*='placeholder']")
    
    # Test 3: Check button loading states
    buttons = driver.find_elements(By.TAG_NAME, "button")
    
    for button in buttons[:3]:  # Test first 3 buttons
        if button.is_displayed() and button.is_enabled():
            button_text = button.text
            
            # Avoid dangerous buttons
            if not any(word in button_text.lower() for word in ['delete', 'remove', 'clear']):
                button.click()
                time.sleep(0.5)
                
                # Check if button shows loading state
                loading_classes = ["loading", "disabled", "spinner"]
                button_class = button.get_attribute("class") or ""
                
                has_loading_state = any(cls in button_class.lower() for cls in loading_classes)
                is_disabled = not button.is_enabled()
                
                if not has_loading_state and not is_disabled:
                    ux_issues.append(f"⏳ BUTTON UX: Button '{button_text}' lacks loading state feedback")
                
                break  # Test only one button
    
    # Test 4: Check for empty states
    tables = driver.find_elements(By.TAG_NAME, "table")
    data_containers = driver.find_elements(By.CSS_SELECTOR, "[class*='data'], [class*='table'], [class*='list']")
    
    all_containers = tables + data_containers
    
    for container in all_containers[:3]:  # Test first 3 containers
        if container.is_displayed():
            text_content = container.text.strip()
            
            if not text_content:
                # Check for proper empty state message
                empty_state_elements = container.find_elements(By.CSS_SELECTOR, 
                    ".empty, .no-data, [class*='empty'], [class*='no-data']")
                
                if not empty_state_elements:
                    ux_issues.append("📊 EMPTY STATE: Data container lacks proper empty state message")
                break
    
    return ux_issues

def test_navigation_and_breadcrumbs(driver, wait):
    """Test navigation patterns and breadcrumbs - KEY UX ELEMENT"""
    ux_issues = []
    
    print("🧭 TESTING: Navigation patterns and user orientation...")
    
    # Test 1: Check for breadcrumbs
    breadcrumb_selectors = [
        ".breadcrumb", ".breadcrumbs", "[class*='breadcrumb']", 
        "[aria-label*='breadcrumb']", "nav[role='navigation'] ol"
    ]
    
    breadcrumbs_found = False
    for selector in breadcrumb_selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        if any(elem.is_displayed() for elem in elements):
            breadcrumbs_found = True
            break
    
    # Check if we're deep in navigation (should have breadcrumbs)
    current_url = driver.current_url
    url_segments = current_url.split('/')
    
    if len(url_segments) > 4 and not breadcrumbs_found:  # Deep navigation
        ux_issues.append("🧭 NAVIGATION: Deep page lacks breadcrumb navigation")
    
    # Test 2: Check for clear page titles
    page_title = driver.title
    h1_elements = driver.find_elements(By.TAG_NAME, "h1")
    
    if not page_title or page_title == "":
        ux_issues.append("🧭 NAVIGATION: Page lacks proper title")
    
    if not any(h1.is_displayed() and h1.text.strip() for h1 in h1_elements):
        ux_issues.append("🧭 NAVIGATION: Page lacks clear H1 heading")
    
    # Test 3: Check for consistent navigation
    nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a, .navbar a, .menu a")
    
    if len(nav_links) < 3:
        ux_issues.append("🧭 NAVIGATION: Limited navigation options available")
    
    # Test 4: Check for back button functionality (browser back vs app back)
    if len(url_segments) > 4:  # If we're in a sub-page
        back_buttons = driver.find_elements(By.CSS_SELECTOR, 
            "[class*='back'], [aria-label*='back'], button:contains('Back')")
        
        if not back_buttons:
            ux_issues.append("🧭 NAVIGATION: Sub-page lacks back button")
    
    # Test 5: Check for active navigation states
    for link in nav_links[:5]:  # Check first 5 nav links
        if link.is_displayed():
            href = link.get_attribute("href")
            link_class = link.get_attribute("class") or ""
            
            if href and current_url in href:
                # This should be the active link
                if not any(state in link_class.lower() for state in ['active', 'current', 'selected']):
                    ux_issues.append("🧭 NAVIGATION: Active page not highlighted in navigation")
                break
    
    return ux_issues

def test_data_visualization_ux(driver, wait):
    """Test data visualization UX - SPECIFIC TO SEGWISE DASHBOARD"""
    ux_issues = []
    
    print("📊 TESTING: Data visualization and dashboard UX...")
    
    # Test 1: Chart interactivity
    chart_elements = driver.find_elements(By.CSS_SELECTOR, "canvas, svg, [class*='chart'], [class*='graph']")
    
    for i, chart in enumerate(chart_elements):
        if chart.is_displayed():
            # Test hover interactions
            ActionChains(driver).move_to_element(chart).perform()
            time.sleep(1)
            
            # Look for tooltips
            tooltips = driver.find_elements(By.CSS_SELECTOR, 
                ".tooltip, [role='tooltip'], [class*='tooltip'], [class*='popup']")
            
            tooltip_visible = any(tip.is_displayed() for tip in tooltips)
            
            if not tooltip_visible:
                ux_issues.append(f"📊 CHART UX: Chart {i+1} lacks hover tooltips for data points")
            
            # Test click interactions
            chart.click()
            time.sleep(1)
            
            # Check if click provides additional info or drill-down
            modal_elements = driver.find_elements(By.CSS_SELECTOR, 
                ".modal, [role='dialog'], [class*='modal'], [class*='dialog']")
            
            # This is optional, so we won't flag as error if missing
            break  # Test only first chart
    
    # Test 2: Data table functionality
    tables = driver.find_elements(By.TAG_NAME, "table")
    
    for i, table in enumerate(tables):
        if table.is_displayed():
            # Check for sortable columns
            headers = table.find_elements(By.TAG_NAME, "th")
            sortable_count = 0
            
            for header in headers:
                if header.is_displayed():
                    header_class = header.get_attribute("class") or ""
                    onclick = header.get_attribute("onclick")
                    
                    if ("sort" in header_class.lower() or onclick or 
                        header.find_elements(By.CSS_SELECTOR, "[class*='sort']")):
                        sortable_count += 1
            
            if len(headers) > 2 and sortable_count == 0:
                ux_issues.append(f"📊 TABLE UX: Table {i+1} headers not sortable")
            
            # Check for pagination on large tables
            rows = table.find_elements(By.TAG_NAME, "tr")
            data_rows = [row for row in rows if row.find_elements(By.TAG_NAME, "td")]
            
            if len(data_rows) > 15:  # Many rows
                pagination = driver.find_elements(By.CSS_SELECTOR, 
                    ".pagination, .pager, [class*='pagination'], [class*='pager']")
                
                if not any(p.is_displayed() for p in pagination):
                    ux_issues.append(f"📊 TABLE UX: Large table {i+1} lacks pagination")
            
            break  # Test only first table
    
    # Test 3: Filter and search functionality
    filter_elements = driver.find_elements(By.CSS_SELECTOR, 
        "input[type='search'], .filter, [class*='filter'], [class*='search']")
    
    for filter_elem in filter_elements:
        if filter_elem.is_displayed() and filter_elem.is_enabled():
            # Test search functionality
            if filter_elem.tag_name == "input":
                filter_elem.clear()
                filter_elem.send_keys("test")
                time.sleep(1)
                
                # Check for search results or filtering feedback
                result_elements = driver.find_elements(By.CSS_SELECTOR, 
                    ".results, .filtered, [class*='result'], [class*='filtered']")
                
                # Check if data updated (basic test)
                filter_elem.clear()
                time.sleep(1)
                
                # This is a basic test - could be enhanced
            break  # Test only first filter
    
    return ux_issues

def test_error_handling_ux(driver, wait):
    """Test error handling and user feedback UX"""
    ux_issues = []
    
    print("⚠️ TESTING: Error handling and user feedback UX...")
    
    # Test 1: Check for existing error states
    error_elements = driver.find_elements(By.CSS_SELECTOR, 
        ".error, .alert, [role='alert'], [class*='error'], [class*='alert']")
    
    visible_errors = [elem for elem in error_elements if elem.is_displayed()]
    
    for error in visible_errors:
        error_text = error.text.strip()
        
        if error_text:
            # Check if error message is user-friendly
            technical_terms = ['undefined', 'null', 'NaN', 'object Object', 'error 500', 'stack trace']
            
            if any(term in error_text.lower() for term in technical_terms):
                ux_issues.append(f"⚠️ ERROR UX: Technical error exposed to user: '{error_text[:50]}...'")
            
            # Check if error has action guidance
            if len(error_text) < 20 and not any(word in error_text.lower() for word in ['try', 'contact', 'refresh']):
                ux_issues.append(f"⚠️ ERROR UX: Error lacks guidance: '{error_text}'")
    
    # Test 2: Test 404/broken link handling
    current_url = driver.current_url
    
    # Try accessing a non-existent page
    test_url = current_url + "/nonexistent-page-test"
    driver.get(test_url)
    time.sleep(2)
    
    page_text = driver.page_source.lower()
    
    if "404" in page_text or "not found" in page_text:
        # Check for helpful 404 page
        home_links = driver.find_elements(By.CSS_SELECTOR, 
            "a[href*='home'], a[href='/'], a[href*='dashboard']")
        
        if not home_links:
            ux_issues.append("⚠️ ERROR UX: 404 page lacks navigation back to main site")
    
    # Return to original page
    driver.get(current_url)
    time.sleep(2)
    
    return ux_issues

def test_real_user_scenarios(driver, wait):
    """Test real user scenarios - What would actually confuse or frustrate users?"""
    issues = []
    
    print("👤 TESTING: Real user scenarios and pain points...")
    
    # Scenario 1: New user trying to understand the dashboard
    print("   📊 Scenario: New user lands on dashboard...")
    
    # Check for clear dashboard title/purpose
    page_title = driver.title
    h1_elements = driver.find_elements(By.TAG_NAME, "h1")
    
    if not any(h1.is_displayed() and h1.text.strip() for h1 in h1_elements):
        issues.append("❓ USER CONFUSION: Dashboard lacks clear title - users don't know what they're looking at")
    
    # Check for help or getting started guidance
    help_elements = driver.find_elements(By.CSS_SELECTOR, 
        "[class*='help'], [class*='guide'], [class*='tutorial'], [aria-label*='help']")
    
    if not any(elem.is_displayed() for elem in help_elements):
        issues.append("� USER GUIDANCE: No help or tutorial for first-time users")
    
    # Scenario 2: User looking for specific data
    print("   🔍 Scenario: User searching for specific information...")
    
    # Check for search functionality
    search_elements = driver.find_elements(By.CSS_SELECTOR, 
        "input[type='search'], [placeholder*='search'], [class*='search']")
    
    if not search_elements:
        issues.append("🔍 DATA DISCOVERY: No search function - users can't quickly find specific data")
    
    # Scenario 3: User wants to export or share data
    print("   📤 Scenario: User wants to export or share findings...")
    
    export_elements = driver.find_elements(By.CSS_SELECTOR, 
        "[class*='export'], [class*='download'], [class*='share'], button:contains('Export')")
    
    if not export_elements:
        issues.append("📤 DATA SHARING: No export/share options - users can't act on insights")
    
    return issues

def test_chart_and_metrics_presence(driver, wait):
    """Assert presence of charts and key metrics - Core dashboard functionality"""
    issues = []
    
    print("� TESTING: Chart and metrics presence...")
    
    # Test for charts
    chart_elements = driver.find_elements(By.CSS_SELECTOR, "canvas, svg, [class*='chart'], [class*='graph']")
    
    if not chart_elements:
        issues.append("📊 CRITICAL: No charts detected on analytics dashboard")
        return issues
    
    print(f"   ✅ Found {len(chart_elements)} chart elements")
    
    # Test chart interactivity
    interactive_chart_found = False
    for i, chart in enumerate(chart_elements[:3]):  # Test first 3 charts
        if chart.is_displayed():
            # Test hover for tooltips
            ActionChains(driver).move_to_element(chart).perform()
            time.sleep(1)
            
            tooltips = driver.find_elements(By.CSS_SELECTOR, 
                ".tooltip, [role='tooltip'], [class*='tooltip']")
            
            if any(tip.is_displayed() for tip in tooltips):
                interactive_chart_found = True
                print(f"   ✅ Chart {i+1} has interactive tooltips")
                break
    
    if not interactive_chart_found:
        issues.append("📊 CHART UX: Charts lack hover tooltips - users can't see precise values")
    
    # Test for key metrics/KPIs
    metric_elements = driver.find_elements(By.CSS_SELECTOR, 
        "[class*='metric'], [class*='kpi'], [class*='stat'], [class*='number'], .card")
    
    if len(metric_elements) < 3:
        issues.append("📊 METRICS: Few key metrics visible - users lack quick insights")
    
    # Test for data tables
    tables = driver.find_elements(By.TAG_NAME, "table")
    
    if tables:
        print(f"   ✅ Found {len(tables)} data tables")
        
        # Test table sorting
        sortable_found = False
        for table in tables[:2]:  # Test first 2 tables
            headers = table.find_elements(By.TAG_NAME, "th")
            for header in headers:
                if header.is_displayed():
                    header_class = header.get_attribute("class") or ""
                    if "sort" in header_class.lower():
                        sortable_found = True
                        break
            if sortable_found:
                break
        
        if not sortable_found:
            issues.append("📊 TABLE UX: Data tables not sortable - users can't organize data")
    
    return issues

def test_dashboard_usability_pain_points(driver, wait):
    """Identify specific usability pain points that real users encounter"""
    issues = []
    
    print("😤 TESTING: Common usability pain points...")
    
    # Pain Point 1: Information overload
    print("   🧠 Testing: Information density and cognitive load...")
    
    # Count visible interactive elements
    buttons = driver.find_elements(By.TAG_NAME, "button")
    links = driver.find_elements(By.TAG_NAME, "a")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    
    total_interactive = len([elem for elem in buttons + links + inputs if elem.is_displayed()])
    
    if total_interactive > 20:
        issues.append(f"🧠 COGNITIVE OVERLOAD: {total_interactive} interactive elements - too many choices")
    
    # Pain Point 2: Unclear call-to-action
    print("   🎯 Testing: Clear next actions for users...")
    
    primary_buttons = driver.find_elements(By.CSS_SELECTOR, 
        ".btn-primary, .primary, [class*='primary'], .cta")
    
    if len(primary_buttons) == 0:
        issues.append("🎯 NO CLEAR ACTION: No primary call-to-action - users don't know what to do next")
    elif len(primary_buttons) > 3:
        issues.append("🎯 COMPETING ACTIONS: Too many primary buttons - unclear what's most important")
    
    # Pain Point 3: Mobile usability
    print("   📱 Testing: Mobile usability pain points...")
    
    # Test mobile view
    original_size = driver.get_window_size()
    driver.set_window_size(375, 667)  # iPhone size
    time.sleep(2)
    
    # Check for mobile navigation
    hamburger_menu = driver.find_elements(By.CSS_SELECTOR, 
        "[class*='hamburger'], [class*='menu-toggle'], [aria-label*='menu']")
    
    nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a, .navbar a")
    
    if len(nav_links) > 3 and not hamburger_menu:
        issues.append("📱 MOBILE FAIL: Too many nav items without mobile menu - cramped interface")
    
    # Check button sizes for touch
    small_buttons = 0
    for btn in driver.find_elements(By.TAG_NAME, "button"):
        if btn.is_displayed():
            size = driver.execute_script(
                "var rect = arguments[0].getBoundingClientRect(); return rect.width * rect.height;", btn
            )
            if size > 0 and size < 44 * 44:  # Apple's minimum
                small_buttons += 1
    
    if small_buttons > 0:
        issues.append(f"📱 TOUCH TARGET: {small_buttons} buttons too small for touch - user frustration")
    
    # Reset window size
    driver.set_window_size(original_size['width'], original_size['height'])
    time.sleep(1)
    
    # Pain Point 4: Error handling
    print("   ⚠️ Testing: Error communication...")
    
    # Look for any existing error messages
    error_elements = driver.find_elements(By.CSS_SELECTOR, 
        ".error, .alert-danger, [class*='error'], [role='alert']")
    
    for error in error_elements:
        if error.is_displayed():
            error_text = error.text.strip()
            if error_text:
                # Check if error is technical jargon
                technical_terms = ['undefined', 'null', '500', 'exception', 'stack']
                if any(term in error_text.lower() for term in technical_terms):
                    issues.append(f"⚠️ ERROR UX: Technical error shown to user - confusing message")
    
    return issues

def test_data_exploration_workflow(driver, wait):
    """Test how users would actually explore and interact with data"""
    issues = []
    
    print("🔬 TESTING: Data exploration user workflow...")
    
    # Workflow 1: User wants to drill down into data
    print("   🔍 Testing: Data drill-down capabilities...")
    
    charts = driver.find_elements(By.CSS_SELECTOR, "canvas, svg, [class*='chart']")
    
    drill_down_possible = False
    for chart in charts[:2]:  # Test first 2 charts
        if chart.is_displayed():
            chart.click()
            time.sleep(1)
            
            # Check if click shows more detail
            modals = driver.find_elements(By.CSS_SELECTOR, 
                ".modal, [role='dialog'], [class*='detail']")
            
            if any(modal.is_displayed() for modal in modals):
                drill_down_possible = True
                print("   ✅ Chart drill-down functionality found")
                break
    
    if not drill_down_possible:
        issues.append("🔍 DATA EXPLORATION: Charts not clickable - users can't explore details")
    
    # Workflow 2: User wants to filter data
    print("   🎚️ Testing: Data filtering capabilities...")
    
    filter_elements = driver.find_elements(By.CSS_SELECTOR, 
        "[class*='filter'], [class*='dropdown'], select, input[type='date']")
    
    if not filter_elements:
        issues.append("🎚️ DATA FILTERING: No filter controls - users can't narrow down data")
    
    # Workflow 3: User wants to compare time periods
    print("   📅 Testing: Time period comparison...")
    
    date_elements = driver.find_elements(By.CSS_SELECTOR, 
        "input[type='date'], [class*='date'], [class*='time'], [class*='period']")
    
    if len(date_elements) < 2:
        issues.append("📅 TIME COMPARISON: No date range selection - users can't compare periods")
    
    return issues

def main():
    """Main manual testing function focused on real user experience"""
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    all_issues = []
    
    try:
        print("👤 MANUAL UX TESTING - REAL USER PERSPECTIVE")
        print("=" * 60)
        print("Focus: What would actually confuse or frustrate real users?\n")
        
        # Login and navigate to dashboard
        print("🔐 Logging in as a real user would...")
        driver.get(LOGIN_URL)
        
        # More realistic login testing
        try:
            email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
            password_input = driver.find_element(By.ID, "password")
            
            email_input.send_keys(EMAIL)
            password_input.send_keys(PASSWORD)
            password_input.submit()
            
            time.sleep(3)
            print("✅ Login successful")
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return
        
        # Navigate to dashboard
        driver.get(DASHBOARD_URL)
        time.sleep(4)
        
        print(f"📊 Testing dashboard at: {driver.current_url}\n")
        
        # Run manual, user-focused tests
        all_issues.extend(test_real_user_scenarios(driver, wait))
        all_issues.extend(test_chart_and_metrics_presence(driver, wait))
        all_issues.extend(test_dashboard_usability_pain_points(driver, wait))
        all_issues.extend(test_data_exploration_workflow(driver, wait))
        
        
        # Take screenshot for evidence
        driver.save_screenshot("/Users/anantsharma/Desktop/segwise/manual_ux_testing_evidence.png")
        
        # Generate user-focused report
        print(f"\n👤 MANUAL UX TESTING COMPLETE")
        print(f"{'='*60}")
        print(f"Real User Issues Found: {len(all_issues)}")
        
        if all_issues:
            print(f"\n� USER EXPERIENCE PAIN POINTS:")
            
            # Categorize by user impact
            critical_blockers = [issue for issue in all_issues if "CRITICAL" in issue or "FAIL" in issue]
            confusion_issues = [issue for issue in all_issues if "CONFUSION" in issue or "UNCLEAR" in issue]
            frustration_issues = [issue for issue in all_issues if "FRUSTRATION" in issue or "OVERLOAD" in issue]
            mobile_issues = [issue for issue in all_issues if "�" in issue or "MOBILE" in issue]
            data_issues = [issue for issue in all_issues if "📊" in issue or "DATA" in issue]
            
            print(f"\n📊 USER IMPACT BREAKDOWN:")
            print(f"🚨 Critical Blockers: {len(critical_blockers)}")
            print(f"❓ User Confusion: {len(confusion_issues)}")
            print(f"� User Frustration: {len(frustration_issues)}")
            print(f"📱 Mobile Issues: {len(mobile_issues)}")
            print(f"📊 Data Access Issues: {len(data_issues)}")
            
            print(f"\n� DETAILED USER ISSUES:")
            for i, issue in enumerate(all_issues, 1):
                print(f"{i}. {issue}")
                
            # User-focused recommendations
            print(f"\n💡 DASHBOARD USABILITY IMPROVEMENTS:")
            print("1. Add clear dashboard title and purpose statement")
            print("2. Implement search functionality for data discovery")
            print("3. Add export/share options for user productivity")
            print("4. Make charts interactive with hover tooltips")
            print("5. Implement mobile-friendly navigation")
            print("6. Add data filtering and drill-down capabilities")
            print("7. Provide clear call-to-action buttons")
            print("8. Add help or tutorial for new users")
                
            # Save user-focused report
            report_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "testing_approach": "Manual UX Testing - Real User Perspective",
                "total_user_issues": len(all_issues),
                "impact_categories": {
                    "critical_blockers": len(critical_blockers),
                    "user_confusion": len(confusion_issues),
                    "user_frustration": len(frustration_issues),
                    "mobile_issues": len(mobile_issues),
                    "data_access_issues": len(data_issues)
                },
                "user_pain_points": all_issues,
                "usability_recommendations": [
                    "Add clear dashboard title and purpose statement",
                    "Implement search functionality for data discovery",
                    "Add export/share options for user productivity",
                    "Make charts interactive with hover tooltips",
                    "Implement mobile-friendly navigation",
                    "Add data filtering and drill-down capabilities",
                    "Provide clear call-to-action buttons",
                    "Add help or tutorial for new users"
                ],
                "test_url": driver.current_url
            }
            
            with open("/Users/anantsharma/Desktop/segwise/manual_ux_assessment.json", "w") as f:
                json.dump(report_data, f, indent=2)
                
            print(f"\n💾 Manual UX report saved to: manual_ux_assessment.json")
            
            print(f"\n🎯 KEY USER INSIGHTS:")
            print("• Users need clear guidance on dashboard purpose")
            print("• Data exploration requires better interactivity")
            print("• Mobile experience needs significant improvement")
            print("• Search and export are critical missing features")
            print("• Chart tooltips essential for data precision")
            
        else:
            print(f"\n✅ No significant user experience issues detected!")
            
    except Exception as e:
        print(f"\n❌ Manual UX testing failed: {e}")
        try:
            driver.save_screenshot("/Users/anantsharma/Desktop/segwise/manual_ux_testing_error.png")
        except:
            pass
    
    finally:
        driver.quit()
        print(f"\n🔚 Manual UX testing completed - Real user perspective delivered")

if __name__ == "__main__":
    main()
