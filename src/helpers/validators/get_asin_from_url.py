import re
from typing import Union


def get_asin_from_url(url) -> Union[None, str]:
    """
    get amazon asin from income product url
    :return: existing asin or None
    """
    asin = re.search(r"(?:/dp/|/gp/product/)([A-Z0-9]{10})", url, flags=re.IGNORECASE)
    if asin:
        return asin.group(1)
    return None
