import uuid
from typing import List

from create_engine import session
from cruds.urls_cruds import UrlsCRUDS
from cruds.videos_cruds import VideosCRUDS
from models.alibaba_source_model import AlibabaSourceModel
from models.product_keywords import ProductKeywords
from models.url_model import URLModel


class AlibabaCRUDS:
    """
    Class to crate alibaba data CRUDS
    """

    def __init__(self):
        self.__url_cruds = UrlsCRUDS()
        self.__video_cruds = VideosCRUDS()

    def update_alibaba_product_by_id(
            self,
            product_id: uuid.UUID,
            description: str = None,
            min_price: str = None,
            max_price: str = None,
            rrp_price: str = None,
            images: str = None,
            videos: str = None,
            link: str = None,
            title: str = None
    ):
        """
        Update existing alibaba data by entering new

        :param product_id: current product id
        :param description: product description
        :param min_price: product min price
        :param max_price: product max price
        :param rrp_price: product rrp price
        :param images: product all images
        :param videos: product all videos
        :return: None
        """
        prod_id = self.__get_alibaba_product_by_id(product_id)
        prod_id.description = description if description else prod_id.description
        prod_id.min_price = min_price if min_price else prod_id.min_price
        prod_id.max_price = max_price if max_price else prod_id.max_price
        prod_id.rrp_price = rrp_price if rrp_price else prod_id.rrp_price
        prod_id.link = link if link else prod_id.link
        prod_id.title = title if title else prod_id.title

        session.commit()

        if images:
            self.__url_cruds.insert_many_images(link=images, alibaba_id=product_id)
        elif videos:
            self.__video_cruds.insert_many_videos(link=videos, alibaba_id=product_id)

    @staticmethod
    def __get_alibaba_product_by_id(product_id: uuid.UUID) -> AlibabaSourceModel:
        """
        Get alibaba product using UUID
        :param product_id: product unique UUID
        :return: existing alibaba product data
        """
        return (
            session.query(AlibabaSourceModel)
            .filter(AlibabaSourceModel.id == product_id)
            .first()
        )

    @staticmethod
    def insert_alibaba_products(title: str = None, link: str = None):
        """
        Insert new alibaba product information
        :param title: alibaba product title
        :param link: alibaba product link
        :return: unique alibaba UUID identifier
        """
        alibaba_id = uuid.uuid4()

        alibaba_product = AlibabaSourceModel(id=alibaba_id, title=title, link=link)
        session.add(alibaba_product)
        session.commit()
        return alibaba_id

    @staticmethod
    def get_alibaba_product_photo_by_id(product_id: uuid.UUID) -> List[URLModel]:
        """
        Get alibaba product from database using UUID
        :param product_id: unique alibaba UUID
        :return: existing alibaba product
        """
        return (
            session.query(URLModel)
            .filter(URLModel.alibaba_product_id == product_id)
            .all()
        )

    @staticmethod
    def get_alibaba_product_keywords(product_id: uuid.UUID) -> List[ProductKeywords]:
        """
        get from database alibaba keywords to compare
        :param product_id: unique alibaba UUID
        :return: existing alibaba product
        """
        return (
            session.query(ProductKeywords)
            .filter(ProductKeywords.alibaba_source_id == product_id)
            .all()
        )

    @staticmethod
    def remove_alibaba_product_by_id(product_id):
        """
        removes alibaba product using id
        :param product_id: unique alibaba UUID
        :return: None
        """
        (
            session.query(AlibabaSourceModel)
            .filter(AlibabaSourceModel.id == product_id)
            .delete()
        )
        session.commit()

    @staticmethod
    def remove_alibaba_product_all():
        """
        removes all  alibaba product
        :return: None
        """
        session.query(AlibabaSourceModel).delete()
        session.commit()
