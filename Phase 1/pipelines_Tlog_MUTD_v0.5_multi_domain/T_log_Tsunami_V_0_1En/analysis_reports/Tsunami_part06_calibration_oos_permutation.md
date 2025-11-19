# Tsunami V0.1 – Partie 6 (cellules 40–47) : Calibration proxy, tests hors-échantillon et test de permutation

## 1. Périmètre de la partie

Cette sixième partie correspond aux cellules **40–47** du notebook `Tsunami_part06.ipynb`, dérivé de `T_log_Tsunami_V_0_1En.ipynb`.

Elle ajoute trois briques de validation autour du modèle **T_log V0.1** pour le dataset Earthquake–Tsunami :

- **Bloc 5.10** : calibration et marges via un proxy logistique (sur une grille (ln(n), d)) ;
- **Bloc 5.11** : cohérence hors-échantillon sur sous‑groupes temporels et géospatiaux ;
- **Bloc 5.12** : test de permutation (shuffle des labels) pour détecter un éventuel signal spurious.

Ces analyses complètent les parties précédentes en testant la stabilité de la frontière et la non‑trivialité du signal.

---

## 2. Bloc 5.10 – Calibration proxy et histogramme des marges

### 2.1 Construction du dataset (proxy probabiliste)

On construit un dataset synthétique similaire à celui du Bloc 5.7 :

- `n_values = linspace(100, 1000, 200)` ;
- `d_values = linspace(2, 5, 200)` ;
- pour chaque (n,d) :
  - calcul de \(T_{\log}(n,d) = (d-4) \ln(n)\) ;
  - label binaire `label = 1` si T_log>0 (Saturation), `0` si T_log<0 (Divergence), exclusion de T_log=0 ;
  - `margin = |T_log|`.

On ajuste ensuite un modèle de **régression logistique** (comme proxy prob.) :

- features : `ln_n = ln(n)`, `d` ;
- cible : `label`.

### 2.2 Courbe de fiabilité (reliability curve)

À partir des probabilités prédites `probs`, on trace une **courbe de calibration** :

- via `calibration_curve(y, probs, n_bins=10, strategy='uniform')` ;
- graphique : fraction de positifs vs probabilité moyenne prédite.

Observation :

- la courbe bleue s’écarte de la diagonale parfaite ;
- ceci montre que le proxy logistique **n’est pas bien calibré** en probabilité (pour les faibles probabilités notamment).

Interprétation :

- ce n’est pas un défaut du modèle T_log lui‑même, qui est **déterministe** (pas probabiliste) ;
- c’est une conséquence du fait qu’on force une régression logistique sur une frontière analytique parfaite :
  - la séparation est triviale ;
  - les "probabilités" n’ont pas de sens physique ici.

### 2.3 Histogramme des marges |T_log|

On trace ensuite un histogramme des marges :

- `margin = |T_log|` pour toutes les paires (n,d) ;
- figure : distribution des marges entre 0 et ~13–14.

Observation textuelle :

- la plupart des points ont des marges faibles à modérées (0–5), avec un pic autour de ~2 ;
- quelques points ont des marges plus grandes (d=2 ou d=5) → régimes très stables ;
- les marges proches de 0 se concentrent autour de d≈4 (zone critique).

Interprétation :

- la **frontière d=4** est nette, mais la plupart des configurations (n,d) restent suffisamment éloignées de cette ligne pour que la classification ne soit pas ambiguë ;
- les marges quantifient correctement :
  - la stabilité des régimes loin de d=4 ;
  - la sensibilité naturelle à proximité de la criticité.

Conclusion de 5.10 :

- la calibration probabiliste du proxy logistique n’est pas pertinente pour juger V0.1 ;
- l’histogramme des marges montre une séparation raisonnable des régimes, renforçant l’idée de **robustesse** de la frontière critique.

---

## 3. Bloc 5.11 – Cohérence hors-échantillon (partitions temporelles et géospatiales)

### 3.1 Configuration

On revient à l’**ensemble réel** `earthquake_data_tsunami.csv` :

- `n_total = 782` ;
- `d_fixed = 3` ;
- on identifie les colonnes :
  - `year_col` (année), `lat_col` (latitude), `lon_col` (longitude).

On calcule d’abord :

\[
T_{\log}(n_{total},3) = (3-4) \ln(782) \approx -6.6619 \quad \to \text{Divergence}.
\]

### 3.2 Splits temporels

- on construit une liste ordonnée des années ;
- on coupe la période en deux moitiés (première moitié vs seconde moitié) ;
- pour chaque split, on calcule :
  - `n_sub` = nombre d’événements dans la sous‑période ;
  - `T_log(n_sub,3)` et le régime.

Résultats :

