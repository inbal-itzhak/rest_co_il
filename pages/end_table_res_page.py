import datetime

import allure

from pages.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class End_Table_Res_Page(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    RES_HEADLINE = (By.CSS_SELECTOR, ".orderTableDetailsWrapper")
    REST_NAME = (By.CSS_SELECTOR, ".address-desktop")
    RES_DATE_AND_TIME = (By.CSS_SELECTOR, "#clock-data")  # get attribute data-date
    NUM_OF_PEOPLE = (By.CSS_SELECTOR, "#guest-data")  # get attribute data-diners
    ORDER_PREFERENCES = (By.CSS_SELECTOR, "")

    @allure.step("wait for reservation conformation  page to load")
    def wait_for_end_res_page_to_load(self):
        WebDriverWait(self.driver,10).until(ec.visibility_of_element_located(self.RES_HEADLINE))

    @allure.step("verify restaurant name is {expected_rest_name}")
    def verify_rest_name(self, expected_rest_name):
        actual_rest_name = self.get_text(self.REST_NAME)
        if expected_rest_name in expected_rest_name:
            print(f"restaurant name is {actual_rest_name}")
            return True
        else:
            print(f" expected rest name is: {expected_rest_name}, actual rest name is {actual_rest_name}")
            return False


    def format_time(self, time_str, am_pm):
        try:
            time_obj = datetime.datetime.strptime(time_str + " " + am_pm, "%I:%M:%S %p").time()
            formatted_time = time_obj.strftime("%H:%M")
            return formatted_time
        except ValueError:
            return None

    def format_date(self, date_str):
        try:
            date_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y")
            formatted_date = date_obj.strftime("%d/%m/%y")
            return formatted_date
        except ValueError:
            return None

    @allure.step("get the date, time and num of guests in reservation")
    def get_reservation_data(self):
        res_time_el = self.driver.find_element(*self.RES_DATE_AND_TIME)
        date_date = res_time_el.get_attribute("data-date")
        num_of_guests = self.get_num_of_guests()
        date_and_time = date_date.split(" ")
        if len(date_and_time) == 3:
            date_str = date_and_time[0]
            time_str = date_and_time[1]
            am_pm = date_and_time[2]
            formatted_time = self.format_time(time_str,am_pm)
            formatted_date = self.format_date(date_str)
            return formatted_date, formatted_time, num_of_guests

    def get_num_of_guests(self):
        num_of_guests_el = self.driver.find_element(*self.NUM_OF_PEOPLE)
        data_diners = num_of_guests_el.get_attribute("data-diners")
        if data_diners:
            return int(data_diners)


