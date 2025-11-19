# Rapport détaillé sur la Partie 1 du Pipeline SunspotPhase2Tlog (Blocs 0 et 1)

## Vue d'ensemble

La Partie 1 du pipeline SunspotPhase2Tlog correspond aux blocs initiaux du notebook principal, couvrant l'infrastructure de base (Bloc 0) et la gestion des données (Bloc 1). Cette partie assure la mise en place d'un environnement reproductible et la préparation des données Sunspots pour les analyses ultérieures.

## Bloc 0 – Infrastructure Phase 2

### Objectif
Le Bloc 0 établit l'infrastructure de base du projet Phase 2, garantissant un environnement isolé, reproductible et traçable.

### Étapes détaillées

#### 0.0 – Installation des dépendances
- **Fonction** : `install_requirements(file_path="requirements.txt")`
- **Code clé** :
  ```python
  import subprocess
  import sys

  def install_requirements(file_path="requirements.txt"):
      """Installe les paquets listés dans requirements.txt."""
      print(f"Installation/Mise à jour des dépendances via {file_path}...")
      try:
          subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file_path])
          print("\n✅ Toutes les dépendances ont été installées ou mises à jour avec succès.")
      except subprocess.CalledProcessError as e:
          print(f"\n❌ ERREUR lors de l'installation des dépendances : {e}")
  ```
- **Dépendances principales** : pandas, numpy, scipy, scikit-learn, matplotlib, seaborn, pathlib, json, datetime, uuid, random
- **Gestion d'erreurs** : Capture des erreurs `subprocess.CalledProcessError` avec message explicite
- **Sortie** : Confirmation d'installation réussie ou message d'erreur

#### 0.1 – Racine, dossiers et manifeste de run
- **Définition de la racine** :
  ```python
  PHASE2_ROOT = Path().resolve()
  if PHASE2_ROOT.name != "SunspotPhase2Tlog":
      raise RuntimeError("Ce notebook doit être exécuté depuis le dossier 'SunspotPhase2Tlog'.")
  ```
- **Graine globale** :
  ```python
  GLOBAL_SEED = 42
  random.seed(GLOBAL_SEED)
  np.random.seed(GLOBAL_SEED)
  ```
- **Sous-dossiers créés** : logs/, logs/runs/, reports/, artifacts/, cache/, config/, data_phase2/
- **RUN_ID génération** :
  ```python
  timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
  short_uid = str(uuid.uuid4())[:8]
  RUN_ID = f"sunspots_phase2_{timestamp_str}_{short_uid}"
  ```
- **Manifeste JSON** :
  ```python
  manifest = {
      "run_id": RUN_ID,
      "created_at": datetime.now().isoformat(),
      "phase2_root": str(PHASE2_ROOT),
      "notebook_name": "SunspotPhase2Tlog.ipynb",
      "python_version": sys.version,
      "platform": platform.platform(),
      "global_seed": GLOBAL_SEED,
  }
  ```
- **Fichiers générés** : `logs/runs/<RUN_ID>/manifest.json`

#### 0.2 – Système de logging
- **Fonctions clés** :
  ```python
  def log_message(level, message, block=None):
      global LOG_STEP
      LOG_STEP += 1
      prefix = f"[STEP={LOG_STEP}][{level.upper()}]"
      if block is not None:
          prefix += f"[{block}]"
      line = f"{prefix} {message}"
      print(line)
      with open(LOG_TEXT_PATH, "a", encoding="utf-8") as f:
          f.write(line + "\n")

  def log_metric(name, value, step=None, extra=None):
      if step is None:
          step_val = LOG_STEP
      else:
          step_val = step
      record = {
          "run_id": RUN_ID,
          "step": step_val,
          "metric": name,
          "value": value,
      }
      if extra is not None:
          record["extra"] = extra
      with open(LOG_JSONL_PATH, "a", encoding="utf-8") as f:
          f.write(json.dumps(record, ensure_ascii=False) + "\n")
      print(f"[METRIC][{name}] = {value} (step={step_val})")
  ```
- **Fichiers générés** : `logs/runs/<RUN_ID>/run_log.txt`, `logs/runs/<RUN_ID>/metrics.jsonl`
- **Caractéristiques** : Sans horodatage pour reproductibilité, compteur d'étapes global

### Mesures de reproductibilité
- Graine globale (GLOBAL_SEED=42) pour random et numpy
- Vérification stricte du dossier racine
- Isolation des fichiers dans PHASE2_ROOT
- Logging déterministe sans timestamps

