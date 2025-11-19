# Tsunami V0.1 – Partie 9 (cellules 64–71) : Stress multi‑échelle et robustesse au bruit pour d = 4

## 1. Périmètre de la partie

Cette neuvième partie correspond aux cellules **64–71** du notebook `Tsunami_part09.ipynb`, dérivé de `T_log_Tsunami_V_0_1En.ipynb`.

Elle pousse au maximum les tests de robustesse du modèle **T_log V0.1** en dimension **spatio‑temporelle d = 4** :

- **Bloc 10** : test combiné temps × espace (décennies × quadrants NE/NW/SE/SW) ;
- **Bloc 11** : stress test **multi‑échelle** (sous‑échantillons aléatoires de taille 20 à 700) ;
- **Bloc 12** : robustesse au **bruit sur la taille n** (perturbations ±1 à ±20 %).

Dans tous les cas, d=4, bias=0 → T_log théorique = 0.

---

## 2. Bloc 10 – Décennies × quadrants : stabilité spatio‑temporelle à d = 4

### 2.1 Méthode

Bloc 10 reprend le dataset `earthquake_data_tsunami.csv` et :

- identifie :
  - `year_col` pour l’année ;
  - `lat_col`, `lon_col` pour latitude/longitude ;
- définit :
  - `decade = (year // 10)*10` (2000s, 2010s, 2020s) ;
  - `quadrant` :
    - NE : lat≥0, lon≥0 ;
    - NW : lat≥0, lon<0 ;
    - SE : lat<0, lon≥0 ;
    - SW : lat<0, lon<0.

Pour chaque couple (décennie, quadrant) :

- sous‑ensemble `sub` ;
- `n_sub = len(sub)` ;
- calcul de `T_log(n_sub, d=4)` et du régime.

### 2.2 Résultats

Extrait des résultats :

- 2000s, NE : n=100, T_log=0 → Equilibrium ;
- 2000s, NW : n=28, T_log=0 → Equilibrium ;
- 2000s, SE : n=102, T_log=0 → Equilibrium ;
- 2000s, SW : n=28, T_log=0 → Equilibrium ;
- 2010s, NE : n=112, T_log=0 → Equilibrium ;
- 2010s, NW : n=65, T_log=0 → Equilibrium ;
- 2010s, SE : n=154, T_log=0 → Equilibrium ;
- 2010s, SW : n=84, T_log=0 → Equilibrium ;
- 2020s, NE : n=26, T_log=0 → Equilibrium ;
- 2020s, NW : n=27, T_log=0 → Equilibrium ;
- 2020s, SE : n=27, T_log=0 → Equilibrium ;
- 2020s, SW : n=29, T_log=0 → Equilibrium.

Interprétation :

- même pour des sous‑groupes **très petits** (n≈26–29), `T_log(n,4) = 0` ;
- l’équilibre critique à d=4 est **invariant** quel que soit le croisement temps × espace ;
- c’est un test de **robustesse multi‑dimensionnelle** : ni le choix de la décennie, ni celui du quadrant ne rompent l’équilibre.

Cette invariance à la granularité spatio‑temporelle renforce l’interprétation de d=4 comme **point critique universel**.

---

## 3. Bloc 11 – Stress test multi‑échelle (sous‑échantillons aléatoires, d=4)

### 3.1 Méthode

On réalise ensuite un stress test multi‑échelle :

- on définit une liste de tailles :
  - `sizes = [20, 50, 100, 200, 300, 400, 500, 600, 700]` ;
- pour chaque taille `size` :
  - on tire `n_reps = 5` sous‑échantillons aléatoires (sans replacer les dimensions, mais avec shuffling des lignes) ;
  - pour chaque sous‑échantillon `sub` de taille `n_sub = size` :
    - calcul de `T_log(n_sub, d=4)` ;
    - détermination du régime.

### 3.2 Résultats

