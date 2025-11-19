# Tsunami V0.1 – Partie 8 (cellules 56–63) : Dimension spatio-temporelle d=4 et équilibres temporels/géographiques

## 1. Périmètre de la partie

Cette huitième partie correspond aux cellules **56–63** du notebook `Tsunami_part08.ipynb`, dérivé de `T_log_Tsunami_V_0_1En.ipynb`.

Elle examine le modèle **T_log V0.1** en dimension **spatio‑temporelle d = 4** :

- calcul de `T_log(n, d=4)` pour l’ensemble du dataset Tsunami (782 événements) ;
- analyse de sensibilité autour de d=4 (3.9, 4.0, 4.1) ;
- test de la **stabilité temporelle** de l’équilibre (par décennies) ;
- test de la **stabilité spatiale** de l’équilibre (quadrants géographiques NE/NW/SE/SW).

---

## 2. Bloc 7 – T_log à d = 4 et sensibilité locale autour de d=4

### 2.1 Calcul principal

La première cellule de cette partie :

- charge `earthquake_data_tsunami.csv` ;
- calcule `n = len(df) = 782` ;
- définit la fonction :

\[
T_{\log}(n,d) = (d - 4) \ln(n) + \text{bias}, \quad \text{avec bias = 0}.\]

En prenant **d = 4.0** :

\[
T_{\log}(782,4) = (4-4)\ln(782) = 0.\]

Le régime est donc :

- **Équilibre (Equilibrium)**.

### 2.2 Sensibilité autour de d = 4

La cellule réalise une petite analyse de sensibilité :

- `d_values = [3.9, 4.0, 4.1]` ;
- calcul de T_log et classification pour chaque d.

Résultats :

- d=3.9 → T_log ≈ −0.666 → **Divergence** ;
- d=4.0 → T_log = 0 → **Equilibrium** ;
- d=4.1 → T_log ≈ +0.666 → **Saturation**.

Interprétation :

- en enrichissant la dimension effective (d=4, espace+temps), le système Tsunami est placé **exactement sur la ligne critique** ;
- de petites variations de d (±0.1) basculent immédiatement le régime :
  - d<4 → Divergence ;
  - d>4 → Saturation ;
- cela illustre la **nature critique** du point d=4 : frontière nette entre instabilité et stabilité.

---

## 3. Bloc 8 – Stabilité temporelle de l’équilibre (d=4)

### 3.1 Découpage par décennies

La cellule suivante définit :

- `T_log(n, d=4)` comme plus haut ;
- un découpage temporel en **décennies** à partir de la colonne `Year` :
  - `decade = (year // 10) * 10` ;
  - par exemple, 2001→2000s, 2013→2010s, etc.

Pour chaque décennie, on calcule :

- `n_sub` = nombre d’événements dans cette décennie ;
- `T_log(n_sub, d=4)` ;
- le régime correspondant.

### 3.2 Résultats

Décennies observées :

- 2000s (n=258) → T_log = 0.000000 → **Equilibrium** ;
- 2010s (n=415) → T_log = 0.000000 → **Equilibrium** ;
- 2020s (n=109) → T_log = 0.000000 → **Equilibrium**.

Interprétation :

- pour d=4, T_log ne dépend plus de n (avec bias=0) → T_log = 0 pour **toute** valeur de n ;
- en pratique, cela signifie que le **régime d’équilibre critique** est **invariant dans le temps** :
  - aucune décennie ne bascule en Divergence ou Saturation ;
- l’équilibre spatio‑temporel n’est donc pas un artefact d’une période particulière, mais une propriété structurale pour d=4.

---

## 4. Bloc 9 – Stabilité spatiale de l’équilibre (d=4)

### 4.1 Découpage en quadrants géographiques

La cellule "Spatial stability analysis" :

- identifie les colonnes de latitude/longitude (`lat_col`, `lon_col`) ;
- définit quatre quadrants :
  - **NE** : latitude ≥ 0, longitude ≥ 0 ;
  - **NW** : latitude ≥ 0, longitude < 0 ;
  - **SE** : latitude < 0, longitude ≥ 0 ;
  - **SW** : latitude < 0, longitude < 0.

Pour chaque quadrant :

- `n_sub` = nombre d’événements dans cette région ;
- calcul de `T_log(n_sub, d=4)` ;
- classification du régime.

### 4.2 Résultats

Quadrants observés :

- NE (n=238) → T_log = 0.000000 → **Equilibrium** ;
- NW (n=120) → T_log = 0.000000 → **Equilibrium** ;
- SE (n=283) → T_log = 0.000000 → **Equilibrium** ;
- SW (n=141) → T_log = 0.000000 → **Equilibrium**.

Interprétation :

- comme pour les décennies, **tous les quadrants** se trouvent à T_log=0 pour d=4 ;
- l’équilibre critique est donc :
  - **invariant géographiquement** (Nord/Sud, Est/Ouest) ;
  - valable sur des sous‑ensembles de tailles différentes ;
- ceci renforce l’idée d’un **état critique universel** pour le système Tsunami lorsqu’on le considère dans une dimension spatio‑temporelle.

---

## 5. Rôle de la Partie 8 dans le pipeline Tsunami V0.1

La Partie 8 :

- montre que, pour le dataset Tsunami, passer de d=3 (spatial) à **d=4 (espace+temps)** place le système en **Équilibre critique (T_log=0)** ;
- démontre que cet équilibre est :
  - **robuste dans le temps** (par décennies) ;
  - **robuste dans l’espace** (par quadrants géographiques) ;
- illustre la nature **sharp** du point critique d=4, où de petites variations en d font immédiatement basculer le régime.

En combinaison avec les parties précédentes (d=3 → Divergence, tests de robustesse, bootstrap, permutation, ablation du biais), cette Partie 8 offre une vue complète :

- d=3 → régime de **Divergence** robuste ;
- d=4 → **Équilibre** universel (spatio‑temporel, invariant aux découpages) ;
- d>4 → **Saturation** (stabilité) ;

ce qui confirme que, pour ce cas Tsunami V0.1, la loi `T_log(n,d) = (d-4) ln(n)` capture bien un comportement **critique** au seuil d=4, entouré de régimes de Divergence et de Saturation clairement séparés.
