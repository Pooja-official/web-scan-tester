import time
import requests
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, base_url, max_pages=50, delay=0.2):
        self.base = base_url.rstrip('/')
        self.visited = set()
        self.queue = [self.base]
        self.pages = {}
        self.forms = {}
        self.max_pages = max_pages
        self.delay = delay

    def _is_same_domain(self, url):
        return urlparse(url).netloc == urlparse(self.base).netloc

    def _extract_links(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for a in soup.find_all("a", href=True):
            l = urljoin(url, a["href"])
            l = urldefrag(l)[0]
            if l.startswith("http") and self._is_same_domain(l):
                links.add(l.rstrip("/"))
        return links

    def _extract_forms(self, html):
        soup = BeautifulSoup(html, "html.parser")
        forms = []
        for form in soup.find_all("form"):
            data = {
                "action": form.get("action"),
                "method": form.get("method"),
                "inputs": []
            }
            for inp in form.find_all(["input", "textarea", "select"]):
                data["inputs"].append({
                    "name": inp.get("name"),
                    "type": inp.get("type"),
                    "value": inp.get("value")
                })
            forms.append(data)
        return forms

    def crawl(self):
        pages_crawled = 0
        while self.queue and pages_crawled < self.max_pages:
            url = self.queue.pop(0)
            if url in self.visited:
                continue
            try:
                r = requests.get(url, timeout=10)
                html = r.text
            except Exception as e:
                print(f"[!] Failed to fetch {url}: {e}")
                self.visited.add(url)
                continue

            self.pages[url] = html
            forms = self._extract_forms(html)
            if forms:
                self.forms[url] = forms

            for l in self._extract_links(html, url):
                if l not in self.visited and l not in self.queue:
                    self.queue.append(l)

            self.visited.add(url)
            pages_crawled += 1
            time.sleep(self.delay)
        return {"pages": self.pages, "forms": self.forms}

if __name__ == "__main__":
    start_url = "http://localhost/webscanpro"  # Change to your site
    C = Crawler(start_url, max_pages=20)
    results = C.crawl()
    print("Pages discovered:", list(results["pages"].keys()))
    print("Forms discovered:", results["forms"])
