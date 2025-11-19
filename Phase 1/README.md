# MUTD & T_log – Version 0.5

This folder contains the **v0.5 specification** of the Logarithmic Tension parameter `T_log` and the Unified Dynamic Tension Model `MUTD`, together with four reproducible pipelines applied to real-world datasets.

The goal of this version is to provide a **clean, executable and multi-domain testbed** for the core equations, before later versions (v1, v2, v3).

## Contents

- `THEORY/`
  - Original theoretical documents (French):
    - `ComicsTensionV0.5_T_log.txt`
    - `MixV0.5.txt`
    - `V0.5.5_Tension_Dynamique_MUTD.txt`

- `THEORY_EN/`
  - English versions of the core theoretical texts:
    - `ComicsTensionV0.5_T_log_EN.txt` – definition and interpretation of the T_log parameter.
    - `MixV0.5_EN.txt` – MUTD as a two-step unified framework (D_eff then T_dyn).
    - `V0.5.5_Tension_Dynamique_MUTD_EN.txt` – concise formulation of MUTD and its regimes.

- `pipelines_Tlog_MUTD_v0.5_multi_domain/`
  - Four pipelines applying T_log / MUTD to different domains:
    - `Pipeline_Tlog_V0.1_Sunspots_En/` – Sunspots time series.
    - `T_log_Tsunami_V_0_1En/` – Earthquake–Tsunami dataset.
    - `T_log_Pipeline_PM2.5_Global_vs_Local_(New_York)EN/` – Global vs local PM2.5 air quality.
    - `T_log_UrbanClimate/` – Urban climate dataset (MUTD, with effective dimension estimation).

Each pipeline is designed to be **self-contained**, with its own `requirements.txt`, data folder, logs, and results.

## Core ideas (v0.5 / v0.5.5)

- **T_log (v0.5)**
  - `T_log(n, d) = (d - 4) * log(n)`
  - `n`: system size (number of elements/events/data points).
  - `d`: effective dimension of the system.
  - Regimes (via sign of `T_log`):
    - `T_log > 0`  → Saturation / Stability.
    - `T_log ≈ 0` → Criticality (transition).
    - `T_log < 0`  → Divergence / Instability.

- **MUTD (v0.5.5)**
  - Step 1: structural complexity via effective dimension
    - `D_eff = log(n) / log(d_obs)`
  - Step 2: dynamic tension
    - `T_dyn = (D_eff - 4) * log(n)`
  - The sign of `T_dyn` is interpreted in the same three regimes as above.

For full details, see the documents in `THEORY_EN/`.

## How to run a pipeline

1. Install Python 3 and a virtual environment tool (e.g. `venv` or `conda`).
2. Open a terminal in one of the pipeline folders, for example:
   - `pipelines_Tlog_MUTD_v0.5_multi_domain/Pipeline_Tlog_V0.1_Sunspots_En/`
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies listed in `requirements.txt`, for example:
   - `pip install -r requirements.txt`
5. Open the main notebook of the pipeline (e.g. `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`) in Jupyter, JupyterLab or VS Code and execute the cells.

### Kaggle API key (for pipelines using Kaggle)

Some pipelines download data via the Kaggle API and expect a `kaggle.json` file. You have two options:

1. **Edit the placeholders in the provided `kaggle.json` files**:
   - Set `"username"` to your Kaggle username.
   - Set `"key"` to your personal Kaggle API token.
