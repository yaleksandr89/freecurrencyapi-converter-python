# Contribuer au projet

## Choisir la langue

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../.github/CONTRIBUTING.md) | [English](CONTRIBUTING_en.md) | [Español](CONTRIBUTING_es.md) | [中文](CONTRIBUTING_zh.md) | **Sélectionné** | [Deutsch](CONTRIBUTING_de.md) |

## Avant de commencer

Vérifiez si votre modification est déjà discutée. Pour créer une [issue](https://github.com/yaleksandr89/freecurrencyapi-converter-python/issues/new/choose), choisissez le formulaire de bogue ou de proposition.

- Pour un bogue, indiquez l’environnement, la commande, les données saisies, les étapes de reproduction, ainsi que les résultats attendus et observés.
- Pour une proposition, décrivez le besoin et le comportement CLI souhaité.
- Signalez les vulnérabilités selon la [politique de sécurité](../security/SECURITY_fr.md).

## Branches et commits

Créez une branche depuis `master`, par exemple `fix/invalid-amount` ou `docs/setup-guide`. Utilisez Conventional Commits pour les commits et titres de pull requests : type en anglais et **description en russe**.

```text
docs: уточнить запуск конвертера
fix: отклонять недопустимые суммы
test: проверить обработку некорректных ответов API
```

## Vérifications locales

À la racine du dépôt sous Linux ou macOS avec Python 3.12 ou une version ultérieure, exécutez les commandes suivantes. `make setup` crée `.venv` si nécessaire et installe les dépendances de développement. `PYTHON` permet de choisir l’interpréteur à la création.

```bash
make setup PYTHON=python3
make check
```

`make check` lance pytest, les contrôles de style et formatage Ruff et `pip check`. Les tests simulent les réponses FreecurrencyAPI, sans clé réelle. Les commandes PowerShell figurent dans le [guide de démarrage](../guides/getting-started_fr.md#vérifications-locales).

Ne commitez pas `.env`, de vraies clés API ou des journaux contenant des secrets.

## Pull requests

Ouvrez une pull request vers `master`. Décrivez la raison du changement, les contrôles effectués et son effet éventuel sur le CLI, les requêtes FreecurrencyAPI ou les secrets. Mettez à jour tests et documentation si nécessaire.
