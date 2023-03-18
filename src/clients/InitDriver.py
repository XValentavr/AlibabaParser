from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.webdriver import WebDriver

from helpers.project_envs import ProjectEnvs


class InitDriver:
    @staticmethod
    def create_instance_of_driver() -> WebDriver:
        chrome_options = webdriver.ChromeOptions()

        __webdriver = webdriver.Chrome(options=chrome_options)
        __webdriver.implicitly_wait(int(ProjectEnvs.WAIT))

        return __webdriver


init_driver = InitDriver()
