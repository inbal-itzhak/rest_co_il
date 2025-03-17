import allure
from selenium.common import NoSuchElementException, TimeoutException
import time
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains


class RestaurantPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    REST_NAME = (By.CSS_SELECTOR, ".main_banner .reviews_info_box")
    REST_ADDRESS = (By.CSS_SELECTOR, "")
    NEARBY_RESTAURANTS = (By.CSS_SELECTOR, "")
    SHOW_MORE_REVIEWS_BTN = (By.CSS_SELECTOR, ".show_more_btn.bottom_btn")
    OPINION_WIDGET = (By.CSS_SELECTOR, "[class='opinion_widget']")
    REST_DATA_DOES_NOT_EXIST = (By.CSS_SELECTOR, ".non_paying_main_banner .gallery_info_column")
    REST_DATA_EXISTS = (By.CSS_SELECTOR, ".gallery_area.customer-exists")
    REST_OPEN = (By.CSS_SELECTOR, ".gallery_info_right.opening_hours strong")
    REST_CLOSED = (By.CSS_SELECTOR, ".gallery_info_right.opening_hours .closed")
    ORDER_TABLE_BTN = (By.CSS_SELECTOR, "[data-ordertabledesktop]")
    MORE_REVIEWS = (By.CSS_SELECTOR, "[data-reviews-count]")
    ALL_REVIEWS = (By.CSS_SELECTOR, ".review_content")
    NO_REVIEWS = (By.CSS_SELECTOR, ".user_rating_inner")
    DATE_PICKER = (By.CSS_SELECTOR, "[name='datepicker']")
    SELECT_DAYS = (By.CSS_SELECTOR, "[data-handler='selectDay']")
    SELECTED_DAY = (By.CSS_SELECTOR, "[data-date-display]")
    NUM_OF_GUESTS = (By.CSS_SELECTOR, "[name='orderTableDinersVal']")
    TIME_DISABLED = (By.CSS_SELECTOR, ".disabled")
    ALL_TIME_SLOTS = (By.CSS_SELECTOR, ".booking_time_row .booking_time_column")
    TIME_SLOT_CLICK = (By.CSS_SELECTOR, ".booking_column_bg")
    BOOKING_DATA_CONTAINER = (By.CSS_SELECTOR, ".tab_left_info .booking_time_container")
    REVIEW_INFO_BOX = (By.XPATH, "//*[@class='reviews_info_box']/h1")

    @allure.step("wait for restaurant  page to load")
    def wait_for_rest_page_to_load(self):
        try:
            WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(self.REST_NAME))
        except TimeoutException:
            WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(self.REVIEW_INFO_BOX))

    @allure.step("verify correct restaurant page opens: {rest_name}")
    def verify_correct_rest_page_open(self, rest_name):
        rest_name_in_page = self.driver.find_element(self.REST_NAME)
        if rest_name in rest_name_in_page:
            return True

    def get_restaurant_name(self):
        rest_name = self.get_text(self.REST_NAME)
        return rest_name

    @allure.step("get the number of reviews in restaurant page")
    def get_reviews_amount(self):
        try:
            reviews = self.get_list_of_elements(self.ALL_REVIEWS)
            if len(reviews) == 5:
                if self.driver.find_element(*self.MORE_REVIEWS):
                    more_reviews = self.get_text(self.MORE_REVIEWS)
                    more_reviews_int = int(more_reviews)
                    return len(reviews) + more_reviews_int
                else:
                    return len(reviews)
            elif len(reviews) >= 0:
                return len(reviews)
        except NoSuchElementException:
            try:
                no_reviews = self.driver.find_element(self.NO_REVIEWS)
                if no_reviews:
                    return 0
            except NoSuchElementException:
                return None

    @allure.step("get restaurant name from restaurant page")
    def get_rest_name(self):
        try:
            rest_name_el = self.driver.find_element(*self.REST_NAME)
            if rest_name_el is not None:
                heb_name = self.get_text_by_element(rest_name_el)
                rest_name = heb_name
                return rest_name
            else:
                return "could not retrieve restaurant name"
        except NoSuchElementException:
            rest_name_el = self.get_text(self.REVIEW_INFO_BOX)
            print(rest_name_el)
            return rest_name_el

    @allure.step("check if restaurant is open")
    def is_rest_open(self):
        try:
            if self.driver.find_element(*self.REST_DATA_EXISTS):
                rest_open = self.driver.find_element(*self.REST_OPEN)
                is_open = rest_open.get_attribute("class")
                print(f"is open attr = {is_open}")
                if is_open == "closed":
                    allure.attach(body="restaurant is closed", name="restaurant is closed",
                                  attachment_type=allure.attachment_type.TEXT)
                    # print("rest is closed")
                    return False
                else:
                    allure.attach(body="restaurant is open", name="restaurant is open",
                                  attachment_type=allure.attachment_type.TEXT)
                    # print("rest is open")
                    return True
        except NoSuchElementException:
            print("could not retrieve opening hours")
            return False

    def can_make_reservation(self):
        if self.driver.find_element(*self.ORDER_TABLE_BTN):
            return True
        else:
            return False

    @allure.step("check if reservation is available from restaurant page")
    def is_reservation_in_rest_page(self):
        try:
            order_table_btn = self.driver.find_element(*self.ORDER_TABLE_BTN)
            data_scroll_to = order_table_btn.get_attribute("data-scroll-to")
            if data_scroll_to == "#customerAboutThePlaceBlock":
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    @allure.step("make reservation from restaurant page")
    def make_reservation_in_rest_page(self):
        wait = WebDriverWait(self.driver, 10)
        if self.is_reservation_in_rest_page():
            self.click_make_reservation_btn()
            self.click(self.DATE_PICKER)
            all_days = self.get_list_of_elements(self.SELECT_DAYS)
            self.click_el(all_days[0])
            selected_day = self.get_text(self.SELECTED_DAY)
            wait.until(ec.presence_of_element_located(self.NUM_OF_GUESTS))
            guests_element = self.driver.find_element(*self.NUM_OF_GUESTS)
            num_of_guests_str = guests_element.get_attribute("value")
            try:
                num_of_guests = int(num_of_guests_str)
            except ValueError:
                num_of_guests = None
            booking_data_container = self.driver.find_element(*self.BOOKING_DATA_CONTAINER)
            actions = ActionChains(self.driver)
            actions.move_to_element(booking_data_container).perform()
            print("moved")
            time_slots = (WebDriverWait(self.driver, 5).until
                          (ec.presence_of_all_elements_located(self.ALL_TIME_SLOTS)))
            for time_slot in time_slots:
                try:
                    class_time_slot = time_slot.get_attribute("class")
                    print(class_time_slot)
                    # time_slot.find_element(*self.TIME_DISABLED)
                    if "disabled" in class_time_slot:
                        span_element = time_slot.find_element(By.CSS_SELECTOR, "span")
                        time_text = self.get_text_by_element(span_element)
                        self.highlight(span_element)
                        allure.attach(body=f"{time_text}", name="time is disabled, cannot select time",
                                      attachment_type=allure.attachment_type.TEXT)
                        # print(f"time {time_text} is disabled cannot select time")
                    else:
                        span_element = time_slot.find_element(By.CSS_SELECTOR, "span")
                        time_text = self.get_text_by_element(span_element)
                        print(f"time {time_text} is enabled click this time slot")
                        time_slot_click = time_slot.find_element(*self.TIME_SLOT_CLICK)
                        self.highlight(time_slot_click)
                        time.sleep(1)
                        actions = ActionChains(self.driver)
                        actions.move_to_element(time_slot_click).click(time_slot_click).perform()
                        try:
                            wait.until(ec.invisibility_of_element_located(self.BOOKING_DATA_CONTAINER))
                        except TimeoutException:
                            print("booking container is still in page - click did not occur, retrying... ")
                            actions.click(span_element)
                            wait.until(ec.invisibility_of_element_located(self.BOOKING_DATA_CONTAINER))
                        return selected_day, time_text, num_of_guests
                except NoSuchElementException:
                    print("element not found")

    @allure.step("click on 'make reservation' button - reservation on restaurant page")
    def click_make_reservation_btn(self):
        self.click(self.ORDER_TABLE_BTN)

    def get_num_of_guests(self):
        guests_element = self.driver.find_element(*self.NUM_OF_GUESTS)
        num_of_guests = guests_element.get_attribute("value")
        return num_of_guests