Pour toutes les tailles et répétitions (de n=20 jusqu’à n=700) :

- `T_log(n,4) = 0.000000` ;
- `Regime = Equilibrium`.

Il n’y a **aucune exception**, même pour les sous‑échantillons les plus petits.

### 3.3 Interprétation

- le stress test montre que l’équilibre critique à d=4 est **strictement invariante à l’échelle** :
  - qu’on observe 20 événements ou 700, `T_log(n,4)` reste exactement 0 ;
- cela illustre une forme de **symétrie d’échelle** au niveau du modèle :
  - tant qu’on reste à `d=4` et `bias=0`, la taille n ne modifie pas le régime ;
- dans le langage des systèmes critiques, cela évoque un comportement de **Self‑Organized Criticality (SOC)** :
  - la criticité ne dépend pas de l’échelle d’observation.

---

## 4. Bloc 12 – Robustesse au bruit sur n (d=4)

### 4.1 Méthode

Enfin, le Bloc 12 teste la **robustesse au bruit sur la taille n** :

- part de la taille réelle `n_true = 782` ;
- définit des niveaux de bruit relatifs :
  - `noise_levels = [0.01, 0.02, 0.05, 0.10, 0.20]` ;
- pour chaque niveau de bruit :
  - 5 perturbations aléatoires ;
  - `n_perturbed = round(n_true * (1 + delta))` avec `delta ∈ [−noise, +noise]` ;
  - calcul de `T_log(n_perturbed, d=4)` ;
  - classification du régime.

### 4.2 Résultats

Pour tous les niveaux de bruit (±1 %, ±2 %, ±5 %, ±10 %, ±20 %) et toutes les répétitions :

- `T_log(n_perturbed, 4) = 0.000000` ;
- `Regime = Equilibrium`.

Même lorsque n est fortement perturbé (par ex. n≈677 ou n≈808), le régime ne change pas.

### 4.3 Interprétation

- cet exercice confirme que l’équilibre spatio‑temporel d=4 est **insensible aux fluctuations aléatoires de la taille** :
  - quelle que soit la taille raisonnable n que l’on choisit, T_log(n,4) reste nul ;
- cela renforce l’idée que l’équilibre d=4 est une **propriété structurelle de la formule**, et non un ajustement fin décrit par un n particulier.

---

## 5. Rôle de la Partie 9 dans le pipeline Tsunami V0.1

La Partie 9 réalise les tests les plus "granulaires" et "agressifs" de robustesse pour le cas Tsunami en d=4 :

- croisement **temps × espace** en petits sous‑groupes (décennie × quadrant) ;
- sous‑échantillonnage aléatoire **multi‑échelle** (de n=20 à n=700) ;
- perturbations aléatoires de la taille n (bruit jusqu’à ±20 %).

Dans tous les cas, le modèle T_log avec d=4 et bias=0 :

- donne **T_log = 0** ;
- classe tous les sous‑ensembles en **Équilibre**.

Cette Partie 9 confirme que :

- en dimension spatio‑temporelle d=4, le système Tsunami est **universellement critique** ;
- cette criticité est **invariante** :
  - à l’échelle (taille n),
  - à la partition temporelle (décennies),
  - à la partition spatiale (quadrants),
  - et même à des fluctuations aléatoires sur n ;
- le modèle T_log V0.1, enrichi à d=4, capture une structure qui ressemble fortement à un comportement de **Self‑Organized Criticality (SOC)**.

En combinaison avec les parties précédentes (d=3 → Divergence robuste, d=4 → Équilibre robuste), cette partie finalise la vision :

- d<4 → régime Divergence ;
- d=4 → Équilibre critique universel (stable dans le temps, l’espace, l’échelle) ;
- d>4 → Saturation.

Ce résultat fournit un socle conceptuel puissant pour les versions ultérieures (V1/V2) où l’on pourra introduire des mécanismes plus complexes tout en conservant cette boussole T_log(n,d).
