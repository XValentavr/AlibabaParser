from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from helpers.project_envs import ProjectEnvs


class InitDriver:
    """
    Class to generate chrome instance
    """

    @staticmethod
    def create_instance_of_driver():
        """
        Function to generate chrome instance
        :return: chrome instance
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        capabilities = DesiredCapabilities().CHROME

        my_webdriver = webdriver.Remote(
            command_executor=ProjectEnvs.SELENIUM_WEBDRIVER_HOST,
            desired_capabilities=capabilities,
            options=chrome_options,
        )
        my_webdriver.implicitly_wait(int(ProjectEnvs.WAIT))

        return my_webdriver

    # def another(self):
    #     chrome_options = webdriver.ChromeOptions()
    #     __webdriver = webdriver.Chrome()
    #     __webdriver.implicitly_wait(int(ProjectEnvs.WAIT))
    #
    #     return __webdriver


init_driver = InitDriver()
