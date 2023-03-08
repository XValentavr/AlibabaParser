from collections import OrderedDict

from src.ai.aws.amazon import amazon_ai


class DataHandler:
    def __init__(self, amazon: OrderedDict, alibaba: OrderedDict):
        self.amazon = dict(amazon)
        self.alibaba = alibaba
        self.aws = amazon_ai
        self.similarity_rate = 90.0

    def aws_similarity(self):
        amazon_link, amazon_images = self.__extract_product_data(self.amazon)
        for am_image in amazon_images.values():
            for dicts in self.alibaba:
                alibaba_link, alibaba_images = self.__extract_product_data(dicts)
                for al_image in alibaba_images.values():
                    print(al_image)
                    # similarity = self.aws.image_similarity(
                    #     image_amazon_url=am_image, image_alibaba_url=al_image
                    # )
                    # if float(similarity.get("similarity")) * 100 >= self.similarity_rate:
                    #     print(similarity)
                    #     print("more than")
                    # write next logic
                    break
                break
            break

    @staticmethod
    def __extract_product_data(product: dict):
        return product.get("link"), product.get("images")

    def change_similarity(self, new_rate: float):
        self.similarity_rate = new_rate
