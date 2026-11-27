# Contribuir al proyecto

## Elegir idioma

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../../.github/CONTRIBUTING.md) | [English](../en/CONTRIBUTING.md) | **Seleccionado** | [中文](../zh/CONTRIBUTING.md) | [Français](../fr/CONTRIBUTING.md) | [Deutsch](../de/CONTRIBUTING.md) |

## Antes de comenzar

Compruebe si el cambio ya se está comentando. Para abrir una [incidencia](https://github.com/yaleksandr89/freecurrencyapi-converter-python/issues/new/choose), seleccione el formulario de error o propuesta.

- Para un error, indique el entorno, el comando, los datos de entrada, los pasos para reproducirlo y el resultado esperado y obtenido.
- Para una mejora, describa el problema y el comportamiento deseado del CLI.
- Informe de vulnerabilidades según la [política de seguridad](SECURITY.md).

## Ramas y commits

Cree una rama nueva desde `master`, por ejemplo `fix/invalid-amount` o `docs/setup-guide`. Los commits y títulos de pull requests deben seguir Conventional Commits: prefijo de tipo en inglés y **descripción en ruso**.

```text
docs: уточнить запуск конвертера
fix: отклонять недопустимые суммы
test: проверить обработку некорректных ответов API
```

## Comprobaciones locales

Desde la raíz del repositorio, en Linux o macOS con Python 3.12 o posterior, ejecute estos comandos. `make setup` crea `.venv` si no existe e instala las dependencias de desarrollo. Puede escoger el intérprete mediante `PYTHON` al crear el entorno.

```bash
make setup PYTHON=python3
make check
```

`make check` ejecuta pytest, Ruff (estilo y formato) y `pip check`. Las pruebas simulan las respuestas de FreecurrencyAPI y no requieren una clave real. Las instrucciones de PowerShell figuran en la [guía de inicio](guides/getting-started.md#comprobaciones-locales).

No añada a los commits `.env`, claves reales ni registros con información secreta.

## Pull requests

Abra un pull request hacia `master`. Explique el motivo, las comprobaciones realizadas y los cambios en el CLI, las solicitudes a FreecurrencyAPI o el tratamiento de secretos. Actualice las pruebas y la documentación cuando corresponda.

Mantenga sincronizadas las seis traducciones de documentación y ambos idiomas de la interfaz.
