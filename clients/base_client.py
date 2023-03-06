from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from helpers.envs.project_envs import ProjectEnvs


class InitDriver:
    @staticmethod
    def initialize() -> WebDriver:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(options=chrome_options)
        browser.set_window_size(900, 900)
        browser.implicitly_wait(int(ProjectEnvs.WAIT))

        return browser

    @staticmethod
    def initialize_firefox() -> WebDriver:
        browser = webdriver.Firefox()
        browser.implicitly_wait(int(ProjectEnvs.WAIT))

        return browser
