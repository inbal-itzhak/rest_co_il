from pages.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By


class Rest_TypePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    EATING_OUT_OPTIONS = (By.CSS_SELECTOR, "[data-id='sortersBlock'] .item")
    RIGHT_ARROW = (By.CSS_SELECTOR, ".page-section.articles.sorters .arrows-nav-right")
    LEFT_HIDDEN_ARROW = (By.CSS_SELECTOR, ".page-section.articles.sorters .arrows-nav-left.hide")
    KOSHER_REST_OPTIONS = (By.CSS_SELECTOR, "[class='page-section customers '] .item")
    BREAKFAST_OPTIONS = (By.CSS_SELECTOR, ".customer-think-about .item")
