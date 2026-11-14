# Proyecto de integración continua: pedidos e inventario

Aplicación de ejemplo para validar líneas de pedido, consultar existencias en un servicio de inventario y calcular descuentos. El proyecto se desarrolla en dos entregas: el aplicativo contenerizado y su verificación automatizada con Jenkins.

## Entrega 1 — Aplicación y contenedores

Aplicación de línea de comandos para validar líneas de pedido y calcular el descuento de acuerdo con el caso. No tiene interfaz gráfica ni base de datos.

### Requisitos

- Python 3.12 para ejecución local.
- Docker Desktop con motor Linux activo y Docker Compose para ejecutar los contenedores.

### Ejecutar pedido de ejemplo

```powershell
python app/pedido.py examples/pedido.json
```

### Ejecutar pruebas unitarias

```powershell
python -m unittest discover -s tests -v
```

### Construir y ejecutar la imagen

```powershell
docker build -t entrega1-pedidos .
docker run --rm entrega1-pedidos
docker run --rm entrega1-pedidos python -m unittest discover -s tests -v
```

### Ejecutar los dos contenedores comunicados

Docker Compose crea una red privada. El cliente de pedidos consulta las existencias usando el nombre DNS `inventario` y calcula el total con la respuesta recibida.

```powershell
docker compose up --build
```

El pedido de ejemplo debe mostrar subtotal `210000`, descuento `21000` y total `189000`. El contenedor `pedidos` termina al finalizar el cálculo; `inventario` permanece disponible. Para detener y retirar ambos servicios:

```powershell
docker compose down --remove-orphans
```

Para consultar los registros:

```powershell
docker compose logs
```

El flujo de GitHub Actions ejecuta las pruebas unitarias al recibir cambios por `push` y `pull_request`.

## Entrega 2 — Integración continua con Jenkins

La entrega incorpora un `Jenkinsfile` que automatiza la verificación del proyecto usando Docker Compose. Jenkins obtiene el código de la rama `main`, construye las imágenes, ejecuta las pruebas, inicia el servicio de inventario, ejecuta el pedido remoto y comprueba el total esperado. Al terminar, incluso si una etapa falla, intenta retirar los contenedores y la red.

### Requisitos del entorno

- Jenkins 2.580.2 instalado en Windows.
- Java 21.
- Git.
- Docker Desktop con el motor Linux activo y Docker Compose disponible.
- El servicio de Jenkins debe poder acceder a Docker Desktop.

### Configurar la tarea en Jenkins

1. Crear una tarea de tipo **Pipeline**.
2. En **Definition**, seleccionar **Pipeline script from SCM**.
3. Seleccionar **Git** y usar este repositorio: <https://github.com/Rebecapachon/Proyecto-integracion-continua>.
4. Usar la rama `*/main`, dejar credenciales vacías porque el repositorio es público e indicar `Jenkinsfile` como **Script Path**.
5. Guardar la tarea. El `Jenkinsfile` configura `pollSCM('H/2 * * * *')` para consultar cambios en el repositorio aproximadamente cada dos minutos.

### Etapas y resultado esperado

- Obtener el código desde GitHub.
- Verificar Docker y Docker Compose.
- Construir las imágenes de los servicios.
- Ejecutar las 8 pruebas unitarias.
- Iniciar `inventario`, esperar a que esté saludable y ejecutar el pedido en `pedidos`.
- Aprobar la ejecución solo si el pedido produce total `189000`.
- Retirar contenedores y redes con `docker compose down --remove-orphans`.

Para ejecutar manualmente, abrir la tarea en Jenkins y seleccionar **Construir ahora**. La salida de la consola muestra cada etapa, el resultado del pedido y el estado final. Si falla, abrir la consola de esa compilación, localizar la primera línea de error, corregir la causa en el repositorio y volver a ejecutar.

### Prueba funcional de fallo y corrección

Para comprobar la validación, se introdujo temporalmente un incremento de 1 peso al total en `app/pedido_remoto.py`. La compilación #9 calculó `189001`, no coincidió con el total esperado de `189000` y terminó en **FALLO**; después se retiró el incremento y la compilación #10 volvió a producir `189000` y terminó en **ÉXITO**. Este cambio fue únicamente para la prueba y no debe permanecer en el código final.

No incluir contraseñas, tokens ni la clave inicial de Jenkins en el repositorio, este archivo o las capturas. El informe de la entrega contiene las evidencias detalladas de configuración y ejecución.
