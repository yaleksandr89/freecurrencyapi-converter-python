# Installation et premier lancement

## Choisir la langue

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](../../ru/guides/getting-started.md) | [English](../../en/guides/getting-started.md) | [Español](../../es/guides/getting-started.md) | [中文](../../zh/guides/getting-started.md) | **Sélectionné** | [Deutsch](../../de/guides/getting-started.md) |

## Versions autonomes

Lorsqu’une archive adaptée à votre système est disponible sur la [page des versions](https://github.com/yaleksandr89/freecurrencyapi-converter-python/releases), téléchargez-la et décompressez-la dans un dossier. La version autonome fonctionne sans Python ni `make`.

1. Dans le dossier décompressé, copiez `.env.example` dans `.env` et renseignez votre clé FreecurrencyAPI dans `API_TOKEN`. Conservez la valeur de `API_URL` du modèle.
2. Sous Windows, double-cliquez sur `currency-converter.exe`. Sous Linux et macOS, lancez `./currency-converter` dans un terminal depuis ce dossier. Sous macOS, vous pouvez aussi ouvrir `Launch Currency Converter.command`.

Le `README.md` inclus contient des instructions brèves en russe et en anglais.

Pour compiler depuis les sources avec GitHub Actions, utilisez le workflow [Standalone](https://github.com/yaleksandr89/freecurrencyapi-converter-python/actions/workflows/standalone.yml) : `Run workflow`, branche `master` et paramètre `targets`. Sélectionnez `all` pour une version complète (Windows x64, Linux x86_64, macOS arm64). Extrayez de l’artefact l’archive et son fichier `.sha256`. Comparez le SHA-256 de l’archive à la somme indiquée avant de la décompresser.

## Prérequis pour l’installation depuis les sources

- Git pour cloner le dépôt, Python 3.12 ou une version ultérieure, ainsi que le module `venv` avec `pip`.
- Votre propre clé FreecurrencyAPI pour effectuer les conversions. Inscrivez-vous au service, récupérez la clé dans votre compte et consultez la [documentation FreecurrencyAPI](https://freecurrencyapi.com/docs/).

## Récupérer les sources

Clonez le dépôt et placez-vous à sa racine, là où se trouve `index.py`. Toutes les commandes suivantes doivent être lancées depuis ce répertoire.

```bash
# Cloner le dépôt et accéder à son répertoire.
git clone https://github.com/yaleksandr89/freecurrencyapi-converter-python.git
cd freecurrencyapi-converter-python
```

## Installer les dépendances

### Linux et macOS

Vérifiez que `python3` désigne Python 3.12 ou une version ultérieure et que `make` est installé. `make setup` crée `.venv` si nécessaire puis installe le projet et les dépendances de développement.

```bash
# Vérifier la version de Python.
python3 --version

# Créer .venv et installer les dépendances de développement.
make setup

# Copier le modèle sans écraser une clé existante.
cp -n .env.example .env
```

Si le bon interpréteur porte un autre nom, passez-le avec `PYTHON`, par exemple `make setup PYTHON=python3.12`. Cette variable sert uniquement à la création de l’environnement.

### Windows PowerShell

Dans cet exemple, `python` correspond à Python 3.12 ou plus récent, accessible via `PATH`. Les commandes appellent directement l’interpréteur de `.venv` : ni activation ni `make` ne sont nécessaires.

```powershell
# Vérifier la version de Python.
python --version

# Créer l’environnement et installer les dépendances de développement.
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

# Copier le modèle uniquement si .env est absent.
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Pour installer uniquement le programme et ses dépendances d’exécution, remplacez `requirements-dev.txt` par `requirements.txt` dans `pip install`. Les vérifications locales nécessitent les dépendances de développement.

## Configurer la clé et l’adresse

Ouvrez le fichier `.env`. Remplacez `API_TOKEN` par votre clé et conservez dans `API_URL` l’adresse de base de l’API, sans chemin d’endpoint.

```ini
API_TOKEN=your_api_token_here
API_URL=https://api.freecurrencyapi.com/v1
```

Gardez votre clé en local. N’ajoutez pas `.env` à Git et ne publiez pas son contenu dans les signalements. Les variables déjà présentes dans l’environnement du processus ont priorité sur celles du fichier.

## Lancement et vérification

Sous Linux et macOS, lancez le convertisseur avec `make` :

```bash
# Interface russe (par défaut).
make run

# Interface anglaise.
make run CLI_LANG=en
```

Sous Windows PowerShell, utilisez l’interpréteur Python de l’environnement virtuel pour exécuter `index.py` :

```powershell
# Interface russe (par défaut).
.\.venv\Scripts\python.exe index.py

# Interface anglaise.
.\.venv\Scripts\python.exe index.py --lang en
```

Après l’accueil, la liste des devises s’affiche. Si elle contient `USD`, `EUR` et `GBP`, saisissez `USD`, `12.5` puis `EUR,GBP`, en validant chaque entrée. Le CLI affiche une ligne par devise cible. Les montants dépendent des taux récupérés.

Pour vérifier le démarrage sans clé ni appel à l’API, lancez `.venv/bin/python index.py --help` sous Linux/macOS ou `.\.venv\Scripts\python.exe index.py --help` dans PowerShell.

## En cas de problème

| Symptôme | À vérifier |
| --- | --- |
| `API_TOKEN` ou `API_URL` manquant | Vérifiez le nom du fichier `.env`, les noms des variables et leurs valeurs non vides. Contrôlez également les variables définies dans le shell. |
| Erreur avec un code HTTP | Vérifiez l’adresse de base, la validité de la clé et le quota FreecurrencyAPI disponible. |
| Délai dépassé ou échec de la requête | Vérifiez `API_URL` et la disponibilité de FreecurrencyAPI. |
| Saisie refusée par le CLI | Relancez le convertisseur, choisissez les codes affichés, séparez les devises cibles par des virgules et saisissez un montant positif avec un point décimal. |

Les causes et codes de sortie sont détaillés dans la [référence CLI et erreurs](../reference/cli-and-errors.md).

## Vérifications locales

Après l’installation des dépendances de développement, effectuez les vérifications depuis la racine du dépôt.

Sous Linux et macOS :

```bash
# Lancer les tests, Ruff et le contrôle des dépendances.
make check
```

Sous Windows PowerShell :

```powershell
# Tests hors ligne.
.\.venv\Scripts\python.exe -m pytest

# Vérifier le style et le formatage.
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .

# Vérifier les dépendances installées.
.\.venv\Scripts\python.exe -m pip check
```

Les tests simulent les réponses et erreurs FreecurrencyAPI et empêchent les appels HTTP réels. Ils ne nécessitent pas de clé active. Une conversion interactive reste nécessaire pour vérifier l’accès au service et la validité de la clé.
