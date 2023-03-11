from collections import OrderedDict

from src.ai.aws.amazon import amazon_ai


class DataHandler:
    def __init__(self, amazon: OrderedDict, alibaba: OrderedDict):
        self.__amazon = amazon
        self.__alibaba = alibaba
        self.__aws = amazon_ai
        self.__similarity_rate = 90.0
        self.__similar = list()

    def aws_similarity(self):
        _, amazon_images = self.__extract_product_data(self.__amazon)
        for am_image in dict(amazon_images).values():
            for dicts in self.__alibaba:
                _, alibaba_images = self.__extract_product_data(dicts)
                for al_image in alibaba_images.values():
                    is_break = False
                    similarity = self.__aws.image_similarity(
                        image_amazon_url=am_image, image_alibaba_url=al_image
                    )
                    if float(similarity.get("similarity")) * 100 >= self.similarity_rate:
                        self.__similar.append(self.__amazon)
                        self.__similar.append(dicts)
                        is_break = True
                        break
                if is_break:
                    break
            break

    @staticmethod
    def __extract_product_data(product: dict):
        return product.get("link"), product.get("images")

    def change_similarity(self, new_rate: float):
        self.__similarity_rate = new_rate
