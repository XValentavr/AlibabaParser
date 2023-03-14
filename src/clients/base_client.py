from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.webdriver import WebDriver

from helpers.project_envs import ProjectEnvs


class InitDriver:
    @staticmethod
    def initialize() -> WebDriver:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        wb = webdriver.Remote(
            command_executor="http://0.0.0.0:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )

        return wb

    @staticmethod
    def initialize_firefox() -> WebDriver:
        browser = webdriver.Firefox()
        browser.implicitly_wait(int(ProjectEnvs.WAIT))

        return browser