### Fichiers de sortie Bloc 0
- `logs/runs/<RUN_ID>/manifest.json` : Métadonnées du run
- `logs/runs/<RUN_ID>/run_log.txt` : Logs texte
- `logs/runs/<RUN_ID>/metrics.jsonl` : Métriques JSONL
- Sous-dossiers : logs/, reports/, artifacts/, cache/, config/, data_phase2/

## Bloc 1 – Données & traçabilité

### Objectif
Le Bloc 1 assure la détection, extraction et préparation initiale des données Sunspots, garantissant une traçabilité complète depuis le zip source.

### Étapes détaillées

#### 1.0 – Détection du zip source
- **Chemin relatif** : `SUNSPOTS_ZIP_PATH = PHASE2_ROOT / "sunspots.zip"`
- **Vérification d'existence** :
  ```python
  if not SUNSPOTS_ZIP_PATH.exists():
      raise FileNotFoundError(f"Le fichier sunspots.zip est introuvable à l'emplacement attendu : {SUNSPOTS_ZIP_PATH}.")
  ```
- **Logging** : Confirmation de présence avec métrique

#### 1.1 – Inspection et extraction
- **Inspection du contenu** :
  ```python
  with zipfile.ZipFile(SUNSPOTS_ZIP_PATH, "r") as zf:
      members = zf.namelist()
  csv_members = [m for m in members if m.lower().endswith(".csv")]
  ```
- **Extraction contrôlée** :
  ```python
  with zipfile.ZipFile(SUNSPOTS_ZIP_PATH, "r") as zf:
      for m in csv_members:
          target_path = DATA_PHASE2_RAW_DIR / m
          target_path.parent.mkdir(parents=True, exist_ok=True)
          with zf.open(m, "r") as src, open(target_path, "wb") as dst:
              dst.write(src.read())
  ```
- **Dossier cible** : `data_phase2/sunspots_raw/`
- **Fichiers générés** : Copie fidèle des CSV du zip (typiquement `Sunspots.csv`)

### Gestion d'erreurs et contraintes
- Aucun chemin absolu codé en dur
- Vérification d'existence des fichiers critiques
- Extraction uniquement des fichiers .csv
- Conservation de la structure interne du zip
- Logging détaillé de chaque étape

### Fichiers de sortie Bloc 1
- `data_phase2/sunspots_raw/Sunspots.csv` : Données brutes extraites
- Métriques dans logs : Présence du zip, nombre de CSV extraits

## Aspects techniques clés

### Dépendances Python
- **Core** : pandas, numpy, pathlib
- **Système** : subprocess, sys, json, datetime, uuid, random, platform
- **Archives** : zipfile
- **Logging** : json (pour JSONL)

### Gestion des chemins
- Utilisation exclusive de `pathlib.Path` pour la portabilité
- Chemins relatifs à `PHASE2_ROOT`
- Vérifications d'existence avant accès aux fichiers

### Reproductibilité
- Graine globale pour tous les générateurs aléatoires
- RUN_ID unique basé sur timestamp + UUID
- Logging sans horodatage
- Manifeste complet avec version Python et plateforme

### Gestion d'erreurs
- Exceptions explicites avec messages détaillés
- Vérifications de cohérence (dossier racine, existence de fichiers)
- Capture d'erreurs lors de l'installation des dépendances

## Artefacts et logs générés

### Structure de dossiers créée
```
SunspotPhase2Tlog/
├── logs/
│   └── runs/
│       └── <RUN_ID>/
│           ├── manifest.json
│           ├── run_log.txt
│           └── metrics.jsonl
├── reports/
├── artifacts/
├── cache/
├── config/
└── data_phase2/
    └── sunspots_raw/
        └── Sunspots.csv
```

### Exemple de contenu manifest.json
```json
{
  "run_id": "sunspots_phase2_20251117_105209_c8283a4a",
  "created_at": "2025-11-17T15:52:09.123456",
  "phase2_root": "C:\\Users\\zackd\\OneDrive\\Desktop\\Phase2_Tlog_v0.5\\SunspotPhase2Tlog",
  "notebook_name": "SunspotPhase2Tlog.ipynb",
  "python_version": "3.9.7",
  "platform": "Windows-10-10.0.19041-SP0",
  "global_seed": 42
}
```

## Prochaines étapes

La Partie 1 établit les fondations pour les analyses ultérieures :
- **Partie 2** : Prétraitements et fenêtres (Bloc 2) – Construction de séries temporelles, normalisation, définition des fenêtres
- **Transition** : Les données nettoyées et l'infrastructure de logging permettent de passer aux estimations de dimension (Blocs 3-4)

Cette partie garantit que le pipeline est exécutable sur n'importe quelle machine respectant la structure de dossiers, avec une traçabilité complète de chaque étape.