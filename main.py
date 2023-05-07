from services import alibaba_search_by_api
from src.helpers.enums.alibaba.search_types import SearchTypes
from src.helpers.validators.check_if_url import url_validator
from services import amazon_search_by_rainforest_api

if __name__ == "__main__":
    while True:
        print("1. By API")
        request = str(input())
        if request == SearchTypes.API:
            print("Enter photo url")
            photo = str(input())
            if url_validator(photo):
                print(
                    "Enter number to select type of parsing\n" "1. API\n" "2. Selenium"
                )
                type_parse = int(input())

                if type_parse == 1:
                    # rainforest api
                    amazon_product_id = amazon_search_by_rainforest_api.get_products(photo)
                    alibaba_product_ids = alibaba_search_by_api.get_products(
                        amazon_product_id=amazon_product_id
                    )
                #  create aws handler

            else:
                print("Wrong url")
