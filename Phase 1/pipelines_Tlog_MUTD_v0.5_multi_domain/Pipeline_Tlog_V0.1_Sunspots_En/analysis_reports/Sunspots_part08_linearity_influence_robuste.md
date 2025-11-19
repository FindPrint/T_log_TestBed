# Sunspots V0.5 – Partie 8 (cellules 70–79) : Linéarité, points influents et régressions robustes

## 1. Périmètre de la partie

Cette huitième partie correspond aux cellules **70–79** du notebook `Sunspots_part08.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle complète le bloc "dimension spectrale" en examinant de près :

- la **qualité des fits log‑log** N(λ) vs λ (linéarité, résidus, Cook, R²) ;
- l’influence de **points fortement influents** sur la pente spectrale ;
- l’impact de **régressions robustes** (Theil‑Sen, RANSAC) par rapport à l’OLS classique ;
- des tests appariés entre méthodes (Wilcoxon) et une synthèse des d_s obtenus.

---

## 2. Tests statistiques appariés Levina–Bickel vs d_s spectral (résumé)

La première cellule rappelle les résultats des tests sur 150 paires (pour chaque λ_max = 0.1, 0.2, 0.4) :

- Levina–Bickel (m_hat) médiane ≈ **7.94** ;
- d_s spectral médian ≈ **0.21** (λ=0.1), **0.30** (λ=0.2), **0.52** (λ=0.4) ;
- différence moyenne Levina − spectral ≈ 7.7, 7.6, 7.4 selon λ_max ;
- tests Wilcoxon appariés : p‑value ≈ 2.3e−26 pour chaque λ_max (différence extrêmement significative) ;
- corrélations Spearman faibles ou nulles (rho ~0.1, −0.04, 0.0, p non significatives) ;
- tailles d’effet (Cohen d apparié) énormes, dues à la grande moyenne de la différence pour une variance très petite.

Interprétation succincte :

- les deux estimateurs ne sont **pas comparables en échelle absolue** (8 vs <1) ;
- leurs variations ne sont **pas corrélées** sur les mêmes sous‑échantillons ;
- il faut donc choisir explicitement **quelle notion de dimension** on reporte.

Ces constats préparent les diagnostics plus fins sur la linéarité du fit spectral lui‑même.

---

## 3. Diagnostics de linéarité log‑log sur N(λ)

### 3.1 Méthode

Une cellule "Linear regression diagnostics" effectue, pour `n_diagnostics = 10` sous‑échantillons (embedding_dim=10, k=10) :

- calcul de `n_eig = 400` valeurs propres (pour mieux couvrir small‑to‑mid λ) ;
- construction de N(λ) et sélection des points λ ≤ `lambda_max_diag = 0.2` ;
- régression linéaire sur `log N` vs `log λ` ;
- calcul de diagnostics de régression :
  - R², MSE, résidus, résidus standardisés ;
  - leverage, Cook’s distance ;
- production de figures `diag_##_diagnostic.png` avec :
  - à gauche : log‑log + droite de fit ;
  - à droite : résidus vs fitted + QQ‑plot des résidus standardisés.

Résumé dans `results/spectral_diagnostics_linearity/linearity_diagnostics_summary.csv` :

- `n_points_fit` (points dans λ ≤ 0.2), `slope`, `stderr_slope`, `r2`, `max_cook`, `n_influential`.

### 3.2 Résultats

La cellule d’analyse indique :

- `n_points_fit` = 16–18 → assez de points pour un fit, mais plage courte ;
- `slope` ≈ 0.140–0.154 → `d_s = 2*slope ≈ 0.28–0.31` ;
- `stderr_slope` ≈ 0.027–0.029 → estimation de pente précise ;
- `R²` ≈ 0.64–0.66 → bonne linéarité, mais pas parfaite ;
- `max_cook ≫ 1` et `n_influential = 1` pour chaque diag : 
  - un point très influent domine le fit (Cook >> 4/n) ;
- MSE ≈ 0.23–0.25 (en log‑espace).

Conclusion :

- les pentes small‑λ sont **cohérentes et stables** sur les sous‑échantillons ;
- le fit OLS est raisonnable, mais **un point influent** par diag pèse fortement sur la pente.

---

## 4. Influence des points et régressions robustes

### 4.1 Identification et refit sans points influents

Une cellule "Influence diagnostics" :

