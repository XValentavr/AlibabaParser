import os

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from clients.base_client import InitDriver
from helpers.enums.alibaba.css_classes import CssClasses
from helpers.envs.alibaba_envs import AlibabaEnvs
import urllib.request


class AlibabaClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)

    def _navigate(self, url: str = None):
        self.__webdriver.get(AlibabaEnvs.BASE_URL if not url else url)

    def search_by_upload_photo(self, images):
        self._navigate()
        # self.__webdriver.refresh()

        element = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-imgsearch-icon"
        )
        element.click()

        # base_div_to_search = self.__webdriver.find_element(By.CLASS_NAME, CssClasses.URL_LINK)

        # upload = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-url')

        path = 'D:\Work\AI\AlibabaParser\image_storage\\test.png'
        number = 0

        for image in images.get('images').values():
            urllib.request.urlretrieve(image,
                                       path)

            upload = self.__webdriver.find_element(By.XPATH, "//input[@type='file']")

            upload.send_keys(path)

            # go_button = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-search')

            # go_button.click()

            goods = self.__webdriver.find_elements(By.CLASS_NAME, "bc-ife-gallery-image-box")
            self._get_good_url(goods=goods)
            os.remove(path)
            number += 1
            break

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
        self._navigate(good)
        all_images = self._get_images()
        print('all_images', all_images)

    def _get_images(self):

        list_of_images = []

        # get started image
        current = self.__webdriver.find_element(By.CLASS_NAME, 'main-img')
        self.__action_chains.double_click(current).perform()

        list_of_images.append({'alibaba_url': self.__webdriver.current_url,
                               'alibaba_image': self._get_main_image_of_slider()})

        # work with slider and get others photo
        slider = self.__webdriver.find_element(By.CLASS_NAME, 'slider-list')
        self._get_slide_images(slider, list_of_images)

        # close popup menu
        close = self.__webdriver.find_element(By.CLASS_NAME, 'detail-next-dialog-close')
        self.__action_chains.double_click(close).perform()
        return list_of_images

    def _get_slide_images(self, slider, list_of_images):
        slide_images = slider.find_elements(By.CLASS_NAME, 'slider-item')

        for slide in slide_images:
            self.__action_chains.double_click(slide).perform()
            list_of_images.append({'alibaba_url': self.__webdriver.current_url,
                                   'alibaba_image': self._get_main_image_of_slider()})

    def _get_main_image_of_slider(self):
        main_layout = self.__webdriver.find_element(By.CLASS_NAME, 'image-layout')

        main_div = main_layout.find_element(By.CLASS_NAME, 'detail-next-slick-list')

        pre_main_div = main_div.find_element(By.CLASS_NAME, 'detail-next-slick-track')

        image_div = pre_main_div.find_element(By.XPATH,
                                              "//div[@class='detail-next-slick-slide detail-next-slick-active slider-img-wrapper']/img")
        return image_div.get_attribute('src')

    def _close_browser(self):
        self.__webdriver.close()
