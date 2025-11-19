# Rapport détaillé sur la Partie 3 du Pipeline SunspotPhase2Tlog (Bloc 2 Complet et Introduction Bloc 3)

## Vue d'ensemble

La Partie 3 du pipeline SunspotPhase2Tlog complète le Bloc 2 (Prétraitements & fenêtres) et initie le Bloc 3 (Estimation de la dimension effective `d`). Cette partie finalise la préparation méthodologique des données et pose les bases pour les estimations dimensionnelles multi-méthodes.

## Bloc 2 – Prétraitements & fenêtres (Complet)

### Bloc 2.0 – Construction d'une série temporelle de base

#### Objectif
Créer un objet série temporelle pandas avec Date comme index temporel, sans transformation du signal.

#### Étapes détaillées

- **Vérification de df_sunspots_clean** :
  ```python
  try:
      df_sunspots_clean
  except NameError:
      raise RuntimeError("df_sunspots_clean n'est pas défini...")
  ```

- **Création de df_ts** :
  ```python
  df_ts = df_sunspots_clean.copy()
  df_ts = df_ts.sort_values("Date").set_index("Date")
  ```

- **Diagnostics temporels** :
  ```python
  is_monotonic = df_ts.index.is_monotonic_increasing
  n_duplicates = int(df_ts.index.duplicated().sum())
  freq = pd.infer_freq(df_ts.index)
  ```

#### Résultats
- Nombre de points : 3265
- Index monotone croissant : True
- Nombre de dates dupliquées : 0
- Fréquence inférée : 'ME' (MonthEnd)

#### Fichiers de sortie
- Objet df_ts en mémoire
- Métriques dans logs : `sunspots_timeseries_length`

### Bloc 2.1 – Vérification des valeurs manquantes et anomalies simples

#### Objectif
Confirmer que la série brute est exploitable sans prétraitements globaux.

#### Comptages détaillés
```python
n_total = len(series)
n_nan = int(series.isna().sum())
n_inf = int(np.isinf(series).sum())
n_neg = int((series < 0).sum())
n_zero = int((series == 0).sum())
val_min = float(series.min())
val_max = float(series.max())
val_mean = float(series.mean())
```

#### Résultats
- Nombre total de points : 3265
- Nombre de NaN : 0
- Nombre de +/-inf : 0
- Nombre de valeurs < 0 : 0
- Nombre de valeurs = 0 : 67
- min : 0.0
- max : 398.2
- moyenne : 81.78

#### Décisions méthodologiques
- Zéros conservés (minima physiques des cycles solaires)
- Pas de suppression/modification globale
- Série brute exploitable telle quelle

#### Fichiers de sortie
- Métriques dans logs : `sunspots_value_checks`

### Bloc 2.2 – Décisions initiales de prétraitement

#### Décisions méthodologiques clés

1. **Pas de suppression des zéros** :
   - 67 valeurs à 0.0 interprétées comme minima d'activité solaire
   - Conservées telles quelles dans la série

2. **Pas de lissage ni filtrage global** :
   - Aucun lissage (moyennes mobiles, filtres) appliqué
   - Série de référence : df_ts / Sunspots_clean.csv

3. **Pas de normalisation globale imposée** :
   - Normalisation locale possible dans chaque méthode si nécessaire
   - Fichier de base demeure non normalisé

4. **Série de référence Phase 2** :
   - Sunspots_clean.csv (Date, Monthly Mean Total Sunspot Number)
   - Utilisée pour fenêtres, estimation d, calcul de T_log

#### Plan des séries
- **S0 – Série brute nettoyée (référence)** : Sunspots_clean.csv
- **S1 – Série normalisée (z-score)** : À construire dans Bloc 2.3

### Bloc 2.3 – Construction et sauvegarde de la série normalisée (S1, z-score)

#### Objectif
Créer une version z-score de la série pour tester la robustesse aux changements d'échelle.

#### Calcul du z-score
```python
mean_val = df_sunspots_clean[value_col].mean()
std_val = df_sunspots_clean[value_col].std()
df_sunspots_z = df_sunspots_clean.copy()
df_sunspots_z[value_col] = (df_sunspots_z[value_col] - mean_val) / std_val
```

#### Statistiques de normalisation
- Moyenne brute : 81.78
- Écart-type : 67.89

#### Fichier généré
- `data_phase2/sunspots_clean/Sunspots_clean_zscore.csv`
- Colonnes : Date, Monthly Mean Total Sunspot Number (normalisé)

#### Fichiers de sortie
- `Sunspots_clean_zscore.csv`
- Métriques dans logs : `sunspots_zscore_created`

### Bloc 2.4 – Construction et traçabilité des fenêtres temporelles (W, G)

#### Paramètres de fenêtres

- **Tailles de fenêtres (W en mois)** : [60, 132, 264]
  - W60 : 5 ans
  - W132 : ≈11 ans (cycle solaire typique)
  - W264 : ≈22 ans (deux cycles)

- **Pas de glissement (G en mois)** : [1, 6, 12]
  - G1 : 1 mois (suivi fin)
  - G6 : 6 mois (intermédiaire)
  - G12 : 12 mois (grossier, proche annuel)

#### Construction des fenêtres
```python
for W in window_sizes:
    for G in strides:
        start_indices = range(0, max(0, n - W + 1), G)
        for start_idx in start_indices:
            end_idx = start_idx + W - 1
            # ... création record fenêtre
```

