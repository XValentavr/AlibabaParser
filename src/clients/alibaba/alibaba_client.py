import os
from collections import OrderedDict
from typing import Dict, Any

import ray
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import urllib.request

from src.clients.alibaba.alibaba_threads import AlibabaThreads
from src.clients.base_client import InitDriver
from src.helpers.enums.alibaba.alibaba_css_classes import CssClasses
from src.helpers.project_envs import ProjectEnvs


class AlibabaClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)
        self.__path = ProjectEnvs.BASE_IMAGE_URL
        self.__dict = OrderedDict()
        self.__ray_events = []

    def __navigate(self, url: str = None) -> None:
        self.__webdriver.get(ProjectEnvs.BASE_URL if not url else url)

    def search_by_upload_photo(
            self, images: Dict[Any, Any], stored_index: int = 0
    ) -> list[OrderedDict]:
        ray.init()
        self.__navigate()
        # self.__webdriver.refresh()

        element = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-imgsearch-icon"
        )
        self.__action_chains.double_click(element).perform()

        # base_div_to_search = self.__webdriver.find_element(By.CLASS_NAME, CssClasses.URL_LINK)

        # upload = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-url')

        for index, image in enumerate(images.get("images").values()):  # type: ignore
            urllib.request.urlretrieve(image, self.__path + f"test{index}.png")

        upload = self.__webdriver.find_element(By.XPATH, "//input[@type='file']")

        upload.send_keys(self.__path + f"test{stored_index}.png")

        # go_button = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-search')

        # go_button.click()

        goods = self.__webdriver.find_elements(
            By.CLASS_NAME, "bc-ife-gallery-image-box"
        )
        alibaba_images = self.__get_good_url(goods=goods, max_length=len(goods))
        os.remove(self.__path + f"test{stored_index}.png")

        self.__webdriver.close()

        return alibaba_images

    def search_by_title(self, title: str) -> None:
        self.__navigate()

        search_field = self.__webdriver.find_element(By.XPATH, "//input[@type='text']")
        search_field.send_keys(title)

        search_button = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-submit"
        )

        search_button.click().perform()

    def __get_good_url(self,
                       goods: list[WebElement],
                       max_length: int,
                       start_index: int = 0,
                       finish_index: int = 5) -> list[OrderedDict]:
        # permanently trunk data
        for image in goods[start_index:finish_index]:
            # create parallel threads
            alibaba_threads = AlibabaThreads.remote()
            url = image.get_attribute("href")
            self.__ray_events.append(alibaba_threads.get_images_by_threads.remote(image=url))

        ray.wait(self.__ray_events, num_returns=len(self.__ray_events))

        if finish_index <= max_length:
            self.__get_good_url(goods=goods, max_length=len(goods), start_index=finish_index, finish_index=finish_index+5)

        return ray.get(self.__ray_events)
