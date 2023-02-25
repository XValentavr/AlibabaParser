from selenium import webdriver

from helpers.envs.base_envs import BaseEnvs


class InitDriver:
    @staticmethod
    def initialize():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(options=chrome_options)
        browser.implicitly_wait(int(BaseEnvs.WAIT))

        return browser

    @staticmethod
    def initialize_firefox():
        browser = webdriver.Firefox()
        browser.implicitly_wait(int(BaseEnvs.WAIT))

        return browser
