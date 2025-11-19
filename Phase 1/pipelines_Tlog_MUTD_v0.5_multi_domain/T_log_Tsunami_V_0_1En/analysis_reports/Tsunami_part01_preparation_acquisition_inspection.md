# Tsunami V0.1 – Partie 1 (cellules 0–7) : Préparation, acquisition Kaggle et inspection initiale

## 1. Périmètre de la partie

Cette première partie correspond aux cellules **0–7** du notebook splitté `Tsunami_part01.ipynb`, dérivé de :

`T_log_Tsunami_V_0_1En.ipynb`

Elle couvre :

- l’**installation des dépendances** via `requirements.txt` ;
- la **préparation de l’environnement** (dossiers, logger, fichiers de log) ;
- l’**acquisition du dataset Kaggle Tsunami** (Earthquake–Tsunami Risk Assessment) sous forme de ZIP ;
- la **décompression** et l’**inspection du fichier CSV principal** `earthquake_data_tsunami.csv` ;
- la préparation conceptuelle du calcul de `T_log(n,d)` pour ce jeu de données.

Aucun calcul numérique de T_log n’est encore effectué, mais les données sont prêtes et le cadre T_log (choix de n et d) est posé.

---

## 2. Installation des dépendances (requirements.txt)

Comme pour les autres pipelines v0.5, la première cellule exécutable installe les dépendances du projet :

- import de `subprocess` et `sys` ;
- définition de `install_requirements(file_path="requirements.txt")` ;
- exécution :

  - `subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file_path])`.

Si l’installation se passe bien :

- un message de succès est affiché ;
- une note rappelle de **redémarrer le kernel** lors de la première exécution.

Cette étape assure que les librairies nécessaires (pandas, numpy, matplotlib, kaggle, etc.) sont disponibles pour la suite du pipeline Tsunami.

---

## 3. Bloc 1 – Préparation de l’environnement (logs, dossiers, logger)

### 3.1 Imports, seeds et création des dossiers

La cellule "Bloc 1 — Préparation" :

- importe : `os`, `sys`, `logging`, `random`, `time`, `datetime`, `numpy`, `pandas`, `matplotlib` (backend non interactif `Agg`) ;
- fixe les **seeds** :
  - `random.seed(42)` ;
  - `np.random.seed(42)` ;
- crée (idempotent) les dossiers :

  - `data/`, `results/`, `logs/`.

### 3.2 Logger et fichiers de log

Un logger est configuré :

- logger nommé `T_log_V0_1`, niveau `INFO` ;
- format standard : `'%(asctime)s | %(levelname)s | %(message)s'` ;
- deux handlers :
  - fichier `logs/logs.txt` (lecture humaine rapide) ;
  - console (stdout).

Deux fichiers de log structurés sont initialisés :

- `logs/logs.csv` :
  - colonnes `['timestamp', 'level', 'message']` ;
  - créé vide si absent ;
- `logs/summary.md` :
  - entête Markdown `# Journal de test — Modèle T_log V0.1` ;
  - date de création ;
  - section "Événements clés".

Fonction utilitaire :

- `log_to_csv(level, message)` :
  - construit une ligne `[timestamp ISO, level, message]` ;
  - l’ajoute à `logs/logs.csv` ;
  - utilisée pour centraliser les événements dans un format tabulaire.

### 3.3 Nettoyage d’environnement et messages de confirmation

La cellule tente de supprimer `/content/sample_data` (cas usage Colab) :

- si le dossier existe, suppression et log `INFO` ;
- sinon, log qu’il n’y a rien à supprimer.

En sortie :

- messages dans les logs (txt + csv) ;
- affichage de la carte des dossiers avec chemins absolus ;
- confirmation que le logger et les fichiers de log sont opérationnels.

Ce bloc met en place un socle de **reproductibilité et traçabilité** similaire à celui des pipelines Sunspots et PM2.5.

---

## 4. Bloc 2 – Acquisition Kaggle du dataset Tsunami (ZIP) et inspection du CSV

### 4.1 Téléchargement du ZIP Kaggle

Une cellule installe silencieusement `kaggle` (`!pip install kaggle --quiet`), puis :

- importe `kaggle.api` sous le nom `kaggle_api` ;
- définit `KAGGLE_DATASET_ID = "ahmeduzaki/global-earthquake-tsunami-risk-assessment-dataset"` ;
- fixe `DOWNLOAD_DIR = '/content/data'` et crée ce dossier.

Fonction `find_and_auth_kaggle()` :

- cherche les identifiants Kaggle via :
  - variables d’environnement `KAGGLE_USERNAME`, `KAGGLE_KEY` ;
  - ou un fichier `kaggle.json` dans `~/.kaggle/` ou le répertoire courant ;
