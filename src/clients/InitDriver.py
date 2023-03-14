from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from helpers.project_envs import ProjectEnvs


class InitDriver:
    @staticmethod
    def create_instance_of_driver():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        capabilities = DesiredCapabilities().CHROME

        capabilities["pageLoadStrategy"] = "eager"

        __webdriver = webdriver.Remote(
            command_executor=ProjectEnvs.SELENIUM_WEBDRIVER_HOST,
            desired_capabilities=capabilities,
            options=chrome_options,
        )
        __webdriver.implicitly_wait(int(ProjectEnvs.WAIT))

        return __webdriver


init_driver = InitDriver()
