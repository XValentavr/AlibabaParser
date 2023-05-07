import logging
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

from clients.alibaba.selenium.alibaba_threads import AlibabaThreads
from clients.InitDriver import init_driver
from cruds.amazon_cruds import AmazonCRUDS
from helpers.enums.alibaba.alibaba_css_classes import CssClasses
from helpers.init_logger import create_logger
from helpers.project_envs import ProjectEnvs


class AlibabaClient:
    """
    This class is needed in order to get a product with api using selenium
    """

    def __init__(self):
        self.__path = join(
            dirname(dirname(dirname(abspath(__file__)))), "image_storage\\"
        )
        self.__init_driver = init_driver
        self.__amazon_cruds = AmazonCRUDS()
        self.__ray_events = []
        self.__step = 5
        self.__logger = create_logger()

    def __generate_webdriver_instance(self) -> WebDriver:
        """
        This method is needed to create chrome instance
        :return: chrome instance to work with
        """
        return self.__init_driver.create_instance_of_driver()

    @staticmethod
    def __navigate(main_webdriver: WebDriver, url: str = None) -> None:
        """
        Navigate chrome to entered url
        :param main_webdriver: chrome instance
        :param url: url to go on
        :return: None
        """
        main_webdriver.get(ProjectEnvs.BASE_URL if not url else url)

    def search_by_upload_photo(
        self, amazon_product_id: UUID, current_image_to_search_id: int = 0
    ) -> List[OrderedDict]:
        """
        This main method needed to search product by amazon photo
        :param current_image_to_search_id: num of image to search
        :param amazon_product_id: amazon product id to rely on
        :return: return actual alibaba product ids
        """
        try:
            ray.init(ignore_reinit_error=True)
        except Exception:
            self.__logger.setLevel(logging.DEBUG)

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
        except Exception:
            self.__logger.setLevel(logging.DEBUG)
        # go_button = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-search')

        # go_button.click()
        try:
            goods = main_webdriver.find_elements(
                By.CLASS_NAME, "bc-ife-gallery-image-box"
            )

            alibaba_image_ids = self.__get_good_url(goods=goods, max_length=len(goods))

            main_webdriver.quit()

            ray.shutdown()
            return alibaba_image_ids
        except Exception:
            self.__logger.setLevel(logging.DEBUG)
        finally:
            os.remove(self.__path + f"\\test{current_image_to_search_id}.png")
        return []

    def __get_good_url(
        self,
        goods: List[WebElement],
        max_length: int,
        start_index: int = 0,
        finish_index: int = 5,
    ) -> List[OrderedDict]:
        """
        This module needs to run chrome in parallel threads
        :param goods: product links not get info about
        :param max_length: count of goods
        :param start_index: start index for recursion
        :param finish_index: finish index for recursion
        :return: alibaba product ids which been extracted
        """
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
