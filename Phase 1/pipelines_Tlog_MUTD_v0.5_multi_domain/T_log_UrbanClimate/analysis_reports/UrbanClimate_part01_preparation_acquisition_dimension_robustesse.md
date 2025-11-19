# UrbanClimate V0.1 – Partie 1 (cellules 0–9) : Préparation, acquisition Kaggle et première évaluation T_log

## 1. Périmètre de la partie

Cette première partie correspond aux cellules **0 à 9** du notebook `UrbanClimate_part01.ipynb`, dérivé de `T_log_UrbanClimate.ipynb` après découpe en blocs de 10 cellules.

Elle couvre quatre blocs principaux :

- **Bloc 0/installation** : installation des dépendances via `requirements.txt`.
- **Bloc 1** : préparation de l’environnement (seed, dossiers, logs).
- **Bloc 2** : téléchargement du dataset Kaggle *Urban Air Quality and Climate* et inspection initiale du fichier `urban_climate.csv`.
- **Blocs 3–4** : estimation de la dimension effective `d` pour les villes, calcul de `T_log` et première validation empirique/robustesse (leave‑one‑out, balayage n/d).

Cette partie installe donc à la fois le **contexte technique** (environnement de travail) et un premier **diagnostic T_log** sur le système UrbanClimate.

---

## 2. Installation des dépendances et préparation de l’environnement

### 2.1 Installation via `requirements.txt` (cellule 1)

La cellule d’installation :

- importe `subprocess` et `sys` ;
- définit la fonction `install_requirements(file_path="requirements.txt")` qui :
  - exécute `pip install -r requirements.txt` dans le même environnement Python ;
  - affiche des messages de succès ou d’erreur détaillés ;
  - invite à **redémarrer le noyau** en première exécution.

Cette étape garantit que toutes les dépendances nécessaires (pandas, numpy, matplotlib, sklearn, scipy, kaggle, etc.) sont disponibles pour le reste du pipeline.

### 2.2 Bloc 1 – Préparation, dossiers, logs (cellule 2)

Le **Bloc 1** initialise l’environnement d’exécution :

- imports principaux : `os`, `sys`, `shutil`, `random`, `numpy`, `pandas`, `matplotlib` (mode `Agg` pour éviter les soucis d’affichage en environnement non interactif), `logging`, `datetime` ;
- configuration de la **reproductibilité** :
  - `SEED = 42` ;
  - `random.seed(SEED)` et `np.random.seed(SEED)` ;
- création/validation des dossiers de travail :
  - `DIRS = ['data', 'results', 'logs']` ;
  - pour chaque dossier : `os.makedirs(d, exist_ok=True)` ;
- nettoyage optionnel de `/content/sample_data` (cas Colab) ;
- mise en place d’un **logger Python** (`logger = logging.getLogger('Tlog_V0_1')`) avec :
  - niveau DEBUG, sortie console formatée (`timestamp\tlevel\tmessage`).

La cellule initialise aussi la **traçabilité** :

- fichier `logs/logs.csv` :
  - créé s’il n’existe pas, avec une première ligne d’INFO : *"Initialisation des logs pour T_log V0.1 - Bloc 1"* ;
  - sinon, ajout d’une entrée *"Re-initialisation des logs à l'exécution de Bloc 1"* ;
- fichier `logs/summary.md` :
  - créé avec un titre et la date d’initialisation si absent ;
  - sinon, ajout d’une ligne indiquant la ré‑exécution du Bloc 1.

Enfin, la cellule imprime un **état synthétique** :

- existence des dossiers `data/`, `results/`, `logs/` ;
- tailles des fichiers `logs/logs.csv` et `logs/summary.md`.

En cas d’erreur, un bloc `except` écrit un log d’erreur dans `logs/logs.csv` avant de relancer l’exception.

**Rôle** : fournir un environnement reproductible, structuré, et entièrement logué pour les étapes UrbanClimate.

---

## 3. Acquisition Kaggle et inspection du dataset urban_climate.csv

### 3.1 Authentification Kaggle et téléchargement (cellules 3–4)

Les cellules suivantes assurent la connexion à Kaggle et la récupération du dataset :

- installation silencieuse de la librairie `kaggle` (`!pip install kaggle --quiet`) ;
- tentative d’import de `kaggle.api` ;
- fonction `append_log(level, message)` :
  - ajoute des lignes à `logs/logs.csv` et `logs/summary.md` avec horodatage UTC ;
- fonction `find_and_auth_kaggle()` :
  - essaie d’abord de trouver `KAGGLE_USERNAME` / `KAGGLE_KEY` dans les variables d’environnement ;
  - sinon cherche un fichier `kaggle.json` soit dans `~/.kaggle/`, soit dans le répertoire courant ;
  - si trouvé, configure les variables d’environnement, puis appelle `kaggle_api.authenticate()` ;
  - écrit des logs de succès ou d’erreur.

Config Kaggle spécifique :

