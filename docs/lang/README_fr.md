# Convertisseur de devises

[![Source Code](https://img.shields.io/badge/source-yaleksandr89%2Ffreecurrencyapi--converter--python-blue.svg?style=flat-square)](https://github.com/yaleksandr89/freecurrencyapi-converter-python)
[![CI](https://github.com/yaleksandr89/freecurrencyapi-converter-python/actions/workflows/ci.yml/badge.svg)](https://github.com/yaleksandr89/freecurrencyapi-converter-python/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?style=flat-square&logo=python&logoColor=white)](../../pyproject.toml)
[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](../../LICENSE.md)

![Currency Converter — convertisseur de devises interactif en Python](../assets/currency-converter-readme-cover.png)

## Choisir la langue

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../README.md) | [English](README_en.md) | [Español](README_es.md) | [中文](README_zh.md) | **Sélectionné** | [Deutsch](README_de.md) |

Convertisseur interactif en ligne de commande écrit en Python. Il convertit un montant d’une devise vers une ou plusieurs autres à partir des taux de FreecurrencyAPI.

- La liste des devises disponibles est chargée au début de chaque exécution interactive.
- Les taux des devises choisies sont demandés après la validation des données saisies.
- Les invites et messages de l’interface sont disponibles en russe et en anglais.

L’installation depuis les sources nécessite Python 3.12 ou une version ultérieure. La conversion nécessite votre propre clé FreecurrencyAPI. Les commandes ci-dessous s’adressent à Linux et macOS avec `make`. La CI vérifie Python 3.12, 3.13 et 3.14 sur Ubuntu.

## Déroulement d’une conversion

Saisissez la devise d’origine, le montant et les devises cibles. Le convertisseur demande les taux correspondants et affiche les montants dans le terminal.

```mermaid
flowchart LR
    A["Charger les devises"] --> B["Lire et valider la saisie"]
    B --> C["Demander les taux"]
    C --> D["Calculer et afficher les montants"]
```

Le [document d’architecture](../reference/architecture_fr.md) présente les modules, les appels à l’API et la gestion des erreurs.

## Versions autonomes

Les versions autonomes fonctionnent sans installation de Python. Lorsqu’une archive adaptée à votre système est disponible sur la [page des versions](https://github.com/yaleksandr89/freecurrencyapi-converter-python/releases), téléchargez-la et décompressez-la. Copiez `.env.example` dans `.env`, renseignez votre clé dans `API_TOKEN` et suivez le `README.md` inclus pour lancer le programme.

## Démarrage rapide depuis les sources

Clonez le dépôt, créez l’environnement virtuel avec ses dépendances et copiez le modèle de configuration.

```bash
# Cloner le dépôt et ouvrir son répertoire.
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python

# Créer .venv et installer les dépendances de développement.
make setup

# Copier le modèle sans écraser un fichier .env existant.
cp -n .env.example .env
```

Renseignez `API_TOKEN` dans `.env` avec votre clé FreecurrencyAPI. L’adresse de base `API_URL` figure déjà dans le modèle. Exécutez l’une des commandes suivantes depuis la racine du projet.

```bash
# Interface en russe.
make run

# Interface en anglais.
make run CLI_LANG=en
```

Pour l’installation et le lancement sous Windows PowerShell, consultez le [guide de démarrage](../guides/getting-started_fr.md). Les options, la saisie et les codes de sortie figurent dans la [référence CLI](../reference/cli-and-errors_fr.md).

## Démonstrations

### Conversion réussie

Calcul et affichage du montant.

https://github.com/user-attachments/assets/47d64727-342d-4cb8-ba4c-d223253b2338

### Erreur de conversion

Message d’erreur du convertisseur.

https://github.com/user-attachments/assets/5b0408fb-e59c-467a-bef5-72b7e30c066b

### Changement de langue de l’interface

Lancement du CLI avec une autre langue pour les invites et les messages.

https://github.com/user-attachments/assets/217d4e51-7e09-460e-a6be-c7712ecb7b0f

## Retours

- Signaler un bogue ou proposer une amélioration — [GitHub Issues](https://github.com/yaleksandr89/freecurrencyapi-converter-python/issues).
- Discuter de l’utilisation du convertisseur — [GitHub Discussions](https://github.com/yaleksandr89/freecurrencyapi-converter-python/discussions).

---

<p align="center">
  Si ce projet vous a été utile, attribuez-lui une étoile sur GitHub pour aider d’autres personnes à le trouver. 🤘
</p>
