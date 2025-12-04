## WebScanPro – Web Application Security Scanner

This repository contains "WebScanPro", a Python‑based tool that performs basic security testing on web applications and generates a clear, colourful HTML report of all findings.
It was developed as a learning project to practice web security concepts such as SQL Injection, XSS, IDOR and insecure session handling, along with Python scripting and automation.

## Features

- Crawls a target web application and discovers links to test.
- Runs automated checks for:
  - SQL Injection
  - Cross‑Site Scripting (XSS)
  - Insecure Direct Object References (IDOR)
  - Weak / missing session cookie flags (HttpOnly, Secure, SameSite).
- Produces "webscanpro_report.html":
  - Summary of total findings.
  - Table of vulnerabilities with type, endpoint, parameter, payload, evidence and severity.
  - High‑level remediation suggestions for each vulnerability category.

## Tech Stack
- Standard Python libraries ("requests", "BeautifulSoup", etc.).
- Developed and tested in VS Code with Git and GitHub for version control.

## Project Status
This is a student project created for practicing web application security testing and Python automation.
Future improvements could include more vulnerability modules, better error handling, authentication support and a simple web UI.


## Author
**Pooja**

