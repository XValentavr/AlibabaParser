from helpers.enums.alibaba.search_types import SearchTypes
from helpers.validators.check_if_url import url_validator
from services.alibaba.search_by_photo import alibaba_service
from services.amazon.search_by_url import amazon_service

if __name__ == "__main__":
    while True:
        print("1. By photo")
        print("2. By title")
        request = str(input())
        if request == SearchTypes.PHOTO:
            print("Enter photo url")
            photo = str(input())
            if url_validator(photo):
                image_list = amazon_service.search_by_url(photo)
                # alibaba_service.search_by_photo_service(images=image_list)
            else:
                print("Wrong url")
                break
        elif request == SearchTypes.TITLE:
            print("Enter title")
            title = str(input())
            alibaba_service.search_by_title_service(title=title)
        break
