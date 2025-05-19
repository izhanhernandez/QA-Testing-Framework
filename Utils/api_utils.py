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
api_utils.py es un módulo que proporciona funciones y clases auxiliares para realizar pruebas de APIs.

Este módulo incluye:
- Funciones para realizar peticiones HTTP (GET, POST, PUT, DELETE)
- Validación de respuestas y esquemas JSON
- Manejo de autenticación y headers
- Utilidades para manipular datos de respuesta
- Funciones de logging para peticiones y respuestas

Las utilidades están diseñadas para simplificar la creación de tests de API y proporcionar
una capa de abstracción sobre las funcionalidades básicas de requests.
"""

# ================================================================================================================================================ #
# IMPORTS
# ================================================================================================================================================ #

import os
import json
import logging
import requests
import jsonschema
from datetime import datetime
from requests.exceptions import RequestException

# Importaciones locales
from .config import API_BASE_URL, DEFAULT_TIMEOUT

# ================================================================================================================================================ #
# CONSTANTS
# ================================================================================================================================================ #

# Headers comunes
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# ================================================================================================================================================ #
# API REQUEST FUNCTIONS
# ================================================================================================================================================ #

def make_request(method, endpoint, params=None, data=None, headers=None, timeout=None, verify=True, base_url=None):
    """
    Realiza una petición HTTP genérica.
    
    Args:
        method (str): Método HTTP (GET, POST, PUT, DELETE)
        endpoint (str): Endpoint de la API (sin incluir base_url)
        params (dict, optional): Parámetros de query string
        data (dict, optional): Datos para enviar en el cuerpo de la petición
        headers (dict, optional): Headers HTTP
        timeout (int, optional): Timeout en segundos
        verify (bool, optional): Verificar certificado SSL
        base_url (str, optional): URL base para la petición
        
    Returns:
        requests.Response: Objeto de respuesta
        
    Raises:
        RequestException: Si ocurre un error en la petición
    """
    # Usar valores por defecto si no se especifican
    if timeout is None:
        timeout = DEFAULT_TIMEOUT
    
    if headers is None:
        headers = DEFAULT_HEADERS.copy()
    
    if base_url is None:
        base_url = API_BASE_URL
    
    # Construir URL completa
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    
    # Convertir data a JSON si es un diccionario
    json_data = None
    if data and isinstance(data, dict):
        json_data = data
        data = None
    
    try:
        # Realizar la petición
        logging.info(f"Realizando petición {method} a {url}")
        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json_data,
            headers=headers,
            timeout=timeout,
            verify=verify
        )
        
        # Registrar información de la respuesta
        log_response(response)
        
        return response
    
    except RequestException as e:
        logging.error(f"Error en petición {method} a {url}: {e}")
        raise

def get(endpoint, params=None, headers=None, timeout=None, verify=True, base_url=None):
    """
    Realiza una petición GET.
    
    Args:
        endpoint (str): Endpoint de la API
        params (dict, optional): Parámetros de query string
        headers (dict, optional): Headers HTTP
        timeout (int, optional): Timeout en segundos
        verify (bool, optional): Verificar certificado SSL
        base_url (str, optional): URL base para la petición
        
    Returns:
        requests.Response: Objeto de respuesta
    """
    return make_request("GET", endpoint, params=params, headers=headers, timeout=timeout, verify=verify, base_url=base_url)

def post(endpoint, data=None, params=None, headers=None, timeout=None, verify=True, base_url=None):
    """
    Realiza una petición POST.
    
    Args:
        endpoint (str): Endpoint de la API
        data (dict, optional): Datos para enviar en el cuerpo de la petición
        params (dict, optional): Parámetros de query string
        headers (dict, optional): Headers HTTP
        timeout (int, optional): Timeout en segundos
        verify (bool, optional): Verificar certificado SSL
        base_url (str, optional): URL base para la petición
        
    Returns:
        requests.Response: Objeto de respuesta
    """
    return make_request("POST", endpoint, params=params, data=data, headers=headers, timeout=timeout, verify=verify, base_url=base_url)

def put(endpoint, data=None, params=None, headers=None, timeout=None, verify=True, base_url=None):
    """
    Realiza una petición PUT.
    
    Args:
        endpoint (str): Endpoint de la API
        data (dict, optional): Datos para enviar en el cuerpo de la petición
        params (dict, optional): Parámetros de query string
        headers (dict, optional): Headers HTTP
        timeout (int, optional): Timeout en segundos
        verify (bool, optional): Verificar certificado SSL
        base_url (str, optional): URL base para la petición
        
    Returns:
        requests.Response: Objeto de respuesta
    """
    return make_request("PUT", endpoint, params=params, data=data, headers=headers, timeout=timeout, verify=verify, base_url=base_url)

def delete(endpoint, params=None, headers=None, timeout=None, verify=True, base_url=None):
    """
    Realiza una petición DELETE.
    
    Args:
        endpoint (str): Endpoint de la API
        params (dict, optional): Parámetros de query string
        headers (dict, optional): Headers HTTP
        timeout (int, optional): Timeout en segundos
        verify (bool, optional): Verificar certificado SSL
        base_url (str, optional): URL base para la petición
        
    Returns:
        requests.Response: Objeto de respuesta
    """
    return make_request("DELETE", endpoint, params=params, headers=headers, timeout=timeout, verify=verify, base_url=base_url)

# ================================================================================================================================================ #
# HELPER FUNCTIONS
# ================================================================================================================================================ #

def log_response(response):
    """
    Registra información sobre la respuesta HTTP.
    
    Args:
        response (requests.Response): Objeto de respuesta
    """
    logging.info(f"Respuesta: {response.status_code} {response.reason}")
    logging.debug(f"Headers: {response.headers}")
    
    try:
        logging.debug(f"Contenido: {response.json()}")
    except ValueError:
        logging.debug(f"Contenido: {response.text[:200]}...")

def validate_json_schema(data, schema):
    """
    Valida que los datos cumplan con un esquema JSON.
    
    Args:
        data (dict): Datos a validar
        schema (dict): Esquema JSON para validación
        
    Returns:
        bool: True si los datos son válidos, False en caso contrario
        
    Raises:
        jsonschema.exceptions.ValidationError: Si los datos no cumplen con el esquema
    """
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        logging.error(f"Error de validación de esquema: {e}")
        raise

def extract_data(response, key_path=None):
    """
    Extrae datos de una respuesta JSON usando una ruta de claves.
    
    Args:
        response (requests.Response): Objeto de respuesta
        key_path (str, optional): Ruta de claves separadas por puntos (ej: "data.items.0.id")
        
    Returns:
        any: Valor extraído o None si no se encuentra
    """
    try:
        data = response.json()
        
        if not key_path:
            return data
            
        keys = key_path.split('.')
        result = data
        
        for key in keys:
            if key.isdigit() and isinstance(result, list):
                index = int(key)
                if 0 <= index < len(result):
                    result = result[index]
                else:
                    return None
            elif key in result:
                result = result[key]
            else:
                return None
                
        return result
        
    except (ValueError, KeyError, IndexError) as e:
        logging.error(f"Error al extraer datos: {e}")
        return None

# ================================================================================================================================================ #
# MAIN EXECUTION
# ================================================================================================================================================ #

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Ejemplo de uso
    response = get("posts/1")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