- en cas de succès, appelle `kaggle_api.authenticate()` ;
- logge les étapes et les erreurs éventuelles.

Téléchargement :

- `kaggle_api.dataset_download_files(KAGGLE_DATASET_ID, path=DOWNLOAD_DIR, unzip=False, quiet=True)` ;
- le ZIP téléchargé est ensuite :
  - détecté dans `/content/data` ;
  - renommé en :

    - `"Global Earthquake-Tsunami Risk Assessment Dataset.zip"` ;

- un message confirme :
  - succès du téléchargement ;
  - chemin du ZIP : `/content/data/Global Earthquake-Tsunami Risk Assessment Dataset.zip`.

Ce fichier ZIP contient les données sismiques et tsunamis à analyser.

### 4.2 Décompression et inspection des CSV (Bloc 2)

Le Bloc 2 décompresse le ZIP et inspecte les CSV :

- `zip_path = '/content/data/Global Earthquake-Tsunami Risk Assessment Dataset.zip'` ;
- `extract_dir = 'data/extracted'` ;
- extraction via `zipfile.ZipFile(...).extractall(extract_dir)` ;
- liste des fichiers extraits loggée via `logger` et `log_to_csv`.

Filtrage :

- `csv_files = [f for f in extracted_files if f.lower().endswith('.csv')]` ;
- dans l’exécution observée :
  - un seul CSV : `earthquake_data_tsunami.csv`.

Inspection de `earthquake_data_tsunami.csv` :

- lecture dans un DataFrame ;
- calcul :
  - `shape = (782, 13)` → 782 événements, 13 colonnes ;
  - `empty_cols = []` → aucune colonne entièrement vide ;
  - `total_NaN = 0` → aucune valeur manquante ;
- impression d’un aperçu (3 premières lignes) ;
- enregistrement d’un résumé dans `results/data_summary.csv` avec colonnes :
  - file, rows, cols, empty_cols, total_NaN.

Un log INFO enregistre ces informations dans `logs/logs.csv`.

Conclusion :

- le fichier `earthquake_data_tsunami.csv` est **propre** (0 NaN, aucune colonne vide) ;
- il contient l’échantillon sur lequel T_log sera calculé.

---

## 5. Bloc 3 – Préparation conceptuelle du calcul de T_log

La dernière cellule Markdown de cette partie prépare le **Block 3 — Calcul de T_log**.

Éléments clés :

- on dispose de **n = 782** événements sismiques/tsunami ;
- il faut choisir une **dimension effective d** pour ce système ;
- le dataset n’est pas (pour l’instant) représenté comme un graphe avec spectre de Laplacien, donc d doit être choisi comme **approximation physique** plutôt que comme dimension spectrale estimée.

Deux options proposées :

1. **Dimension physique spatiale** :
   - latitude, longitude, profondeur → 3D → **d = 3** ;
2. **Dimension spatiale + temps** :
   - latitude, longitude, profondeur, temps → 4D → **d = 4**.

Dans l’esprit de la version V0.1 (sans extension PDE), la cellule propose de commencer avec :

- **d = 3** comme choix naturel (dimension de l’espace physique) ;
- puis d’explorer la sensibilité autour de d ≈ 3–4.

Le prochain bloc (non encore exécuté dans cette partie) calculera donc :

\[
T_{\log}(782, 3) = (3 - 4) \ln(782)
\]

et classifiera le régime correspondant (a priori Divergence, car d=3<4).

---

## 6. Rôle de la Partie 1 dans le pipeline Tsunami V0.1

La Partie 1 du pipeline Tsunami :

- installe les dépendances nécessaires (avec appel à `requirements.txt`) ;
- prépare un **environnement loggé** complet (dossiers, logger, logs CSV + Markdown) ;
- télécharge de manière robuste le dataset Kaggle "Global Earthquake-Tsunami Risk Assessment" ;
- décompresse le ZIP, identifie et inspecte le fichier CSV principal (`earthquake_data_tsunami.csv`) ;
- vérifie que ce CSV est **propre** (782×13, aucune valeur manquante, aucune colonne vide) ;
- pose le cadre conceptuel pour T_log : choix de **n = 782** et proposition initiale **d = 3** comme dimension effective.

En résumé, cette première partie prépare tous les éléments nécessaires pour que les parties suivantes se concentrent sur :

- le calcul effectif de T_log(n,d) pour le système tsunami ;
- la comparaison de régimes pour différents choix de d (3 vs 4, etc.) ;
- et, éventuellement, l’extension du modèle vers des dimensions effectives dérivées de structures plus riches (graphes, spectres, etc.), comme dans les pipelines Sunspots et PM2.5.
