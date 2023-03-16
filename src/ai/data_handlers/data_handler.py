from typing import List
from uuid import UUID

from ai.aws.amazon import amazon_ai
from cruds.alibaba_cruds import AlibabaCRUDS
from cruds.amazon_cruds import AmazonCRUDS
from cruds.result_similarity_cruds import ResultSimilarityCRUDS
from cruds.similiraty_cruds import SimilarityCRUDS
from helpers.init_logger import create_logger


class DataHandler:
    def __init__(self, amazon: UUID, alibaba: List[UUID]):
        self.__amazon = amazon
        self.__alibaba = alibaba
        self.__aws = amazon_ai

        self.__similarity_cruds = SimilarityCRUDS()
        self.__amazon_cruds = AmazonCRUDS()
        self.__alibaba_cruds = AlibabaCRUDS()
        self.__most_similar_cruds = ResultSimilarityCRUDS()
        self.__logger = create_logger()

    def aws_similarity(self):
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
                            alibaba_product_id)
                        if len(already_in_similar) != 0:
                            break

                        similarity = self.__aws.image_similarity(
                            image_amazon_url=am_image.link, image_alibaba_url=al_image.link
                        )
                        if (
                                float(similarity.get("similarity")) * 100
                                >= self.__get_similarity()
                        ):
                            print('similarity.get("similarity")', similarity)
                            self.__most_similar_cruds.insert_result_similarity(
                                amazon_product_id=am_image.amazon_product_id,
                                alibaba_product_id=al_image.alibaba_product_id,
                                similarity=similarity.get("similarity"),
                            )

                alibaba_and_amazon_is_similar = self.__most_similar_cruds.get_result_similarity_by_amazon_id(
                    amazon_id=am_image.amazon_product_id)

                if alibaba_and_amazon_is_similar:
                    break

            # check product if their similarity is between 0.5 and 0.9
            self.__additional_checking()

        except Exception as error:
            self.__logger.error(error)

    def __additional_checking(self):
        product_for_more_checking = self.__most_similar_cruds.get_result_similarity_between(0.5, 0.9)
        if not product_for_more_checking:
            return None
        print('product_for_more_checking', product_for_more_checking)

    def change_similarity(self, new_rate: float):
        self.__similarity_cruds.change_similarity(new_similarity=new_rate)

    def __get_similarity(self) -> float:
        similarity = self.__similarity_cruds.get_similarity()
        return float(similarity.similarity) * 100
