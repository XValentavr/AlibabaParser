from uuid import UUID

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from clients.InitDriver import InitDriver, init_driver
from cruds.amazon_cruds import AmazonCRUDS
from helpers.enums.amazon.amazon_css_classes import CssClasses
from helpers.init_logger import create_logger
from helpers.project_envs import ProjectEnvs


class AmazonClient(InitDriver):
    def __init__(self):
        self.__init_driver = init_driver
        self.__amazon_cruds = AmazonCRUDS()
        self.__logger = create_logger()

    def __generate_webdriver_instance(self):
        return self.__init_driver.create_instance_of_driver()

    @staticmethod
    def __navigate(main_webdriver, url: str = None) -> None:
        main_webdriver.get(ProjectEnvs.BASE_URL if not url else url)

    def search_on_url(self, url: str):
        try:
            main_webdriver = self.__generate_webdriver_instance()
            self.__navigate(main_webdriver, url)
            self.__get_single_photo(main_webdriver)
            main_webdriver.quit()
        except Exception as error:
            self.__logger.error(error)

    def __get_single_photo(self, main_webdriver, num_image: int = 0):
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

        return self.__with_alibaba(num_image, main_webdriver)

        # extract subimages from images
        # self.__extractor.extract(image_list)

    def __with_alibaba(self, num_image: int, main_webdriver):
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

    def __get_slider_images(self, product_id: UUID, main_webdriver):
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
    def __get_main_slider_image(main_webdriver) -> str:
        # get image src
        large_image = main_webdriver.find_element(By.ID, "ivLargeImage").find_element(
            By.CLASS_NAME, "fullscreen"
        )
        return large_image.get_attribute("src")

    @staticmethod
    def close_tab(main_webdriver) -> None:
        main_webdriver.close()

    @staticmethod
    def __generate_path_for_image(num_image: int) -> str:
        return (
            f"//li[@class='image item itemNo{num_image} maintain-height selected']"
            f"/span[@class='a-{CssClasses.LIST_ITEM}']/span[@class='a-{CssClasses.DECLARATIVE}']"
            f"/div[@class='{CssClasses.IMAGE_WRAPPER}']/img"
        )

    @staticmethod
    def __generate_path_for_close_large_image() -> str:
        return "//div[@class='a-popover-wrapper']/header/button"
