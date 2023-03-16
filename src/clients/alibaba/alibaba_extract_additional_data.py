from typing import Tuple
from uuid import UUID

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from cruds.alibaba_cruds import AlibabaCRUDS
from helpers.init_logger import create_logger
from helpers.project_envs import ProjectEnvs


class AlibabaExtractAdditionalData:
    def __init__(self, webdriver: WebDriver):
        self.__webdriver = webdriver
        self.__alibaba_cruds = AlibabaCRUDS()
        self.__logger = create_logger()

    def combine_info(self, product_id: UUID):
        try:
            text = self.__get_product_text()

            min_price, max_price = self.__get_product_price()

            self.__alibaba_cruds.update_alibaba_product_by_id(
                product_id, description=text, min_price=min_price, max_price=max_price
            )
        except Exception as error:
            self.__logger.error(error)

    def __get_product_text(self) -> str:
        title_div = self.__webdriver.find_element(By.CLASS_NAME, "product-title")
        title = title_div.find_element(By.XPATH, "//h1")

        if title:
            return title.text

        return ""

    def __get_product_price(self) -> Tuple[str, str]:
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
