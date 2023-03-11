from collections import OrderedDict

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class AlibabaExtractAdditionalData:
    def __init__(self, data_dict: OrderedDict, webdriver: WebDriver):
        self.__dict = data_dict
        self.__webdriver = webdriver

    def combine_info(self) -> OrderedDict:
        text = self.__get_product_text()
        self.__dict.update(text)

        price = self.__get_product_price()
        self.__dict.update(price)

        return self.__dict

    def __get_product_text(self) -> dict:
        title_div = self.__webdriver.find_element(By.CLASS_NAME, "product-title")
        title = title_div.find_element(By.XPATH, "//h1")

        if title:
            return {"title": title.text}

        return {"title": ""}

    def __get_product_price(self) -> dict:
        self.__webdriver.implicitly_wait(1)
        price_div = self.__webdriver.find_element(By.CLASS_NAME, "price-list")

        try:
            price = price_div.find_element(By.CLASS_NAME, "promotion")

        except NoSuchElementException:
            price = price_div.find_element(By.CLASS_NAME, 'price')

        self.__webdriver.implicitly_wait(20)

        if price:

            price_range = price.text.split("-")
            start_price = price_range[0].strip() if len(price_range) == 2 else 0
            end_price = price_range[1].strip() if len(price_range) == 2 else price_range[0]

            price_dict = {"price": {"min": start_price, "max": end_price}}
            return price_dict

        return {"price": ""}