- `KAGGLE_DATASET_ID = "krishd123/urban-air-quality-and-climate-dataset-1958-2025"` ;
- `TARGET_FILE_NAME = "urban_climate.csv"` ;
- fichier cible local : `data/urban_climate.csv`.

La cellule :

- télécharge et **décompresse** le dataset dans `data/` (`dataset_download_files(..., unzip=True, force=True, quiet=True)`) ;
- vérifie que `data/urban_climate.csv` existe, sinon déclenche une erreur explicite ;
- logue le succès (*"Téléchargement et préparation du fichier"*) et affiche un message de confirmation.

### 3.2 Lecture robuste et inspection

Après le téléchargement :

- tentative de lecture du CSV avec plusieurs stratégies (UTF‑8 virgule, UTF‑8 point‑virgule, Latin‑1) pour gérer des encodages/formatages potentiellement variés ;
- calcul des caractéristiques globales :
  - `n_rows = 11040` ;
  - `n_cols = 12` ;
  - colonnes :
    - `['city', 'country', 'latitude', 'longitude', 'year', 'month', 'temperature_celsius', 'humidity_percent', 'precipitation_mm', 'wind_speed_ms', 'urban_heat_island_intensity', 'data_source']` ;
  - `missing_counts` montre **aucune valeur manquante** (série vide).

Un aperçu des 200 premières lignes est sauvegardé dans :

- `results/urban_climate_preview.csv`.

Des logs supplémentaires enregistrent :

- le succès du chargement ;
- la liste des colonnes détectées ;
- les colonnes avec valeurs manquantes (ici aucune).

L’affichage console récapitule ces informations (taille, colonnes, absence de NA, chemin de l’aperçu).

**Conclusion** : le dataset UrbanClimate est **propre**, complet (pas de NA détectés) et prêt pour les calculs T_log.

---

## 4. Bloc 3 – Estimation de la dimension effective d et calcul de T_log

Le **Bloc 3** réalise le premier calcul T_log pour UrbanClimate en estimant une **dimension effective d** basée sur les variables climatiques urbaines.

### 4.1 Construction des entités et features

- lecture de `data/urban_climate.csv` ;
- définition d’une clé de ville :
  - `city_key = city + country + latitude + longitude` (concaténation sous forme de chaîne) ;
- nombre de villes distinctes :
  - `n_cities = 20` ;
- sélection des variables climatiques :
  - `['temperature_celsius','humidity_percent','precipitation_mm','wind_speed_ms','urban_heat_island_intensity']` ;
- agrégation par ville : moyenne temporelle de ces variables pour chaque `city_key` ;
- standardisation (`StandardScaler`) pour obtenir une matrice `Xs` (villes × features) centrée‑réduite.

### 4.2 Estimation de d (participation ratio + PCA 90%)

Deux estimateurs complémentaires de dimension effective sont combinés :

- **Participation ratio** :
  - calcul des valeurs propres de la matrice de covariance de `Xs` ;
  - definition d’une dimension spectrale
    \[
    d_{part} = \frac{(\sum_i \lambda_i)^2}{\sum_i \lambda_i^2};
    \]
  - sur UrbanClimate, on obtient **`d_participation ≈ 3.8005`**.
- **PCA 90%** :
  - PCA sur les features ;
  - nombre minimal de composantes nécessaires pour expliquer 90% de la variance (`d_pca90`) ;
  - ici **`d_pca90 = 4`**.

La dimension effective retenue est la moyenne :

\[
 d_{estimate} = \frac{d_{participation} + d_{pca90}}{2} \approx \frac{3.8005 + 4}{2} = 3.90025.
\]

Cette valeur est loguée dans `logs/logs.csv`.

### 4.3 Calcul de T_log et régime global

On applique la loi T_log (sans biais) :

\[
T_{\log}(n,d) = (d-4) \ln(n).
\]

Ici :

- `n_cities = 20`, avec `n_eff = max(2, n_cities) = 20` ;
- `d_estimate ≈ 3.90025` ;
- donc :

\[
T_{\log} \approx (3.90025-4) \ln(20) \approx -0.298824.
\]

Le régime est alors classé comme :

- **`regime = Divergence`** (T_log < 0).

Un CSV `results/tlog_d_estimates.csv` est créé avec un résumé global (n_cities, d_participation, d_pca90, d_estimate, T_log, regime, n_used_for_ln, bias).

Deux figures sont sauvées :

- `results/d_estimates_hist.png` : spectre des valeurs propres de la covariance (structure de variance entre villes) ;
- `results/tlog_distribution.png` : T_log en fonction de d pour quelques valeurs n (0.5×n_eff, 1×n_eff, 2×n_eff), avec une ligne horizontale à T_log=0.

**Message clé** : pour UrbanClimate, avec une dimension effective d≈3.90 légèrement **inférieure à 4**, le système est en **régime Divergence** global.

---

## 5. Bloc 4 – Validation empirique et robustesse (LOO, balayage n/d)

