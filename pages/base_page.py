from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



class BasePage:
    def __init__(self, driver):
        self.driver:webdriver = driver

    def send_text_by_locator(self, locator, text):
        el = self.driver.find_element(*locator)
        el.clear()
        el.send_keys(text)

    def send_text_by_element(self, el: WebElement , text):
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        text = self.driver.find_element(*locator).text
        return text

    def get_text_by_element(self, el: WebElement):
        text = el.text
        return text

    def wait_and_click(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(locator))
        element.click()

    def click(self, locator):
        element = self.driver.find_element(*locator)
        element.click()

    def click_el(self, el,  timeout=10):
        el.click()

    def get_list_of_elements(self, locator):
        el_list = self.driver.find_elements(*locator)
        return el_list

    def switch_to_frame(self, locator, timeout=10):  # Add timeout
        WebDriverWait(self.driver, timeout).until(ec.frame_to_be_available_and_switch_to_it(*locator))

    def switch_to_default_frame(self):
        self.driver.switch_to.default_content()

    def highlight(self, element):
        """Highlights a Selenium WebDriver element."""
        self.driver.execute_script("arguments[0].style.backgroundColor = 'yellow'", element)




