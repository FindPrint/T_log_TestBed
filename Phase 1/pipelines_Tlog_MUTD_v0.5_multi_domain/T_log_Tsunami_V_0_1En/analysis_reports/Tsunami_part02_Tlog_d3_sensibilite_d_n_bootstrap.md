# Tsunami V0.1 – Partie 2 (cellules 8–15) : T_log pour n=782, sensibilité en d et n, bootstrap

## 1. Périmètre de la partie

Cette deuxième partie correspond aux cellules **8–15** du notebook `Tsunami_part02.ipynb`, dérivé de `T_log_Tsunami_V_0_1En.ipynb`.

Elle réalise les **premiers calculs explicites de T_log** pour le dataset `earthquake_data_tsunami.csv` (782 événements) :

- calcul de `T_log(n=782, d=3)` ;
- balayage de `T_log(n=782, d)` pour d = 2,3,4,5 (visualisation de la transition Divergence/Équilibre/Saturation) ;
- **stress test** en fonction de n pour d=3 ;
- **bootstrap** sur n=782 et d=3 (variabilité statistique de T_log).

---

## 2. Bloc 3 – Calcul de T_log pour le dataset Earthquake–Tsunami (n=782, d=3)

### 2.1 Paramètres et formule

La cellule "Bloc 3" fixe :

- `n = 782` (nombre d’événements sismiques/tsunami dans `earthquake_data_tsunami.csv`) ;
- `d = 3` (dimension effective choisie comme dimension spatiale : latitude, longitude, profondeur) ;
- `biais = 0`.

T_log est calculé par :

\[
T_{\log}(n,d) = (d - 4) \ln(n) + \text{biais}.
\]

### 2.2 Résultats

Avec n=782, d=3 :

\[
T_{\log}(782,3) = (3-4) \ln(782) = -\ln(782) \approx -6.6619.
\]

Classification :

- `T_log = -6.6619` → régime **Divergence (instabilité)**.

La cellule :

- affiche `n`, `d`, `T_log` et le régime ;
- logge l’événement dans `logs/logs.csv` et `logs/logs.txt` via `log_to_csv`/`logger.info`.

Interprétation :

- avec d=3 (<4), le facteur `(d-4)` est négatif ;
- à n=782, `ln(n)` est déjà substantiel → T_log est nettement < 0 ;
- le système Tsunami (dans cette approximation spatiale) est en **régime de Divergence**.

---

## 3. Bloc 4 – Classification et visualisation de T_log en fonction de d (2 → 5)

### 3.1 Méthode

Le Bloc 4 examine comment T_log varie avec d pour n fixé (782) :

- paramètres :
  - `n = 782` ;
  - `biais = 0` ;
  - `d_values = [2, 3, 4, 5]`.

Pour chaque d dans {2,3,4,5}, on calcule :

\[
T_{\log}(782,d) = (d-4) \ln(782).
\]

Un DataFrame `df_results` est construit avec colonnes : `d`, `T_log`, `Régime` (Divergence, Équilibre, Saturation).

### 3.2 Résultats

Tableau récapitulatif (issu de l’exécution) :

| d | T_log     | Régime      |
|---|-----------|------------|
| 2 | −13.3237  | Divergence |
| 3 | −6.6619   | Divergence |
| 4 | 0.0000    | Équilibre  |
| 5 | +6.6619   | Saturation |

Une figure `results/tlog_vs_d.png` est générée :

- T_log(d) (points/ligne) ;
- ligne horizontale à 0 pour marquer T_log=0 ;
- légende signalant la criticité.

Interprétation :

- on retrouve le schéma classique :
  - d < 4 → T_log < 0 → **Divergence** ;
  - d = 4 → T_log = 0 → **Équilibre** (point critique) ;
  - d > 4 → T_log > 0 → **Saturation** ;
- la dimension **critique d_c = 4** est donc explicitement confirmée pour ce système Tsunami, de la même manière que dans les pipelines Sunspots et PM2.5.

---

## 4. Bloc 5.1 – Stress test sur n (T_log vs n à d = 3)

### 4.1 Méthode

Le bloc 5.1 explore la sensibilité de T_log à la **taille du système n** à dimension fixée `d = 3`.

- paramètres :
  - `d = 3`, `biais = 0` ;
  - `n_values = [100, 200, 300, 400, 500, 600, 700]` (pas de 100 jusqu’à ~782) ;

Pour chaque n :

\[
T_{\log}(n,3) = (3-4) \ln(n) = -\ln(n).
\]

