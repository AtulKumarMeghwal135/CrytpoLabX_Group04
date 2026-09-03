# SonarQube SAST Analysis Report

## 1. Project Information

| Item                 | Details                   |
| -------------------- | ------------------------- |
| Application          | Library Management System |
| Assignment           | Lab Assignment 3          |
| SAST Tool            | SonarQube                 |
| Programming Language | python                      |
| Repository           | CryptoLabX                |
| Project Folder       | secure_application        |

---

## 2. Objective

The objective of the SAST analysis is to analyze the source code of the Library Management System and identify potential security vulnerabilities and insecure coding practices.

The analysis was performed using SonarQube.

---

## 3. Source Code Analyzed

The source code analyzed by SonarQube is located in:

```text
secure_application/src/
```

The analyzed application implements:

* Member registration
* Book search
* Book issue
* Book return
* Fine calculation

---

## 4. SonarQube Analysis

The project was scanned using SonarQube.

The analysis provides information about:

* Bugs
* Vulnerabilities
* Security Hotspots
* Code Smells
* Duplicated Code
* Code Quality
* Security Rating

The exact results should be recorded from the SonarQube dashboard.

---

## 5. Security Findings

### 5.1 SQL Injection

**SonarQube Status:** [Detected/Not Detected]

**Severity:** [Enter actual severity shown by SonarQube]

The application contains a database operation where user-controlled input may be incorporated into an SQL query without proper parameterization.

**Potential Impact:**

* Unauthorized database access
* Manipulation of database queries
* Unauthorized modification of records

**Recommended Fix:**

Use parameterized queries or `PreparedStatement`.

---

### 5.2 Cross-Site Scripting (XSS)

**SonarQube Status:** [Detected/Not Detected]

**Severity:** [Enter actual severity shown by SonarQube]

The application accepts user-controlled data that may be displayed without appropriate output encoding.

**Potential Impact:**

* Execution of malicious scripts
* Modification of displayed content
* Potential information theft

**Recommended Fix:**

Validate user input and encode untrusted output before displaying it.

---

### 5.3 Improper Input Validation

**SonarQube Status:** [Detected/Not Detected]

**Severity:** [Enter actual severity shown by SonarQube]

The application contains input-handling operations where user-provided values may not be sufficiently validated.

**Potential Impact:**

* Invalid data
* Unexpected application behavior
* Application errors
* Potential security issues

**Recommended Fix:**

Apply appropriate type, range, length, and format validation.

---

## 6. SonarQube Results

Enter the actual values displayed by your SonarQube dashboard.

| Metric                 | Result         |
| ---------------------- | -------------- |
| Bugs                   | [Actual value] |
| Vulnerabilities        | [Actual value] |
| Security Hotspots      | [Actual value] |
| Code Smells            | [Actual value] |
| Reliability Rating     | [Actual value] |
| Security Rating        | [Actual value] |
| Maintainability Rating | [Actual value] |
| Coverage               | [Actual value] |
| Duplications           | [Actual value] |

---

## 7. Screenshots

Screenshots of the SonarQube analysis are stored in:

```text
secure_application/screenshots/
```

Recommended screenshots:

```text
screenshots/
├── sonarqube_dashboard.png
├── sonarqube_issues.png
├── sql_injection_sast.png
├── xss_sast.png
└── input_validation_sast.png
```

The screenshots provide evidence of the actual SonarQube analysis.

---

## 8. Remediation

The identified vulnerabilities can be addressed using secure coding practices.

| Vulnerability             | Remediation                                 |
| ------------------------- | ------------------------------------------- |
| SQL Injection             | Use PreparedStatement/parameterized queries |
| XSS                       | Validate input and encode output            |
| Improper Input Validation | Validate type, range, format and length     |

After applying fixes, the project should be scanned again using SonarQube to verify whether the issues have been resolved.

---

## 9. Conclusion

SonarQube was used to perform Static Application Security Testing on the Library Management System.

The analysis helps identify security weaknesses and insecure coding practices before the application is deployed.

The SAST results, together with the screenshots stored in the `screenshots/` directory, provide evidence of the security analysis performed for Lab Assignment 3.

