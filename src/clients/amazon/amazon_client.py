from uuid import UUID

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from clients.InitDriver import InitDriver
from cruds.amazon_cruds import AmazonCRUDS
from helpers.enums.amazon.amazon_css_classes import CssClasses
from helpers.project_envs import ProjectEnvs


class AmazonClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)
        self.__amazon_cruds = AmazonCRUDS()

    def __navigate(self, url: str = None) -> None:
        self.__webdriver.get(ProjectEnvs.BASE_URL if not url else url)

    def search_on_url(self, url: str):
        self.__navigate(url)
        self.__get_single_photo()
        self.__webdriver.quit()

    def __get_single_photo(self, num_image: int = 0):
        ul = self.__webdriver.find_element(
            By.XPATH, f"//div[@id='{CssClasses.ALT_IMAGES}']/ul"
        )

        li = ul.find_element(
            By.XPATH,
            f"//li[@class='a-spacing-small item imageThumbnail a-{CssClasses.DECLARATIVE}']",
        )
        # hover image to change span in site
        span = li.find_element(By.CLASS_NAME, "a-button-text")

        hover = self.__action_chains.move_to_element(span)
        hover.perform()

        return self.__with_alibaba(num_image)

        # extract subimages from images
        # self.__extractor.extract(image_list)

    def __with_alibaba(self, num_image: int):
        # get full image from screen
        product_id = self.__amazon_cruds.insert_amazon_products(
            link=self.__webdriver.current_url
        )

        path = self.__generate_path_for_image(num_image)
        div = self.__webdriver.find_element(By.XPATH, path)
        self.__action_chains.double_click(div).perform()
        large_image_src = self.__get_main_slider_image()

        self.__amazon_cruds.update_amazon_product_by_id(
            product_id, images=large_image_src
        )

        self.__get_main_slider_image()
        # close popup menu
        self.__get_slider_images(product_id)

        return product_id

    def __get_slider_images(self, product_id: UUID):
        slider = self.__webdriver.find_element(By.ID, "ivThumbs")
        image_rows = slider.find_elements(By.CLASS_NAME, "ivRow")
        for image in image_rows:
            images_in_rows = image.find_elements(By.XPATH, "//div[@class='ivThumb']")
            for inner_image in images_in_rows:
                self.__action_chains.double_click(inner_image).perform()
                image = self.__get_main_slider_image()
                self.__amazon_cruds.update_amazon_product_by_id(
                    product_id, images=image
                )
            break

    def __get_main_slider_image(self) -> str:
        # get image src
        large_image = self.__webdriver.find_element(By.ID, "ivLargeImage").find_element(
            By.CLASS_NAME, "fullscreen"
        )
        return large_image.get_attribute("src")

    def close_tab(self) -> None:
        self.__webdriver.close()

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
