import os
from collections import OrderedDict

import ray
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from clients.alibaba.alibaba_threads import AlibabaThreads
from clients.base_client import InitDriver
from helpers.enums.alibaba.css_classes import CssClasses
import urllib.request

from helpers.envs.project_envs import ProjectEnvs


class AlibabaClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)
        # self.__s3_client = AmazonS3Client()
        self.__path = ProjectEnvs.BASE_IMAGE_URL
        self.__dict = OrderedDict()

    def __navigate(self, url: str = None) -> None:
        self.__webdriver.get(ProjectEnvs.BASE_URL if not url else url)

    def search_by_upload_photo(
        self, images: dict, stored_index: int = 0
    ) -> OrderedDict:
        ray.init()
        self.__navigate()
        # self.__webdriver.refresh()

        element = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-imgsearch-icon"
        )
        self.__action_chains.double_click(element).perform()

        # base_div_to_search = self.__webdriver.find_element(By.CLASS_NAME, CssClasses.URL_LINK)

        # upload = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-url')

        for index, image in enumerate(images.get("images").values()):
            urllib.request.urlretrieve(image, self.__path + f"test{index}.png")

        upload = self.__webdriver.find_element(By.XPATH, "//input[@type='file']")

        upload.send_keys(self.__path + f"test{stored_index}.png")

        # go_button = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-search')

        # go_button.click()

        goods = self.__webdriver.find_elements(
            By.CLASS_NAME, "bc-ife-gallery-image-box"
        )
        self.__get_good_url(goods=goods)
        os.remove(self.__path + f"test{stored_index}.png")

    def search_by_title(self, title: str) -> None:
        self.__navigate()

        search_field = self.__webdriver.find_element(By.XPATH, "//input[@type='text']")
        search_field.send_keys(title)

        search_button = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-submit"
        )

        search_button.click().perform()

    def __get_good_url(self, goods: list[WebElement]) -> OrderedDict:
        events = []
        # permanently trunk data
        for image in goods[2:4]:
            # create parallel threads
            alibaba_threads = AlibabaThreads.remote()
            url = image.get_attribute("href")
            events.append(alibaba_threads.get_images_by_threads.remote(image=url))
        print(ray.get(events))
