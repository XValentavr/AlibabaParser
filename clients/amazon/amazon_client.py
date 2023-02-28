from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from ai.extractor.extract import Extractor
from clients.base_client import InitDriver
from helpers.envs.alibaba_envs import AlibabaEnvs
from helpers.enums.amazon.css_classes import CssClasses


class AmazonClient(InitDriver):
    def __init__(self):
        self.__webdriver = super().initialize()
        self.__action_chains = ActionChains(self.__webdriver)
        self.__extractor = Extractor()

    def _navigate(self, url: str = None):
        self.__webdriver.get(AlibabaEnvs.BASE_URL if not url else url)

    def search_on_url(self, url):
        self._navigate(url)
        return self._get_single_photo()

    def _get_single_photo(self, num_image=0):
        ul = self.__webdriver.find_element(By.XPATH, f"//div[@id='{CssClasses.ALT_IMAGES}']/ul")

        li = ul.find_element(
            By.XPATH, f"//li[@class='a-spacing-small item imageThumbnail a-{CssClasses.DECLARATIVE}']"
        )
        # hover image to change span in site
        span = li.find_element(By.CLASS_NAME, "a-button-text")

        hover = self.__action_chains.move_to_element(span)
        hover.perform()

        image_list = self._with_alibaba(num_image)
        num_image += 1


        # extract subimages from images
        # self.__extractor.extract(image_list)
        return image_list

    def _with_alibaba(self, num_image):
        # get full image from screen
        path = self._generate_path_for_image(num_image)
        div = self.__webdriver.find_element(By.XPATH, path)
        self.__action_chains.double_click(div).perform()
        large_image_src = self._get_main_slider_image()

        self._get_main_slider_image()
        # close popup menu
        images_from_slider = self._get_slider_images()

        data_dict = {
            'amazon_good_url': self.__webdriver.current_url,
            'amazon_image': large_image_src
        }
        images_from_slider.append(data_dict)
        return images_from_slider

    def _get_slider_images(self):
        images_list = []
        slider = self.__webdriver.find_element(By.ID, 'ivThumbs')
        image_rows = slider.find_elements(By.CLASS_NAME, 'ivRow')
        for image in image_rows:
            images_in_rows = image.find_elements(By.XPATH, "//div[@class='ivThumb']")
            for inner_image in images_in_rows:
                self.__action_chains.double_click(inner_image).perform()
                image = self._get_main_slider_image()
                images_list.append({
                    'amazon_good_url': self.__webdriver.current_url,
                    'amazon_image': image
                })
            break
        return images_list

    def _get_main_slider_image(self):
        # get image src
        large_image = self.__webdriver.find_element(By.ID, 'ivLargeImage').find_element(By.CLASS_NAME, 'fullscreen')
        return large_image.get_attribute('src')

    def close_browser(self):
        self.__webdriver.close()

    @staticmethod
    def _generate_path_for_image(num_image):
        return f"//li[@class='image item itemNo{num_image} maintain-height selected']" \
               f"/span[@class='a-{CssClasses.LIST_ITEM}']/span[@class='a-{CssClasses.DECLARATIVE}']" \
               f"/div[@class='{CssClasses.IMAGE_WRAPPER}']/img"

    @staticmethod
    def _generate_path_for_close_large_image():
        return f"//div[@class='a-popover-wrapper']/header/button"
