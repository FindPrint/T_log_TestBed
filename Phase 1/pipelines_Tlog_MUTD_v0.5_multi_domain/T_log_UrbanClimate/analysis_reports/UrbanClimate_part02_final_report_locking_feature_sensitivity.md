# UrbanClimate V0.1 – Partie 2 (cellules 10–19)

## 1. Périmètre

Cette partie correspond aux cellules 10–19 de `UrbanClimate_part02.ipynb` et traite :

- du **nettoyage** des résultats (NaN/Inf + clipping sur d) ;
- de la génération d’un **rapport final V0.1** (`results/final_report.md`) ;
- du **verrouillage de la méthode** d’estimation de d (`params.json`, `README_method.md`) ;
- d’un test de **sensibilité aux features** (ablation drop‑one‑feature).

---

## 2. Bloc 5 – Nettoyage et rapport final

- Chargement des sorties de la Partie 1 :
  - `tlog_d_estimates.csv` (résumé global n, d, T_log, régime) ;
  - `tlog_leave_one_out.csv` (LOO par ville) ;
  - `tlog_sweep_summary.csv` + `tlog_sweep_fraction_summary.csv` (balayage n/d).
- Fonction `sanitize_df` :
  - détecte NaN/Inf ;
  - remplace Inf par NaN ;
  - impute les NaN numériques par la **médiane** (ou 0 si nécessaire) ;
  - logue un WARNING si correction.
- Clipping de `d_estimate` dans `[0.1, 100]` ; recalcul de `T_log` via
  `(d-4)*ln(n_eff)` avec `n_eff = max(2, n_used)`.
- Sauvegarde des versions nettoyées :
  - `tlog_d_estimates_sanitized.csv` ;
  - `tlog_leave_one_out_sanitized.csv` ;
  - `tlog_sweep_summary_sanitized.csv`.
- Construction du **rapport final** `results/final_report.md` :
  - résumé chiffré (n_cities, d_participation, d_pca90, d estimate, T_log recalculé, régime) ;
  - statistiques LOO (mean, std, rel_std, p‑value re‑lue depuis les logs) ;
  - table du sweep (fractions 0.5/0.75/1.0) ;
  - liste des fichiers produits (CSVs + PNGs) ;
  - 3 recommandations courtes pour V0.1 (documenter méthode, ajouter CV temporelle/sensibilité aux features, exposer cutoffs).

**Résultat clé** :

- après sanitization, on obtient toujours :
  - `n ≈ 20`, `d ≈ 3.9003`, `T_log ≈ −0.2988` → **régime Divergence**.

---

## 3. Verrouillage de la méthode d’estimation de d

Une cellule dédiée crée :

- `results/params.json` : dictionnaire de paramètres verrouillés :
  - seed ;
  - groupe d’agrégation (`city,country,latitude,longitude`) ;
  - liste exacte des features : température, humidité, précipitation, vent, UHI ;
  - prétraitement : `StandardScaler` ;
  - règle de fusion d_participation / d_pca90 ;
  - définition de T_log et règles de sanitization.
- `results/README_method.md` : description textuelle de la méthode (agrégation, PCA, participation ratio, T_log, cutoffs).

Puis, la cellule **ré‑exécute** l’estimation de d selon cette méthode verrouillée :

- agrégation par ville ;
- standardisation des features ;
- calcul du spectre de covariance, d_participation, d_pca90 ;
- fusion en `d_estimate` + clipping ;
- calcul de `T_log = (d-4)*ln(n_eff)` ;
- sauvegarde dans `tlog_d_estimates_locked.csv` et `d_spectrum_locked.png`.

Résultat verrouillé (repris dans la console et les logs) :

- `n_cities = 20` ;
- `d_participation ≈ 3.8005` ;
- `d_pca90 = 4` ;
- `d_estimate ≈ 3.90025` ;
- `T_log ≈ −0.2988` → **Divergence**.

Cela confirme que la méthode documentée reproduit exactement le diagnostic initial.

---

## 4. Sensibilité aux features (drop‑one‑feature)

Un bloc de sensibilité charge `params.json` et réalise :

- agrégation par ville avec **toutes** les features définies ;
- calcul d’un baseline `(d_full, T_full)` ;
- boucle "drop‑one" : pour chaque feature retirée à son tour, recalcul de d et T_log.

Les résultats sont sauvegardés dans :

- `results/sensitivity_feature_drop.csv` ;
- `results/sensitivity_feature_drop.png` (barplot des T_log avec baseline en ligne pointillée).

Tableau résumé (valeurs indiquées dans la sortie) :

- baseline (aucune feature retirée) : `d≈3.90`, `T_log≈−0.30`. 
- suppression `temperature_celsius` ou `precipitation_mm` :
  - d_est légèrement modifié (~3.85–3.88), T_log ≈ −0.37 à −0.43 (divergence un peu plus forte, mais changement modéré).
- suppression `humidity_percent`, `wind_speed_ms`, `urban_heat_island_intensity` :
  - d_part et d_pca90 chutent, d_est ≈ 3, T_log ≈ −3 → régime de Divergence **fortement accentué**.

Interprétation :

- les features **humidity_percent**, **wind_speed_ms** et **urban_heat_island_intensity** portent une part majeure de la structure de dimension effective ;
- leur retrait abaisse d ≈ 3 (plus loin de 4), ce qui renforce le caractère divergent ;
- à l’inverse, température et précipitations ont un impact plus marginal sur d et T_log dans ce dataset.

---

## 5. Message global de la Partie 2

Cette partie :

- **stabilise** la version UrbanClimate V0.1 en nettoyant les résultats et en produisant un `final_report.md` cohérent ;
- **verrouille** la méthode d’estimation de d dans des artefacts explicites (README + JSON), garantissant la reproductibilité du diagnostic `d≈3.90, T_log<0` ;
- montre que la conclusion en Divergence est **robuste**, mais fortement dépendante de quelques features clés (humidité, vent, UHI), ce qui signale à la fois leur importance et un risque méthodologique si ces variables sont mal mesurées ou absentes.

Les parties suivantes pourront s’appuyer sur ce socle (méthode verrouillée + sensibilité aux features) pour explorer des ajustements (biais, autre granularité, mémoire, cross‑validation) de manière contrôlée.
