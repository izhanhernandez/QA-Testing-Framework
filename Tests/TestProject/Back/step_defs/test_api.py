#!/usr/bin/env python

# ================================================================================================================================================ #
# IMPORTS
# ================================================================================================================================================ #

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import json

# Importaciones locales
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../.."))
from Utils.api_utils import get, extract_data

# ================================================================================================================================================ #
# CONSTANTS
# ================================================================================================================================================ #

API_BASE_URL = "https://jsonplaceholder.typicode.com"

# ================================================================================================================================================ #
# SCENARIOS
# ================================================================================================================================================ #

scenarios('../features/api_test.feature')

# ================================================================================================================================================ #
# FIXTURES
# ================================================================================================================================================ #

@pytest.fixture
def api_response():
    """Fixture para almacenar la respuesta de la API entre pasos."""
    return {}

# ================================================================================================================================================ #
# STEP DEFINITIONS
# ================================================================================================================================================ #

@given("que tengo acceso a la API de JSONPlaceholder")
def access_api():
    """Verificar que tenemos acceso a la API."""
    # Este paso es principalmente declarativo, pero podríamos verificar la conectividad
    response = get("", base_url=API_BASE_URL)
    assert response.status_code < 400, "No se puede acceder a la API de JSONPlaceholder"

@when(parsers.parse('realizo una petición GET al endpoint "{endpoint}"'))
def make_get_request(api_response, endpoint):
    """Realizar una petición GET al endpoint especificado."""
    response = get(endpoint, base_url=API_BASE_URL)
    # Guardar la respuesta en el fixture para usarla en pasos posteriores
    api_response["response"] = response
    api_response["data"] = response.json()

@then(parsers.parse('debo recibir un código de estado {status_code:d}'))
def verify_status_code(api_response, status_code):
    """Verificar el código de estado de la respuesta."""
    assert api_response["response"].status_code == status_code, \
        f"Se esperaba código de estado {status_code}, pero se recibió {api_response['response'].status_code}"

@then(parsers.parse('la respuesta debe contener los datos del usuario con id {user_id:d}'))
def verify_user_data(api_response, user_id):
    """Verificar que la respuesta contiene los datos del usuario especificado."""
    user_data = api_response["data"]
    assert user_data["id"] == user_id, f"Se esperaba usuario con id {user_id}, pero se recibió {user_data['id']}"
    assert "name" in user_data, "Los datos del usuario no contienen el campo 'name'"
    assert "email" in user_data, "Los datos del usuario no contienen el campo 'email'"
    
    # Guardar la respuesta en un archivo para referencia
    report_dir = os.path.join(os.path.dirname(__file__), "../../../../Reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        
    with open(os.path.join(report_dir, f"user_{user_id}_data.json"), "w") as f:
        json.dump(user_data, f, indent=4)
