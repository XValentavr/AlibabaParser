import re


def remove_special_symbols(string: str):
    """
    Remove specific symbols from string
    """
    return re.sub(r"[^a-zA-Z0-9 \n\.]", "", string).strip()
