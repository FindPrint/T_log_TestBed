# Tsunami V0.1 – Partie 5 (cellules 32–39) : Régression logistique, frontière critique d* et sensibilités n/d

## 1. Périmètre de la partie

Cette cinquième partie correspond aux cellules **32–39** du notebook `Tsunami_part05.ipynb`, dérivé de `T_log_Tsunami_V_0_1En.ipynb`.

Elle complète la validation du modèle **T_log V0.1** pour le cas Tsunami en :

- utilisant une **régression logistique** sur une grille (ln(n), d) pour re‑découvrir la frontière Divergence/Saturation (Bloc 5.7) ;
- quantifiant précisément la **frontière critique d*** où T_log≈0 et les marges |T_log| autour de d=4 (Bloc 5.8) ;
- testant la **sensibilité de T_log** à de petites perturbations de n et de d autour de (n=782, d=3) (Bloc 5.9).

---

## 2. Bloc 5.7 – Régression logistique (ln(n), d) : Divergence vs Saturation

### 2.1 Construction du dataset artificiel

Pour analyser la frontière de décision, le notebook génère une grille continue :

- `n_values = linspace(100, 1000, 120)` ;
- `d_values = linspace(2, 5, 120)` ;

Pour chaque paire (n,d) :

- calcule \(T_{\log}(n,d) = (d-4) \ln(n)\) ;
- attribue un label binaire :
  - `label=1` si T_log > 0 → **Saturation** ;
  - `label=0` si T_log < 0 → **Divergence** ;
  - points avec T_log=0 (d=4) sont exclus (équilibre exact).

Le jeu de données final `df` contient :

- features : `ln_n = ln(n)`, `d` ;
- cible : `label` (0/1).

Le dataset est séparé en train/test (stratifié) et une **régression logistique** est ajustée :

- `X = [ln_n, d]` ;
- `y` = label ;
- `LogisticRegression(max_iter=1000)`.

### 2.2 Résultats numériques

La régression logistique donne :

- Accuracy = **1.0000** ;
- AUC = **1.0000** ;
- matrice de confusion :
  - parfaitement diagonale (aucune erreur de classification) ;
- coefficients :
  - coefficient sur ln(n) ≈ **−0.045** (très petit) ;
  - coefficient sur d ≈ **+18.39** (dominant) ;
  - intercept ≈ **−73.38**.

Une figure montre :

- le nuage de points (ln(n), d) coloré par label (Divergence/Saturation) ;
- la courbe de frontière de décision p=0.5 (contour logistique).

### 2.3 Interprétation

- la régression logistique **retrouve exactement** la frontière analytique :
  - frontière quasiment **horizontale en d ≈ 4** ;
  - l’impact de ln(n) sur la classification est négligeable (coeff. proche de 0) ;
- la variable d porte l’essentiel de la décision, ln(n) ne joue qu’un rôle d’échelle ;
- les performances parfaites (Accuracy=1, AUC=1) traduisent :
  - la **séparabilité parfaite** du modèle analytique ;
  - l’absence d’overfitting : le classifieur ne fait que recoder la relation théorique.

En d’autres termes : la régression logistique confirme que la frontière Divergence/Saturation est bien dominée par **d vs 4**, comme prévu, et ne dépend pas de détails spécifiques du dataset.

---

## 3. Bloc 5.8 – Frontière critique d* et analyse des marges

### 3.1 Calcul de d* et de |T_log|

Le bloc 5.8 cherche la valeur **d*** telle que :

\[T_{\log}(n=782, d^*) \approx 0.\]

- `d_values = linspace(2.0, 5.0, 601)` ;
- `tlog_vals = (d_values - 4.0) ln(782)` ;
- `d_star = d_values[argmin(|tlog_vals|)]`.

Résultats :

- `d* = 4.0000` ;
- `min |T_log| = 0.000000` à d*, ce qui est attendu (points d’équilibre).

Les marges |T_log| pour d ∈ {2,3,4,5} :

