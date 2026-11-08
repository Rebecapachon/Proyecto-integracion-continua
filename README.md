# Entrega 1 - Integración continua

Aplicación de línea de comandos para validar líneas de pedido y calcular el descuento de acuerdo con el caso. No tiene interfaz gráfica ni base de datos.

## Requisitos
Python 3.12 o Docker Desktop con motor Linux activo.

## Ejecutar pedido de ejemplo
`python app/pedido.py examples/pedido.json`

## Ejecutar pruebas
`python -m unittest discover -s tests -v`

## Construir y ejecutar con Docker
`docker build -t entrega1-pedidos .`
`docker run --rm entrega1-pedidos`
`docker run --rm entrega1-pedidos python -m unittest discover -s tests -v`

El 31 de octubre de 2026 cloné este repositorio y ejecuté las pruebas dentro de Docker. Resultado: 8 pruebas ejecutadas, OK.

## Ejecutar los dos contenedores comunicados
La entrega incluye un servicio de inventario y un cliente de pedidos. Docker Compose crea una red privada: el cliente consulta las existencias usando el nombre DNS `inventario` y calcula el total con la respuesta recibida.

`docker compose up --build`

En la salida se debe ver el servicio de inventario activo y el resultado calculado por `pedidos`. El contenedor `pedidos` termina al finalizar el cálculo; `inventario` permanece disponible. Para detener y retirar los contenedores, presiona `Ctrl+C` y ejecuta `docker compose down`.

Para ver los registros de comunicación y el resultado:

`docker compose logs`

## Flujo
GitHub Actions ejecuta las pruebas en cada push y pull request. La evidencia de ejecución local debe registrarse con fecha; no se deben agregar capturas ficticias.
