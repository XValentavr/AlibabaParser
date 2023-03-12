from uuid import UUID

import ray
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.clients.alibaba.alibaba_extract_additional_data import (
    AlibabaExtractAdditionalData,
)
from src.clients.base_client import InitDriver
from src.cruds.alibaba_cruds import AlibabaCRUDS
from src.helpers.project_envs import ProjectEnvs


@ray.remote
class AlibabaThreads(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)
        self.__alibaba_cruds = AlibabaCRUDS()

    def get_images_by_threads(self, image: str):
        self.__webdriver.get(image)
        return self.__prepare_for_thread()

    def __prepare_for_thread(self) -> UUID:
        product_id = self.__alibaba_cruds.insert_alibaba_products(
            link=self.__webdriver.current_url
        )
        # extract price and description
        more_data_extractor = AlibabaExtractAdditionalData(self.__webdriver)
        more_data_extractor.combine_info(product_id)

        self.__get_images(product_id)
        return product_id

    def __get_images(self, product_id: UUID):
        # get started image
        self.__check_if_video_to_pass()

        current = self.__webdriver.find_element(By.CLASS_NAME, "main-img")
        self.__action_chains.double_click(current).perform()

        # work with slider and get others photo
        slider = self.__webdriver.find_element(By.CLASS_NAME, "slider-list")
        self.__get_slide_images(slider, product_id)

        # close popup menu
        close = self.__webdriver.find_element(By.CLASS_NAME, "detail-next-dialog-close")
        self.__action_chains.double_click(close).perform()

        # configure images
        self.__webdriver.close()

    def __get_slide_images(self, slider: WebElement, product_id: UUID):
        slide_images = slider.find_elements(By.CLASS_NAME, "slider-item")

        for index, slide in enumerate(slide_images):
            self.__action_chains.double_click(slide).perform()
            try:
                self.__alibaba_cruds.update_alibaba_product_by_id(
                    product_id, images=self.__get_main_image_of_slider()
                )
            except NoSuchElementException as error:
                # print('error', error)
                continue

    def __get_main_image_of_slider(self) -> str:
        main_layout = self.__webdriver.find_element(By.CLASS_NAME, "image-layout")

        main_div = main_layout.find_element(By.CLASS_NAME, "detail-next-slick-list")

        pre_main_div = main_div.find_element(By.CLASS_NAME, "detail-next-slick-track")

        image_div = pre_main_div.find_element(
            By.XPATH,
            "//div[@class='detail-next-slick-slide detail-next-slick-active slider-img-wrapper']/img",
        )
        return image_div.get_attribute("src")

    def __check_if_video_to_pass(self):
        #  change waiting to find video
        self.__webdriver.implicitly_wait(1)
        try:
            is_video = self.__webdriver.find_element(By.ID, "main-video")
            if is_video:
                main_layout = self.__webdriver.find_element(By.CLASS_NAME, "thumb-list")

                main_div = main_layout.find_element(
                    By.CLASS_NAME, "detail-next-slick-list"
                )

                pre_main_div = main_div.find_element(
                    By.CLASS_NAME, "detail-next-slick-track"
                )

                line_slider = pre_main_div.find_elements(
                    By.XPATH,
                    "//div[@class='detail-next-slick-slide detail-next-slick-active main-item false']",
                )
                self.__action_chains.double_click(line_slider[0]).perform()

        except NoSuchElementException:
            self.__webdriver.implicitly_wait(int(ProjectEnvs.WAIT))
