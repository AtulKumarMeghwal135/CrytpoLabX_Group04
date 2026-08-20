# Library Management System

## Lab Assignment 3

This project implements a small **Library Management System** as part of Lab Assignment 3. The application demonstrates the core functionalities of a library system and intentionally contains selected security vulnerabilities for analysis using a SAST tool.

The objective is to understand common software vulnerabilities, identify them using Static Application Security Testing (SAST), and understand how they can be fixed.

---

## 1. Project Structure

```text
secure_application/
│
├── src/
│   └── [source code]
│
├── reports/
│   └── Lab_Assignment_3_Report.md
│
├── screenshots/
│   └── [screenshots of application and SAST results]
│
├── sast/
│   └── [SAST reports/results]
│
├── outputs/
│   └── [program outputs]
│
├── testcases/
│   └── [test cases]
│
└── README.md
```

---

## 2. Application Description

The Library Management System provides basic functionality for managing books and library members.

The application is intentionally kept small and focuses only on the core functionality required for this laboratory assignment.

---

## 3. Core Functionalities

The application supports the following functionalities:

1. **Book Search**

   * Search for books by title, author, or other available information.

2. **Book Issue**

   * Issue an available book to a registered member.

3. **Book Return**

   * Return an issued book.

4. **Member Registration**

   * Register a new library member.

5. **Fine Calculation**

   * Calculate fines for books returned after the due date.

---

## 4. Vulnerabilities Implemented

Three vulnerabilities have been intentionally included for the purpose of security analysis.

### 4.1 SQL Injection

The application contains an insecure database query where user input can be directly included in an SQL statement.

Example:

```text
User Input → SQL Query → Database
```

An attacker may provide specially crafted input that changes the intended SQL query.

**Impact:**

* Unauthorized access to database information
* Modification of database records
* Possible deletion of records

**Recommended Fix:**

* Use prepared statements / parameterized queries.
* Never concatenate untrusted input directly into SQL queries.

---

### 4.2 Cross-Site Scripting (XSS)

The application does not properly validate or encode user-controlled data before displaying it.

For example, malicious input entered as a member name or book-related field could potentially be rendered as HTML/JavaScript when displayed.

**Impact:**

* Execution of malicious scripts in a user's browser
* Session or information theft
* Manipulation of displayed content

**Recommended Fix:**

* Validate user input.
* Apply appropriate output encoding.
* Avoid directly rendering untrusted input as HTML.

---

### 4.3 Improper Input Validation

The application does not properly validate some user inputs before processing them.

Examples include:

* Invalid book IDs
* Negative quantities
* Invalid member IDs
* Unexpected characters
* Invalid date values

**Impact:**

* Application crashes
* Incorrect database records
* Unexpected application behavior
* Potential security vulnerabilities

**Recommended Fix:**

* Validate all input before processing.
* Apply type, range, length, and format validation.
* Reject unexpected or malformed input.

---

## 5. SAST Analysis

A Static Application Security Testing (SAST) tool is used to analyze the source code without executing the application.

The SAST analysis is used to identify the intentionally introduced vulnerabilities.

The SAST results and screenshots are stored in:

```text
secure_application/sast/
secure_application/screenshots/
```

---

## 6. Testing

Test cases are provided to verify both normal functionality and security vulnerabilities.

The test cases are stored in:

```text
secure_application/testcases/
```

Testing includes:

* Valid book searches
* Invalid book searches
* Book issue and return
* Member registration
* Fine calculation
* SQL injection test inputs
* XSS test inputs
* Invalid input test cases

---

## 7. Technologies Used

* Programming Language: Java
* Database: [SQLite/MySQL/Other]
* Development Environment: [IDE/Terminal]
* SAST Tool: [SonarQube/Other SAST Tool]
* Version Control: Git and GitHub

---

## 8. Learning Objectives

Through this project, the following concepts are demonstrated:

* Secure software development
* Common application vulnerabilities
* Static Application Security Testing
* Input validation
* SQL Injection
* Cross-Site Scripting
* Vulnerability identification and remediation
* Git and GitHub based collaborative development

---

## 9. Repository

This project is part of the **CryptoLabX** repository.

```text
CryptoLabX/
└── secure_application/
```

The project follows the structure specified in Lab Assignment 3.

---

## 10. Disclaimer

The vulnerabilities in this application are intentionally introduced for educational and laboratory purposes. The application is not intended for production use.

