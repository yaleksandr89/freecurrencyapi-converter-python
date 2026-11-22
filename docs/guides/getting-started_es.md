# Instalación y primer uso

## Elegir idioma

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](getting-started.md) | [English](getting-started_en.md) | **Seleccionado** | [中文](getting-started_zh.md) | [Français](getting-started_fr.md) | [Deutsch](getting-started_de.md) |

## Versiones ejecutables

Cuando haya un archivo para su sistema en la [página de lanzamientos](https://github.com/yaleksandr89/freecurrencyapi-converter-python/releases), descárguelo y descomprímalo en una carpeta. La versión ejecutable funciona sin Python ni `make`.

1. En la carpeta descomprimida, copie `.env.example` a `.env` y escriba su clave de FreecurrencyAPI en `API_TOKEN`. Conserve el valor de `API_URL` de la plantilla.
2. En Windows, haga doble clic en `currency-converter.exe`. En Linux y macOS, ejecute `./currency-converter` desde esa carpeta en una terminal. En macOS también puede abrir `Launch Currency Converter.command`.

El `README.md` incluido contiene instrucciones breves en ruso e inglés.

## Requisitos para instalar desde el código fuente

- Git para clonar el repositorio, Python 3.12 o posterior y el módulo `venv` con `pip`.
- Una clave propia de FreecurrencyAPI para convertir divisas. Regístrese, obtenga la clave en su cuenta y consulte la [documentación de FreecurrencyAPI](https://freecurrencyapi.com/docs/).

## Obtener el código fuente

Clone el repositorio y entre en la carpeta raíz, donde se encuentra `index.py`. Ejecute allí todos los comandos siguientes.

```bash
# Clonar el repositorio y entrar en su directorio.
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

## Instalar las dependencias

### Linux y macOS

Compruebe que `python3` corresponde a Python 3.12 o posterior y que `make` está instalado. `make setup` crea `.venv` si no existe e instala el proyecto y las dependencias de desarrollo.

```bash
# Comprobar la versión de Python.
python3 --version

# Crear .venv e instalar las dependencias de desarrollo.
make setup

# Crear la configuración local sin sobrescribir una clave existente.
cp -n .env.example .env
```

Si la versión adecuada tiene otro nombre, indíquelo mediante `PYTHON`, por ejemplo `make setup PYTHON=python3.12`. Solo se utiliza al crear el entorno.

### Windows PowerShell

En este ejemplo, `python` es Python 3.12 o posterior y está disponible en `PATH`. Se invoca directamente el intérprete de `.venv`; no es necesario activarlo ni utilizar `make`.

```powershell
# Comprobar la versión instalada de Python.
python --version

# Crear el entorno e instalar las dependencias de desarrollo.
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

# Copiar el archivo de ejemplo solo si .env no existe.
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Para instalar solo el programa y sus dependencias de ejecución, cambie `requirements-dev.txt` por `requirements.txt` en `pip install`. Las comprobaciones locales necesitan las dependencias de desarrollo.

## Configurar la clave y la dirección

Abra el archivo `.env` creado. Sustituya `API_TOKEN` por su clave y mantenga `API_URL` como dirección base de la API, sin la ruta de un endpoint.

```ini
API_TOKEN=your_api_token_here
API_URL=https://api.freecurrencyapi.com/v1
```

Guarde la clave de forma local. No incluya `.env` en Git ni en informes de errores. Las variables ya definidas en el entorno del proceso prevalecen sobre las del archivo.

## Ejecutar y comprobar

En Linux y macOS, inicie el programa mediante `make`:

```bash
# Interfaz en ruso (predeterminada).
make run

# Interfaz en inglés.
make run CLI_LANG=en
```

En Windows PowerShell, ejecute `index.py` con el intérprete del entorno virtual:

```powershell
# Interfaz en ruso (predeterminada).
.\.venv\Scripts\python.exe index.py

# Interfaz en inglés.
.\.venv\Scripts\python.exe index.py --lang en
```

Después del saludo aparece la lista de divisas. Si contiene `USD`, `EUR` y `GBP`, introduzca sucesivamente `USD`, `12.5` y `EUR,GBP`, pulsando Enter tras cada dato. Si todo va bien, se muestra una línea por divisa de destino. Los valores dependen de los tipos de cambio.

Puede comprobar el inicio del CLI sin clave ni solicitud a la API: ejecute `.venv/bin/python index.py --help` en Linux/macOS o `.\.venv\Scripts\python.exe index.py --help` en PowerShell.

## Si el programa no se inicia

| Síntoma | Qué comprobar |
| --- | --- |
| Falta `API_TOKEN` o `API_URL` | Revise el nombre `.env`, los nombres de las variables y sus valores. Compruebe también las variables definidas en la consola. |
| Error con código HTTP | Revise la dirección base, la validez de la clave y la cuota disponible en FreecurrencyAPI. |
| Tiempo de espera agotado o error de solicitud | Revise `API_URL` y la disponibilidad de FreecurrencyAPI. |
| El CLI rechaza los datos | Reinicie el conversor, elija los códigos de la lista, separe los destinos con comas e introduzca un importe positivo con punto decimal. |

Las causas y los códigos de salida figuran en la [referencia de CLI y errores](../reference/cli-and-errors_es.md).

## Comprobaciones locales

Una vez instaladas las dependencias de desarrollo, compruebe el proyecto desde la raíz del repositorio.

En Linux y macOS:

```bash
# Ejecutar las pruebas, Ruff y la comprobación de dependencias.
make check
```

En Windows PowerShell:

```powershell
# Pruebas sin acceso a la API real.
.\.venv\Scripts\python.exe -m pytest

# Análisis de estilo y formato.
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .

# Comprobar las dependencias instaladas.
.\.venv\Scripts\python.exe -m pip check
```

Las pruebas simulan respuestas y errores de FreecurrencyAPI y bloquean solicitudes HTTP reales. No necesitan una clave activa. Para verificar el acceso al servicio y la clave, realice una conversión interactiva.
