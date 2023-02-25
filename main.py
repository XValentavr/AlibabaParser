from helpers.envs.alibaba.search_types import SearchTypes
from helpers.validators.check_if_url import url_validator
from services.alibaba.search_by_photo import search_by_photo_service
from services.alibaba.search_by_titile import search_by_title_service

if __name__ == "__main__":
    while True:
        print("1. By photo")
        print("2. By title")
        request = str(input())
        if request == SearchTypes.PHOTO:
            print("Enter photo url")
            photo = str(input())
            if url_validator(photo):
                search_by_photo_service(photo=photo)
            else:
                print("Wrong url")
                break
        elif request == SearchTypes.TITLE:
            print("Enter title")
            title = str(input())
            search_by_title_service(title=title)
        break
