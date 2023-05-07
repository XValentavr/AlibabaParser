import enum


class SearchTypes(str, enum.Enum):
    """
    Search type of products. Can be selenium or api
    """

    API: str = "API"
    SELENIUM: str = "PARSE"
    TEXT: str = "TEXT"
    PHOTO: str = "PHOTO"
