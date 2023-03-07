from urllib.parse import urlparse


def url_validator(url: str) -> bool:
    """
    Thi function check if string is url. If yrl the returns true else false
    :param url: string of entered url
    :return: true or false
    """

    result = urlparse(url)
    return all([result.scheme, result.netloc])
