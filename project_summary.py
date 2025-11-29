def print_project_summary():
    summary = """
# WebScanPro Project Documentation

## Overview
WebScanPro is an automated web application security scanner built as part of the semester project. It identifies common vulnerabilities (SQLi, XSS, authentication/session bugs, access control flaws) and produces security reports.

## Modules Implemented
- **Target Discovery**: Finds all accessible URLs and forms.
- **SQL Injection Scanner**: Detects input fields vulnerable to SQLi.
- **XSS Scanner**: Detects reflected/stored XSS injection points.
- **Authentication and Session Tester**: Checks weak credentials, cookie flags, session fixation.
- **Access Control/IDOR Tester**: Checks for privilege escalation and IDOR bugs.
- **Report Generator**: Exports structured HTML (optionally PDF) with all findings.
  
## Usage Walkthrough
1. Initialize & crawl the target: `crawler.py`
2. Run each scanner module on discovered endpoints/forms:
    - `sql_injection_tester.py`
    - `xss_tester.py`
    - `auth_session_tester.py`
    - `access_idor_tester.py`
3. Review collected vulnerabilities in output.
4. Export results using `report_generator.py`.
5. Copy this documentation and add screenshots for your final project deliverables.

## Demo Guidance
- Show code running for each module.
- Present sample output, HTML report, and how a vulnerability was detected.
- Discuss remediations and project architecture.

---
    """
    print(summary)

if __name__ == "__main__":
    print_project_summary()
