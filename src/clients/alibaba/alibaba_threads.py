from uuid import UUID

import ray
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from clients.alibaba.alibaba_extract_additional_data import (
    AlibabaExtractAdditionalData,
)
from clients.InitDriver import InitDriver, init_driver
from cruds.alibaba_cruds import AlibabaCRUDS
from helpers.project_envs import ProjectEnvs


@ray.remote
class AlibabaThreads(InitDriver):
    def __init__(self):
        self.__alibaba_cruds = AlibabaCRUDS()
        self.__init_driver = init_driver

    def __generate_webdriver_instance(self):
        return self.__init_driver.create_instance_of_driver()

    def get_images_by_threads(self, image: str):
        main_webdriver = self.__generate_webdriver_instance()
        main_webdriver.get(image)

        product_ids = self.__prepare_for_thread(main_webdriver)
        main_webdriver.quit()

        return product_ids

    def __prepare_for_thread(self, main_webdriver) -> UUID:
        product_id = self.__alibaba_cruds.insert_alibaba_products(
            link=main_webdriver.current_url
        )
        # extract price and description
        more_data_extractor = AlibabaExtractAdditionalData(main_webdriver)
        more_data_extractor.combine_info(product_id)

        self.__get_images(product_id, main_webdriver)
        return product_id

    def __get_images(self, product_id: UUID, main_webdriver):
        # get started image
        self.__check_if_video_to_pass(main_webdriver)

        current = main_webdriver.find_element(By.CLASS_NAME, "main-img")
        ActionChains(main_webdriver).double_click(current).perform()

        # work with slider and get others photo
        slider = main_webdriver.find_element(By.CLASS_NAME, "slider-list")
        self.__get_slide_images(slider, product_id, main_webdriver)

        # close popup menu
        close = main_webdriver.find_element(By.CLASS_NAME, "detail-next-dialog-close")
        ActionChains(main_webdriver).double_click(close).perform()

        # configure images
        main_webdriver.close()

    def __get_slide_images(self, slider: WebElement, product_id: UUID, main_webdriver):
        slide_images = slider.find_elements(By.CLASS_NAME, "slider-item")

        for index, slide in enumerate(slide_images):
            ActionChains(main_webdriver).double_click(slide).perform()
            try:
                self.__alibaba_cruds.update_alibaba_product_by_id(
                    product_id, images=self.__get_main_image_of_slider(main_webdriver)
                )
            except NoSuchElementException as error:
                # print('error', error)
                continue

    def __get_main_image_of_slider(self, main_webdriver) -> str:
        main_layout = main_webdriver.find_element(By.CLASS_NAME, "image-layout")

        main_div = main_layout.find_element(By.CLASS_NAME, "detail-next-slick-list")

        pre_main_div = main_div.find_element(By.CLASS_NAME, "detail-next-slick-track")

        image_div = pre_main_div.find_element(
            By.XPATH,
            "//div[@class='detail-next-slick-slide detail-next-slick-active slider-img-wrapper']/img",
        )
        return image_div.get_attribute("src")

    @staticmethod
    def __check_if_video_to_pass(main_webdriver):
        #  change waiting to find video
        main_webdriver.implicitly_wait(1)
        try:
            is_video = main_webdriver.find_element(By.ID, "main-video")
            if is_video:
                main_layout = main_webdriver.find_element(By.CLASS_NAME, "thumb-list")

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
                ActionChains(main_webdriver).double_click(line_slider[0]).perform()

        except NoSuchElementException:
            main_webdriver.implicitly_wait(int(ProjectEnvs.WAIT))
