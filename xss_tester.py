import requests

# Simple XSS payload
XSS_PAYLOAD = "<script>alert('XSS')</script>"

def test_xss(url, forms):
    """
    Test the given URL/forms for reflected XSS.
    'forms' should be a list of form dictionaries:
        { 'action': ..., 'method': ..., 'inputs': [ {name, type, value}, ... ] }
    Returns a list of vulnerable endpoints (URLs).
    """
    vulnerable = []

    for form in forms:
        action = form.get("action") or url
        method = (form.get("method") or "get").lower()

        data = {}
        for inp in form.get("inputs", []):
            name = inp.get("name")
            if name:
                data[name] = XSS_PAYLOAD

        target_url = action if action.startswith("http") else url

        try:
            if method == "post":
                r = requests.post(target_url, data=data, timeout=8)
            else:
                r = requests.get(target_url, params=data, timeout=8)

            # If the payload appears in the response, treat it as reflected XSS
            if XSS_PAYLOAD in r.text:
                print(f"[!] XSS payload reflected at {target_url}")
                vulnerable.append(target_url)
            else:
                print(f"[+] No obvious XSS vulnerability found for {target_url}")

        except Exception as e:
            print(f"[!] Error testing {target_url}: {e}")

    return vulnerable

if __name__ == "__main__":
    # Small self‑test example; you can ignore or change this.
    test_forms = [
        {
            "action": "http://localhost/webscanpro/search.php",
            "method": "get",
            "inputs": [{"name": "q", "type": "text", "value": ""}],
        }
    ]
    vulns = test_xss("http://localhost/webscanpro/search.php", test_forms)
    print("Vulnerable endpoints:", vulns)
