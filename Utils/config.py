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
config.py es un módulo central que proporciona configuraciones globales para el framework de testing QA.

Este módulo gestiona:
- Rutas de directorios y archivos importantes
- Variables de entorno para diferentes configuraciones de ejecución
- Constantes utilizadas en todo el framework
- Configuración de webdrivers según el sistema operativo
- Parámetros de timeout y espera para tests

La configuración está diseñada para ser modular y adaptable a diferentes entornos de ejecución
(desarrollo, pruebas, CI/CD) y sistemas operativos.
"""

# ================================================================================================================================================ #
# IMPORTS
# ================================================================================================================================================ #

import os
import sys
import json
import yaml
import platform
from dotenv import load_dotenv

# ================================================================================================================================================ #
# CONSTANTS
# ================================================================================================================================================ #

# Detección del Sistema Operativo
OP_SYS = "mac" if "mac" in platform.platform().lower() else "linux"
if "windows" in platform.platform().lower(): OP_SYS = "windows"
PATH_SEPARATOR = "\\" if OP_SYS == "windows" else "/"

# Rutas de directorios
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__)) + PATH_SEPARATOR
MAIN_FOLDER = f"{CURRENT_FOLDER}..{PATH_SEPARATOR}"
WEBDRIVERS_FOLDER = f"{MAIN_FOLDER}Webdrivers{PATH_SEPARATOR}"
ASSETS_FOLDER = f"{MAIN_FOLDER}Assets{PATH_SEPARATOR}"
TESTS_FOLDER = f"{MAIN_FOLDER}Tests{PATH_SEPARATOR}"
REPORTS_FOLDER = f"{MAIN_FOLDER}Reports{PATH_SEPARATOR}"

# Webdrivers según sistema operativo
WEBDRIVER_PATH = f"{WEBDRIVERS_FOLDER}{'Windows' if OP_SYS == 'windows' else 'Unix'}{PATH_SEPARATOR}"

# Carga de variables de entorno
load_dotenv(f"{MAIN_FOLDER}.env")

# Entorno de ejecución
ENV = os.environ.get("ENVIRONMENT", "TEST")
HEADLESS = os.environ.get("HEADLESS", "TRUE").upper() == "TRUE"

# Timeouts y esperas
DEFAULT_TIMEOUT = int(os.environ.get("DEFAULT_TIMEOUT", "30"))
IMPLICIT_WAIT = int(os.environ.get("IMPLICIT_WAIT", "10"))
PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "60"))

# URLs base para tests
BASE_URL = os.environ.get("BASE_URL", "https://www.google.com")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://jsonplaceholder.typicode.com")

# ================================================================================================================================================ #
# FUNCTIONS
# ================================================================================================================================================ #

def get_config():
    """
    Devuelve un diccionario con todas las configuraciones actuales.
    
    Returns:
        dict: Configuración completa del framework
    """
    return {
        "os": OP_SYS,
        "env": ENV,
        "headless": HEADLESS,
        "webdriver_path": WEBDRIVER_PATH,
        "timeouts": {
            "default": DEFAULT_TIMEOUT,
            "implicit_wait": IMPLICIT_WAIT,
            "page_load": PAGE_LOAD_TIMEOUT
        },
        "urls": {
            "base": BASE_URL,
            "api": API_BASE_URL
        }
    }

def load_config_file(config_file):
    """
    Carga configuración desde un archivo JSON o YAML.
    
    Args:
        config_file (str): Ruta al archivo de configuración
        
    Returns:
        dict: Configuración cargada desde el archivo
    """
    if not os.path.exists(config_file):
        return {}
        
    try:
        if config_file.endswith('.json'):
            with open(config_file, 'r') as f:
                return json.load(f)
        elif config_file.endswith(('.yaml', '.yml')):
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            return {}
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}

def create_folder_if_not_exists(folder_path):
    """
    Crea una carpeta si no existe.
    
    Args:
        folder_path (str): Ruta de la carpeta a crear
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Crear carpetas necesarias si no existen
create_folder_if_not_exists(REPORTS_FOLDER)

# ================================================================================================================================================ #
# MAIN EXECUTION
# ================================================================================================================================================ #

if __name__ == "__main__":
    print(json.dumps(get_config(), indent=4))