La cellule construit un DataFrame `df_stress_n` avec `n`, `T_log`, `Régime`, et produit un plot `results/tlog_vs_n.png` :

- T_log vs n ;
- ligne horizontale T_log=0 ;
- annotation du régime (toujours Divergence ici) sur chaque point.

### 4.2 Résultats

Tableau (extrait) :

| n   | T_log    | Régime      |
|-----|----------|------------|
| 100 | −4.6052  | Divergence |
| 200 | −5.2983  | Divergence |
| 300 | −5.7038  | Divergence |
| 400 | −5.9915  | Divergence |
| 500 | −6.2146  | Divergence |
| 600 | −6.3969  | Divergence |
| 700 | −6.5511  | Divergence |

Interprétation (telle que notée dans la cellule texte) :

- pour d=3, T_log est **toujours négatif**, quel que soit n dans la plage testée ;
- T_log devient **de plus en plus négatif** lorsque n augmente, conformément à :

\[
T_{\log}(n) = -\ln(n).
\]

- cela illustre le principe V0.1 : à dimension < 4, augmenter la taille du système **amplifie la divergence** ;
- la classification de régime (Divergence) est donc **robuste** aux variations raisonnables de n.

---

## 5. Bloc 5.2 – Bootstrap sur n=782, d=3

### 5.1 Méthode

Ce bloc effectue un **bootstrap classique** sur les lignes de `earthquake_data_tsunami.csv` :

- paramètres :
  - `d = 3`, `biais = 0` ;
  - `bootstrap_iterations = 1000` ;

Procédure :

- chargement de `data/extracted/earthquake_data_tsunami.csv` dans `df` ;
- `n_original = len(df) = 782` ;
- pour chaque itération :
  - tirage bootstrap d’un échantillon de taille `n_original` avec remise ;
  - `n_boot = len(sample) = 782` ;
  - calcul `T_log = (d - 4) ln(n_boot)` ;
  - stockage de T_log dans une liste.

On construit ensuite :

- un `numpy.array` `tlog_array` ;
- la moyenne, l’écart-type, l’IC95% (percentiles 2.5 % et 97.5 %).

Deux graphiques sont produits :

- `results/bootstrap_hist.png` : histogramme des T_log bootstrap ;
- `results/bootstrap_box.png` : boxplot des T_log bootstrap.

### 5.2 Résultats

Statistiques imprimées :

- Moyenne T_log : **−6.6619** ;
- Écart-type : **0.0000** ;
- IC95% : **[−6.6619, −6.6619]**.

Interprétation :

- le bootstrap ne produit **aucune variabilité** → toutes les valeurs T_log* sont identiques ;
- c’est attendu, car dans ce setup :
  - d est fixé à 3 ;
  - n_boot = n_original pour chaque resample ;
  - la formule V0.1 dépend uniquement de n, d, biais (et pas des valeurs individuelles des événements) ;
- tant que n et d restent constants, T_log est **strictement déterministe** → T_log* = T_log_obs pour tous les bootstrap.

L’interprétation textuelle le souligne :

- le régime de **Divergence** est *robuste et invariant* vis‑à‑vis du resampling ;
- le bootstrap confirme donc la **stabilité numérique** du modèle et l’absence d’artefacts aléatoires dans ce cadre.

---

## 6. Rôle de la Partie 2 dans le pipeline Tsunami V0.1

La Partie 2 accomplit plusieurs objectifs clés :

- elle calcule explicitement `T_log(782,3) ≈ −6.66` et classe le système Tsunami en **régime de Divergence** pour une dimension spatiale d=3 ;
- elle montre que la structure Divergence/Équilibre/Saturation en fonction de d est conforme à la théorie, avec **d_c = 4** :
  - d=2,3 → Divergence ;
  - d=4 → Équilibre ;
  - d=5 → Saturation ;
- elle confirme, via le stress test en n, que la divergence reste présente et se renforce progressivement quand n augmente, pour d=3 ;
- elle démontre, via le bootstrap, que dans ce paramétrage simple (T_log ne dépend que de n et d), le régime de divergence est **parfaitement stable** : aucune variabilité statistique n’est introduite par le resampling.

En résumé, cette Partie 2 valide le comportement attendu de T_log pour le dataset Tsunami dans le cadre V0.1 :

- d=3 (<4) → T_log<0 → Divergence ;
- la dépendance en n suit la loi logarithmique ;
- le modèle est numériquement stable et cohérent.

Les parties suivantes pourront complexifier la situation (p.ex. exploration d’autres d, sous‑ensembles temporels ou spatiaux, ou dimension effective estimée) tout en s’appuyant sur cette base bien comprise.
