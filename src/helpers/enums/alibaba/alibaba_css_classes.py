import enum


class CssClasses(str, enum.Enum):
    """
    Class for selenium that describes styles
    """

    SEARCHBAR: str = "ui-searchbar"
    URL_LINK: str = "image-upload-link"
