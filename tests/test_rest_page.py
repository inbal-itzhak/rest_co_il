import allure
import pytest

from tests.base_test import BaseTest


class TestRestPage(BaseTest):
    data = ["קפה גרג אפק", "פרש דה מרקט ראש", "ביגה", "אגאדיר הרצליה", "ראנץ' האוס מצפה הימים"]
    data2 = ["אגאדיר הרצליה", "קפה גרג אפק"]

    @pytest.mark.parametrize("text", data)
    @allure.description("test correct restaurant page opens")
    @allure.title("open restaurant name")
    def open_rest_page(self, text):
        self.search_menu.search_partial_text_without_autocomplete_selection(text)
        self.search_results.wait_for_search_results_page_to_load()
        self.search_results.click_on_search_result()
        self.restaurant_page.wait_for_rest_page_to_load()

    @pytest.mark.parametrize("text", data)
    @allure.description("test number of reviews in search results match the reviews in the restaurant page")
    @allure.title("verify number of reviews is correct")
    def test_match_reviews_amount(self, text):
        with allure.step("get number of reviews from search result"):
            self.search_menu.search_partial_text_without_autocomplete_selection(text)
            self.search_results.wait_for_search_results_page_to_load()
            num_of_reviews_search_results = self.search_results.get_num_of_reviews()
        self.search_results.click_on_search_result()
        self.restaurant_page.wait_for_rest_page_to_load()
        rest_name = self.restaurant_page.get_rest_name()
        assert text in rest_name
        with allure.step("get number of reviews from restaurant page"):
            reviews_amount = self.restaurant_page.get_reviews_amount()
            allure.attach(body=f"{reviews_amount}", name="number of reviews on restaurant page",
                          attachment_type=allure.attachment_type.TEXT)
            # print(f"reviews_amount is {reviews_amount}")
        assert reviews_amount is not None
        assert reviews_amount == num_of_reviews_search_results

    @pytest.mark.parametrize("text", data)
    @allure.description("test that the indication of open or closed is correct according to reported opening hours")
    @allure.title("verify restaurant open-close status is correct")
    def test_rest_open_now(self, text):
        self.search_menu.search_partial_text_without_autocomplete_selection(text)
        self.search_results.wait_for_search_results_page_to_load()
        is_rest_open_search = self.search_results.is_rest_open_now()
        self.search_results.click_on_search_result()
        self.restaurant_page.wait_for_rest_page_to_load()
        is_rest_open = self.restaurant_page.is_rest_open()
        assert is_rest_open_search == is_rest_open

    @pytest.mark.parametrize("text", data2)
    @allure.description("when reservation in the restaurant page - make sure reservation completes correctly  ")
    @allure.title("make reservation on restaurant page")
    def test_can_make_reservation(self, text):
        with allure.step("open restaurant page"):
            self.search_menu.search_partial_text_without_autocomplete_selection(text)
            self.search_results.wait_for_search_results_page_to_load()
            self.search_results.click_on_search_result()
            self.restaurant_page.wait_for_rest_page_to_load()
            expected_rest_name = self.restaurant_page.get_rest_name()
            allure.attach(body=f"{expected_rest_name}", name="expected rest name in test",
                          attachment_type=allure.attachment_type.TEXT)
            # print(f"expected rest name in test = {expected_rest_name}")
        if self.restaurant_page.is_reservation_in_rest_page():
            with allure.step("if reservation is in restaurant page - make reservation"):
                expected_reservation_data = self.restaurant_page.make_reservation_in_rest_page()
                allure.attach(body=f"{expected_reservation_data}", name="expected_reservation_data",
                              attachment_type=allure.attachment_type.TEXT)
                # print(f"expected_reservation_data: {expected_reservation_data}")
                assert expected_reservation_data is not None, "all time slots are disabled"
                self.confirm_reservation.wait_for_end_res_page_to_load()
            assert self.confirm_reservation.verify_rest_name(expected_rest_name) == True
            actual_reservation_data = self.confirm_reservation.get_reservation_data()
            allure.attach(body=f"{actual_reservation_data}", name="actual_reservation_data",
                          attachment_type=allure.attachment_type.TEXT)
            # print(f"actual_reservation_data : {actual_reservation_data}")
            assert actual_reservation_data == expected_reservation_data
        else:
            with allure.step("reservation is not is restaurant page - failing the test"):
                assert self.restaurant_page.is_reservation_in_rest_page(), (
                    "reservation is not in restaurant page - failing "
                    "the test")
