# Commandes CLI, saisie et erreurs

## Choisir la langue

| Русский | English | Español | 中文 | Français | Deutsch |
| --- | --- | --- | --- | --- | --- |
| [Русский](cli-and-errors.md) | [English](cli-and-errors_en.md) | [Español](cli-and-errors_es.md) | [中文](cli-and-errors_zh.md) | **Sélectionné** | [Deutsch](cli-and-errors_de.md) |

## Options de lancement

Exécutez `index.py` depuis la racine du dépôt avec l’interpréteur Python de `.venv`, créé lors de l’installation. Exemples pour Linux et macOS :

```bash
# Conversion interactive en russe.
.venv/bin/python index.py

# Interface anglaise.
.venv/bin/python index.py --lang en

# Aide sans lecture de .env ni appel à l’API.
.venv/bin/python index.py --help
```

Sous Windows PowerShell, remplacez `.venv/bin/python` par `.\.venv\Scripts\python.exe`. Les deux méthodes figurent dans le [guide de démarrage](../guides/getting-started_fr.md).

| Option | Fonctionnement |
| --- | --- |
| `-h`, `--help` | Affiche l’aide dans la langue sélectionnée sans charger `.env` ni appeler l’API. |
| `--lang ru` | Sélectionne l’interface russe, utilisée par défaut. |
| `--lang en` | Sélectionne l’interface anglaise ; peut être associé à `--help`. |

## Saisie et format du résultat

Le CLI charge et affiche d’abord les devises. Les codes sont entre crochets ; les noms proviennent de FreecurrencyAPI.

1. Saisissez un code de devise d’origine de la liste, par exemple `USD`.
2. Saisissez un nombre positif et fini avec un point décimal, par exemple `2.5`. Les valeurs `2,5`, `NaN` et `inf` sont rejetées.
3. Saisissez un ou plusieurs codes cibles, par exemple `EUR,GBP`. Un élément vide, y compris après une virgule finale, est invalide.

La casse des codes est ignorée, ainsi que les espaces à leurs extrémités. En cas de saisie incorrecte, l’exécution s’arrête : relancez la commande.

Le montant est converti en `float`, puis arrondi par `round` à trois décimales avant multiplication par le taux. Un montant arrondi à zéro ou un résultat non fini provoque une erreur.

Les résultats sont envoyés sur la sortie standard, une ligne par devise cible dans l’ordre de réponse de l’API. Le montant source arrondi n’a pas de nombre fixe de décimales ; le montant converti en a deux. Cet exemple utilise des taux simulés issus des tests.

```text
2.5 USD = 2.00 EUR
2.5 USD = 1.25 GBP
```

## Requêtes FreecurrencyAPI

Les deux requêtes utilisent `GET`, la base `API_URL` et la clé `API_TOKEN` transmise dans le paramètre `apikey`.

| Endpoint | Utilisation par le CLI |
| --- | --- |
| [`/currencies`](https://freecurrencyapi.com/docs/currencies) | Récupère les devises avant la première invite et exige un nom non vide pour chaque code. |
| [`/latest`](https://freecurrencyapi.com/docs/latest) | Demande les taux après validation. Envoie la devise source dans `base_currency` et les cibles séparées par des virgules dans `currencies`. Le montant est multiplié localement. |

Le client accepte HTTP 200 avec un objet JSON `data` non vide. Les délais sont de 4 secondes pour la connexion et de 10 secondes pour la lecture. Les redirections sont désactivées. Un taux doit être présent pour chaque devise demandée ; seuls ces taux sont utilisés. FreecurrencyAPI définit les devises, les taux et les quotas disponibles.

## Codes de sortie

| Code | Signification |
| --- | --- |
| `0` | Conversion réussie ou aide affichée. |
| `1` | Erreur de configuration, requête, réponse API ou saisie, y compris fin prématurée de la saisie (EOF). |
| `2` | Arguments CLI incorrects, notamment option inconnue ou langue `--lang` non prise en charge. |
| `130` | Interruption de la session avec Ctrl+C. |

## Messages d’erreur

Les erreurs sont envoyées sur `stderr` dans la langue de `--lang`. Une valeur `--lang` non prise en charge produit un message en russe.

| Catégorie | Cause |
| --- | --- |
| Configuration | `API_TOKEN` ou `API_URL` absent ou ne contenant que des espaces. |
| Réseau | Délai dépassé ou autre erreur de requête, par exemple une connexion impossible. |
| HTTP | Le serveur renvoie un statut différent de 200 ; le CLI l’affiche. |
| Réponse API | JSON incorrect ; objet `data` manquant, vide ou invalide ; métadonnées de devise incorrectes ; taux manquant, non positif, non numérique ou non fini pour une devise cible. |
| Saisie | Code source ou cible inconnu, cible vide, montant invalide, arrondi à zéro ou dépassement de capacité lors du calcul. |
| Fin de session | La saisie s’est terminée avant que toutes les valeurs soient fournies ou l’utilisateur a appuyé sur Ctrl+C. |
