import requests

BASE_URL = "http://localhost/webscanpro/"  # Change to your system
ENDPOINT = BASE_URL + "profile.php?id={id}"  # Example vulnerable endpoint

# Assume you know test users with ids 1 and 2; simulate as user1 and user2 cookies
USER1_COOKIE = {"session": "user1sessionid"} 
USER2_COOKIE = {"session": "user2sessionid"} 

def test_idor():
    print("Testing for IDOR...")
    for target_id in [1, 2]:
        # Try user1 accessing user2's data
        r = requests.get(ENDPOINT.format(id=target_id), cookies=USER1_COOKIE)
        if "user2-data" in r.text.lower():
            print(f"[!] IDOR risk: user1 accessed data of user id {target_id}")
        else:
            print(f"[-] Access controlled for user id {target_id}")
        # Try privilege escalation (vertical)
        admin_cookie = {"session": "adminsessionid"}
        r2 = requests.get(ENDPOINT.format(id=target_id), cookies=admin_cookie)
        if "admin-section" in r2.text.lower():
            print(f"[!] Vertical escalation: Normal user session got admin section!")
        else:
            print(f"[-] No vertical escalation for user id {target_id}")

if __name__ == "__main__":
    test_idor()
