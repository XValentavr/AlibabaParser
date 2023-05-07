import enum


class CssClasses(str, enum.Enum):
    """
    Class for selenium that describes styles
    """

    LIST_ITEM: str = "list-item"
    DECLARATIVE: str = "declarative"
    IMAGE_WRAPPER: str = "imgTagWrapper"
    LAYOUTS: str = "regularAltImageViewLayout"
    ALT_IMAGES: str = "altImages"
