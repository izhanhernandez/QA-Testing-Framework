# language: es
Característica: Llamada a API de prueba
  Como desarrollador
  Quiero realizar llamadas a una API de prueba
  Para verificar la funcionalidad de testing de APIs

  Escenario: Obtener datos de un usuario específico
    Dado que tengo acceso a la API de JSONPlaceholder
    Cuando realizo una petición GET al endpoint "users/1"
    Entonces debo recibir un código de estado 200
    Y la respuesta debe contener los datos del usuario con id 1
