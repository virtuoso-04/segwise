# Segwise QA Assignment Report

**Candidate**: Anant Sharma  
**Role Applied**: QA Intern  
**Date**: July 9, 2025

---

##  1. Functional Testing – Observed Issues

###  Test URL: [https://ua.segwise.ai](https://ua.segwise.ai)  
**Test Credentials**: qa@segwise.ai / segwise_test

---

### Bug 1: Custom Chart Selection Limit Not Communicated
- **Severity**: Medium  
- The interface allows selecting more than 10 rows for a chart but silently limits rendering to 10, with no warning.  
- **Expected**: Limit row selection to 10 or display a visible warning.  
- **Actual**: User can select more than 10 rows; chart shows “No data found.”

---

### Bug  2: Missing Mobile Navigation
- **Severity**: Medium  
- On smaller screens, navigation elements do not adapt. No hamburger menu or responsive sidebar is visible.  
- **Expected**: Responsive layout with collapsible menu.  
- **Actual**: Layout breaks, and navigation becomes inaccessible.

---

### Bug 3: No Chart Tooltips
- **Severity**: Low-Medium  
- Hovering over chart elements shows no tooltips, limiting interpretability.  
- **Expected**: On-hover values, labels, or breakdowns.  
- **Actual**: Static charts without interactive feedback.

---

### bug 4: Visible Error Message – Onboarding Route
- **Severity**: High  
- Debug-like error `/james_enter/onboarding?...` is visible in UI.  
- **Expected**: Clean UI with no internal error/debug output.  
- **Actual**: Error appears intermittently.

---

### bug 5: Report Navigation Not Intuitive
- **Severity**: Medium  
- No clear menu or UI section leads to saved reports.  
- **Expected**: Prominent reports section in navigation.  
- **Actual**: Reports are hidden; difficult to locate or revisit saved reports.

---

##  2. Regression Checklist (Dashboard)

| Component              | Check                                  | Status   | Notes                              |
|------------------------|-----------------------------------------|----------|------------------------------------|
| Login                  | Valid credentials                      | ✅ Pass   | Login works as expected            |
| Dashboard Load         | Main dashboard loads completely         | ✅ Pass   | Loads with all visible components |
| Chart Rendering        | Default chart visible and loads         | ⚠️ Partial | Missing tooltips                   |
| Custom Chart Limit     | Max 10 rows selected                    | ❌ Fail   | No user warning shown              |
| Mobile Responsiveness  | Sidebar & content adapt to screen size  | ❌ Fail   | No mobile-friendly navigation      |
| Error Handling         | No debug output visible                 | ❌ Fail   | Onboarding error observed          |
| Report Discovery       | Easy access to saved reports            | ❌ Fail   | Navigation unclear                 |
| Logout Functionality   | User able to log out                    | ✅ Pass   | Button redirects to login screen  |

---

##  Suggested Test Cases

### Functional
- Login/logout flow
- Chart visibility and rendering
- Row selection with limits
- Data filters and saved reports
- Export or copy report actions (if available)

### UI/UX
- no clarity of dashboard
- Hover tooltips on charts
- Mobile-friendly layouts
- Element responsiveness
- Button accessibility

### Security (Basic)
- Prevent unauthorized URL access
- Block access to admin-only areas
- Handle broken API responses gracefully

---

##  Recommendations

1. **Improve UX Clarity**
   - add a dark mode/ light mode toggle switch
   - Warn users when chart limit is exceeded
   - Add tooltips to charts for better readability
   - give a brief walkthrough of the dashboard

2. **Mobile Usability**
   - Add hamburger menu or responsive sidebar
   - Improve layout adaptation for smaller devices

3. **Interface Cleanup**
   - Remove or hide internal error messages
   - Clarify dashboard purpose with helpful tooltips or onboarding content

4. **Navigation Enhancements**
   - Add a visible “Reports” section or menu
   - Make saved reports easily accessible

---

## Testing Environment

- **Browser**: Chrome 138, Safari 17.5  
- **OS**: macOS Sonoma 14.5  
- **Screen Sizes**: 2560×1600 (desktop), 768×1024 (tablet simulation)  
- **Tools Used**:  
  - Manual UI exploration  
  - Responsive Design Mode  
  - chrome developer tools (F12)
  - Selenium WebDriver (see `test_dashboard.py` in repo)

---

##  Summary

This report covers 5 functional issues, a regression checklist, and improvement suggestions aligned with Segwise’s QA assignment. 
Testing was performed manually and supported by light automation using Selenium for login and dashboard validation. Screenshots and script are included in the GitHub submission.

Thats all the software testing from my side , overall the UI of the website is clean , minimal, Ios inspired design with green accent 

Regards,
Anant Sharma
anant.sharma.career@gmail.com

---

