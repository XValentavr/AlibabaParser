from collections import OrderedDict

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from clients.base_client import InitDriver
from helpers.enums.alibaba.css_classes import CssClasses
from helpers.envs.ai_envs import AIEnvs
from helpers.envs.alibaba_envs import AlibabaEnvs
import urllib.request


class AlibabaClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)
        # self.__s3_client = AmazonS3Client()
        self.__path = AIEnvs.BASE_IMAGE_URL
        self.__dict = OrderedDict()

    def __navigate(self, url: str = None):
        self.__webdriver.get(AlibabaEnvs.BASE_URL if not url else url)

    def search_by_upload_photo(self, images):
        self.__navigate()
        # self.__webdriver.refresh()

        element = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-imgsearch-icon"
        )
        self.__action_chains.double_click(element).perform()

        # base_div_to_search = self.__webdriver.find_element(By.CLASS_NAME, CssClasses.URL_LINK)

        # upload = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-url')

        for index, image in enumerate(images.get("images").values()):
            urllib.request.urlretrieve(image, self.__path + f"test{index}.png")

        upload = self.__webdriver.find_element(By.XPATH, "//input[@type='file']")

        upload.send_keys(self.__path + "test0.png")

        # go_button = base_div_to_search.find_element(By.CLASS_NAME, f'{CssClasses.URL_LINK}-search')

        # go_button.click()

        goods = self.__webdriver.find_elements(
            By.CLASS_NAME, "bc-ife-gallery-image-box"
        )
        self.__get_good_url(goods=goods)

    def search_by_title(self, title):
        self.__navigate()

        search_field = self.__webdriver.find_element(By.XPATH, "//input[@type='text']")
        search_field.send_keys(title)

        search_button = self.__webdriver.find_element(
            By.CLASS_NAME, f"{CssClasses.SEARCHBAR}-submit"
        )

        search_button.click().perform()

    def __get_good_url(self, goods: list[WebElement]):
        for good in goods:
            url = good.get_attribute("href")
            self.__switch_between_tabs(url)

            self.__parse_good_url()

            self.__go_to_initial_tab()

    def __parse_good_url(self):
        all_images = self.__get_images()
        print("all_images", all_images)

    def __get_images(self):
        list_of_images = []

        # get started image
        current = self.__webdriver.find_element(By.CLASS_NAME, "main-img")
        self.__action_chains.double_click(current).perform()

        list_of_images.append(
            {
                "alibaba_url": self.__webdriver.current_url,
                "alibaba_image": self.__get_main_image_of_slider(),
            }
        )

        # work with slider and get others photo
        slider = self.__webdriver.find_element(By.CLASS_NAME, "slider-list")
        self.__get_slide_images(slider, list_of_images)

        # close popup menu
        close = self.__webdriver.find_element(By.CLASS_NAME, "detail-next-dialog-close")
        self.__action_chains.double_click(close).perform()

        return list_of_images

    def __get_slide_images(self, slider, list_of_images):
        slide_images = slider.find_elements(By.CLASS_NAME, "slider-item")

        for slide in slide_images:
            self.__action_chains.double_click(slide).perform()

            list_of_images.append(
                {
                    "alibaba_url": self.__webdriver.current_url,
                    "alibaba_image": self.__get_main_image_of_slider(),
                }
            )

    def __get_main_image_of_slider(self):
        main_layout = self.__webdriver.find_element(By.CLASS_NAME, "image-layout")

        main_div = main_layout.find_element(By.CLASS_NAME, "detail-next-slick-list")

        pre_main_div = main_div.find_element(By.CLASS_NAME, "detail-next-slick-track")

        image_div = pre_main_div.find_element(
            By.XPATH,
            "//div[@class='detail-next-slick-slide detail-next-slick-active slider-img-wrapper']/img",
        )
        return image_div.get_attribute("src")

    def __close_tab(self):
        self.__webdriver.close()

    def __switch_between_tabs(self, url):
        self.__webdriver.execute_script("window.open('');")
        self.__webdriver.switch_to.window(self.__webdriver.window_handles[1])

        self.__webdriver.get(url)

    def __go_to_initial_tab(self):
        self.__close_tab()
        self.__webdriver.switch_to.window(self.__webdriver.window_handles[0])
