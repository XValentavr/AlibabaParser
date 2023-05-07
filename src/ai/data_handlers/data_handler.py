import logging
from math import ceil
from typing import List
from uuid import UUID

from ai.aws.amazon import amazon_ai
from cruds.alibaba_cruds import AlibabaCRUDS
from cruds.amazon_cruds import AmazonCRUDS
from cruds.product_keywords_cruds import ProductKeywordsCRUDS
from cruds.result_similarity_cruds import ResultSimilarityCRUDS
from cruds.similiraty_cruds import SimilarityCRUDS
from helpers.init_logger import create_logger


class DataHandler:
    """
    Class to work with similarity
    """

    def __init__(self, amazon: UUID, alibaba: List[UUID]):
        self.__amazon = amazon
        self.__alibaba = alibaba
        self.__aws = amazon_ai
        self.__logger = create_logger()

        self.__similarity_cruds = SimilarityCRUDS()
        self.__amazon_cruds = AmazonCRUDS()
        self.__alibaba_cruds = AlibabaCRUDS()
        self.__most_similar_cruds = ResultSimilarityCRUDS()
        self.__product_keywords = ProductKeywordsCRUDS()

    def aws_similarity_images(self):
        """
        Get AWS similarity using alibaba and amazon urls
        :return: None
        """
        amazon_images = self.__amazon_cruds.get_amazon_product_photo_by_id(
            self.__amazon
        )

        try:
            for am_image in amazon_images:
                for alibaba_product_id in self.__alibaba:
                    for al_image in self.__alibaba_cruds.get_alibaba_product_photo_by_id(
                            alibaba_product_id
                    ):

                        #  if product is already in database with good similarity then don`t check
                        already_in_similar = self.__most_similar_cruds.get_result_similarity_by_alibaba_id(
                            alibaba_product_id
                        )
                        if len(already_in_similar) != 0:
                            break

                        similarity = self.__aws.image_similarity(
                            image_amazon_url=am_image.link,
                            image_alibaba_url=al_image.link,
                        )
                        print('similarity', similarity)
                        print('ceil', ceil(round((float(similarity.get("similarity"))) * 100) + 0.01)
                              )
                        if (
                                ceil(round((float(similarity.get("similarity"))) * 100) + 0.01)
                                >= self.__get_similarity()
                        ):
                            print('similarity.get("similarity")', similarity)
                            self.__most_similar_cruds.insert_result_similarity(
                                amazon_product_id=am_image.amazon_product_id,
                                alibaba_product_id=al_image.alibaba_product_id,
                                similarity=similarity.get("similarity"),
                            )

                alibaba_and_amazon_is_similar = (
                    self.__most_similar_cruds.get_result_similarity_by_amazon_id(
                        amazon_id=am_image.amazon_product_id
                    )
                )

                if alibaba_and_amazon_is_similar:
                    break

            # check product if their similarity is between 0.5 and 0.9
            # self.__additional_checking_if_more_than_07()

        except Exception:
            self.__logger.setLevel(logging.DEBUG)

    def __additional_checking_if_more_than_07(self):
        """
        Additional checking for similar images
        :return: None
        """
        product_for_more_checking = (
            self.__most_similar_cruds.get_result_similarity_between(
                amazon_product_id=self.__amazon,
                start_similarity=0.69,
                end_similarity=0.95,
            )
        )

        if not product_for_more_checking:
            return None

        amazon_keywords = self.__product_keywords.get_amazon_product_keywords(self.__amazon)
        for alibaba_product_id in self.__alibaba:
            alibaba_keywords = self.__product_keywords.get_alibaba_product_keywords(alibaba_product_id)
            text_similarity = self.__aws.text_similarity(amazon_keywords=amazon_keywords,
                                                         alibaba_keywords=alibaba_keywords)
            print('text_similarity', text_similarity)
            if float(text_similarity.get("similarity")) * 100 <= 50:
                self.__most_similar_cruds.remove_not_similar_products(amazon_id=self.__amazon,
                                                                      alibaba_id=alibaba_product_id)

    def __get_similarity(self) -> float:
        """
        Get image similarity from database
        :return: image similarity
        """
        similarity = self.__similarity_cruds.get_similarity()
        return float(similarity.similarity) * 100
