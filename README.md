# QA Testing Framework

## Descripción

Framework de automatización de pruebas QA basado en Python que utiliza pytest-bdd para implementar tests con sintaxis Cucumber/Gherkin. Este framework permite la creación y ejecución de pruebas tanto para frontend (usando Selenium) como para backend (API testing).

## Estructura del Proyecto

```
QA_Testing_Framework/
│
├── README.md                 # Documentación principal
├── requirements.txt          # Dependencias Python
├── Dockerfile                # Configuración para contenedores
│
├── Webdrivers/               # Controladores para navegadores
│   ├── Windows/              # Webdrivers para Windows
│   └── Unix/                 # Webdrivers para sistemas Unix
│
├── Assets/                   # Recursos varios (imágenes, etc.)
│
├── Utils/                    # Utilidades y librerías Python
│   ├── __init__.py
│   ├── config.py             # Configuraciones globales
│   ├── selenium_utils.py     # Utilidades para Selenium
│   ├── api_utils.py          # Utilidades para testing de APIs
│   └── reporting.py          # Funciones para generación de reportes
│
└── Tests/                    # Carpeta principal de tests
    └── Project1/             # Tests específicos por proyecto
        ├── Front/            # Tests de frontend
        │   ├── features/     # Archivos .feature (Gherkin)
        │   ├── step_defs/    # Definiciones de pasos
        │   └── pages/        # Page Objects
        │
        └── Back/             # Tests de backend
            ├── features/     # Archivos .feature (Gherkin)
            └── step_defs/    # Definiciones de pasos
```

## Requisitos

- Python 3.8 o superior
- Navegadores web compatibles (Chrome, Firefox)
- Webdrivers correspondientes a las versiones de los navegadores

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/QA_Testing_Framework.git
   cd QA_Testing_Framework
   ```

2. Crear y activar un entorno virtual:

   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En Unix
   source venv/bin/activate
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Asegurarse de tener los webdrivers correctos en la carpeta `Webdrivers` según el sistema operativo.

## Uso

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar tests específicos

```bash
# Ejecutar tests de frontend
pytest Tests/Project1/Front

# Ejecutar tests de backend
pytest Tests/Project1/Back

# Ejecutar un test específico
pytest Tests/Project1/Front/features/test_google_navigation.py
```

### Generar reportes

```bash
pytest --html=report.html
```

## Ejemplos Incluidos

1. **Frontend**: Test de navegación a Google
2. **Backend**: Test de llamada a API de prueba

## Desarrollo con Docker

1. Construir la imagen:

   ```bash
   docker build -t qa-testing-framework .
   ```

2. Ejecutar tests en contenedor:
   ```bash
   docker run qa-testing-framework pytest
   ```

## Contribución

1. Fork del repositorio
2. Crear una rama para la nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de los cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request
