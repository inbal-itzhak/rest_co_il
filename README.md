# Rest.co.il (by Zap) Website Test Automation

This project automates tests for the restaurant website [https://www.rest.co.il/](https://www.rest.co.il/) using Selenium and pytest.

## Project Structure
```
├── pages/
│   ├── base_page.py
│   ├── end_table_res_page.py
│   ├── rest_page_make_reservation.py
│   ├── rest_type_page.py
│   ├── restaurant_page.py
│   ├── search_menu_page.py
│   ├── search_results_page.py
│   ├── tabit_order_reservation_page.py
│   └── top_menu_page.py
├── tests/
│   ├── allure-results/
│   ├── base_test.py
│   ├── conftest.py
│   ├── test_rest_page.py
│   └── test_search.py
└── README.md
```
* **`pages`**: Contains page object classes representing different pages of the website.
* **`tests`**: Contains test scripts and configuration files.
    * **`test_rest_page.py`**: Test scripts related to the restaurant page and reservation functionalities.
    * **`test_search.py`**: Test scripts related to the search functionality.
    * **`base_test.py`**: Base test class for setup and teardown of tests.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/inbal-itzhak/rest_co_il
    cd rest_co_il
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS and Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt # requirements.txt is in the project
    ```

    (Make sure you create a `requirements.txt` file using `pip freeze > requirements.txt` to include all the necessary libraries.)

4.  **Download ChromeDriver:**
    * Download the ChromeDriver that matches your Chrome browser version from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
    * Place the ChromeDriver executable in a directory that is in your system's PATH, or specify the path to the ChromeDriver executable in your `conftest.py` if needed.

## Running Tests

1.  **Run all tests:**

    ```bash
    pytest tests/
    ```

2.  **Run specific test file:**

    ```bash
    pytest tests/test_search.py
    ```

3.  **Run specific test function:**

    ```bash
    pytest tests/test_search.py::test_search_full_name
    ```

4.  **Generate Allure report:**

    ```bash
    pytest tests/ --alluredir=allure-results
    allure serve allure-results/
    ```

    This will generate an Allure report in the `allure-results` directory and open it in your browser.

## Configuration
* **`conftest.py`**: This file contains the pytest configuration, including pytest fixtures, browser setup and teardown and screenshot capturing on test failure. You can modify the browser options and other settings here.
* **Test Data (Optional)**: If you need to use test data, you can create a JSON file (e.g., `test_data.json`) and load it in your tests or fixtures.

## Page Object Model

The project uses the Page Object Model (POM) design pattern to maintain test code reusability and maintainability. Each page of the website is represented by a separate class in the `pages/` directory.

## Allure Reports

The project uses Allure for test reporting. Allure provides detailed and interactive reports that help in analyzing test results.

