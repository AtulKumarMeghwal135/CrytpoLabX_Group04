# Library Management System – SAST Analysis Report

## 1. Introduction

This report documents the Static Application Security Testing (SAST) performed on the Library Management System developed for Lab Assignment 3.

SAST analyzes application source code without executing the application. It helps identify potential security vulnerabilities and insecure coding practices during development.

The purpose of this analysis is to identify the intentionally introduced vulnerabilities and evaluate the security of the source code.

---

# 2. Objective

The objectives of the SAST analysis are:

* Analyze the Library Management System source code.
* Identify security vulnerabilities.
* Determine the location of vulnerable code.
* Understand the severity and impact of identified issues.
* Document SAST findings.
* Recommend appropriate remediation techniques.

---

# 3. SAST Tool

**SAST Tool:** [Enter your SAST tool name]

Example:

```text
SonarQube
```

**Version:** [Enter version]

**Language:** Java

**Project:** Library Management System

---

# 4. Source Code Analyzed

The source code analyzed by the SAST tool is located in:

```text
secure_application/src/
```

The SAST analysis covers the source files used to implement:

* Member registration
* Book search
* Book issue
* Book return
* Fine calculation
* Database operations
* Input handling

---

# 5. SAST Analysis Process

The following process was followed:

### Step 1 – Prepare Source Code

The Library Management System source code was placed inside:

```text
secure_application/src/
```

### Step 2 – Configure SAST Tool

The project was configured in the selected SAST tool.

### Step 3 – Run Analysis

A complete source-code analysis was performed.

### Step 4 – Review Findings

The security findings reported by the SAST tool were reviewed.

### Step 5 – Map Findings

The reported issues were mapped to the vulnerabilities intentionally introduced into the application.

### Step 6 – Document Results

Screenshots and analysis results were stored in:

```text
secure_application/sast/
secure_application/screenshots/
```

---

# 6. SAST Findings

## 6.1 SQL Injection

### Finding

The SAST tool identified a potentially unsafe SQL operation involving user-controlled input.

### Vulnerable Pattern

```java
String query = "SELECT * FROM books WHERE title = '" + userInput + "'";
```

### Security Issue

User input is directly included in the SQL query.

### Risk

An attacker may manipulate the SQL statement and potentially access or modify unauthorized database information.

### Recommended Fix

Use parameterized queries:

```java
PreparedStatement stmt =
    connection.prepareStatement(
        "SELECT * FROM books WHERE title = ?");
stmt.setString(1, userInput);
```

### SAST Evidence

**Screenshot:** Add the SAST screenshot showing the SQL Injection finding.

```text
screenshots/sql_injection_sast.png
```

---

# 7. XSS Finding

## 7.1 Finding

The SAST analysis identified potentially unsafe handling of user-controlled data that may reach an output location without sufficient encoding.

### Security Issue

Untrusted input may be interpreted as executable content when rendered in an HTML-based interface.

### Example Input

```html
<script>alert('XSS')</script>
```

### Risk

An attacker may execute JavaScript in a victim's browser.

### Recommended Fix

* Validate user input.
* Encode output.
* Use safe HTML rendering mechanisms.

### SAST Evidence

Add the corresponding screenshot:

```text
screenshots/xss_sast.png
```

---

# 8. Improper Input Validation Finding

## 8.1 Finding

The SAST analysis identified input-handling locations where user-provided values were not sufficiently validated before processing.

### Examples

* Negative book IDs
* Invalid numeric values
* Empty values
* Invalid date values

### Risk

Improperly validated data may cause application errors, unexpected behavior, or other security issues.

### Recommended Fix

Validate:

* Type
* Range
* Length
* Format
* Null/empty values

### SAST Evidence

Add the corresponding screenshot:

```text
screenshots/input_validation_sast.png
```

---

# 9. SAST Results Summary

Fill in the exact severity/count values from your SAST tool.

| Vulnerability             | SAST Detected | Severity          | Status       |
| ------------------------- | ------------- | ----------------- | ------------ |
| SQL Injection             | Yes/No        | [High/Medium/Low] | [Open/Fixed] |
| Cross-Site Scripting      | Yes/No        | [High/Medium/Low] | [Open/Fixed] |
| Improper Input Validation | Yes/No        | [High/Medium/Low] | [Open/Fixed] |

**Important:** Do not invent severity or issue counts. Enter the values shown by your actual SAST tool.

---

# 10. Screenshots

The following screenshots should be included as evidence of the SAST analysis:

```text
secure_application/screenshots/
│
├── sast_dashboard.png
├── sql_injection_sast.png
├── xss_sast.png
└── input_validation_sast.png
```

Each screenshot should clearly show the relevant finding reported by the SAST tool.

---

# 11. Before and After Analysis

The SAST analysis can be performed before and after applying security fixes.

### Before Fixes

The intentionally vulnerable source code contains insecure practices.

Expected findings include:

* SQL Injection
* XSS
* Improper Input Validation

### After Fixes

After applying remediation:

* SQL queries use prepared statements.
* User input is validated.
* Untrusted output is encoded.
* SAST findings should decrease or disappear depending on the tool and implementation.

---

# 12. Remediation

The following security improvements should be applied:

| Finding                   | Remediation                              |
| ------------------------- | ---------------------------------------- |
| SQL Injection             | Use prepared statements                  |
| XSS                       | Encode output and validate input         |
| Improper Input Validation | Validate type, range, format, and length |

After applying the fixes, the SAST scan should be executed again to verify that the vulnerabilities have been addressed.

---

# 13. Conclusion

The SAST analysis provided a systematic method for identifying security weaknesses in the Library Management System source code.

The analysis focused on SQL Injection, Cross-Site Scripting, and Improper Input Validation. The findings demonstrate the importance of secure input handling, parameterized database queries, and proper output encoding.

SAST is useful because vulnerabilities can be identified during development before the application is deployed.

The final SAST results and screenshots should be included with this report as evidence of the security analysis.

