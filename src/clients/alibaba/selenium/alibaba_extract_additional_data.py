import logging
from typing import Tuple
from uuid import UUID

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from clients.gpt.GPT import GPTClient
from cruds.alibaba_cruds import AlibabaCRUDS
from helpers.init_logger import create_logger
from helpers.project_envs import ProjectEnvs


class AlibabaExtractAdditionalData:
    """
    Helper class to get more data
    """

    def __init__(self, webdriver: WebDriver):
        self.__webdriver = webdriver
        self.__alibaba_cruds = AlibabaCRUDS()
        self.__logger = create_logger()
        self.__gpt_client = GPTClient()

    def combine_info(self, product_id: UUID):
        """
        Combine text and price in one method
        :param product_id: income product (alibaba or amazon)
        :return: None
        """
        try:
            text = self.__get_product_text(product_id)

            min_price, max_price = self.__get_product_price()

            self.__alibaba_cruds.update_alibaba_product_by_id(
                product_id, description=text, min_price=min_price, max_price=max_price
            )
        except Exception:
            self.__logger.setLevel(logging.DEBUG)

    def __get_product_text(self, product_id: UUID) -> str:
        """
        This function needs to get product text
        :return: text of products
        """
        title_div = self.__webdriver.find_element(By.CLASS_NAME, "product-title")
        title = title_div.find_element(By.XPATH, "//h1")

        if title:
            self.__gpt_client.get_keywords(product_id, text_to_extract=title.text)

            return title.text

        return ""

    def __get_product_price(self) -> Tuple[str, str]:
        """
        This function needs to get product price
        :return: price of products
        """
        self.__webdriver.implicitly_wait(10)
        price_div = self.__webdriver.find_element(By.CLASS_NAME, "price-list")

        try:
            price = price_div.find_element(By.CLASS_NAME, "promotion")

        except NoSuchElementException:
            price = price_div.find_element(By.CLASS_NAME, "price")

        self.__webdriver.implicitly_wait(int(ProjectEnvs.WAIT))

        if price:
            price_range = price.text.split("-")
            start_price = price_range[0].strip() if len(price_range) == 2 else 0
            end_price = (
                price_range[1].strip() if len(price_range) == 2 else price_range[0]
            )

            return start_price, end_price

        return "", ""
