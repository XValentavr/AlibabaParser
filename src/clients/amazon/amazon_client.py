from collections import OrderedDict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from src.ai.extractor.extract import Extractor
from clients.base_client import InitDriver
from helpers.enums.amazon.amazon_css_classes import CssClasses
from helpers.project_envs import ProjectEnvs


class AmazonClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)
        self.__extractor = Extractor()
        self.__dict = OrderedDict()

    def __navigate(self, url: str = None) -> None:
        self.__webdriver.get(ProjectEnvs.BASE_URL if not url else url)

    def search_on_url(self, url: str) -> OrderedDict:
        self.__navigate(url)
        return self.__get_single_photo()

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

        image_dict = self.__with_alibaba(num_image)
        num_image += 1

        # extract subimages from images
        # self.__extractor.extract(image_list)
        return image_dict

    def __with_alibaba(self, num_image: int) -> OrderedDict:
        # get full image from screen
        self.__dict.update({"link": self.__webdriver.current_url})
        path = self.__generate_path_for_image(num_image)
        div = self.__webdriver.find_element(By.XPATH, path)
        self.__action_chains.double_click(div).perform()
        large_image_src = self.__get_main_slider_image()

        self.__get_main_slider_image()
        # close popup menu
        images_from_slider = self.__get_slider_images()

        images_dict = {"images_link0": large_image_src}

        images_dict.update(images_from_slider)
        self.__dict.update({"images": images_dict})

        return self.__dict

    def __get_slider_images(self) -> dict:
        images_dict = {}
        slider = self.__webdriver.find_element(By.ID, "ivThumbs")
        image_rows = slider.find_elements(By.CLASS_NAME, "ivRow")
        number = 1
        for image in image_rows:
            images_in_rows = image.find_elements(By.XPATH, "//div[@class='ivThumb']")
            for inner_image in images_in_rows:
                self.__action_chains.double_click(inner_image).perform()
                image = self.__get_main_slider_image()
                images_dict.update({f"images_link{number}": image})
                number += 1
            break
        return images_dict

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
