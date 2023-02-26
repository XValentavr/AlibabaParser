import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from ai.extractor.extract import Extractor
from clients.base_client import InitDriver
from helpers.envs.alibaba_envs import AlibabaEnvs
from helpers.enums.amazon.css_classes import CssClasses


class AmazonClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)
        self.__extractor = Extractor()
    def _navigate(self, url: str = None):
        self.__webdriver.get(AlibabaEnvs.BASE_URL if not url else url)

    def search_on_url(self, url):
        self._navigate(url)
        self._get_single_photo()

    def _get_single_photo(self, num_image=0):
        ul = self.__webdriver.find_element(By.XPATH, f"//div[@id='{CssClasses.ALT_IMAGES}']/ul")

        li = ul.find_elements(
            By.XPATH, f"//li[@class='a-spacing-small item imageThumbnail a-{CssClasses.DECLARATIVE}']"
        )
        image_list = []
        for image in li:
            # hover image to change span in site
            span = image.find_element(By.CLASS_NAME, "a-button-text")
            hover = self.__action_chains.move_to_element(span)
            hover.perform()

            image_src = self._with_alibaba(num_image)
            num_image += 1

            image_list.append(image_src)

        self.__extractor.extract(image_list)
        self._close_browser()

    def _with_alibaba(self, num_image):
        # get full image from screen
        path = self._generate_path_for_image(num_image)
        div = self.__webdriver.find_element(By.XPATH, path)
        self.__action_chains.double_click(div).perform()

        # get image src
        large_image = self.__webdriver.find_element(By.ID, 'ivLargeImage').find_element(By.CLASS_NAME, 'fullscreen')
        large_image_src = large_image.get_attribute('src')

        # close popup menu
        close = self.__webdriver.find_element(By.XPATH, self._generate_path_for_close_large_image())
        self.__action_chains.double_click(close).perform()

        data_dict = {
            'url': self.__webdriver.current_url,
            'image': large_image_src
        }
        return data_dict

    def _close_browser(self):
        self.__webdriver.close()

    @staticmethod
    def _generate_path_for_image(num_image):
        return f"//li[@class='image item itemNo{num_image} maintain-height selected']" \
               f"/span[@class='a-{CssClasses.LIST_ITEM}']/span[@class='a-{CssClasses.DECLARATIVE}']" \
               f"/div[@class='{CssClasses.IMAGE_WRAPPER}']/img"

    @staticmethod
    def _generate_path_for_close_large_image():
        return f"//div[@class='a-popover-wrapper']/header/button"
