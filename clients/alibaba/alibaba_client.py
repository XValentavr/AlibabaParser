from selenium.webdriver.common.by import By

from clients.base_client import InitDriver
from helpers.envs.alibaba.alibaba_envs import AlibabaEnvs


class AlibabaClient(InitDriver):
    def __init__(self):
        self.webdriver = super().initialize()

    def navigate(self):
        self.webdriver.get(AlibabaEnvs.BASE_URL)

    def search_by_upload_photo(self, path):
        self.navigate()

        element = self.webdriver.find_element(
            By.CLASS_NAME, "ui-searchbar-imgsearch-icon"
        )
        element.click()

        upload = self.webdriver.find_element(By.XPATH, "//input[@type='file']")

        upload.send_keys("D:\Work\AI\AlibabaParser\\test.jpg")

    def search_by_title(self, title):
        self.navigate()

        search_field = self.webdriver.find_element(By.XPATH, "//input[@type='text']")
        search_field.send_keys(title)

        search_button = self.webdriver.find_element(
            By.CLASS_NAME, "ui-searchbar-submit"
        )
        search_button.click()

    def search_by_photo_url(self, url):
        self.navigate()
        element = self.webdriver.find_element(
            By.CLASS_NAME, "ui-searchbar-imgsearch-icon"
        )
        element.click()

    def close_browser(self):
        self.webdriver.close()
