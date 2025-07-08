# Segwise QA Assignment

## Overview
This repository contains QA testing results and automation for the Segwise.ai dashboard.

## Files Included

### 📋 QA Report
- **`QA_Report.md`** - Complete testing report with:
  - Found bugs and issues (5 critical issues including security vulnerability)
  - Suggested test cases (functional, security, accessibility)
  - Regression checklist with priority levels
  - Usability improvement suggestions

### 🤖 Automation Script
- **`test_dashboard.py`** - Python script that runs automated tests for:
  - Login functionality
  - Dashboard loading
  - Chart presence and interaction
  - Navigation elements

### 📸 Evidence
- **`screenshots/`** - Bug documentation and test evidence

## Quick Start

### Prerequisites
```bash
pip install selenium chromedriver-autoinstaller
```

### Run Tests
```bash
python test_dashboard.py
```

## Key Findings

### Critical Issues Found:
1. **Authentication Bypass** - Unauthorized admin access possible
2. **Production JavaScript Errors** - 17+ errors affecting stability
3. **Mobile Responsiveness** - No mobile navigation elements
4. **Missing Chart Tooltips** - Poor data exploration experience
5. **Chart Row Limit** - Unclear 10-row restriction communication

### Test Results Summary:
- 5 major bugs identified and documented
- Security vulnerability requiring immediate attention
- User experience issues affecting productivity
- Comprehensive regression checklist provided
- Actionable improvement suggestions included

## Testing Environment
- **Browser**: Chrome (latest)
- **OS**: macOS Sonoma 14.5
- **Tools**: Selenium WebDriver, Chrome DevTools
- **Test Credentials**: qa@segwise.ai / segwise_test
