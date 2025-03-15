from pages.restaurant_page import RestaurantPage
from pages.top_menu_page import TopMenuLinksPage
from pages.search_menu_page import SearchMenuPage
from pages.end_table_res_page import End_Table_Res_Page
from pages.search_results_page import SearchResultsPage
from pages.rest_page_make_reservation import RestOrderReservationPage
from pages.tabit_order_reservation_page import OrderReservationPage
import pytest
from selenium import webdriver
# from selenium.webdriver.chrome.webdriver import WebDriver


@pytest.fixture(scope="function", autouse=True)
def setup_driver_class(request):
    chrome_options = webdriver.ChromeOptions()

    # Disable notifications
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

    request.cls.driver = webdriver.Chrome(options=chrome_options)
    request.cls.driver.maximize_window()
    request.cls.driver.get("https://www.rest.co.il/")
    request.cls.driver.refresh()
    request.cls.search_menu = SearchMenuPage(request.cls.driver)
    request.cls.search_results = SearchResultsPage(request.cls.driver)
    request.cls.restaurant_page = RestaurantPage(request.cls.driver)
    request.cls.rest_reservation = RestOrderReservationPage(request.cls.driver)
    request.cls.tabit_reservation = OrderReservationPage(request.cls.driver)
    request.cls.confirm_reservation = End_Table_Res_Page(request.cls.driver)
    request.cls.top_menu = TopMenuLinksPage(request.cls.driver)
    yield
    request.cls.driver.quit()


