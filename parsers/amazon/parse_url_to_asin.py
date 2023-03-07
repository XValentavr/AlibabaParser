import re
from typing import Union


class ParseUrlToAsin:
    def __init__(self, url: str):
        self.url = url

    def parse(self) -> Union[None, str]:
        asin = re.search(r"/[dg]p/([^/]+)", self.url, flags=re.IGNORECASE)
        if asin:
            return asin.group(1)
        return None
