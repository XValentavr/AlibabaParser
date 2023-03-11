from collections import OrderedDict

import ray
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.clients.alibaba.alibaba_extract_additional_data import AlibabaExtractAdditionalData
from src.clients.base_client import InitDriver
from src.helpers.project_envs import ProjectEnvs


@ray.remote
class AlibabaThreads(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)
        self.__dict = OrderedDict()

    def get_images_by_threads(self, image: str) -> OrderedDict:
        self.__webdriver.get(image)
        return self.__prepare_for_thread()

    def __prepare_for_thread(self) -> OrderedDict:

        self.__dict.update({"link": self.__webdriver.current_url})

        # extract price and description
        more_data_extractor = AlibabaExtractAdditionalData(self.__dict, self.__webdriver)
        additional_data_dict = more_data_extractor.combine_info()
        self.__dict.update(additional_data_dict)

        return self.__get_images()

    def __get_images(self) -> OrderedDict:
        images_dict: dict = {}

        # get started image
        self.__check_if_video_to_pass()

        current = self.__webdriver.find_element(By.CLASS_NAME, "main-img")
        self.__action_chains.double_click(current).perform()

        # work with slider and get others photo
        slider = self.__webdriver.find_element(By.CLASS_NAME, "slider-list")
        all_product_images = self.__get_slide_images(slider, images_dict)

        # close popup menu
        close = self.__webdriver.find_element(By.CLASS_NAME, "detail-next-dialog-close")
        self.__action_chains.double_click(close).perform()

        # configure images
        images_dict.update(all_product_images)
        self.__dict.update({"images": images_dict})

        self.__webdriver.close()

        return self.__dict

    def __get_slide_images(self, slider: WebElement, images_dict: dict) -> dict:
        slide_images = slider.find_elements(By.CLASS_NAME, "slider-item")

        for index, slide in enumerate(slide_images):
            self.__action_chains.double_click(slide).perform()
            try:
                images_dict.update(
                    {f"images_link{index}": self.__get_main_image_of_slider()}
                )
            except NoSuchElementException as error:
                # print('error', error)
                continue

        return images_dict

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
            is_video = self.__webdriver.find_element(By.ID, 'main-video')
            if is_video:
                main_layout = self.__webdriver.find_element(By.CLASS_NAME, "thumb-list")

                main_div = main_layout.find_element(By.CLASS_NAME, "detail-next-slick-list")

                pre_main_div = main_div.find_element(By.CLASS_NAME, "detail-next-slick-track")

                line_slider = pre_main_div.find_elements(By.XPATH,
                                                         "//div[@class='detail-next-slick-slide detail-next-slick-active main-item false']",
                                                         )
                self.__action_chains.double_click(line_slider[0]).perform()

        except NoSuchElementException:
            self.__webdriver.implicitly_wait(int(ProjectEnvs.WAIT))