- split 1 (≈333 événements) → T_log ≈ −5.81 → Divergence ;
- split 2 (≈449 événements) → T_log ≈ −6.11 → Divergence.

### 3.3 Splits géospatiaux (hémisphères)

En utilisant lat/lon :

- **N‑hémisphère** (latitude ≥ 0) : ~358 événements, T_log ≈ −5.88 → Divergence ;
- **S‑hémisphère** (latitude < 0) : ~424 événements, T_log ≈ −6.05 → Divergence ;
- **E‑hémisphère** (longitude ≥ 0) : ~521 événements, T_log ≈ −6.26 → Divergence ;
- **W‑hémisphère** (longitude < 0) : ~261 événements, T_log ≈ −5.56 → Divergence.

### 3.4 Interprétation

- pour toutes les sous-séries testées (temps ou espace), T_log(·,3) reste **strictement négatif** ;
- les différences de magnitude reflètent simplement les différences de n_sub (plus n_sub est grand, plus ln(n_sub) est grand, donc T_log est plus négatif) ;
- le régime de Divergence est donc **invariant** aux partitions temporelles et géospatiales raisonnables.

Conclusion :

- aucun sous‑ensemble ne montre un comportement "contradictif" (pas de bascule en Équilibre/Saturation) ;
- il n’y a pas de dépendance cachée à une zone ou une période ;
- le modèle T_log capture une propriété **globale** de la base Tsunami, plutôt qu’un artefact local.

---

## 4. Bloc 5.12 – Test de permutation (permutation test)

### 4.1 Construction et protocole

On refait un dataset (ln_n, d, label) sur la même grille que pour 5.7 :

- `ln_n = ln(n)` ; `d` ; `label` = 1 (Saturation) / 0 (Divergence) selon le signe de T_log.

On ajuste d’abord un modèle logistique sur les labels **non permutés** :

- on obtient un **AUC vrai** `true_auc` ;
- pour ce problème, true_auc = **1.0000** (séparation parfaite, comme vu en 5.7).

Ensuite, on effectue un **test de permutation** :

- pour 200 itérations :
  - on permute aléatoirement les labels `y` → `y_perm` ;
  - on ajuste une nouvelle régression logistique sur (X, y_perm) ;
  - on calcule l’AUC sur ces labels permutés ;
- on obtient une distribution `perm_aucs` ;
- p‑value permutation = P(AUC_perm ≥ AUC_true).

### 4.2 Résultats

- AUC vrai (non permuté) : **1.0000** ;
- moyenne AUC permutation ≈ **0.5063 ± 0.0037** ;
- p-value permutation ≈ **0.0050**.

Interprétation :

- sous permutation (labels aléatoires), les modèles logistiques ont une performance proche du hasard (AUC≈0.5) ;
- l’AUC=1.0 obtenue avec les labels issus de T_log est extrêmement improbable sous cette distribution ;
- p≈0.005 signifie que seulement ~0.5 % des permutations (ou moins) atteignent un AUC aussi élevé que le vrai (et ici, aucune ne l’atteint réellement).

Conclusion :

- la structure de séparation (Divergence vs Saturation) donnée par T_log n’est pas un artefact aléatoire de la régression logistique ;
- elle correspond à un signal **fortement structuré** (ici, purement analytique) que la logistique ne fait que traduire dans son espace.

---

## 5. Rôle de la Partie 6 dans le pipeline Tsunami V0.1

Cette Partie 6 fournit les derniers éléments de validation avancée :

- **Bloc 5.10** : montre que la calibration probabiliste d’un proxy logistique n’est pas pertinente pour juger V0.1, mais que les marges |T_log| donnent une bonne idée de la séparation des régimes autour de d=4 ;
- **Bloc 5.11** : démontre que le régime de **Divergence** pour d=3 est **invariant** à la séparation des données en sous-groupes temporels ou géospatiaux raisonnables ;
- **Bloc 5.12** : via un test de permutation, confirme que la séparation Divergence/Saturation n’est pas due au hasard, mais à la structure du modèle.

En complément des parties précédentes (stress tests, bootstrap, baselines, heatmap, régression logistique), cette Partie 6 :

- renforce la conclusion que **T_log V0.1 est un modèle simple, analytique, et non sur‑ajusté** pour ce dataset Tsunami ;
- montre que l’instabilité (T_log<0) observée pour d=3 est robuste :
  - aux variations de n (Partie 2),
  - aux perturbations de paramètres (Partie 5),
  - aux partitions temporelles/géographiques,
  - et aux tests d’aléatorisation (permutation).

Le pipeline Tsunami V0.1 dispose ainsi d’un ensemble complet de diagnostics (quantitatifs, graphiques et statistiques) montrant que la loi `T_log(n,d) = (d-4) ln(n)` se comporte comme prévu sur ce cas, avec **d_c = 4** comme frontière critique universelle.
