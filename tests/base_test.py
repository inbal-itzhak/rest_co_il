from pages.end_table_res_page import End_Table_Res_Page
from pages.rest_page_make_reservation import RestOrderReservationPage
from pages.restaurant_page import RestaurantPage
from pages.search_menu_page import SearchMenuPage
from pages.search_results_page import SearchResultsPage
from pages.tabit_order_reservation_page import OrderReservationPage
from pages.top_menu_page import TopMenuLinksPage


class BaseTest():
    search_menu : SearchMenuPage
    search_results : SearchResultsPage
    restaurant_page: RestaurantPage
    rest_reservation : RestOrderReservationPage
    tabit_reservation : OrderReservationPage
    confirm_reservation : End_Table_Res_Page
    top_menu : TopMenuLinksPage