import allure
import pytest

from tests.base_test import BaseTest


class TestSearch(BaseTest):
    data = ["ג'ירף ראשון לציון"]

    @allure.description("test with full restaurant name")
    @allure.title("search with full restaurant name")
    @pytest.mark.parametrize("rest_name_to_test", data)
    def test_search_full_name(self, rest_name_to_test):
        self.search_menu.search_restaurant_explicit(rest_name_to_test)
        self.restaurant_page.wait_for_rest_page_to_load()
        rest_name = self.restaurant_page.get_rest_name()
        allure.attach(body=f"{rest_name}", name="restaurant name from restaurant page",
                      attachment_type=allure.attachment_type.TEXT)
        # print(f"type of rest_name is {type(rest_name)}, rest name is {rest_name}")
        assert rest_name_to_test in rest_name

    data = ["גרג"]

    @allure.description("test with partial restaurant name - check autocomplete functionality")
    @allure.title("search with partial restaurant name - autocomplete")
    @pytest.mark.parametrize("text", data)
    def test_search_partial_text(self, text):
        self.search_menu.search_partial_text(text)
        self.restaurant_page.wait_for_rest_page_to_load()
        rest_name = self.restaurant_page.get_rest_name()
        allure.attach(body=f"{rest_name}", name="restaurant name in restaurant page:",
                      attachment_type=allure.attachment_type.TEXT)
        # print(f"type of rest_name is {type(rest_name)}, rest name is {rest_name}")
        assert text in self.restaurant_page.get_rest_name()

    data = ["ראש העין"]

    @allure.description("test search by city name check filter text and search results matches the city")
    @allure.title("search by city name")
    @pytest.mark.parametrize("text", data)
    def test_search_by_city_name(self, text):
        self.search_menu.search_partial_text(text)
        self.search_results.wait_for_search_results_page_to_load()
        self.search_results.compare_search_text_with_filters(text)
        address_text = self.search_results.get_rest_details()
        assert text in address_text

    data = ["מסעדת בשרים", "בתי קפה ", "ארוחת בוקר "]

    @allure.description("test search by cuisine type")
    @allure.title("test search by cuisine type")
    @pytest.mark.parametrize("text", data)
    def test_search_by_cuisine_type(self, text):
        self.search_menu.search_partial_text_without_autocomplete_selection(text)
        self.search_results.wait_for_search_results_page_to_load()
        self.search_results.compare_search_text_with_filters(text)
        cuisine_text = self.search_results.get_rest_details()
        assert text in cuisine_text

    @allure.description("test search with empty string - should end with an error")
    @allure.title("test search with empty string ")
    def test_search_empty_string(self):
        text = ""
        self.search_menu.search_partial_text_without_autocomplete_selection(text)
        input_error = self.search_menu.wait_for_input_error_element()
        assert input_error is True

    data = ["-", "_", "+", "/", "%", "#", "@", "*", ")", "(", "!"]

    @allure.description("test search with special chars: {text}")
    @allure.title("test search with special chars")
    @pytest.mark.parametrize("text", data)
    def test_special_chars(self, text):
        search_string = "גרג" + text
        allure.attach(body=f"{search_string}", name="search string",
                      attachment_type=allure.attachment_type.TEXT)
        # print(f"search string: {search_string}")
        clean_text = search_string.replace(text, " ")
        self.search_menu.search_partial_text_without_autocomplete_selection(search_string)
        results_page_load = self.search_results.wait_for_search_results_page_to_load()
        assert results_page_load is True
        search_results = self.search_results.get_all_search_results()
        assert len(search_results) > 0
        self.search_results.compare_search_text_with_filters(search_string)
        rest_name = self.search_results.get_rest_name()
        assert clean_text in rest_name

    @allure.description("test for a string that has no results")
    @allure.title("test for a string that has no results")
    def test_no_results(self):
        text = "בש-רים"
        self.search_menu.search_partial_text_without_autocomplete_selection(text)
        results_page_load = self.search_results.wait_for_search_results_page_to_load()
        assert results_page_load is True
        search_results = self.search_results.get_all_search_results()
        assert len(search_results) == 0
