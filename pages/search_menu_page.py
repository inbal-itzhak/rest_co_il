import time

import allure
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class SearchMenuPage(BasePage):
    SEARCH_BOX = (By.CSS_SELECTOR, "#searchBoxHome")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#searchIconHome")
    SEARCH_INPUT_ERROR = (By.CSS_SELECTOR, ".upper-block.flex-center .input-search>.input-error")
    RESERVATION_LINK = (By.CSS_SELECTOR, ".flex-center.home-cover-btn [href='/reservations/']")
    DELIVERY_LINK = (By.CSS_SELECTOR, ".flex-center.home-cover-btn [href='https://www.mishlohim.co.il/']")
    FIND_REST_IN_MY_LOCATION = (By.CSS_SELECTOR, "[data-action='turnOnLocation']")
    AUTOCOMPLETE_OPTIONS = (By.CSS_SELECTOR, "#divAutoCompleteResultsHome li")
    RESERVATIONS_PAGE = (By.CSS_SELECTOR, ".site-main .orderComponent")
    DELIVERY_PAGE_MENU = (By.CSS_SELECTOR, ".menu_area")
    INPUT_ERROR = (By.CSS_SELECTOR, ".search-hover-cover .input-error")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("search restaurant by explicit restaurant name, search string: {search_string}")
    def search_restaurant_explicit(self, search_string):
        action = ActionChains(self.driver)
        search_box = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(self.SEARCH_BOX))
        self.send_text_by_element(search_box, search_string)
        time.sleep(2)
        # search_box.click()
        print(f"sent text {search_string}")
        action.send_keys(Keys.ARROW_DOWN).perform()
        WebDriverWait(self.driver,10).until(ec.element_to_be_clickable(self.SEARCH_BUTTON)).click()

    @allure.step("search restaurant with partial texts, search string:  {search_string}")
    def search_partial_text(self, search_string):
        try:
            search_box = self.driver.find_element(*self.SEARCH_BOX)
            if search_box:
                self.send_text_by_element(search_box, search_string)
                print(f"sent text {search_string}")
            self.wait_for_autocomplete_options()
            autocomplete_options = self.get_list_of_elements(self.AUTOCOMPLETE_OPTIONS)
            if autocomplete_options:
                print(f"autocomplete has {len(autocomplete_options)} values")
                if len(autocomplete_options) > 0:
                    WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(autocomplete_options[0]))
                    autocomplete_options[0].click()
            else:
                print("could not find element")
        except Exception as e:
            print(f"{e.with_traceback()}")

    @allure.step("search restaurant with partial texts and without selecting from autocomplete, search string:  {search_string}")
    def search_partial_text_without_autocomplete_selection(self, search_string):
        try:
            actions = ActionChains(self.driver)
            search_box = self.driver.find_element(*self.SEARCH_BOX)
            if search_box:
                self.send_text_by_element(search_box, search_string)
                actions.send_keys(Keys.RETURN).perform()
                print(f"sent text {search_string}")
        except Exception as e:
            print(f"{e.with_traceback()}")

    def order_reservations(self):
        self.click(self.RESERVATION_LINK)
        WebDriverWait(self.driver, 5).until(ec.presence_of_element_located(*self.RESERVATIONS_PAGE))

    def order_delivery(self):
        self.click(self.DELIVERY_LINK)
        WebDriverWait(self.driver, 5).until(ec.presence_of_element_located(*self.DELIVERY_PAGE_MENU))

    def search_partial(self, search_string):
        search_box = self.driver.find_element(*self.SEARCH_BOX)
        if search_box:
            self.send_text_by_element(search_box, search_string)
            self.click(self.SEARCH_BOX)
            print(f"sent text {search_string}")
            autocomplete_options = WebDriverWait(self.driver, 10).until(ec.presence_of_all_elements_located(self.AUTOCOMPLETE_OPTIONS))
        #   autocomplete_options = self.get_list_of_elements(self.AUTOCOMPLETE_OPTIONS)
            print(f"autocomplete has {len(autocomplete_options)} values")
            if len(autocomplete_options) > 0:
                for option in autocomplete_options:
                    try:
                        print(f"autocomplete option is {option.text.strip()}")
                        print(f"option element type is: {type(option)}")
                        option_text = option.text.strip()
                        print(f"text of autocomplete{option_text}")
                        if search_string in option_text :
                            self.click_el(option)
                            print(f"{search_string} is equal {option_text}")
                            return
                        else:
                            print(f"{search_string} is not equal {option_text}")
                    except StaleElementReferenceException:
                        print("Stale element, re-locating the options...")
                        break  # Retry the loop with fresh element references
            else:
                print("could not find autocomplete element")

    @allure.step("wait for autocomplete options")
    def wait_for_autocomplete_options(self):
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(self.AUTOCOMPLETE_OPTIONS))

    @allure.step("wait for error input tooltip")
    def wait_for_input_error_element(self):
        input_error = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(self.INPUT_ERROR))
        if input_error:
            return True
        else:
            print("no input error element found")
            return False
