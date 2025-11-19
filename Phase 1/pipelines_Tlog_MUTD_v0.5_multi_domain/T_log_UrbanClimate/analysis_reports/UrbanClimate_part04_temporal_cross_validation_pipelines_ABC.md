# UrbanClimate V0.1 – Partie 4 (cellules 30–39) : Cross‑validation temporelle (pipelines A/B/C)

## 1. Périmètre

Cette partie correspond aux cellules 30–39 de `UrbanClimate_part04.ipynb`.

Elle met en place une **cross‑validation temporelle par fenêtres glissantes** pour T_log, en utilisant les trois pipelines de prétraitement définis précédemment :

- Pipeline A : StandardScaler (méthode verrouillée de base).
- Pipeline B : winsorisation 1 % / 99 % puis StandardScaler.
- Pipeline C : projection robuste MinCovDet (fallback sur A si échec).

Objectif : vérifier si l’estimation de `d` et de `T_log` reste stable au cours du temps pour chaque pipeline, à différentes échelles temporelles.

---

## 2. Données et configuration

- Fichier source : `data/urban_climate.csv`.
- Colonnes requises :
  - temporelles : `year`, `month` ;
  - agrégation ville : `city`, `country`, `latitude`, `longitude` ;
  - features : liste issue de `results/params.json` (sinon fallback standard) :
    `temperature_celsius`, `humidity_percent`, `precipitation_mm`, `wind_speed_ms`, `urban_heat_island_intensity`.
- Construction d’un temps continu :
  - `ym = year + (month-1)/12`.

Les paramètres verrouillés (features, colonnes d’agrégation, bornes de clipping `d_clip_min`, `d_clip_max`) sont relus dans `params.json` pour rester cohérent avec les parties précédentes.

---

## 3. Fenêtres temporelles et agrégation

Deux types de fenêtres glissantes sont définis :

- `annual` :
  - largeur = 1 an ;
  - pas = 12 mois (fenêtres annuelles non chevauchantes en centre, mais définies via `ym`).
- `3yr` :
  - largeur = 3 ans ;
  - pas = 6 mois (fenêtres chevauchantes avec recouvrement).

Pour chaque fenêtre (définie par un centre `window_center`) :

1. Sélection des observations dont `ym` tombe dans l’intervalle [début, fin] de la fenêtre.
2. Construction de `city_key = city,country,lat,lon` ;
3. Agrégation par ville : moyenne des features sur la fenêtre ;
4. Rejet des fenêtres avec moins de 2 villes.

On obtient ainsi, par fenêtre, une matrice `villes × features` sur laquelle on applique les pipelines A/B/C.

---

## 4. Calcul de d et T_log par pipeline

Pour chaque fenêtre et chaque pipeline :

1. Construction de la matrice prétraitée `Xs` :
   - **A** : `Xs = StandardScaler(X_raw)`.
   - **B** : winsorisation 1 % / 99 % sur chaque feature, puis StandardScaler.
   - **C** : StandardScaler puis projection via les vecteurs propres de la covariance robuste MinCovDet (avec fallback sur A si MinCovDet échoue).
2. Calcul de la dimension effective :
   - `d_part` via participation ratio (valeurs propres de la covariance de `Xs`) ;
   - `d_pca90` via PCA (nombre de composantes pour 90 % de variance expliquée) ;
   - `d_est = (d_part + d_pca90) / 2`, puis clipping dans `[d_clip_min, d_clip_max]` ;
3. Calcul de `T_log` pour la fenêtre :

   \[
   T_{\log} = (d_{clip} - 4) \ln(n_{cities}), \quad n_{cities} = \text{nombre de villes dans la fenêtre}.
   \]

Les résultats détaillés sont sauvegardés dans :

- `results/temporal_cv/temporal_cv_annual.csv` ;
- `results/temporal_cv/temporal_cv_3yr.csv`.

Chaque ligne de ces fichiers contient : type de fenêtre, centre temporel, pipeline, n_villes, d_part, d_pca90, d_est, d_clipped, T_log.

---

## 5. Séries temporelles, heatmaps et stabilité du signe

Pour chaque type de fenêtre (`annual`, `3yr`) :

1. **Série temporelle T_log** :
   - plot `T_log` en fonction de `window_center` pour chaque pipeline (courbes A/B/C) ;
   - ajout d’une ligne de référence T_log = 0 ;
   - sauvegarde dans :
     - `results/temporal_cv/temporal_cv_annual_Tlog.png` ;
     - `results/temporal_cv/temporal_cv_3yr_Tlog.png`.

2. **Heatmap T_log** :
   - construction d’une matrice `pivot(window_center × pipeline)` avec valeurs T_log ;
   - visualisation par heatmap (`RdBu`, centré sur 0) ;
   - sauvegarde dans :
     - `results/temporal_cv/temporal_cv_annual_heatmap.png` ;
     - `results/temporal_cv/temporal_cv_3yr_heatmap.png`.

3. **Métrique de stabilité** :
   - pour chaque pipeline, calcul de la fraction de fenêtres dont le **signe** de T_log concorde avec le signe médian de T_log pour ce pipeline (cohérence temporelle du régime) ;
   - sauvegarde des tableaux :
     - `results/temporal_cv/temporal_cv_annual_stability.csv` ;
     - `results/temporal_cv/temporal_cv_3yr_stability.csv`.

Ces métriques permettent de voir, par pipeline, si le système reste dans le même régime (Divergence / Équilibre / Saturation) au fil du temps ou si des changements de signe apparaissent.

---

## 6. Rapport Markdown de cross‑validation temporelle

En fin de cellule, un rapport global est généré :

- `results/temporal_cv_report.md`.

Il contient, pour chaque type de fenêtre :

- les chemins des CSV détaillés (T_log par fenêtre) ;
- les chemins des courbes T_log et des heatmaps ;
- les chemins des CSV de stabilité ;
- des notes sur la configuration des fenêtres (largeur, pas) et le lien avec `results/params.json` pour les paramètres de pipeline.

Les logs (`logs/logs.csv`, `logs/summary.md`) sont mis à jour avec l’état de la cross‑validation.

---

## 7. Rôle de la Partie 4 dans UrbanClimate V0.1

Cette partie étend la validation UrbanClimate V0.1 en :

- testant la **stabilité temporelle** de la dimension effective et de T_log pour les trois pipelines A/B/C ;
- offrant une vue détaillée de T_log au cours du temps (séries + heatmaps) à deux échelles (annuelle et 3 ans glissants) ;
- quantifiant, via la métrique de stabilité du signe, dans quelle mesure chaque pipeline maintient le même régime sur la période d’étude.

Combinée aux Parties 1–3 :

- elle permet de vérifier si le régime global Divergence identifié (T_log < 0) pour UrbanClimate est **persistant dans le temps** ou s’il existe des fenêtres temporelles où le système se rapproche de l’équilibre ou de la saturation ;
- elle reste cohérente avec la méthode verrouillée (mêmes features, agrégation par ville, même définition de T_log) tout en testant plusieurs variantes de prétraitement robustes documentées.
