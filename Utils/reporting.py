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
reporting.py es un módulo que proporciona funciones y clases para la generación de reportes de pruebas.

Este módulo incluye:
- Generación de reportes en diferentes formatos (HTML, JSON, XML)
- Captura y organización de screenshots
- Estadísticas de ejecución de pruebas
- Formateo de resultados para mejor visualización
- Integración con sistemas de reporting externos

Las utilidades están diseñadas para proporcionar informes claros y detallados sobre
la ejecución de las pruebas automatizadas.
"""

# ================================================================================================================================================ #
# IMPORTS
# ================================================================================================================================================ #

import os
import json
import logging
import datetime
from pathlib import Path

# Importaciones locales
from .config import REPORTS_FOLDER

# ================================================================================================================================================ #
# CONSTANTS
# ================================================================================================================================================ #

# Formatos de reporte disponibles
REPORT_FORMATS = ["html", "json", "xml"]

# Carpeta para reportes
HTML_REPORTS_FOLDER = os.path.join(REPORTS_FOLDER, "html")
JSON_REPORTS_FOLDER = os.path.join(REPORTS_FOLDER, "json")
SCREENSHOTS_FOLDER = os.path.join(REPORTS_FOLDER, "screenshots")

# Crear carpetas si no existen
for folder in [HTML_REPORTS_FOLDER, JSON_REPORTS_FOLDER, SCREENSHOTS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# ================================================================================================================================================ #
# REPORTING FUNCTIONS
# ================================================================================================================================================ #

def generate_report_filename(prefix="report", extension="html"):
    """
    Genera un nombre de archivo para un reporte basado en la fecha y hora actual.
    
    Args:
        prefix (str, optional): Prefijo para el nombre del archivo
        extension (str, optional): Extensión del archivo
        
    Returns:
        str: Nombre de archivo generado
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def save_json_report(data, filename=None):
    """
    Guarda datos de reporte en formato JSON.
    
    Args:
        data (dict): Datos del reporte
        filename (str, optional): Nombre del archivo. Si no se proporciona, se genera automáticamente
        
    Returns:
        str: Ruta del archivo guardado
    """
    if filename is None:
        filename = generate_report_filename("report", "json")
    
    file_path = os.path.join(JSON_REPORTS_FOLDER, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    logging.info(f"Reporte JSON guardado en: {file_path}")
    return file_path

def create_test_result(test_name, status, duration=None, error=None, screenshots=None):
    """
    Crea un diccionario con el resultado de un test.
    
    Args:
        test_name (str): Nombre del test
        status (str): Estado del test (passed, failed, skipped)
        duration (float, optional): Duración del test en segundos
        error (str, optional): Mensaje de error si el test falló
        screenshots (list, optional): Lista de rutas de screenshots
        
    Returns:
        dict: Resultado del test
    """
    result = {
        "name": test_name,
        "status": status,
        "timestamp": datetime.datetime.now().isoformat(),
    }
    
    if duration is not None:
        result["duration"] = duration
    
    if error is not None:
        result["error"] = error
    
    if screenshots is not None:
        result["screenshots"] = screenshots
    
    return result

def collect_test_results(results):
    """
    Recopila estadísticas de resultados de tests.
    
    Args:
        results (list): Lista de resultados de tests
        
    Returns:
        dict: Estadísticas de los tests
    """
    stats = {
        "total": len(results),
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "duration": 0
    }
    
    for result in results:
        stats[result["status"]] += 1
        if "duration" in result:
            stats["duration"] += result["duration"]
    
    stats["success_rate"] = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0
    
    return stats

def organize_screenshots(test_name, screenshots):
    """
    Organiza screenshots en la carpeta correspondiente.
    
    Args:
        test_name (str): Nombre del test
        screenshots (list): Lista de rutas de screenshots
        
    Returns:
        list: Lista de rutas de screenshots organizados
    """
    # Crear carpeta específica para el test
    test_folder = os.path.join(SCREENSHOTS_FOLDER, test_name.replace(" ", "_"))
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    
    organized_screenshots = []
    
    for i, screenshot in enumerate(screenshots):
        if os.path.exists(screenshot):
            # Copiar screenshot a la carpeta del test
            new_path = os.path.join(test_folder, f"step_{i+1}_{Path(screenshot).name}")
            import shutil
            shutil.copy2(screenshot, new_path)
            organized_screenshots.append(new_path)
    
    return organized_screenshots

# ================================================================================================================================================ #
# MAIN EXECUTION
# ================================================================================================================================================ #

if __name__ == "__main__":
    # Ejemplo de uso
    test_results = [
        create_test_result("Test Login", "passed", 1.5),
        create_test_result("Test Search", "failed", 0.8, "Element not found"),
        create_test_result("Test Checkout", "skipped")
    ]
    
    stats = collect_test_results(test_results)
    
    report_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "results": test_results,
        "statistics": stats
    }
    
    save_json_report(report_data)
