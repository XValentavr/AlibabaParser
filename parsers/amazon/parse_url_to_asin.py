import re


class ParseUrlToAsin:
    def __init__(self, url: str) -> str or None:
        self.url = url

    def parse(self) -> str or None:
        asin = re.search(r"/[dg]p/([^/]+)", self.url, flags=re.IGNORECASE)
        if asin:
            return asin.group(1)
        return None
