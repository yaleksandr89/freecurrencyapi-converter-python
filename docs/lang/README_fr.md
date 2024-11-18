# Convertisseur de devises

### Choisissez la Langue

| Русский | English | Español | 中文 | Français | Deutsch |
|---------|------------|------------|-----------|-------------|----------|
| [Русский](../../README.md) | [English](README_en.md) | [Español](README_es.md) | [中文](README_zh.md) | **Sélectionné** | [Deutsch](README_de.md) |

---

**Currency Converter** est un projet pour travailler avec l'API de change. Vous pouvez demander des taux de change, effectuer des conversions et tester les fonctionnalités via des tests prêts à l'emploi.

---

## Structure du projet

```plain text
currency-converter/
├── docs/...              # Matériaux utilisés dans README.md
├── src/
│   ├── main.py           # Fichier principal pour lancer l'application
│   ├── api_service.py    # Travailler avec l'API (requêtes et traitement)
├── tests/
│   ├── test.py           # Tests pour tester la fonctionnalité
├── index.py              # Point d'entrée pour lancer l'application
├── .env                  # Fichier de configuration (jeton et URL). Créé par vous-même!
├── .env.example          # Exemple de fichier de configuration
├── .gitignore            # Fichiers Git ignorés
├── requirements.txt      # Liste des dépendances
├── README.md             # Documentation du projet
```

---

## Installation

### 1. Clonage d'un référentiel

Clonez le projet sur votre ordinateur local:

```bash
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

### 2. Créer un environnement virtuel

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances:

```bash
# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate  # Pour Bash/Zsh/Linux/MacOS
venv\Scripts\activate     # Pour Windows
```

### 3. Définition des dépendances

Définissez les dépendances de `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Configuration

1. Renommez le fichier `.env.example` en `.env`:

```bash
mv .env.example .env
```

2. Spécifiez le jeton et L'URL de base de l'API dans `.env`:

```plaintext
API_TOKEN='ВАШ_API_ТОКЕН'
API_URL='https://api.freecurrencyapi.com/v1'
```

---

## Démarrage

### 1. Lancement de l'application

Exécutez le projet via le fichier `index.py`:

```bash
python3 index.py
```

---

## Étalonnage

### Exécuter des tests

Pour exécuter les tests, utilisez le fichier `tests/test.py`:

```bash
python3 tests/test.py
```

Ce fichier vérifie que la connexion à l'API est correcte et affiche une liste des devises disponibles.

---

## Démonstration de travail

Conversion réussie

![currency-convert-result-work-success.png](/docs/img/currency-convert-result-work-success.png)

<details>
<summary> Processus de conversion (conversion réussie (GIF))</summary>

![currency-convert-result-work-success.gif](/docs/img/currency-convert-result-work-success.gif)

</details>

Erreur lors de la conversion

![currency-convert-result-work-error.png](/docs/img/currency-convert-result-work-error.png)

<details>
<summary>Processus de conversion (erreur de conversion (GIF))</summary>

![currency-convert-result-work-error.gif](/docs/img/currency-convert-result-work-error.gif)

</details>

---

## Convertisseur de devises en PHP

Créé un projet en PHP avec des fonctionnalités similaires, mais ayant un certain nombre de différences:

- Mise en œuvre de l'interface Web
- Décrit tous les Endpoints de service disponibles.

Exemple de code: [freecurrencyapi-converter-php](https://github.com/yaleksandr89/freecurrencyapi-converter-php) — tout le monde, entrez! 😄

---

## Exemple

1. **Jeton de sécurité:**
   - Assurez-vous que votre jeton API est correctement répertorié dans `.env`.
   - Ne jamais ajouter un fichier `.env` dans le référentiel.

2. **Recommandation:**
   - Utilisez un environnement virtuel pour isoler les dépendances.
   - Mettre à jour les paramètres si nécessaire via `pip install --upgrade`.
