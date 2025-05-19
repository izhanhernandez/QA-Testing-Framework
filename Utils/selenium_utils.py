#!/usr/bin/env python

# ================================================================================================================================================ #
# SYSTEM CONFIGURATION
# ================================================================================================================================================ #

# -*- coding: utf-8 -*-

# ================================================================================================================================================ #
# TODO LIST
# ================================================================================================================================================ #

# ================================================================================================================================================ #
# DESCRIPTION
# ================================================================================================================================================ #

"""
selenium_utils.py es un módulo que proporciona funciones y clases auxiliares para trabajar con Selenium WebDriver.

Este módulo incluye:
- Inicialización y configuración de WebDriver
- Wrappers para operaciones comunes de Selenium
- Funciones de espera y manejo de timeouts
- Utilidades para captura de screenshots
- Helpers para interacción con elementos web

Las utilidades están diseñadas para simplificar la creación de tests de UI y proporcionar
una capa de abstracción sobre las funcionalidades básicas de Selenium.
"""

# ================================================================================================================================================ #
# IMPORTS
# ================================================================================================================================================ #

import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Importaciones locales
from .config import WEBDRIVER_PATH, HEADLESS, DEFAULT_TIMEOUT, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT, OP_SYS, REPORTS_FOLDER

# ================================================================================================================================================ #
# CONSTANTS
# ================================================================================================================================================ #

SCREENSHOTS_FOLDER = f"{REPORTS_FOLDER}screenshots/"

# Asegurar que existe la carpeta de screenshots
if not os.path.exists(SCREENSHOTS_FOLDER):
    os.makedirs(SCREENSHOTS_FOLDER)

# ================================================================================================================================================ #
# WEBDRIVER SETUP
# ================================================================================================================================================ #

def setup_chrome_driver(headless=None, download_dir=None):
    """
    Configura y devuelve una instancia de Chrome WebDriver.
    
    Args:
        headless (bool, optional): Si se debe ejecutar en modo headless. Por defecto usa la configuración global.
        download_dir (str, optional): Directorio para descargas. Por defecto usa la carpeta de descargas del sistema.
        
    Returns:
        webdriver.Chrome: Instancia configurada del WebDriver de Chrome
    """
    # Usar configuración global si no se especifica
    if headless is None:
        headless = HEADLESS
    
    # Configurar opciones de Chrome
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
    
    # Configuraciones comunes
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Configurar directorio de descargas si se especifica
    if download_dir:
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)
    
    try:
        # Intentar usar webdriver-manager para gestionar el driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.warning(f"Error al usar webdriver-manager: {e}")
        logging.info("Intentando usar webdriver local...")
        
        # Intentar usar webdriver local
        chrome_driver = "chromedriver.exe" if OP_SYS == "windows" else "chromedriver"
        driver_path = os.path.join(WEBDRIVER_PATH, chrome_driver)
        
        if os.path.exists(driver_path):
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            raise FileNotFoundError(f"No se encontró el webdriver en {driver_path}")
    
    # Configurar timeouts
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    
    return driver

# ================================================================================================================================================ #
# HELPER FUNCTIONS
# ================================================================================================================================================ #

def wait_for_element(driver, locator, timeout=None):
    """
    Espera a que un elemento esté presente en el DOM y sea visible.
    
    Args:
        driver (webdriver): Instancia de Selenium WebDriver
        locator (tuple): Tupla con el tipo de localizador y el valor (By.ID, "id_value")
        timeout (int, optional): Tiempo máximo de espera en segundos
        
    Returns:
        WebElement: El elemento web encontrado
        
    Raises:
        TimeoutException: Si el elemento no se encuentra en el tiempo especificado
    """
    if timeout is None:
        timeout = DEFAULT_TIMEOUT
        
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_element_located(locator))

def wait_for_element_clickable(driver, locator, timeout=None):
    """
    Espera a que un elemento esté presente en el DOM y sea clickeable.
    
    Args:
        driver (webdriver): Instancia de Selenium WebDriver
        locator (tuple): Tupla con el tipo de localizador y el valor (By.ID, "id_value")
        timeout (int, optional): Tiempo máximo de espera en segundos
        
    Returns:
        WebElement: El elemento web encontrado
        
    Raises:
        TimeoutException: Si el elemento no se encuentra en el tiempo especificado
    """
    if timeout is None:
        timeout = DEFAULT_TIMEOUT
        
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable(locator))

def safe_click(driver, locator, timeout=None):
    """
    Intenta hacer click en un elemento de forma segura, esperando a que sea clickeable.
    
    Args:
        driver (webdriver): Instancia de Selenium WebDriver
        locator (tuple): Tupla con el tipo de localizador y el valor (By.ID, "id_value")
        timeout (int, optional): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si el click fue exitoso, False en caso contrario
    """
    try:
        element = wait_for_element_clickable(driver, locator, timeout)
        element.click()
        return True
    except Exception as e:
        logging.error(f"Error al hacer click en {locator}: {e}")
        return False

def take_screenshot(driver, name=None):
    """
    Toma una captura de pantalla y la guarda en la carpeta de screenshots.
    
    Args:
        driver (webdriver): Instancia de Selenium WebDriver
        name (str, optional): Nombre para el archivo. Si no se proporciona, se usa timestamp
        
    Returns:
        str: Ruta del archivo de screenshot guardado
    """
    if name is None:
        name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if not name.endswith(".png"):
        name += ".png"
        
    screenshot_path = os.path.join(SCREENSHOTS_FOLDER, name)
    driver.save_screenshot(screenshot_path)
    logging.info(f"Screenshot guardado en: {screenshot_path}")
    
    return screenshot_path

def is_element_present(driver, locator):
    """
    Verifica si un elemento está presente en el DOM.
    
    Args:
        driver (webdriver): Instancia de Selenium WebDriver
        locator (tuple): Tupla con el tipo de localizador y el valor (By.ID, "id_value")
        
    Returns:
        bool: True si el elemento está presente, False en caso contrario
    """
    try:
        driver.find_element(*locator)
        return True
    except NoSuchElementException:
        return False

# ================================================================================================================================================ #
# MAIN EXECUTION
# ================================================================================================================================================ #

if __name__ == "__main__":
    # Ejemplo de uso
    driver = setup_chrome_driver()
    driver.get("https://www.google.com")
    print(f"Título de la página: {driver.title}")
    take_screenshot(driver, "google_homepage")
    driver.quit()
