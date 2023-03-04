from selenium import webdriver

from helpers.envs.project_envs import ProjectEnvs


class InitDriver:
    @staticmethod
    def initialize():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(options=chrome_options)
        browser.set_window_size(900, 900)
        browser.implicitly_wait(int(ProjectEnvs.WAIT))

        return browser

    @staticmethod
    def initialize_firefox():
        browser = webdriver.Firefox()
        browser.implicitly_wait(int(ProjectEnvs.WAIT))

        return browser
