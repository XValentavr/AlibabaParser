import os
import pickle
from collections import OrderedDict
from os.path import join, abspath, dirname
from typing import List
from uuid import UUID

import ray
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import urllib.request

from clients.alibaba.alibaba_threads import AlibabaThreads
from clients.InitDriver import init_driver
from cruds.amazon_cruds import AmazonCRUDS
from helpers.enums.alibaba.alibaba_css_classes import CssClasses
from helpers.init_logger import create_logger
from helpers.project_envs import ProjectEnvs


class AlibabaClient:
    def __init__(self):
        self.__path = join(dirname(dirname(dirname(abspath(__file__)))), 'image_storage\\')
        self.__init_driver = init_driver
        self.__amazon_cruds = AmazonCRUDS()
        self.__ray_events = []
        self.__step = 5
        self.__logger = create_logger()

    def __generate_webdriver_instance(self) -> WebDriver:
        return self.__init_driver.create_instance_of_driver()

    @staticmethod
    def __navigate(main_webdriver: WebDriver, url: str = None) -> None:
        main_webdriver.get(ProjectEnvs.BASE_URL if not url else url)

    def search_by_upload_photo(self, amazon_product_id: UUID, current_image_to_search_id: int = 0) -> List[OrderedDict]:

        try:
            ray.init(ignore_reinit_error=True)
        except Exception as error:
            self.__logger.error(error)

        main_webdriver = self.__generate_webdriver_instance()

        self.__navigate(main_webdriver=main_webdriver)
        # main_webdriver.refresh()

        element = main_webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-imgsearch-icon"
        )
        ActionChains(main_webdriver).double_click(element).perform()

        # base_div_to_search = main_webdriver.find_element(By.CLASS_NAME, CssClasses.URL_LINK)

        # upload = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-url')
        try:
            images = self.__amazon_cruds.get_amazon_product_photo_by_id(
                product_id=amazon_product_id
            )

            for index, image in enumerate(images):  # type: ignore
                urllib.request.urlretrieve(image.link, self.__path + f"test{index}.png")

            upload = main_webdriver.find_element(By.XPATH, "//input[@type='file']")

            upload.send_keys(self.__path + f"test{current_image_to_search_id}.png")
        except Exception as error:
            self.__logger.error(error)
        # go_button = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-search')

        # go_button.click()
        try:
            goods = main_webdriver.find_elements(By.CLASS_NAME, "bc-ife-gallery-image-box")

            alibaba_image_ids = self.__get_good_url(goods=goods, max_length=len(goods))

            main_webdriver.quit()

            ray.shutdown()
            return alibaba_image_ids
        except Exception as error:
            self.__logger.error(error)
        finally:
            os.remove(self.__path + f"\\test{current_image_to_search_id}.png")
        return []

    def search_by_title(self, title: str, main_webdriver: WebDriver) -> None:
        try:
            self.__navigate(main_webdriver=main_webdriver)

            search_field = main_webdriver.find_element(By.XPATH, "//input[@type='text']")
            search_field.send_keys(title)

            search_button = main_webdriver.find_element(
                By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-submit"
            )

            search_button.click().perform()
        except Exception as error:
            self.__logger.error(error)

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

            serialized = pickle.dumps(alibaba_threads)

            deserialized = pickle.loads(serialized)

            url = image.get_attribute("href")
            self.__ray_events.append(
                deserialized.get_images_by_threads.remote(image=url)
            )

        ray.wait(self.__ray_events, num_returns=len(self.__ray_events))

        if changed_finish_index <= max_length or changed_finish_index < 6:
            return self.__get_good_url(
                goods=goods,
                max_length=len(goods),
                start_index=changed_finish_index,
                finish_index=changed_finish_index + 5,
            )