2. **Replace the placeholder file with the official token from Kaggle**:
   - Create a free account at [https://www.kaggle.com/](https://www.kaggle.com/) (if you do not have one).
   - Go to **My Account → API → Create New Token**.
   - Download the generated `kaggle.json` and copy it into the corresponding pipeline folder.

Never commit real credentials to a public repository.

Each pipeline writes logs and results in its own `logs/` and `results/` folders.

## Scientific status and limitations

- These equations are currently used as **heuristic models** inspired by statistical physics and fractal concepts.
- The choice of critical dimension `4` and the definition of effective dimension `D_eff` must be **validated empirically** in each application domain.
- The pipelines provide **case studies and stress tests**, not final proofs of universality.

Users are encouraged to:

- Reproduce the results.
- Adapt the notion of effective dimension to their own data.
- Compare alternative definitions of `d` or `D_eff`.

## Versioning

This folder corresponds to **version 0.5 / 0.5.5** of the equations (T_log and MUTD).

Later versions (v1, v2, v3) expand the framework and test new datasets and protocols, but are kept separate to preserve the clarity of this baseline version.

---

## MUTD & T_log – Version 0.5 (FR)

Ce dossier contient la **spécification v0.5** du paramètre de tension logarithmique `T_log` et du Modèle Unifié de Tension Dynamique `MUTD`, ainsi que quatre pipelines reproductibles appliqués à des jeux de données réels.

L'objectif de cette version est de fournir un **banc d'essai propre, exécutable et multi-domaines** pour les équations centrales, avant les versions ultérieures (v1, v2, v3).

## Contenu

- `THEORY/`
  - Documents théoriques originaux (français) :
    - `ComicsTensionV0.5_T_log.txt`
    - `MixV0.5.txt`
    - `V0.5.5_Tension_Dynamique_MUTD.txt`

- `THEORY_EN/`
  - Versions anglaises des textes théoriques principaux :
    - `ComicsTensionV0.5_T_log_EN.txt` – définition et interprétation du paramètre T_log.
    - `MixV0.5_EN.txt` – MUTD comme cadre unifié en deux étapes (D_eff puis T_dyn).
    - `V0.5.5_Tension_Dynamique_MUTD_EN.txt` – formulation concise de MUTD et de ses régimes.

- `pipelines_Tlog_MUTD_v0.5_multi_domain/`
  - Quatre pipelines appliquant T_log / MUTD à différents domaines :
    - `Pipeline_Tlog_V0.1_Sunspots_En/` – série temporelle des taches solaires (Sunspots).
    - `T_log_Tsunami_V_0_1En/` – jeu de données Séisme–Tsunami.
    - `T_log_Pipeline_PM2.5_Global_vs_Local_(New_York)EN/` – qualité de l’air PM2.5 globale vs locale (New York).
    - `T_log_UrbanClimate/` – jeu de données de climat urbain (MUTD, estimation de dimension effective).

Chaque pipeline est conçu pour être **autonome**, avec son propre `requirements.txt`, dossier de données, journaux (`logs/`) et résultats (`results/`).

## Idées centrales (v0.5 / v0.5.5)

- **T_log (v0.5)**
  - `T_log(n, d) = (d - 4) * log(n)`
  - `n` : taille du système (nombre d’éléments/événements/points de données).
  - `d` : dimension effective du système.
  - Régimes (via le signe de `T_log`) :
    - `T_log > 0`  → Saturation / Stabilité.
    - `T_log ≈ 0` → Criticité (transition).
    - `T_log < 0`  → Divergence / Instabilité.

- **MUTD (v0.5.5)**
  - Étape 1 : complexité structurelle via la dimension effective
    - `D_eff = log(n) / log(d_obs)`
  - Étape 2 : tension dynamique
    - `T_dyn = (D_eff - 4) * log(n)`
  - Le signe de `T_dyn` se lit dans les mêmes trois régimes que ci‑dessus.

Pour les détails complets, voir les documents dans `THEORY_EN/` (EN) et `THEORY/` (FR).

## Comment exécuter un pipeline

1. Installer Python 3 et un outil d’environnement virtuel (par ex. `venv` ou `conda`).
2. Ouvrir un terminal dans l’un des dossiers de pipeline, par exemple :
   - `pipelines_Tlog_MUTD_v0.5_multi_domain/Pipeline_Tlog_V0.1_Sunspots_En/`
3. Créer et activer un environnement virtuel (recommandé).
4. Installer les dépendances listées dans `requirements.txt`, par exemple :
   - `pip install -r requirements.txt`
5. Ouvrir le notebook principal du pipeline (par ex. `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`) dans Jupyter, JupyterLab ou VS Code, puis exécuter les cellules.

Chaque pipeline écrit ses journaux et résultats dans ses propres dossiers `logs/` et `results/`.

### Clé API Kaggle (pour les pipelines utilisant Kaggle)

Certains pipelines téléchargent des données via l’API Kaggle et attendent un fichier `kaggle.json`. Vous avez deux options :

1. **Modifier les placeholders dans les fichiers `kaggle.json` fournis** :
   - Mettre `"username"` à votre nom d’utilisateur Kaggle.
   - Mettre `"key"` à votre jeton API Kaggle personnel.
2. **Remplacer le fichier de placeholder par le fichier officiel téléchargé depuis Kaggle** :
   - Créer un compte gratuit sur [https://www.kaggle.com/](https://www.kaggle.com/) (si ce n’est pas déjà fait).
   - Aller dans **My Account → API → Create New Token**.
   - Télécharger le `kaggle.json` généré et le copier dans le dossier du pipeline correspondant.

Ne jamais committer de véritables identifiants dans un dépôt public.

## Statut scientifique et limites

- Ces équations sont actuellement utilisées comme **modèles heuristiques**, inspirés de la physique statistique et des concepts fractals.
- Le choix de la dimension critique `4` et la définition de la dimension effective `D_eff` doivent être **validés empiriquement** dans chaque domaine d’application.
- Les pipelines fournissent des **études de cas et des tests de résistance**, pas des preuves finales d’universalité.

Les utilisateurs sont encouragés à :

- Reproduire les résultats.
- Adapter la notion de dimension effective à leurs propres données.
- Comparer des définitions alternatives de `d` ou de `D_eff`.

## Versionnage

Ce dossier correspond à la **version 0.5 / 0.5.5** des équations (T_log et MUTD).

Les versions ultérieures (v1, v2, v3) étendent ce cadre et testent de nouveaux jeux de données et protocoles, mais sont conservées séparément afin de préserver la clarté de cette version de base.
