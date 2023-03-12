from src.ai.data_handlers.data_handler import DataHandler
from src.helpers.enums.alibaba.search_types import SearchTypes
from src.helpers.validators.check_if_url import url_validator
from src.services.alibaba.search_by_photo import alibaba_service
from src.services.amazon.search_by_rainforest import rainforest_api
from src.services.amazon.search_by_url import amazon_service

if __name__ == "__main__":
    while True:
        print("1. By photo")
        print("2. By title")
        request = str(input())
        if request == SearchTypes.PHOTO:
            print("Enter photo url")
            photo = str(input())
            if url_validator(photo):
                print(
                    "Enter number to select type of parsing\n" "1. API\n" "2. Selenium"
                )
                type_parse = int(input())

                if type_parse == 1:
                    # rainforest api
                    amazon_product_id = rainforest_api.get_products(photo)

                    # get alibaba photos
                    alibaba_product_ids = alibaba_service.search_by_photo_service(amazon_product_id)
                    #  create aws handler
                    data_handler = DataHandler(amazon_product_id, alibaba_product_ids)

                    data_handler.aws_similarity()

                elif type_parse == 2:
                    # selenium parser
                    amazon_product_id = amazon_service.search_by_url(photo)

                    alibaba_service.search_by_photo_service(amazon_product_id)

            else:
                print("Wrong url")
                break

        elif request == SearchTypes.TITLE:
            print("Enter title")
            title = str(input())

            alibaba_service.search_by_title_service(title=title)
        break
