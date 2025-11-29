import re
import time
from urllib.parse import urljoin, urlparse, parse_qs, urlencode

import requests
from bs4 import BeautifulSoup

# Default HTTP headers
DEFAULT_HEADERS = {
    "User-Agent": "WebScanPro/1.0 (+https://github.com/yourname/WebScanPro)"
}

# SQL Injection error patterns
SQL_ERROR_PATTERNS = [
    r"sql syntax",
    r"mysql_fetch",
    r"you have an error in your sql syntax",
    r"unterminated quoted string",
    r"oracle error",
    r"sqlstate",
    r"pdoexception",
    r"mysqli_sql",
    r"syntax error.*near",
]

# XSS reflection patterns
XSS_REFLECT_PATTERNS = [
    r"<script>alert\(",
]


def get_session():
    """Return a requests.Session with default headers."""
    s = requests.Session()
    s.headers.update(DEFAULT_HEADERS)
    return s


def is_same_domain(base, url):
    """Check if two URLs belong to the same domain."""
    return urlparse(base).netloc == urlparse(url).netloc


def normalize_url(base, link):
    """Return absolute URL built from base + relative link."""
    if not link:
        return None
    return urljoin(base, link)


def extract_links(html, base_url):
    """Extract all links (a, link, area, form action) from a page."""
    soup = BeautifulSoup(html, "lxml")
    out = set()

    for tag in soup.find_all(["a", "link", "area"]):
        href = tag.get("href")
        if href:
            full = normalize_url(base_url, href)
            if full:
                out.add(full)

    # include form actions
    for form in soup.find_all("form"):
        action = form.get("action") or base_url
        full = normalize_url(base_url, action)
        if full:
            out.add(full)

    return out


def extract_forms(html, base_url):
    """Extract all forms with method, action and inputs."""
    soup = BeautifulSoup(html, "lxml")
    forms = []

    for form in soup.find_all("form"):
        method = (form.get("method") or "get").lower()
        action = normalize_url(base_url, form.get("action") or base_url)

        inputs = []
        for inp in form.find_all(["input", "textarea", "select"]):
            name = inp.get("name")
            if not name:
                continue
            input_type = inp.get("type", "text")
            value = inp.get("value") or ""
            inputs.append({"name": name, "type": input_type, "value": value})

        forms.append({"method": method, "action": action, "inputs": inputs})

    return forms


def find_sql_errors(text):
    """Return (True, pattern) if SQL error pattern is found in text."""
    t = text.lower()
    for pat in SQL_ERROR_PATTERNS:
        if re.search(pat.lower(), t):
            return True, pat
    return False, None
