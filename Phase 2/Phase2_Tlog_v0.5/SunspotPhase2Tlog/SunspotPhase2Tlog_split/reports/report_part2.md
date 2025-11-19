# Rapport détaillé sur la Partie 2 du Pipeline SunspotPhase2Tlog (Fin Bloc 1 et Début Bloc 2)

## Vue d'ensemble

La Partie 2 du pipeline SunspotPhase2Tlog complète le traitement des données (fin du Bloc 1) et initie les prétraitements et fenêtres (Bloc 2). Cette partie finalise la préparation des données Sunspots et pose les bases pour les analyses dimensionnelles.

## Fin du Bloc 1 – Données & traçabilité (Blocs 1.2 à 1.5)

### Bloc 1.2 – Chargement du CSV Sunspots et premières informations

#### Objectif
Charger automatiquement le CSV extrait et examiner sa structure sans hypothèses préalables.

#### Étapes détaillées

- **Détection automatique des CSV** :
  ```python
  csv_files = sorted(DATA_PHASE2_RAW_DIR.rglob("*.csv"))
  if len(csv_files) == 0:
      raise RuntimeError("Aucun fichier .csv trouvé dans data_phase2/sunspots_raw/ après extraction.")
  elif len(csv_files) > 1:
      raise RuntimeError("Plusieurs fichiers .csv trouvés... la Phase 2 attend exactement un fichier CSV Sunspots.")
  SUNSPOTS_CSV_PATH = csv_files[0]
  ```

- **Chargement sans hypothèses** :
  ```python
  df_sunspots = pd.read_csv(SUNSPOTS_CSV_PATH)
  n_rows, n_cols = df_sunspots.shape
  columns = df_sunspots.columns.tolist()
  ```

- **Informations de base** :
  - Nombre de lignes : 3265
  - Nombre de colonnes : 3
  - Colonnes : ['Unnamed: 0', 'Date', 'Monthly Mean Total Sunspot Number']
  - Aperçu des 5 premières lignes avec `display(df_sunspots.head())`

#### Gestion d'erreurs et contraintes
- Vérification d'existence du dossier `data_phase2/sunspots_raw/`
- Imposition d'exactement un fichier CSV pour reproductibilité
- Logging détaillé avec métriques (nombre de lignes/colonnes, noms de colonnes)

#### Fichiers de sortie
- Aucun nouveau fichier créé (chargement en mémoire)
- Métriques dans logs : `sunspots_csv_rows`, `sunspots_csv_extracted_count`

### Bloc 1.3 – Sélection et nettoyage des colonnes

#### Objectif
Nettoyer le DataFrame brut basé sur la structure réelle observée, sans hypothèses fictives.

#### Étapes détaillées

- **Copie de travail** :
  ```python
  df_sunspots_clean = df_sunspots.copy()
  ```

- **Suppression de la colonne d'index artificiel** :
  ```python
  if "Unnamed: 0" in df_sunspots_clean.columns:
      df_sunspots_clean = df_sunspots_clean.drop(columns=["Unnamed: 0"])
  ```

- **Conversion datetime** :
  ```python
  df_sunspots_clean["Date"] = pd.to_datetime(df_sunspots_clean["Date"], errors="coerce")
  nb_nat = df_sunspots_clean["Date"].isna().sum()
  if nb_nat > 0:
      raise RuntimeError(f"{nb_nat} valeur(s) de date invalide(s) détectée(s)...")
  ```

- **Conversion numérique** :
  ```python
  value_col = "Monthly Mean Total Sunspot Number"
  df_sunspots_clean[value_col] = pd.to_numeric(df_sunspots_clean[value_col], errors="coerce")
  nb_nan_val = df_sunspots_clean[value_col].isna().sum()
  if nb_nan_val > 0:
      raise RuntimeError(f"{nb_nan_val} valeur(s) non numérique(s) détectée(s)...")
  ```

- **Tri et réindexation** :
  ```python
  df_sunspots_clean = df_sunspots_clean.sort_values("Date").reset_index(drop=True)
  ```

- **Statistiques finales** :
  - Nombre de lignes : 3265
  - Nombre de colonnes : 2
  - Période temporelle : 1749-01-31 → 2021-01-31
  - Monthly Mean Total Sunspot Number : min=0.0, max=398.2, moyenne≈81.78

#### Décisions méthodologiques
- Toutes les décisions basées sur la structure réelle du CSV
- Gestion robuste des erreurs de conversion (dates invalides, valeurs non numériques)
- Tri chronologique pour assurer l'ordre temporel
- Conservation des zéros (valeurs physiques minima)

#### Fichiers de sortie
- Aucun fichier créé (DataFrame en mémoire)
- Métriques dans logs : `sunspots_clean_rows` avec statistiques détaillées

### Bloc 1.4 – Export d'un CSV Sunspots nettoyé (persistant)

#### Objectif
Créer un fichier CSV nettoyé persistant pour éviter la dépendance à l'état en mémoire.

#### Étapes détaillées

- **Vérification de l'existence de df_sunspots_clean** :
  ```python
  try:
      df_sunspots_clean
  except NameError:
      raise RuntimeError("df_sunspots_clean n'est pas défini...")
  ```

- **Création du dossier cible** :
  ```python
  DATA_PHASE2_CLEAN_DIR = PHASE2_ROOT / "data_phase2" / "sunspots_clean"
  DATA_PHASE2_CLEAN_DIR.mkdir(parents=True, exist_ok=True)
  SUNSPOTS_CLEAN_CSV_PATH = DATA_PHASE2_CLEAN_DIR / "Sunspots_clean.csv"
  ```

- **Écriture du CSV** :
  ```python
  df_sunspots_clean.to_csv(SUNSPOTS_CLEAN_CSV_PATH, index=False)
  ```

