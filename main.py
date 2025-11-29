from util import get_session, extract_links, extract_forms, is_same_domain
from crawler import Crawler
from sql_injection_tester import test_sql_injection
from xss_tester import test_xss
from auth_session_tester import test_weak_credentials, test_cookie_flags, test_session_fixation
from access_idor_tester import test_idor
from report_generator import generate_report

TARGET_URL = "http://localhost/webscanpro"  # change if needed

def run_crawler():
    print("[*] Running crawler...")
    c = Crawler(TARGET_URL, max_pages=30, delay=0.2)
    results = c.crawl()
    print(f"[+] Crawler finished. Pages: {len(results['pages'])}, forms: {sum(len(v) for v in results['forms'].values())}")
    return results

def build_form_list(crawl_results):
    all_forms = []
    for url, forms in crawl_results["forms"].items():
        for f in forms:
            entry = dict(f)
            entry["origin"] = url
            all_forms.append(entry)
    return all_forms

def run_vulnerability_scans(all_forms):
    vulnerabilities = []

    # SQL Injection scans
    print("\n[*] Running SQL Injection tests...")
    for f in all_forms:
        vulns = test_sql_injection(f["origin"], [f])
        for v in vulns:
            vulnerabilities.append({
                "type": "SQL Injection",
                "endpoint": v,
                "severity": "High",
                "description": "Potential SQL error / injection behavior detected.",
                "mitigation": "Use parameterized queries and input validation."
            })

    # XSS scans
    print("\n[*] Running XSS tests...")
    for f in all_forms:
        vulns = test_xss(f["origin"], [f])
        for v in vulns:
            vulnerabilities.append({
                "type": "Cross-Site Scripting (XSS)",
                "endpoint": v,
                "severity": "Medium",
                "description": "Reflected XSS payload appeared in response.",
                "mitigation": "Escape/encode output and validate inputs."
            })

    # Auth & session tests (use existing functions)
    print("\n[*] Running authentication and session tests...")
    test_weak_credentials()
    test_cookie_flags()
    test_session_fixation()

    # Access control / IDOR tests
    print("\n[*] Running access control / IDOR tests...")
    test_idor()

    return vulnerabilities

def main():
    print("==== WebScanPro – Main Runner ====")
    print(f"Target: {TARGET_URL}")

    crawl_results = run_crawler()
    all_forms = build_form_list(crawl_results)

    vulnerabilities = run_vulnerability_scans(all_forms)

    print("\n[*] Generating final report...")
    if not vulnerabilities:
        vulnerabilities.append({
            "type": "Info",
            "endpoint": TARGET_URL,
            "severity": "Low",
            "description": "No automatic vulnerabilities detected by current checks.",
            "mitigation": "Perform manual review and extend test payloads."
        })

    generate_report(vulnerabilities, filename="webscanpro_report.html")
    print("[+] All done. Open webscanpro_report.html in your browser to view the report.")

if __name__ == "__main__":
    main()