- relit les fichiers `diag_##_counting.csv` produits précédemment ;
- pour chaque diagnostic, sélectionne λ ≤ 0.2 ;
- ajuste un OLS log‑log (pente_orig) et calcule leverage, Cook ;
- identifie les points avec Cook > 4/n (règle heuristique) ;
- refait un fit OLS **sans** ces points influents (pente_noinfl) ;
- ajuste deux estimateurs robustes :
  - **Theil–Sen** ;
  - **RANSAC** + LinearRegression ;
- sauvegarde :
  - `results/spectral_influence_refit/influence_refit_summary.csv` ;
  - plots `diag_##_influence_refit.png` (données + 4 droites : OLS, OLS sans influents, Theil–Sen, RANSAC) ;
  - tables `diag_##_influential_points.csv` (λ, N(λ), Cook, leverage, résidu standardisé).

Les logs montrent qu’à chaque diag :

- `n_infl = 1` ;
- `slope_orig ≈ 0.14–0.154` ;
- `slope_noinfl ≈ 0.54–0.56` → d_s ≈ 1.08–1.12 ;
- Theil–Sen slope ≈ 0.72–0.85 (d_s ≈ 1.44–1.70) ;
- RANSAC slope ≈ slope_noinfl dans la plupart des cas.

### 4.2 Synthèse numérique des méthodes

Une autre cellule assemble ces résultats :

- calcule d_s = 2*slope pour chaque méthode : OLS orig, OLS sans influent, Theil–Sen, RANSAC ;
- produit :
  - `results/spectral_influence_summary/d_s_methods_aggregate.csv` (médianes et IQR) ;
  - `results/spectral_influence_summary/d_s_paired_tests.csv` (tests Wilcoxon appariés entre méthodes) ;
  - `results/spectral_influence_summary/d_s_per_diag.csv` ;
  - `results/spectral_influence_summary/d_s_methods_comparison.png` (boxplots + points).

Résumé final (cellule de texte) :

- d_s_OLS_orig médiane ≈ 0.30 (cohérent avec les parties précédentes) ;
- d_s_noinfl médiane ≈ 1.12 ;
- d_s_Theil–Sen médiane ≈ 1.56 ;
- d_s_RANSAC médiane ≈ 1.12 ;
- tests Wilcoxon appariés (K=10 diagnostics) montrent des différences significatives entre OLS orig et les autres (p ≈ 0.002) ;
- en clair : **supprimer 1 point influent ou utiliser un estimateur robuste change la pente d’un facteur ~3–5**.

Interprétation :

- la pente spectrale small‑λ est **fortement sensible** à un unique point influent ;
- l’OLS original produit une pente faible (d_s ≈ 0.3) essentiellement dictée par ce point ;
- les estimateurs robustes donnent des pentes plus élevées et plus proches de ce qui pourrait être la "tendance générale" sur la plage λ ≤ 0.2 ;
- il n’existe pas ici une "valeur absolue unique" pour d_s spectral : le résultat dépend de la politique de traitement des points influents.

---

## 5. Synthèse de la Partie 8 et implication pour T_log

Cette Partie 8 montre que :

- le **fit spectral small‑λ** est :
  - numériquement cohérent (pentes stables, R² ~0.65) ;
  - mais **fragile** à des points de forte influence ;
- enlever un point influent ou utiliser des méthodes robustes peut **multiplier la pente** (et donc d_s) par 3–5 pour les diagnostics analysés ;
- les méthodes Levina–Bickel (dimension intrinsèque locale) et spectrale (pente small‑λ) mesurent des aspects **différents** du graphe, et il n’est pas légitime de vouloir les faire coïncider numériquement.

Pour T_log(n, d) :

- quel que soit le choix raisonnable de d (spectral small‑λ, spectral robuste, Levina–Bickel), tant que d_est < 4, **T_log(n,d_est)** reste **négatif** → régimes de **Divergence** robustes ;
- en revanche, la **valeur absolue** de T_log (−30 vs −20 vs −14, etc.) dépend directement de la convention choisie pour d.

La Partie 8 clôt ainsi la séquence de diagnostics avancés sur la dimension pour Sunspots V0.5 en clarifiant que :

- la **qualité globale** de la typologie (T_log<0) est solide ;
- l’interprétation **quantitative fine** de d_s et T_log nécessite de **documenter explicitement** la chaîne d’estimation (Laplacien, plage λ, OLS/robuste, etc.) et d’accepter qu’il n’y a pas de valeur "canonique" unique, mais un éventail structuré par les choix méthodologiques.
