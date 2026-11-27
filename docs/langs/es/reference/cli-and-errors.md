# Comandos, entrada y errores de CLI

## Elegir idioma

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../ru/reference/cli-and-errors.md) | [English](../../en/reference/cli-and-errors.md) | **Seleccionado** | [中文](../../zh/reference/cli-and-errors.md) | [Français](../../fr/reference/cli-and-errors.md) | [Deutsch](../../de/reference/cli-and-errors.md) |

## Opciones de ejecución

Ejecute `index.py` desde la raíz del proyecto con el intérprete Python de `.venv`, creado durante la instalación. Ejemplos para Linux y macOS:

```bash
# Conversión interactiva en ruso.
.venv/bin/python index.py

# Interfaz en inglés.
.venv/bin/python index.py --lang en

# Mostrar la ayuda sin leer .env ni llamar a la API.
.venv/bin/python index.py --help
```

En Windows PowerShell sustituya `.venv/bin/python` por `.\.venv\Scripts\python.exe`. La [guía de inicio](../guides/getting-started.md) explica ambos sistemas.

| Opción | Comportamiento |
| --- | --- |
| `-h`, `--help` | Muestra la ayuda en el idioma seleccionado sin leer `.env` ni solicitar datos a la API. |
| `--lang ru` | Selecciona la interfaz rusa; es el valor predeterminado. |
| `--lang en` | Selecciona la interfaz inglesa; también se puede usar con `--help`. |

## Entrada y formato de resultados

El CLI primero obtiene y muestra las divisas. Los códigos aparecen entre corchetes; los nombres proceden de FreecurrencyAPI.

1. Introduzca un código de origen de la lista, por ejemplo `USD`.
2. Introduzca un número positivo y finito; use punto decimal, por ejemplo `2.5`. Se rechazan `2,5`, `NaN` e `inf`.
3. Introduzca uno o varios códigos de destino, por ejemplo `EUR,GBP`. Los elementos vacíos, incluida una coma final, son inválidos.

El CLI no distingue mayúsculas en los códigos y elimina los espacios de sus extremos. Si la entrada es incorrecta, el proceso termina; ejecute el comando de nuevo.

El importe se convierte a `float` y se redondea mediante `round` a tres decimales antes de multiplicarlo por el tipo de cambio. Si se redondea a cero o el producto deja de ser finito, se muestra un error.

Los resultados se escriben en la salida estándar, una línea por código de destino y en el orden devuelto por la API. El importe de origen redondeado no tiene un número fijo de decimales; el resultado se muestra con dos. El ejemplo utiliza tipos de cambio simulados de las pruebas.

```text
2.5 USD = 2.00 EUR
2.5 USD = 1.25 GBP
```

## Solicitudes a FreecurrencyAPI

Ambas solicitudes utilizan `GET`, la dirección base `API_URL` y el parámetro de consulta `apikey` con el valor de `API_TOKEN`.

| Endpoint | Uso en el CLI |
| --- | --- |
| [`/currencies`](https://freecurrencyapi.com/docs/currencies) | Obtiene la lista antes de pedir datos al usuario y exige que cada divisa tenga un nombre no vacío. |
| [`/latest`](https://freecurrencyapi.com/docs/latest) | Solicita los tipos tras validar la entrada. Envía el código de origen en `base_currency` y los destinos separados por comas en `currencies`. El importe se multiplica localmente. |

El cliente acepta HTTP 200 con un objeto JSON `data` no vacío. Los tiempos de espera son 4 segundos para la conexión y 10 segundos para leer la respuesta. Los redireccionamientos están desactivados. Se exige un tipo para cada destino solicitado y solo se utilizan esos tipos. FreecurrencyAPI determina las divisas disponibles, los valores y las cuotas.

## Códigos de salida

| Código | Significado |
| --- | --- |
| `0` | Conversión correcta o ayuda mostrada. |
| `1` | Error de configuración, solicitud, respuesta de la API o entrada, incluido fin de entrada (EOF). |
| `2` | Argumentos no válidos, como opciones desconocidas o un valor `--lang` no admitido. |
| `130` | Interrupción de la sesión con Ctrl+C. |

## Mensajes de error

Los errores se escriben en `stderr`, en el idioma de `--lang`. Cuando `--lang` no es válido, el mensaje se muestra en ruso.

| Categoría | Causa |
| --- | --- |
| Configuración | Falta `API_TOKEN` o `API_URL`, o su valor solo contiene espacios. |
| Red | Tiempo de espera agotado u otro error de solicitud, como un fallo de conexión. |
| HTTP | El servidor devuelve un código distinto de 200; el CLI lo muestra. |
| Respuesta de la API | JSON incorrecto; `data` ausente, vacío o inválido; metadatos de divisas incorrectos; tipo ausente, no positivo, no numérico o no finito para un destino. |
| Entrada | Código de origen o destino desconocido, destino vacío, importe no válido, redondeo a cero o desbordamiento durante el cálculo. |
| Fin de sesión | El flujo de entrada terminó antes de completar los datos o se pulsó Ctrl+C. |
