import uuid
from typing import Optional, List

from create_engine import session
from cruds.urls_cruds import UrlsCRUDS
from cruds.videos_cruds import VideosCRUDS
from models.amazon_source_model import AmazonSourceModel
from models.product_keywords import ProductKeywords
from models.url_model import URLModel


class AmazonCRUDS:
    def __init__(self):
        self.__url_cruds = UrlsCRUDS()
        self.__video_cruds = VideosCRUDS()

    def update_amazon_product_by_id(
            self,
            product_id: uuid.UUID,
            description: str = None,
            min_price: str = None,
            max_price: str = None,
            rrp_price: str = None,
            images: str = None,
            videos: str = None,
    ):
        """
        Update existing amazon data by entering new

        :param product_id: current product id
        :param description: product description
        :param min_price: product min price
        :param max_price: product max price
        :param rrp_price: product rrp price
        :param images: product all images
        :param videos: product all videos
        :return: None
        """
        prod_id = self.__get_amazon_product_by_id(product_id)

        prod_id.description = description if description else prod_id.description
        prod_id.min_price = min_price if min_price else prod_id.min_price
        prod_id.max_price = max_price if max_price else prod_id.max_price
        prod_id.rrp_price = rrp_price if rrp_price else prod_id.rrp_price

        session.commit()

        if images:
            self.__url_cruds.insert_many_images(link=images, amazon_id=product_id)
        elif videos:
            self.__video_cruds.insert_many_videos(link=videos, amazon_id=product_id)

    @staticmethod
    def __get_amazon_product_by_id(product_id: uuid.UUID) -> AmazonSourceModel:
        """
        Get amazon product using UUID
        :param product_id: product unique UUID
        :return: existing amazon product data
        """
        return (
            session.query(AmazonSourceModel)
            .filter(AmazonSourceModel.id == product_id)
            .first()
        )

    @staticmethod
    def insert_amazon_products(title: Optional[str] = None, link: Optional[str] = None):
        """
        Insert new amazon product information
        :param title: amazon product title
        :param link: amazon product link
        :return: unique amazon UUID identifier
        """
        amazon_id = uuid.uuid4()

        alibaba_product = AmazonSourceModel(id=amazon_id, title=title, link=link)
        session.add(alibaba_product)
        session.commit()
        return amazon_id

    @staticmethod
    def get_amazon_product_photo_by_id(product_id: uuid.UUID) -> List[URLModel]:
        """
        Get amazon product from database using UUID
        :param product_id: unique amazon UUID
        :return: existing alibaba product
        """
        return (
            session.query(URLModel)
            .filter(URLModel.amazon_product_id == product_id)
            .all()
        )

    @staticmethod
    def get_amazon_product_keywords(product_id: uuid.UUID) -> List[ProductKeywords]:
        """
        get from database amazon keywords to compare
        :param product_id: unique alibaba UUID
        :return: existing amazon product
        """
        return (
            session.query(ProductKeywords)
            .filter(ProductKeywords.amazon_source_id == product_id)
            .all()
        )

    @staticmethod
    def remove_amazon_product_by_id(product_id: uuid.UUID):
        """
        Delete specific amazon product
        :param product_id: amazon product UUID
        :return: None
        """
        (session.query(AmazonSourceModel)
         .filter(AmazonSourceModel.id == product_id)
         .delete()
         )

        session.commit()

    @staticmethod
    def remove_amazon_product_all():
        """
        Delete all amazon products
        :return: None
        """
        session.query(AmazonSourceModel).delete()
        session.commit()
