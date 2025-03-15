import allure

from pages.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RestOrderReservationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    SEARCH_RESULTS_HEADLINE = (By.CSS_SELECTOR, "[class='restaurant-info-top'] h2")
    BOOK_TABLE_HEADLINE = (By.CSS_SELECTOR, ".OrderRestaurantWrapper .timeTableComponent")
    REST_NAME = (By.CSS_SELECTOR, "[class='orderRestaurantDataComponent'] h1")
    DATE_FIELD = (By.CSS_SELECTOR, "div .date-div")
    DATE_TIME_PICKER_AVAILABLE_DAYS = (By.CSS_SELECTOR, "[data-handler='selectDay']")
    GUESTS_FIELD = (By.CSS_SELECTOR, "[name='guests']")
    SELECT_GUESTS_NUM = (By.CSS_SELECTOR, ".guests li")
    SELECT_TIME = (By.CSS_SELECTOR, ".booking_time_row .booking_time_column")
    TIME_NOT_AVAILABLE = (By.CSS_SELECTOR, ".booking_time_row .booking_time_column.disabled")

    @allure.step("wait for reservation page to load")
    def wait_for_rest_res_page_to_load(self):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(*self.SEARCH_RESULTS_HEADLINE))

    def get_available_dates(self):
        self.click(self.driver.find_element(self.DATE_FIELD))
        available_dates = self.driver.find_elements(self.DATE_TIME_PICKER_AVAILABLE_DAYS)
        if len(available_dates) > 0:
            return available_dates

    @allure.step("select available date from date time picker")
    def select_date(self, index):
        available_dates = self.get_available_dates()
        if len(available_dates) > index:
            self.click(available_dates[index])

    @allure.step("select number of guests in reservation")
    def select_num_of_guests(self, num_of_guests):
        self.click(self.driver.find_element(self.GUESTS_FIELD))
        num_of_guests_list = self.driver.find_elements(self.SELECT_GUESTS_NUM)
        if num_of_guests <= 2:
            self.click(num_of_guests_list[0])
        else:
            self.click((num_of_guests_list[num_of_guests-1]))

    @allure.step("select time in reservation")
    def select_time(self):
        time_options = self.driver.find_elements(self.SELECT_TIME)
        for time_option in time_options:
            time = time_option.get_attribute("class")
            if "disabled" in time:
                time_options.remove(time_option)
        self.click(time_options[0])




