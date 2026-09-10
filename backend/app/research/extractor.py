from bs4 import BeautifulSoup

class HTMLExtractor:
    def extract_text(self, html: str) -> str:
        """
        Extracts clean text from HTML, removing scripts and styles.
        """
        soup = BeautifulSoup(html, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=" ")
        return " ".join(text.split())

    def extract_links(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        return links
