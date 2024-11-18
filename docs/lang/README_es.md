# Convertidor de divisas

### Elija Idioma

| Русский | English | Español | 中文 | Français | Deutsch |
|---------|------------|------------|-----------|-------------|----------|
| [Русский](../../README.md) | [English](README_en.md) | **Seleccionado** | [中文](README_zh.md) | [Français](README_fr.md) | [Deutsch](README_de.md) |

---

**Currency Converter** es un proyecto para trabajar con la API de cambio de divisas. Puede solicitar tipos de cambio, realizar conversiones y probar la funcionalidad a través de pruebas listas para usar.

---

## Estructura del proyecto

```plain text
currency-converter/
├── docs/...              # Materiales utilizados en README.md
├── src/
│   ├── main.py           # Archivo principal para iniciar la aplicación
│   ├── api_service.py    # Trabajar con API (solicitudes y procesamiento)
├── tests/
│   ├── test.py           # Pruebas para verificar la funcionalidad
├── index.py              # Punto de entrada para iniciar la aplicación
├── .env                  # Archivo de configuración (token y URL). ¡Creado por TI mismo!
├── .env.example          # Ejemplo de archivo de configuración
├── .gitignore            # Archivos Git ignorados
├── requirements.txt      # Lista de dependencias
├── README.md             # Documentación del proyecto
```

---

## Instalación

### 1. Clonación del repositorio

Clone el proyecto en su computadora local:

```bash
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

### 2. Crear un entorno virtual

Se recomienda utilizar un entorno virtual para aislar dependencias:

```bash
# Crear un entorno virtual
python3 -m venv venv

# Activación del entorno virtual
source venv/bin/activate  # Para Bash/Zsh/Linux/MacOS
venv\Scripts\activate     # Para Windows
```

### 3. Instalación de dependencias

Instale las dependencias de `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Configuración

1. Cambie el nombre del archivo `.env.example ' in `.env`:

```bash
mv .env.example .env
```

2. Especifique el token y la URL base de la API en `.env`:

```plaintext
API_TOKEN='ВАШ_API_ТОКЕН'
API_URL='https://api.freecurrencyapi.com/v1'
```

---

## Lanzamiento

### 1. Iniciar la aplicación

Ejecute el proyecto a través del archivo `index.py`:

```bash
python3 index.py
```

---

## Pruebas

### Ejecutar pruebas

Para ejecutar las pruebas, use el archivo `tests/test.py`:

```bash
python3 tests/test.py
```

Este archivo comprueba si la conexión a la API es correcta y muestra una lista de las monedas disponibles.

---

## Demostración de trabajo

Conversión exitosa

![currency-convert-result-work-success.png](/docs/img/currency-convert-result-work-success.png)

<details>
<summary>Proceso de conversión (conversión exitosa (GIF))</summary>

![currency-convert-result-work-success.gif](/docs/img/currency-convert-result-work-success.gif)

</details>

Error de conversión

![currency-convert-result-work-error.png](/docs/img/currency-convert-result-work-error.png)

<details>
<summary>Proceso de conversión (error al convertir (GIF))</summary>

![currency-convert-result-work-error.gif](/docs/img/currency-convert-result-work-error.gif)

</details>

---

## Convertidor de divisas a PHP

Se creó un proyecto en PHP con una funcionalidad similar, pero con varias diferencias:

- Interfaz web implementada
- Se describen todos los endpoints disponibles del Servicio.

Código de ejemplo: [freecurrencyapi-converter-php](https://github.com/yaleksandr89/freecurrencyapi-converter-php) — ¡todos adentro! 😄

---

## Ejemplo

1. **Token de seguridad:**
   - Asegúrese de que su token de API se especifique correctamente en `.env`.
   - Nunca agregue un archivo `.env` al repositorio.

2. **Recomendación:**
   - Utilice un entorno virtual para aislar dependencias.
   - Actualice la configuración si es necesario a través de `pip install --upgrade`.