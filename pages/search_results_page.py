import allure
from selenium.common import TimeoutException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pages.rest_page_make_reservation import RestOrderReservationPage


class SearchResultsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    TEXT_FILTERED = (By.CSS_SELECTOR, ".sidebar .tags-item-holder")
    ALL_FILTERS = (By.CSS_SELECTOR, ".tags-item-holder>[data-tag]")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".feature-column .feature-col-info")
    SEARCH_RESULTS_CLICK = (By.CSS_SELECTOR, ".feature-column-photo")
    REST_TITLE = (By.CSS_SELECTOR, "#customersContainer .feature-column .rest-title a")
    REST_DETAILS = (By.CSS_SELECTOR, "#customersContainer .feature-column p")
    REST_DETAILS_BTN = (By.CSS_SELECTOR, ".restaurant-details-box .details-column [class='details-link-item']")
    REST_DETAILS_LINK = (By.CSS_SELECTOR, "#customersContainer .feature-column .details-link-item")
    DELIVERY_LINK = (By.CSS_SELECTOR, "#customersContainer .feature-column .details-column.ver-mid")
    RESERVATION_LINK = (By.CSS_SELECTOR, "#customersContainer .feature-column .details-link-item.red-btn-color")
    OPEN_HOURS = (By.CSS_SELECTOR, ".rested-drop-container .rested-drop span")
    IS_OPEN_STATUS = (By.CSS_SELECTOR, "span [data-open-status]")  # optional only if rest has opening hours updated
    CLEAR_FILTER = (By.CSS_SELECTOR, ".sidebar .clear-all")
    SORT_RESULTS_BY = (By.CSS_SELECTOR, "[data-sort-menu-options]")
    STAR_SLIDER = (By.CSS_SELECTOR, ".yellow-star-slider")
    NO_REVIEWS_INDICATOR = (By.CSS_SELECTOR, ".reviews_box .main_info_stars_noreviews")
    NUM_OF_REVIEWS_TEXT = (By.CSS_SELECTOR, ".reviews_box a>small")
    SEARCH_SIDEBAR = (By.CSS_SELECTOR, "[data-block='searchSorters']")

    @allure.step("wait for search results page to load")
    def wait_for_search_results_page_to_load(self):
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located(self.SEARCH_SIDEBAR))
            return True
        except TimeoutException:
            allure.attach(body="results page did not load on time", name="results page did not load on time",
                          attachment_type=allure.attachment_type.TEXT)
            # print("results page did not load on time")
            return False

    @allure.step("check if restaurant is open now - search page")
    def is_rest_open_now(self):
        try:
            now = datetime.datetime.now().time()
            current_day = now.strftime("%a")
            if self.driver.find_element(*self.IS_OPEN_STATUS):
                self.click(self.IS_OPEN_STATUS)
                if len(self.driver.find_elements(*self.OPEN_HOURS)) > 0:
                    open_hours_elements = self.get_list_of_elements(self.OPEN_HOURS)
                    if len(open_hours_elements) > 0:
                        print(f"open_hours_elements > 0 {len(open_hours_elements)}")
                        for element in open_hours_elements:
                            parts = self.get_text_by_element(element).splitlines()
                            print(f"{parts}")
                            if len(parts) == 2:
                                days = parts[0]
                                print(f"days: {days}")
                                hours = parts[1]
                                print(f"hours: {hours}")
                                en_days = (self.convert_hebrew_days_to_en(days))
                                print(en_days)
                                if current_day in en_days:
                                    hours_range = hours.split("-")
                                    print(f"hours range: {hours_range}")
                                    if len(hours_range) == 2:
                                        try:
                                            start_time = datetime.datetime.strptime(hours_range[0].strip(),
                                                                                    "%H:%M").time()
                                            print(f"start_time: {start_time}")
                                            end_time = datetime.datetime.strptime(hours_range[1].strip(),
                                                                                  "%H:%M").time()
                                            print(f"end_time: {end_time}")
                                            print(f"now: {now}")
                                            if start_time <= end_time:
                                                if start_time <= now <= end_time:
                                                    allure.attach(body="restaurant is open", name="restaurant is open",
                                                                  attachment_type=allure.attachment_type.TEXT)
                                                    # print("restaurant is open")
                                                    self.click(self.IS_OPEN_STATUS)
                                                    return True
                                                else:
                                                    allure.attach(body="restaurant is closed",
                                                                  name="restaurant is closed",
                                                                  attachment_type=allure.attachment_type.TEXT)
                                                    # print("restaurant is closed")
                                                    self.click(self.IS_OPEN_STATUS)
                                                    return False
                                            elif start_time <= now or now <= end_time:
                                                allure.attach(body="restaurant is open", name="restaurant is open",
                                                              attachment_type=allure.attachment_type.TEXT)
                                                # print("restaurant is open")
                                                self.click(self.IS_OPEN_STATUS)
                                                return True
                                        except ValueError:
                                            allure.attach(body="Error parsing time", name="Error parsing time",
                                                          attachment_type=allure.attachment_type.TEXT)
                                            # print("Error parsing time")
                                            return False
                                    else:
                                        print(f"hour range is incorrect: {hours_range}")
                                elif en_days is None:
                                    print("en_days is none: {en_days}")
                            else:
                                print(f"parts is not correct {parts}")
                    else:
                        allure.attach(body="could not retrieve open status", name="could not retrieve open status",
                                      attachment_type=allure.attachment_type.TEXT)
                        # print(f"could not retrieve open status")
        except Exception as e:
            allure.attach(body=f"{e}", name="exception thrown",
                          attachment_type=allure.attachment_type.TEXT)
            # print(f"exception thrown: {e}")
            return False

    def check_if_today_in_list(self, en_days):
        now = datetime.datetime.now()
        today = now.strftime("%a")
        if today in en_days:
            return True

    def check_if_now_in_time_range(self, start_time, end_time):
        now = datetime.datetime.now()
        if start_time <= now <= end_time:
            return True

    def convert_hebrew_days_to_en(self, day):
        hebrew_to_english = {
            "א'": "Sun",
            "ב'": "Mon",
            "ג'": "Tue",
            "ד'": "Wed",
            "ה'": "Thu",
            "ו'": "Fri",
            "ש'": "Sat"
        }
        try:
            hebrew_range = day.split()[0]
            start_day, end_day = day.split('-')
            print(f"start day is {start_day}")
            start_day = start_day.strip()
            end_day = end_day.strip()
            print(f"end day is {end_day}")

            start_index = list(hebrew_to_english.keys()).index(start_day)
            end_index = list(hebrew_to_english.keys()).index(end_day)

            if start_index > end_index:
                return None  # invalid range

            result = [hebrew_to_english[day] for day in list(hebrew_to_english.keys())[start_index:end_index + 1]]
            return result

        except (ValueError, KeyError, Exception) as e:
            print(f"error in convert_hebrew_days_to_en {e}")
            return None  # Invalid input format or Hebrew day

    def compare_search_text_with_filters(self, search_string):
        filters = self.get_list_of_elements(self.ALL_FILTERS)
        for search_filter in filters:
            filter_text = self.get_text_by_element(search_filter)
            if search_string in filter_text:
                allure.attach(body=f"search string {search_string} is in the search filter {filter_text}",
                              name="search string is in search filter",
                              attachment_type=allure.attachment_type.TEXT)
                # print(f"search string {search_string} is in the search filter {filter_text} ")
                return True
            else:
                allure.attach(body=f"search string {search_string} is not in the search filter {filter_text}",
                              name="search string is not in search filter",
                              attachment_type=allure.attachment_type.TEXT)
                # print(f"search string {search_string} is not in the search filter {filter_text} ")

    def get_rest_details(self):
        rest_address = self.driver.find_element(*self.REST_DETAILS)
        address_text = self.get_text_by_element(rest_address)
        allure.attach(body=f"{address_text}", name="address text: ",
                      attachment_type=allure.attachment_type.TEXT)
        # print(address_text)
        return address_text

    def verify_rest_title_match_search(self, search_string):
        restaurant_name = self.get_text(self.driver.find_element(self.REST_TITLE))
        if search_string in restaurant_name:
            return True
        else:
            return False

    def get_rest_rate(self):
        start_slider = self.driver.find_element(self.STAR_SLIDER)
        if start_slider is not None:
            rate_text = self.get_text(start_slider.get_attribute("style"))
            percent_text = rate_text.split("width:")[1].split("%")[0]
            try:
                percent_int = int(percent_text)
                return percent_int
            except Exception as e:
                allure.attach(body=f"{e}", name="exception thrown",
                              attachment_type=allure.attachment_type.TEXT)
                # print(f"{e}")
                return 0

    @allure.step("get restaurant number of reviews from search results")
    def get_num_of_reviews(self):
        try:
            if self.driver.find_element(*self.NUM_OF_REVIEWS_TEXT):
                text_num_of_reviews = self.get_text(self.NUM_OF_REVIEWS_TEXT)
                all_text = text_num_of_reviews.split()
                num_of_reviews = int(all_text[0])
                return num_of_reviews
            elif self.driver.find_element(self.NO_REVIEWS_INDICATOR):
                return 0
        except Exception as e:
            allure.attach(body=f"{e}", name="exception thrown",
                          attachment_type=allure.attachment_type.TEXT)
            # print(f"{e}")
            return 0

    def get_rest_name(self):
        return self.get_text(self.REST_TITLE)

    def get_all_search_results(self):
        search_results = self.get_list_of_elements(self.SEARCH_RESULTS)
        return search_results

    @allure.step("click on a search result")
    def click_on_search_result(self):
        search_results = self.get_all_search_results()
        if len(search_results) > 0:
            try:
                allure.attach(body=f"{len(search_results)}", name="number of search results",
                              attachment_type=allure.attachment_type.TEXT)
                # print(f"len of search results = {len(search_results)}")
                # search_results[0].find_element(By.CSS_SELECTOR, ".feature-column-photo").click()
                # WebDriverWait(self.driver,10).until(ec.element_to_be_clickable(search_results[0]))
                # self.click_el(search_results[0])
                WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.REST_DETAILS_BTN)).click()
                print("clicked search result")
            except Exception as e:
                allure.attach(body=f"{e}", name="exception thrown",
                              attachment_type=allure.attachment_type.TEXT)
                # print(f"exceptin thrown {e}")

    def click_on_make_reservation(self):
        reservation_page = RestOrderReservationPage(self.driver)
        try:
            if self.driver.find_element(*self.RESERVATION_LINK):
                self.click(self.RESERVATION_LINK)
                reservation_page.wait_for_rest_res_page_to_load()
                return True
            else:
                allure.attach(body="no reservation link - unable to make reservation",
                              name="no reservation link - unable to make reservation",
                              attachment_type=allure.attachment_type.TEXT)
                # print("no reservation link - unable to make reservation")
                return False
        except Exception as e:
            allure.attach(body=f"{e}", name="exception in make reservation page",
                          attachment_type=allure.attachment_type.TEXT)
            # print(f"exception in make reservation page: {e}")