#### Caractéristiques du fichier généré
- Colonnes : Date, Monthly Mean Total Sunspot Number
- Format : CSV sans index
- Emplacement : `data_phase2/sunspots_clean/Sunspots_clean.csv`

#### Fichiers de sortie
- `data_phase2/sunspots_clean/Sunspots_clean.csv` : Données nettoyées persistantes
- Métriques dans logs : `sunspots_clean_csv_written`

### Bloc 1.5 – Source officielle des données Sunspots pour la Phase 2

#### Objectif
Établir le fichier officiel de référence pour tous les blocs suivants.

#### Étapes détaillées

- **Rechargement depuis disque** :
  ```python
  df_sunspots_clean = pd.read_csv(SUNSPOTS_CLEAN_CSV_PATH, parse_dates=["Date"])
  ```

- **Vérifications** :
  - Existence du fichier
  - Chargement avec parsing automatique des dates

#### Définition de la source officielle
- Fichier : `data_phase2/sunspots_clean/Sunspots_clean.csv`
- Colonnes : Date (datetime), Monthly Mean Total Sunspot Number (float)
- Dérivé du CSV brut mais nettoyé et validé
- Destiné au rechargement systématique pour éviter la dépendance RAM

#### Fichiers de sortie
- Aucun nouveau fichier (rechargement)
- Métriques dans logs : `sunspots_clean_reloaded_rows`

## Synthèse du Bloc 1 – Données & traçabilité

### Flux de données reproductible
1. **Source canonique** : `sunspots.zip` local (identique à Kaggle)
2. **Extraction contrôlée** : Inspection sans hypothèses, extraction des CSV uniquement
3. **Chargement et nettoyage** : Basé sur structure réelle, conversions robustes, tri chronologique
4. **Persistance** : Export CSV nettoyé pour référence officielle
5. **Rechargement** : Systématique depuis disque pour chaque bloc

### Statistiques finales des données
- **Période** : 1749-01-31 → 2021-01-31 (3265 points mensuels)
- **Variable principale** : Monthly Mean Total Sunspot Number
  - Min : 0.0
  - Max : 398.2
  - Moyenne : ≈81.78
- **Qualité** : Aucune valeur manquante, dates valides, zéros conservés

### Audit et traçabilité
- Toutes les étapes logguées dans `logs/runs/<RUN_ID>/run_log.txt`
- Métriques détaillées dans `logs/runs/<RUN_ID>/metrics.jsonl`
- Vérifications d'intégrité à chaque étape
- Pas de dépendance à l'environnement Phase 1

## Bloc 2 – Prétraitements & fenêtres (Introduction)

### Objectif général
Préparer la série temporelle pour les analyses (mesure de d, calcul de T_log, baselines) sans biais cachés.

### Principes méthodologiques
- **Raw-first** : Référence reste la série brute nettoyée
- **Explicite et motivé** : Tout prétraitement (lissage, normalisation, fenêtres) doit être justifié
- **Réversible** : Conservation des copies avant/après transformation

### Plan du Bloc 2
- **Bloc 2.0** : Construction série temporelle de base (Date comme index, vérifications ordre/doublons/fréquence)
- **Bloc 2.1** : Vérification valeurs manquantes/anomalies simples
- **Bloc 2.2** : Décisions prétraitements et construction fenêtres (taille W, recouvrement G)

### État actuel
Le fichier part_02.ipynb s'arrête à l'introduction du Bloc 2.0, indiquant que les blocs suivants (2.0 et au-delà) sont développés dans les parties ultérieures du notebook split.

## Aspects techniques clés de la Partie 2

### Dépendances Python
- **Core** : pandas, pathlib
- **Validation** : Vérifications d'existence, conversions types, gestion erreurs
- **Persistance** : CSV export/import avec parse_dates

### Gestion des données
- **Chargement robuste** : Gestion erreurs conversion datetime/numérique
- **Nettoyage basé sur réalité** : Décisions fondées sur structure CSV observée
- **Persistance stratégique** : Évite dépendance état mémoire

### Reproductibilité
- **Chemins relatifs** : Tout dans PHASE2_ROOT
- **Vérifications intégrité** : Existence fichiers, cohérence données
- **Logging systématique** : Chaque étape tracée

### Gestion d'erreurs
- **Exceptions explicites** : Messages détaillés pour diagnostic
- **Vérifications préalables** : Existence dossiers/fichiers avant accès
- **Gestion types** : Conversion sécurisée avec errors="coerce"

## Artefacts et logs générés

### Structure de dossiers complétée
```
SunspotPhase2Tlog/
├── data_phase2/
│   ├── sunspots_raw/
│   │   └── Sunspots.csv  # Archive fidèle du zip
│   └── sunspots_clean/
│       └── Sunspots_clean.csv  # Données officielles nettoyées
├── logs/runs/<RUN_ID>/
│   ├── run_log.txt
│   └── metrics.jsonl
```

### Métriques clés logguées
- `sunspots_csv_rows` : Dimensions et colonnes du CSV brut
- `sunspots_clean_rows` : Statistiques après nettoyage
- `sunspots_clean_csv_written` : Confirmation export
- `sunspots_clean_reloaded_rows` : Confirmation rechargement

## Prochaines étapes

La Partie 2 finalise la préparation des données et initie les prétraitements :
- **Partie 3** : Suite du Bloc 2 (construction série temporelle, vérifications anomalies, décisions fenêtres)
- **Transition** : Passage aux estimations de dimension (Bloc 3) avec données propres et traçables

Cette partie assure que toutes les analyses Phase 2 partent d'une base de données validée, nettoyée et persistante, éliminant les sources de variabilité liées au chargement ou au nettoyage des données.