
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import socket
import ipaddress


def extract_website(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return {"success": False, "error": "Invalid URL"}

        # Block local and private network addresses
        addresses = socket.getaddrinfo(
            parsed.hostname, None, type=socket.SOCK_STREAM
        )

        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])
            if not ip.is_global:
                return {"success": False, "error": "Private or local URLs are not allowed"}

        response = requests.get(
            url,
            timeout=12,
            headers={"User-Agent": "InfoTraceAI/1.0"},
            allow_redirects=False
        )

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"Website returned status {response.status_code}"
            }

        if len(response.content) > 2_000_000:
            return {"success": False, "error": "Website is too large"}

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"

        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())

        return {
            "success": True,
            "url": url,
            "title": title,
            "content": text[:12000],
            "character_count": len(text)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
