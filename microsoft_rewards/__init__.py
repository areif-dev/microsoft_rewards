from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def await_essential_element(query_selector: str) -> WebElement:
    """
    Tells the webdriver to wait for an element of a particular query selector.
    If the element is not found within the global WAIT_PERIOD, then the driver
    will quit and the program will exit with a status of 1

    :param query_selector: The string representing the CSS selector of the element
    to wait for
    :returns: Return the WebElement represented by the query_selector
    """

    try:
        elem = WebDriverWait(DRIVER, WAIT_PERIOD).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, query_selector)),
            "Could not find element: " + query_selector,
        )
    except Exception as e:
        print(e)
        DRIVER.quit()
        quit(1)

    return elem


def try_await_element(query_selector: str) -> WebElement:
    """
    Tells the webdriver to wait for an element of a particular query selector.
    If the element is not found within the global WAIT_PERIOD, then raise
    `selenium.common.exceptions.TimeoutException`

    :param query_selector: The string representing the CSS selector of the element
    to wait for
    :returns: Return the WebElement represented by the query_selector
    :raises: :exc: Raise `selenium.common.exceptions.TimeoutException` if the
    element is not found within `WAIT_PERIOD`
    """

    return WebDriverWait(DRIVER, WAIT_PERIOD).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, query_selector)),
        "Could not find element: " + query_selector,
    )


WAIT_PERIOD = 10
SHORT_WAIT = 3
DRIVER = webdriver.Firefox()
