from pages.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By


class TopMenuLinksPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    LINKS_LIST = (By.CSS_SELECTOR, ".menu .tab_name")
    BASE = "https://www.rest.co.il/"
    RESTAURANT_URL = "restaurants/israel/"
    KOSHER_REST_URL = "/kosher-restaurants/israel/kosher/"
