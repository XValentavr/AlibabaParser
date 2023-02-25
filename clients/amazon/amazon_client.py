from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from clients.base_client import InitDriver
from helpers.envs.alibaba_envs import AlibabaEnvs
from helpers.enums.amazon.css_classes import CssClasses


class AmazonClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()

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
        for image in li:
            span = image.find_element(By.CLASS_NAME, "a-button-text")
            hover = ActionChains(self.__webdriver).move_to_element(span)
            hover.perform()
            self._with_alibaba(num_image)
            num_image += 1

    def _with_alibaba(self, num_image):
        path = self._generate_path_for_image(num_image)
        div = self.__webdriver.find_element(By.XPATH, path)
        amazon_image = div.get_attribute('src')

    def _close_browser(self):
        self.__webdriver.close()

    @staticmethod
    def _generate_path_for_image(num_image):
        return f"//li[@class='image item itemNo{num_image} maintain-height selected']" \
               f"/span[@class='a-{CssClasses.LIST_ITEM}']/span[@class='a-{CssClasses.DECLARATIVE}']" \
               f"/div[@class='{CssClasses.IMAGE_WRAPPER}']/img"
