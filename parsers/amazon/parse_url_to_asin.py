import re


class ParseUrlToAsin:
    def __init__(self, url):
        self.url = url

    def parse(self):
        asin = re.search(r"/[dg]p/([^/]+)", self.url, flags=re.IGNORECASE)
        if asin:
            return asin.group(1)
        return None
