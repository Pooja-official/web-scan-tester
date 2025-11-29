import requests

# A list of weak/default credentials to test
CREDENTIALS = [
    ("admin", "admin"),
    ("admin", "password"),
    ("user", "password"),
    ("test", "test123")
]

LOGIN_URL = "http://localhost/webscanpro/login.php"    # Change to your login endpoint

def test_weak_credentials():
    print("Testing weak/default credentials...")
    for username, password in CREDENTIALS:
        data = {"username": username, "password": password}
        try:
            r = requests.post(LOGIN_URL, data=data, timeout=8)
            if "dashboard" in r.text.lower() or "welcome" in r.text.lower():   # adjust as per your response
                print(f"[!] Weak credential found: {username}:{password}")
            else:
                print(f"[-] {username}:{password} not accepted")
        except Exception as e:
            print(f"Error for {username}:{password} ->", e)

def test_cookie_flags():
    print("\nChecking session cookie flags...")
    # Start a session and login with a valid credential
    s = requests.Session()
    r = s.post(LOGIN_URL, data={"username": "admin", "password": "password"})
    cookies = r.cookies
    for c in cookies:
        print(f"Cookie: {c} has Secure: {c.secure} HttpOnly: {getattr(c, 'httponly', 'N/A')}")
    # For SameSite, you need to parse the Set-Cookie header
    set_cookie = r.headers.get("Set-Cookie", "")
    if "SameSite" in set_cookie:
        print("[+] SameSite flag detected in Set-Cookie header")
    else:
        print("[-] SameSite flag NOT detected")

def test_session_fixation():
    print("\nTesting session fixation...")
    # Get session cookie before login
    s = requests.Session()
    r1 = s.get(LOGIN_URL)
    pre_login_cookies = r1.cookies.get_dict()
    r2 = s.post(LOGIN_URL, data={"username": "admin", "password": "password"})
    post_login_cookies = r2.cookies.get_dict()
    if pre_login_cookies != post_login_cookies:
        print("[+] Session rotated after login (fixation defended)")
    else:
        print("[-] Session did NOT rotate after login (fixation risk)")

if __name__ == "__main__":
    test_weak_credentials()
    test_cookie_flags()
    test_session_fixation()
