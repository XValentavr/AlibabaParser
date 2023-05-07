import logging
from uuid import UUID

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from clients.InitDriver import InitDriver, init_driver
from cruds.amazon_cruds import AmazonCRUDS
from helpers.enums.amazon.amazon_css_classes import CssClasses
from helpers.init_logger import create_logger
from helpers.project_envs import ProjectEnvs


class AmazonClient(InitDriver):
    """
    Class to find amazon data using selenium
    """

    def __init__(self):
        self.__init_driver = init_driver
        self.__amazon_cruds = AmazonCRUDS()
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

    def search_on_url(self, url: str):
        """
        Main function to find amazon images using selenium
        :param url: url to extract data from
        :return: None
        """
        try:
            main_webdriver = self.__generate_webdriver_instance()
            self.__navigate(main_webdriver, url)
            self.__get_single_photo(main_webdriver)
            main_webdriver.quit()
        except Exception:
            self.__logger.setLevel(logging.DEBUG)

    def __get_single_photo(self, main_webdriver: WebDriver, num_image: int = 0) -> UUID:
        """
        Get photo from amazon page to work with
        :param main_webdriver: chrome instance
        :param num_image: number of image. Starts with 0
        :return: amazon product id
        """
        ul = main_webdriver.find_element(
            By.XPATH, f"//div[@id='{CssClasses.ALT_IMAGES}']/ul"
        )

        li = ul.find_element(
            By.XPATH,
            f"//li[@class='a-spacing-small item imageThumbnail a-{CssClasses.DECLARATIVE}']",
        )
        # hover image to change span in site
        span = li.find_element(By.CLASS_NAME, "a-button-text")

        hover = ActionChains(main_webdriver).move_to_element(span)
        hover.perform()

        return self.__image_extractor(num_image, main_webdriver)

        # extract subimages from images
        # self.__extractor.extract(image_list)

    def __image_extractor(self, num_image: int, main_webdriver: WebDriver) -> UUID:
        """
        The main function to extract images. Works with main image and slider
        :param num_image: number of image that starts on 0
        :param main_webdriver: chrome instance
        :return: current amazon product id
        """
        # get full image from screen
        product_id = self.__amazon_cruds.insert_amazon_products(
            link=main_webdriver.current_url
        )

        path = self.__generate_path_for_image(num_image)
        div = main_webdriver.find_element(By.XPATH, path)
        ActionChains(main_webdriver).double_click(div).perform()
        large_image_src = self.__get_main_slider_image(main_webdriver)

        self.__amazon_cruds.update_amazon_product_by_id(
            product_id, images=large_image_src
        )

        self.__get_main_slider_image(main_webdriver)
        # close popup menu
        self.__get_slider_images(product_id, main_webdriver)

        return product_id

    def __get_slider_images(self, product_id: UUID, main_webdriver: WebDriver):
        """
        Get all images from slider
        :param product_id: income amazon product id
        :param main_webdriver: chrome instance
        :return: None
        """
        slider = main_webdriver.find_element(By.ID, "ivThumbs")
        image_rows = slider.find_elements(By.CLASS_NAME, "ivRow")
        for image in image_rows:
            images_in_rows = image.find_elements(By.XPATH, "//div[@class='ivThumb']")
            for inner_image in images_in_rows:
                ActionChains(main_webdriver).double_click(inner_image).perform()
                image = self.__get_main_slider_image(main_webdriver)
                self.__amazon_cruds.update_amazon_product_by_id(
                    product_id, images=image
                )
            break

    @staticmethod
    def __get_main_slider_image(main_webdriver: WebDriver) -> str:
        """
        Get main image from amazon page slider
        :param main_webdriver: chrome instance
        :return: image source
        """
        # get image src
        large_image = main_webdriver.find_element(By.ID, "ivLargeImage").find_element(
            By.CLASS_NAME, "fullscreen"
        )
        return large_image.get_attribute("src")

    @staticmethod
    def __generate_path_for_image(num_image: int) -> str:
        """
        Generate XPATH for the image
        :return: XPATH
        """
        return (
            f"//li[@class='image item itemNo{num_image} maintain-height selected']"
            f"/span[@class='a-{CssClasses.LIST_ITEM}']/span[@class='a-{CssClasses.DECLARATIVE}']"
            f"/div[@class='{CssClasses.IMAGE_WRAPPER}']/img"
        )

    @staticmethod
    def __generate_path_for_close_large_image() -> str:
        """
        Generate XPATH for the largest image
        :return: XPATH
        """
        return "//div[@class='a-popover-wrapper']/header/button"
