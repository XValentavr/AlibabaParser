import logging
import urllib.request
from os.path import join, dirname, abspath

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from clients.InitDriver import InitDriver, init_driver
from clients.alibaba.api.alibaba_client_helper import alibaba_client_helper
from cruds.alibaba_cruds import AlibabaCRUDS
from cruds.alibaba_product_ids_cruds import AlibabaProductIdsCRUDS
from cruds.amazon_cruds import AmazonCRUDS
from helpers.enums.alibaba.alibaba_css_classes import CssClasses
from helpers.enums.alibaba.search_types import SearchTypes
from helpers.init_logger import create_logger
from helpers.project_envs import ProjectEnvs


class AlibabaSeleniumGetIds(InitDriver):
    """
    This class is needed in order to get a product ids with selenium
    """

    def __init__(self, amazon_product_id):
        self.__amazon_product_id = amazon_product_id
        self.__init_driver = init_driver
        self.__logger = create_logger()
        self.__path = join(
            dirname(dirname(dirname(dirname(abspath(__file__))))), "image_storage\\"
        )

        self.__amazon_cruds = AmazonCRUDS()
        self.__alibaba_product_ids = AlibabaProductIdsCRUDS()
        self.__alibaba_cruds = AlibabaCRUDS()

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

    def search_by_upload_photo(self, current_image_to_search_id: int = 0, from_where: SearchTypes = None):
        """
        This main method needed to search product by amazon photo
        :param current_image_to_search_id: num of image to search
        :param from_where: text pr image
        :return: None
        """

        main_webdriver = self.__generate_webdriver_instance()

        self.__navigate(main_webdriver=main_webdriver)

        element = main_webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-imgsearch-icon"
        )
        ActionChains(main_webdriver).double_click(element).perform()

        try:
            images = self.__amazon_cruds.get_amazon_product_photo_by_id(
                product_id=self.__amazon_product_id
            )

            for index, image in enumerate(images):  # type: ignore
                urllib.request.urlretrieve(image.link, self.__path + f"test{index}.png")

            upload = main_webdriver.find_element(By.XPATH, "//input[@type='file']")

            upload.send_keys(self.__path + f"test{current_image_to_search_id}.png")
            self.__get_product_ids_from_uls(main_webdriver, from_where)

        except Exception:
            self.__logger.setLevel(logging.DEBUG)

    def __get_product_ids_from_uls(self, main_webdriver: WebDriver, from_where: SearchTypes):
        """
        Extract product ids from alibaba product url
        :param main_webdriver: chrome instance
        :return: None
        """
        goods = main_webdriver.find_elements(By.CLASS_NAME, "bc-ife-gallery-image-box")
        alibaba_client_helper.insert_alibaba_products(goods=goods,
                                                      amazon_product_id=self.__amazon_product_id,
                                                      from_where=from_where)
