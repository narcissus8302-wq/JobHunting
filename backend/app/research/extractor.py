from bs4 import BeautifulSoup
import re

class HTMLExtractor:
    def extract_text(self, html: str) -> str:
        """
        Extracts clean text from HTML, removing scripts, styles, and empty spaces.
        """
        if not html:
            return ""
        soup = BeautifulSoup(html, "html.parser")
        # Remove invisible elements
        for script in soup(["script", "style", "noscript", "meta", "head", "title", "svg"]):
            script.extract()

        text = soup.get_text(separator=" ")
        # Collapse whitespace
        return re.sub(r'\s+', ' ', text).strip()

    def extract_links(self, html: str) -> list[str]:
        """Extracts valid absolute and relative href links."""
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        # Filter out anchors, mailto, javascript
        valid_links = [l for l in links if l and not l.startswith(('javascript:', 'mailto:', '#'))]
        return valid_links

    def extract_metadata(self, html: str) -> dict:
        """Extracts title, description, and key metadata tags for intelligence."""
        if not html:
            return {}
        soup = BeautifulSoup(html, "html.parser")
        meta = {}

        if soup.title:
            meta['title'] = soup.title.string

        description_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        if description_tag:
            meta['description'] = description_tag.get('content', '')

        return meta