Le **Bloc 4** teste la robustesse de ce diagnostic en jouant sur la composition des villes et sur de petites perturbations de d.

### 5.1 Leave‑one‑out (LOO) sur les villes

- pour chaque ville i :
  - on retire cette ville de la matrice `Xs` ;
  - on recalcule `d_participation`, `d_pca90`, donc `d_est` ;
  - on ajuste `n_eff` au nouveau nombre de villes ;
  - on recalcule `T_log` ;
- on stocke ces résultats dans `results/tlog_leave_one_out.csv`.

Résumé LOO :

- moyenne T_log (LOO) : **≈ −0.353** ;
- écart type : **≈ 0.086** ;
- écart relatif `rel_std_pct` ≈ **24.36%** ;
- test t (H0 : mean T_log = 0) → p‑value ≈ **0.000000**.

Interprétation :

- la moyenne de T_log reste **nettement négative** lorsque l’on retire chaque ville à tour de rôle ;
- l’écart relatif (~24%) montre que l’amplitude de T_log est **sensible** à la composition exacte des villes, mais le **signe** reste clairement en Divergence ;
- le test t rejette H0 : T_log n’est pas compatible avec 0 → le système est significativement hors‑équilibre (d’en‑deçà de la frontière critique).

Une figure `results/tlog_loo_hist.png` visualise la distribution LOO de T_log, centrée dans la zone négative, avec la ligne T_log=0 en référence.

### 5.2 Balayage systématique n/d (fractions et perturbations de d)

L’étape suivante combine :

- sous‑échantillonnages de villes par fractions **50%, 75%, 100%** (tirages répétés, `repeats = 100`) ;
- perturbations de la dimension locale via des facteurs multiplicatifs sur `d_est_sub` :
  - `d_perturb_factors` dans [0.8, 1.2] (±20%).

Pour chaque combinaison (fraction, tirage, facteur de d), on calcule :

- `d_pert` ;
- `n_eff_sub` (nombre de villes dans le sous‑échantillon) ;
- `T_log = (d_pert-4)*ln(n_eff_sub)` ;
- le régime (Divergence / Équilibre / Saturation) ;
- on sauvegarde `results/tlog_sweep_summary.csv`.

Un résumé par fraction est calculé dans `results/tlog_sweep_fraction_summary.csv`, contenant :

- `match_frac` = fraction d’expériences où le régime coïncide avec le régime global (ici Divergence) ;
- `unstable_frac` = 1 − `match_frac` ;
- `median_T`, `std_T` pour T_log.

Valeurs clés affichées :

- fraction = 0.50 → `match_frac ≈ 0.8389` (≈84% de cas alignés avec le régime global) ;
- fraction = 0.75 → `match_frac ≈ 0.6433` ;
- fraction = 1.00 → `match_frac ≈ 0.5556`.

Il y a également une heatmap `results/tlog_sweep_heatmap.png` montrant la médiane de T_log en fonction de la fraction et du facteur de d.

Interprétation :

- pour des sous‑échantillons plus petits (50% des villes), le régime Divergence est très robuste (~84% des perturbations conservent le même régime) ;
- lorsque l’on utilise toutes les villes et que l’on perturbe d jusqu’à ±20%, la fraction de cas où le régime reste identique diminue (~56%) :
  - ce n’est pas surprenant, car de fortes perturbations de d autour de 4 permettent de franchir la frontière critique ;
- globalement, le signe de T_log reste **négatif dans la majorité des configurations** raisonnables, ce qui conforte le diagnostic Divergence pour l’UrbanClimate V0.1.

---

## 6. Bilan de la Partie 1 pour UrbanClimate

Cette première partie du pipeline UrbanClimate V0.1 montre que :

- l’environnement de travail (dépendances, dossiers, logs) est correctement initialisé et entièrement tracé ;
- le dataset **Urban Air Quality and Climate (1958–2025)** est propre (aucune valeur manquante détectée), avec **11040 enregistrements** et **12 colonnes** dont les variables climatiques centrales pour T_log ;
- la dimension effective **d_estimate ≈ 3.90**, légèrement inférieure à 4, se traduit par un **T_log global ≈ −0.30** → régime de **Divergence** ;
- les tests de robustesse (leave‑one‑out et balayage n/d) confirment que :
  - T_log reste significativement **négatif** en moyenne ;
  - le régime Divergence est majoritaire sur un large ensemble de perturbations ;
  - mais l’amplitude de T_log est sensible à la composition exacte des villes et aux variations fortes de d.

En résumé, UrbanClimate V0.1, dans cette première partie, se comporte comme un système **globalement divergent** par rapport à la frontière critique d=4, avec une dimension effective légèrement sous‑critique et une structure statistique robuste mais non triviale. Les parties suivantes exploreront si, et comment, il est possible de rapprocher ce système d’un équilibre T_log=0 (par exemple via recalibrage de d, segmentation temporelle/spatiale, ou introduction de mémoire).
