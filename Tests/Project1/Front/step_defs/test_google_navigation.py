#!/usr/bin/env python

# ================================================================================================================================================ #
# IMPORTS
# ================================================================================================================================================ #

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Importaciones locales
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../.."))
from Utils.selenium_utils import setup_chrome_driver, wait_for_element, take_screenshot

# ================================================================================================================================================ #
# CONSTANTS
# ================================================================================================================================================ #

GOOGLE_URL = "https://www.google.com"
SEARCH_BOX = (By.NAME, "q")
GOOGLE_LOGO = (By.CSS_SELECTOR, "img[alt='Google']")

# ================================================================================================================================================ #
# SCENARIOS
# ================================================================================================================================================ #

scenarios('../features/google_navigation.feature')

# ================================================================================================================================================ #
# FIXTURES
# ================================================================================================================================================ #

@pytest.fixture
def browser():
    driver = setup_chrome_driver()
    yield driver
    driver.quit()

# ================================================================================================================================================ #
# STEP DEFINITIONS
# ================================================================================================================================================ #

@given("que abro el navegador")
def open_browser(browser):
    """Abrir el navegador utilizando el fixture."""
    assert browser is not None

@when("navego a la página de Google")
def navigate_to_google(browser):
    """Navegar a la página de Google."""
    browser.get(GOOGLE_URL)
    take_screenshot(browser, "google_homepage")

@then("debo ver la página principal de Google")
def verify_google_page(browser):
    """Verificar que estamos en la página principal de Google."""
    assert "Google" in browser.title
    # Verificar que el logo de Google está presente
    logo = wait_for_element(browser, GOOGLE_LOGO)
    assert logo is not None

@then("debo ver el campo de búsqueda")
def verify_search_field(browser):
    """Verificar que el campo de búsqueda está presente."""
    search_box = wait_for_element(browser, SEARCH_BOX)
    assert search_box is not None
    take_screenshot(browser, "google_search_box")