- d=2 → |T_log| ≈ 13.32 (divergence très forte) ;
- d=3 → |T_log| ≈ 6.66 (divergence claire) ;
- d=4 → |T_log| = 0 (criticité) ;
- d=5 → |T_log| ≈ 6.66 (saturation nette).

### 3.2 Interprétation

- la **frontière critique** est parfaitement localisée en **d*=4** ;
- les marges symétriques pour d=3 et d=5 indiquent une **symétrie** de la loi autour de d=4 :
  - même amplitude de divergence et de saturation ;
- la distance en |T_log| aux deux côtés de d=4 est suffisamment grande pour :
  - rendre la classification de régime **non ambiguë** ;
  - montrer que de petites perturbations autour de d=3 ou d=5 ne font pas basculer le régime.

Cela confirme que la frontière d=4 est **stable, nette et robuste**.

---

## 4. Bloc 5.9 – Sensibilité à de petites perturbations en n et d

### 4.1 Perturbations de n autour de n=782

Le bloc 5.9 examine la robustesse du régime pour (n=782, d=3) face à de petites variations de n et de d.

Perturbations en n :

- facteurs multiplicatifs : {0.99, 1.01, 0.95, 1.05, 0.90, 1.10, 0.80, 1.20} ;
- plages de n testés ≈ [625, 938].

Pour chaque n perturbé, T_log(n,3) = (3−4) ln(n) est calculé et le régime est déterminé.

Résultat :

- T_log reste **toujours négatif** ;
- régime = **Divergence** pour toutes les tailles testées ;
- la valeur de T_log varie modérément (≈ −6.44 à −6.84), mais le signe ne change pas.

### 4.2 Perturbations de d autour de d=3

Perturbations en d :

- d ∈ {2.80, 2.90, 2.95, 2.99, 3.01, 3.05, 3.10, 3.20} ;
- n=782 fixé.

Pour chaque d, T_log(782,d) et le régime sont calculés.

Résultat :

- pour toutes ces valeurs proches de 3, T_log reste **strictement négatif** ;
- régime = **Divergence** ;
- T_log se rapproche de 0 lorsque d→4, mais sans changer de signe dans cette fenêtre.

### 4.3 Interprétation

- les tests montrent que la configuration (n=782, d=3) est **robuste** :
  - ni des variations de ±1–20 % sur n,
  - ni des perturbations raisonnables de d autour de 3,
  ne changent le régime de Divergence ;
- la frontière critique d=4 n’est franchie qu’avec un changement de d beaucoup plus important (de 3 à 4), ce qui confirme :
  - la **stabilité locale** du modèle ;
  - la non‑sensibilité à de petites fluctuations de paramètres.

---

## 5. Rôle de la Partie 5 dans le pipeline Tsunami V0.1

Cette Partie 5 fournit une validation encore plus fine de T_log V0.1 pour le cas Tsunami :

- la **régression logistique** montre que la frontière Divergence/Saturation est entièrement portée par d, avec une séparation quasi parfaite alignée sur d=4, ce qui est exactement la prédiction théorique ;
- le calcul de **d*** et des marges |T_log| montre que la frontière critique est localisée en d=4 avec des marges confortables de part et d’autre (d=3,5), rendant la classification robuste ;
- les **tests de sensibilité** confirment que de petites perturbations en n ou en d ne modifient pas le régime de Divergence pour (n≈782, d≈3).

En résumé, la Partie 5 renforce la conclusion que :

- la loi `T_log(n,d) = (d-4) ln(n)` est **cohérente, stable et non sur‑ajustée** dans ce cadre Tsunami ;
- la dimension critique universelle **d_c = 4** est retrouvée et confirmée par des méthodes statistiques et de machine learning (logistic regression) ;
- le régime de Divergence pour d=3 est **robuste** à de nombreuses perturbations paramétriques.

Cette validation complète prépare le terrain pour des versions ultérieures du modèle (V1, V2) où d ne sera plus fixé a priori mais estimé à partir de structures plus complexes (graphes, spectres, dimensions intrinsèques), tout en conservant la grille de lecture T_log consolidée ici.
