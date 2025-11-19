# Sunspots V0.5 – Partie 1 (cellules 0–9) : Préparation, données et premier T_log

## 1. Périmètre de la partie

Cette première partie correspond aux **10 premières cellules** du notebook `Sunspots_part01.ipynb` (split fixe 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle couvre trois blocs logiques enchaînés :

- **Block 1 — Preparation** (environnement, seeds, structure de projet, logger) ;
- **Block 2 — Data Acquisition** (authentification Kaggle et téléchargement de Sunspots) ;
- **Block 3 — Calculating T_log** (définition de `n` et `d`, calcul et diagnostic initial de `T_log`).

En pratique, cette "Partie 1" est donc une **phase d’initialisation complète** : mise en place de l’infrastructure + arrivée de la donnée + premier diagnostic T_log.

---

## 2. Installation des dépendances (requirements.txt)

Une première cellule exécute une fonction utilitaire :

- **`install_requirements("requirements.txt")`** qui appelle `pip` via `subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file_path])`.

Comportement :

- si tout se passe bien :
  - affichage d’un message signalant que **toutes les dépendances sont installées ou mises à jour** ;
  - recommandation de **redémarrer le kernel** lors de la première exécution ;
- en cas d’erreur `CalledProcessError` :
  - un message ❌ est imprimé avec le détail de l’exception.

Cette étape garantit que l’environnement Python dispose des librairies nécessaires (numpy, pandas, matplotlib, statsmodels, scikit‑learn, etc.), ce qui est crucial pour les blocs suivants (régressions, bootstrap, graphes).

---

## 3. Préparation de l’environnement (Block 1 — Preparation)

La cellule suivante met en place l’ossature standard du pipeline :

### 3.1 Imports et reproductibilité

- **Imports principaux** : `os`, `sys`, `csv`, `random`, `time`, `shutil`, `logging`, `datetime`, `numpy`, `pandas`, `matplotlib`, `scipy.sparse`.
- Fixation des **seeds** :
  - `random.seed(42)` ;
  - `np.random.seed(42)`.

Ces choix assurent la **reproductibilité** des tirages aléatoires (bootstrap, graphes k‑NN, etc.).

### 3.2 Structure de dossiers

Création de trois dossiers racine :

- `data/` ;
- `results/` ;
- `logs/`.

avec `os.makedirs(..., exist_ok=True)` pour éviter les erreurs si les dossiers existent déjà.

Un nettoyage conditionnel est prévu pour l’environnement Colab (`/content/sample_data`), sans impact sur un environnement local classique.

### 3.3 Logger CSV et résumé Markdown

Le pipeline pose une double journalisation :

- **`logs/logs.csv`** :
  - créé si absent, avec en‑tête `timestamp, level, message` ;
  - destiné à une analyse structurée des événements.
- **`logs/summary.md`** :
  - créé si absent ;
  - contient un titre `# Journal de session T_log V0.1` ;
  - enregistre la ligne `Session démarrée: <UTC>` (via `datetime.utcnow().isoformat() + "Z"`) ;
  - rappelle les conventions (biais=0, seeds=42, sorties dans `results/`).

Un **logger Python** est configuré sur la console (`logging.basicConfig(...)`) pour afficher les messages INFO/WARNING/ERROR.

### 3.4 Fonction utilitaire `log_event`

La fonction :

```python
def log_event(level: str, message: str):
    ts = datetime.utcnow().isoformat() + "Z"
    # append à logs.csv + summary.md + logging
```

- écrit une ligne dans `logs/logs.csv` (timestamp, niveau, message) ;
- ajoute une entrée dans `logs/summary.md` (`- <ts> [LEVEL] message`) ;
- imprime le message via `logging`.

Elle est utilisée pour :

- signaler que **Block 1 est prêt** (imports, seeds, dossiers, logger) ;
- logguer la sauvegarde du plot de vérification (voir §3.6).

### 3.5 Résumé de l’état

La cellule imprime ensuite un petit diagnostic :

- liste des dossiers présents (`data, results, logs`) avec leurs chemins absolus ;
- présence de `logs/logs.csv` et `logs/summary.md` ;
- sauvegarde d’un fichier de configuration `results/session_config.txt` contenant :
  - titre "T_log V0.1 — Session de tests" ;
  - timestamp UTC de début ;
  - seeds utilisées ;
  - conventions.

### 3.6 Plot de vérification de l’environnement graphique

Enfin, un **plot simple** est généré :

- `y = ln(x)` pour `x ∈ [1,10]` ;
- figure sauvegardée en `results/env_check_plot.png` et affichée dans le notebook ;
- loggée via `log_event`.

Ce plot n’a pas de valeur scientifique en soi, mais valide que l’environnement graphique fonctionne correctement.

#### Remarque sur `datetime.utcnow()`

Des warnings `DeprecationWarning` remontent (Python moderne préfère `datetime.now(datetime.UTC)`), mais ils sont **sans impact fonctionnel**. Ils pourront être corrigés plus tard dans une passe de nettoyage, sans changer la logique scientifique.

---

## 4. Acquisition des données Sunspots (Block 2)

Dans cette même tranche de 10 cellules, le **Block 2 — Data Acquisition** est déjà présent :

- import de `kaggle`, `json`, `zipfile` ;
- définition de `find_kaggle_config()` qui cherche `kaggle.json` dans :
  - `~/.kaggle/kaggle.json` (chemin standard) ;
  - `./kaggle.json` (répertoire courant) ;
- chargement du JSON pour récupérer `username` et `key`, puis
  - configuration de `os.environ['KAGGLE_USERNAME']` et `os.environ['KAGGLE_KEY']` ;
  - authentification via `kaggle.api.authenticate()`.

Ensuite, la cellule :

- télécharge les fichiers du dataset `robervalt/sunspots` dans `data/` sans unzip automatique ;
- détecte le fichier ZIP (ex. `data/sunspots.zip`) ;
- décompresse ce ZIP dans `data/sunspots_raw/` ;
- liste les fichiers extraits.

Résultat important :

- le fichier clé `data/sunspots_raw/Sunspots.csv` est identifié comme **source principale** du pipeline Sunspots.

Ce bloc loggue également (via une fonction `log_event` locale ou des prints) le chemin du ZIP téléchargé et celui du dossier d’extraction.

---

## 5. Premier calcul de T_log et contrôle qualité (Block 3)

Toujours dans ces 10 premières cellules, on trouve :

### 5.1 Définition de n et d

À partir de `Sunspots.csv` :

- chargement dans `df` puis `df = df.dropna()` ;
- définition de **`n`** = nombre de lignes du DataFrame nettoyé = **3265** ;
- définition de **`d`** = 1, car il s’agit d’une **série temporelle unidimensionnelle** (seulement le temps).

### 5.2 Calcul de T_log

La formule utilisée est :

\[
T_{\log}(n,d) = (d - 4) \cdot \ln(n), \quad \text{avec biais = 0.}
\]

Avec `n = 3265` et `d = 1` :

- `T_log ≈ (1−4)·ln(3265) ≈ -24.2730`.

Une classification de régime est appliquée :

- `T_log > 0` → **Saturation (stabilité)** ;
- `T_log ≈ 0` (|T_log| < 1e-2) → **Équilibre (criticité)** ;
- `T_log < 0` → **Divergence (instabilité)**.

Ici, `T_log ≪ 0` ⇒ **régime Divergence (instabilité)**.

Le résultat est imprimé et loggué via `log_event` (niveau INFO).

### 5.3 Contrôle qualité des données Sunspots

Une cellule supplémentaire vérifie la qualité de `Sunspots.csv` :

- rechargement brut dans `df_raw` ;
- `df_raw.head()` pour visualiser les premières lignes :
  - colonne d’index `Unnamed: 0` ;
  - `Date` (fin de mois) ;
  - `Monthly Mean Total Sunspot Number` (valeur numérique) ;
- comptage des NaN par colonne (`df_raw.isna().sum()`) ;
- comptage de lignes entièrement vides (`df_raw.isna().all(axis=1).sum()`) ;
- comparaison `n_initial = len(df_raw)` vs `n_clean = len(df_raw.dropna())`.

Résultat :

- aucune valeur manquante dans les colonnes ;
- aucune ligne vide ;
- `n_initial = 3265`, `n_clean = 3265` ⇒ **aucune ligne supprimée**.

Ce contrôle confirme que le calcul de `T_log` ne souffre pas d’artefacts de données manquantes.

---

## 6. Rôle global de cette première partie (cellules 0–9)

Sur les 10 premières cellules, le pipeline Sunspots V0.5 :

- **installe et vérifie** l’environnement logiciel (`requirements.txt`, plot de test) ;
- **met en place** une infrastructure de projet reproductible (dossiers `data/results/logs`, seeds fixées, logs CSV + Markdown) ;
- **acquiert la donnée réelle** via l’API Kaggle et isole `Sunspots.csv` dans `data/sunspots_raw/` ;
- **applique pour la première fois la formule T_log** au dataset Sunspots, avec `(n=3265, d=1)` ;
- conclut, pour ce choix minimal de dimension, à un régime **Divergence (instabilité)** ;
- **vérifie la propreté** des données (aucun NaN), ce qui donne confiance dans ce diagnostic initial.

Cette première partie joue donc à la fois :

- le rôle d’**environnement technique** ;
- le rôle de **premier point de repère théorique** dans la carte \((n,d) \mapsto T_{\log}\) pour le domaine Sunspots.

Les parties suivantes raffineront ensuite :

- la dépendance à la dimension `d` (sensibilité T_log(d)),
- la dépendance à la taille `n`,
- puis la dimension effective estimée via graphes et spectre du Laplacien.
