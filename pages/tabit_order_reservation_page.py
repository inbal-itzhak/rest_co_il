from pages.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class OrderReservationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    ORDER_RESERVATION_HEADLINE = (By.CSS_SELECTOR, "[data-container='restaurantData'] h1")
    DATE_FIELD = (By.CSS_SELECTOR, ".date.reservation-details-item")
    AVAILABLE_DATES = (By.CSS_SELECTOR , "mat-option")
    TIME_FIELD = (By.CSS_SELECTOR , ".time.reservation-details-item")
    AVAILABLE_TIMES = (By.CSS_SELECTOR , "mat-option")
    NUM_OF_GUESTS_FIELD = (By.CSS_SELECTOR, ".guests-number")
    NUM_OF_GUESTS_OPTIONS = (By.CSS_SELECTOR, "mat-option")
    PREFERRED_AREA = (By.CSS_SELECTOR, ".value.preference-name")
    PREFERRED_AREA_OPTIONS = (By.CSS_SELECTOR, "[role='option']")
    MAKE_RES_BTN = (By.CSS_SELECTOR, "div .search-button")
    # TIME_OPTIONS_FUTURE = (By.CSS_SELECTOR, "[data-hours-list='future'] li")
    # NUM_OF_GUESTS_FIELD = (By.CSS_SELECTOR, "[data-item-display='diners']")
    # NUM_OF_GUESTS_OPTIONS = (By.CSS_SELECTOR, "[data-drop='guests'] .booking_select_dropdown li")
    TABIT_FRAME = (By.CSS_SELECTOR, "tabit-iframe")

    def wait_for_rest_res_page_to_load(self):
        WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located(*self.ORDER_RESERVATION_HEADLINE))

    def verify_rest_name(self, rest_name):
        rest_res_name = self.driver.find_element(self.ORDER_RESERVATION_HEADLINE)
        if rest_name in rest_res_name:
            print(f"restaurant reservation name is {rest_res_name}, restaurant name is {rest_name}")
            return True
        else:
            return False

    def select_date(self, num_of_days_from_today):
        self.switch_to_frame(self.TABIT_FRAME)
        self.click(self.driver.find_element(self.DATE_FIELD))
        available_dates = self.driver.find_elements(self.AVAILABLE_DATES)
        if len(available_dates) <= num_of_days_from_today:
            self.click(available_dates[num_of_days_from_today])
        else:
            # select last element in the available dates list
            self.click(available_dates[-1])
        self.switch_to_default_frame()

    def select_time(self,time_box_index):
        self.switch_to_frame(self.TABIT_FRAME)
        self.click(self.driver.find_element(self.TIME_FIELD))
        available_times = self.driver.find_elements(self.AVAILABLE_TIMES)
        if len(available_times) <= time_box_index:
            self.click(available_times[time_box_index])
        else:
            self.click(available_times[-1])
        self.switch_to_default_frame()

    def select_num_of_guest(self, num_of_guests):
        self.switch_to_frame(self.TABIT_FRAME)
        self.click(self.driver.find_element(self.NUM_OF_GUESTS_FIELD))
        num_of_guests_list = self.driver.find_elements(self.NUM_OF_GUESTS_OPTIONS)
        if len(num_of_guests_list) <= num_of_guests:
            self.click(num_of_guests_list[num_of_guests])
        else:
            self.click(num_of_guests_list[-1])
        self.switch_to_default_frame()

    def select_preferred_area(self):
        self.switch_to_frame(self.TABIT_FRAME)
        self.click(self.driver.find_element(self.PREFERRED_AREA))
        preferred_areas = self.driver.find_elements(self.PREFERRED_AREA_OPTIONS)
        if len(preferred_areas) > 0:
            preferred_area = self.get_text(preferred_areas[0])
            self.click(preferred_areas[0])
        else:
            return "no preferred areas in restaurant"
        self.switch_to_default_frame()

    def get_preferred_area_text(self):
        self.switch_to_frame(self.TABIT_FRAME)
        preferred_area_text = self.get_text(self.driver.find_element(self.PREFERRED_AREA))
        self.switch_to_default_frame()
        return preferred_area_text

    def click_on_make_reservation(self):
        self.switch_to_frame(self.TABIT_FRAME)
        self.click(self.driver.find_element(self.MAKE_RES_BTN))

