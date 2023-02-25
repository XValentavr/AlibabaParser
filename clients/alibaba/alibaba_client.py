from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from clients.base_client import InitDriver
from helpers.enums.alibaba.css_classes import CssClasses
from helpers.envs.alibaba_envs import AlibabaEnvs


class AlibabaClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()

    def _navigate(self, url: str = None):
        self.__webdriver.get(AlibabaEnvs.BASE_URL if not url else url)

    def search_by_upload_photo(self, path):
        self._navigate()

        element = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-imgsearch-icon"
        )
        element.click()

        upload = self.__webdriver.find_element(By.XPATH, "//input[@type='file']")

        upload.send_keys("D:\Work\AI\AlibabaParser\\test.jpg")
        goods = self.__webdriver.find_elements(By.CLASS_NAME, "bc-ife-gallery-image-box")
        self._get_good_url(goods=goods)

    def search_by_title(self, title):
        self._navigate()

        search_field = self.__webdriver.find_element(By.XPATH, "//input[@type='text']")
        search_field.send_keys(title)

        search_button = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-submit"
        )
        search_button.click().perform()

    def search_by_photo_url(self, url):
        self._navigate()
        element = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-imgsearch-icon"
        )
        element.click()

    def _get_good_url(self, goods: list[WebElement]):
        for good in goods:
            url = good.get_attribute("href")
            self._parse_good_url(url)
            break

    def _parse_good_url(self, good):
        self.__webdriver.execute_script(f"window.open('{good}')")

    def _close_browser(self):
        self.__webdriver.close()