#### Nombre de fenêtres par combinaison
- W60 : 3206 (G1), 535 (G6), 268 (G12)
- W132 : 3134 (G1), 523 (G6), 262 (G12)
- W264 : 3002 (G1), 501 (G6), 251 (G12)
- **Total** : 11 682 fenêtres

#### Fichier de définitions
- `data_phase2/windows/window_definitions.csv`
- Colonnes : window_id, window_size_months, stride_months, start_index, end_index, start_date, end_date, n_points

#### Fichiers de sortie
- `window_definitions.csv`
- Métriques dans logs : `windows_defined_count`

## Synthèse du Bloc 2 – Prétraitements, séries dérivées et fenêtres

### Séries disponibles
- **S0 (brute)** : Référence physique, Sunspots_clean.csv
- **S1 (z-score)** : Test de robustesse à l'échelle, Sunspots_clean_zscore.csv

### Propriétés de la série
- 3265 points mensuels (ME)
- Index temporel strictement croissant
- Aucune valeur manquante/infinie/négative
- 67 zéros conservés (minima solaires)

### Fenêtres temporelles
- 3 tailles W × 3 pas G = 9 combinaisons
- 11 682 fenêtres totales
- Traçabilité complète via window_definitions.csv

### Décisions méthodologiques
- Raw-first : référence reste la série brute
- Explicite et motivé : tout prétraitement justifié
- Réversible : conservation des copies avant/après
- Traçabilité : logs détaillés de chaque choix

## Bloc 3 – Estimation de la dimension effective `d` (Introduction)

### Objectif général
Estimer `d` + incertitude en utilisant plusieurs méthodes complémentaires sur les fenêtres définies.

### Méthodes candidates

#### M1 – Dimension Levina-Bickel (k-NN)
- Estimation dimension intrinsèque via distances k-plus-proches-voisins
- Points critiques : choix plage k, stabilité, sensibilité au bruit

#### M2 – Dimension Participation Ratio / PCA
- Valeurs propres de la matrice de covariance
- Dimension effective par ratio de participation
- Points critiques : normalisation S0/S1, seuil variance

#### M3 – Dimension spectrale (pente du spectre)
- Estimation slope à partir spectre de puissance (log-log)
- Points critiques : bande fréquentielle, lissage spectral

### Stratégie sur les fenêtres : calibration puis application complète

#### Étape 1 – Sous-échantillon de calibration
- Sélection contrôlée de fenêtres (dizaines par couple W,G)
- Exploration comportement méthodes
- Choix hyperparamètres (k, bandes, seuils)
- Détection pathologies (instabilité, aberrantes)

#### Étape 2 – Application complète
- Méthodes avec paramètres fixés sur toutes fenêtres pertinentes
- Stockage résultats dans fichiers dédiés :
  - `d_levina_bickel.csv`
  - `d_participation_ratio.csv`
  - `d_spectral.csv`
- Structure : window_id, d estimé, incertitudes, flags qualité

### Rappel méthodologique
- Distribution de d (pas valeur unique)
- Indicateurs fiabilité par estimation
- Comparaisons S0/S1 pour détecter artefacts échelle
- Impact W/G analysé explicitement

### Infrastructure commune
- Loader de fenêtres depuis window_definitions.csv
- Sélection sous-échantillons calibration
- Implémentation M1 en premier sur sous-ensemble

## Aspects techniques clés de la Partie 3

### Dépendances Python
- **Core** : pandas, numpy
- **Temporel** : datetime, index pandas
- **Système** : pathlib, vérifications existence

### Gestion des séries
- **S0/S1** : Versions brute/normalisée sauvegardées séparément
- **df_ts** : Objet série temporelle avec index Date
- **Vérifications** : Intégrité temporelle, absence anomalies

### Construction fenêtres
- **Paramétrique** : W et G configurables
- **Traçable** : Chaque fenêtre identifiée par window_id
- **Métadonnées** : start/end dates et indices

### Reproductibilité
- **Graine globale** : Pour tout aléatoire futur
- **Chemins relatifs** : Tout dans PHASE2_ROOT
- **Logs détaillés** : Chaque étape tracée

### Gestion d'erreurs
- **Vérifications préalables** : Existence objets/dossiers
- **Exceptions explicites** : Messages diagnostics
- **Sécurité** : Bounds checking fenêtres

## Artefacts et logs générés

### Structure de dossiers complétée
```
SunspotPhase2Tlog/
├── data_phase2/
│   ├── sunspots_clean/
│   │   ├── Sunspots_clean.csv          # S0 brute
│   │   └── Sunspots_clean_zscore.csv   # S1 normalisée
│   └── windows/
│       └── window_definitions.csv      # 11,682 fenêtres
├── logs/runs/<RUN_ID>/
│   ├── run_log.txt
│   └── metrics.jsonl
```

### Métriques clés logguées
- `sunspots_timeseries_length` : Longueur série de base
- `sunspots_value_checks` : Comptages valeurs (NaN, inf, neg, zeros)
- `sunspots_zscore_created` : Confirmation S1
- `windows_defined_count` : Nombre total fenêtres

## Prochaines étapes

La Partie 3 finalise la préparation des données et initie les estimations dimensionnelles :
- **Partie 4** : Implémentation méthodes d'estimation d (M1, M2, M3) sur sous-échantillon calibration
- **Transition** : Calibration hyperparamètres puis application complète sur toutes fenêtres
- **Objectif** : Distributions robustes de d avec incertitudes, sensibilité analysée

Cette partie établit une base méthodologique rigoureuse pour les estimations de dimension, avec traçabilité complète des choix de prétraitement et fenêtrage, évitant les problèmes de sensibilité observés en Phase 1.