import os
from collections import OrderedDict
from typing import List
from uuid import UUID

import ray
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import urllib.request

from clients.alibaba.alibaba_threads import AlibabaThreads
from clients.base_client import InitDriver
from cruds.amazon_cruds import AmazonCRUDS
from helpers.enums.alibaba.alibaba_css_classes import CssClasses
from helpers.project_envs import ProjectEnvs


class AlibabaClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)
        self.__path = ProjectEnvs.BASE_IMAGE_URL
        self.__amazon_cruds = AmazonCRUDS()
        self.__ray_events = []
        self.__step = 5

    def __navigate(self, url: str = None) -> None:
        print(url)
        self.__webdriver.get(ProjectEnvs.BASE_URL if not url else url)

    def search_by_upload_photo(self, amazon_product_id: UUID) -> List[OrderedDict]:
        try:
            ray.init()
            self.__navigate()
            # self.__webdriver.refresh()

            element = self.__webdriver.find_element(
                By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-imgsearch-icon"
            )
            self.__action_chains.double_click(element).perform()

            # base_div_to_search = self.__webdriver.find_element(By.CLASS_NAME, CssClasses.URL_LINK)

            # upload = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-url')
            images = self.__amazon_cruds.get_amazon_product_photo_by_id(
                product_id=amazon_product_id
            )

            for index, image in enumerate(images):  # type: ignore
                urllib.request.urlretrieve(image.link, self.__path + f"test{index}.png")

            upload = self.__webdriver.find_element(By.XPATH, "//input[@type='file']")

            upload.send_keys(self.__path + f"test0.png")

            # go_button = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-search')

            # go_button.click()

            goods = self.__webdriver.find_elements(
                By.CLASS_NAME, "bc-ife-gallery-image-box"
            )
            alibaba_image_ids = self.__get_good_url(goods=goods, max_length=len(goods))

            os.remove(self.__path + f"test0.png")

            self.__webdriver.quit()
            return alibaba_image_ids
        except Exception as e:
            print(e)
            self.__webdriver.quit()

    def search_by_title(self, title: str) -> None:
        self.__navigate()

        search_field = self.__webdriver.find_element(By.XPATH, "//input[@type='text']")
        search_field.send_keys(title)

        search_button = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-submit"
        )

        search_button.click().perform()

    def __get_good_url(
            self,
            goods: List[WebElement],
            max_length: int,
            start_index: int = 0,
            finish_index: int = 5,
    ) -> List[OrderedDict]:

        if start_index >= max_length:
            return ray.get(self.__ray_events)

        changed_finish_index = (
            finish_index if finish_index <= max_length else max_length
        )

        # permanently trunk data
        for image in goods[start_index:finish_index]:
            # create parallel threads
            alibaba_threads = AlibabaThreads.remote()
            url = image.get_attribute("href")
            self.__ray_events.append(
                alibaba_threads.get_images_by_threads.remote(image=url)
            )

        ray.wait(self.__ray_events, num_returns=len(self.__ray_events))

        if changed_finish_index <= max_length:
            return self.__get_good_url(
                goods=goods,
                max_length=len(goods),
                start_index=changed_finish_index,
                finish_index=changed_finish_index + 5,
            )
