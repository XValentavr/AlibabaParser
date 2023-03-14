from uuid import UUID

import ray
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from clients.alibaba.alibaba_extract_additional_data import (
    AlibabaExtractAdditionalData,
)
from cruds.alibaba_cruds import AlibabaCRUDS
from helpers.project_envs import ProjectEnvs
from selenium import webdriver

alibaba_cruds = AlibabaCRUDS()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')

webdriver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    desired_capabilities=DesiredCapabilities.CHROME,
    options=chrome_options
)
webdriver.implicitly_wait(int(ProjectEnvs.WAIT))


@ray.remote
def get_images_by_threads(image: str):
    webdriver.get(image)
    print()
    ids = prepare_for_thread()
    webdriver.quit()
    return ids


def prepare_for_thread() -> UUID:
    product_id = alibaba_cruds.insert_alibaba_products(
        link=webdriver.current_url
    )
    # extract price and description
    more_data_extractor = AlibabaExtractAdditionalData()
    more_data_extractor.combine_info(product_id, webdriver)

    get_images(product_id)
    return product_id


def get_images(product_id: UUID):
    # get started image
    check_if_video_to_pass()

    current = webdriver.find_element(By.CLASS_NAME, "main-img")
    ActionChains(webdriver).double_click(current).perform()

    # work with slider and get others photo
    slider = webdriver.find_element(By.CLASS_NAME, "slider-list")
    get_slide_images(slider, product_id)

    # close popup menu
    close = webdriver.find_element(By.CLASS_NAME, "detail-next-dialog-close")
    ActionChains(webdriver).double_click(close).perform()

    # configure images
    webdriver.close()


def get_slide_images(slider: WebElement, product_id: UUID):
    slide_images = slider.find_elements(By.CLASS_NAME, "slider-item")

    for index, slide in enumerate(slide_images):
        ActionChains(webdriver).double_click(slide).perform()
        try:
            alibaba_cruds.update_alibaba_product_by_id(
                product_id, images=get_main_image_of_slider()
            )
        except NoSuchElementException as error:
            # print('error', error)
            continue


def get_main_image_of_slider() -> str:
    main_layout = webdriver.find_element(By.CLASS_NAME, "image-layout")

    main_div = main_layout.find_element(By.CLASS_NAME, "detail-next-slick-list")

    pre_main_div = main_div.find_element(By.CLASS_NAME, "detail-next-slick-track")

    image_div = pre_main_div.find_element(
        By.XPATH,
        "//div[@class='detail-next-slick-slide detail-next-slick-active slider-img-wrapper']/img",
    )
    return image_div.get_attribute("src")


def check_if_video_to_pass():
    #  change waiting to find video
    webdriver.implicitly_wait(1)
    try:
        is_video = webdriver.find_element(By.ID, "main-video")
        if is_video:
            main_layout = webdriver.find_element(By.CLASS_NAME, "thumb-list")

            main_div = main_layout.find_element(
                By.CLASS_NAME, "detail-next-slick-list"
            )

            pre_main_div = main_div.find_element(
                By.CLASS_NAME, "detail-next-slick-track"
            )

            line_slider = pre_main_div.find_elements(
                By.XPATH,
                "//div[@class='detail-next-slick-slide detail-next-slick-active main-item false']",
            )
            ActionChains(webdriver).double_click(line_slider[0]).perform()

    except NoSuchElementException:
        webdriver.implicitly_wait(int(ProjectEnvs.WAIT))
