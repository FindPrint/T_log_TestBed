# Sunspots V0.5 – Synthèse globale du pipeline T_log

## 1. Contexte scientifique et objectif

Le pipeline `Pipeline_Tlog_V0.1_Sunspots_En.ipynb` implémente, pour la série mensuelle Sunspots (n ≈ 3265), une analyse complète basée sur l’**équation universelle T_log** :

\[
T_{\log}(n,d) = (d - 4) \ln(n) + \text{bias}, \quad \text{(bias = 0 dans ce pipeline)}.
\]

La valeur de `T_log` permet de classifier le régime :

- **Divergence** : T_log < 0 ;
- **Équilibre** : T_log ≈ 0 ;
- **Saturation** : T_log > 0.

L’objectif global de Sunspots V0.5 est :

- d’estimer de manière robuste une **dimension effective d_est** pour la dynamique sous-jacente (sur base graph-spectrale et/ou dimension intrinsèque) ;
- de propager cette dimension dans T_log(n, d_est) ;
- de tester la stabilité du **signe** et de l’ordre de grandeur de T_log face à :
  - différentes méthodes d’estimation de dimension (spectrale vs Levina–Bickel) ;
  - hyperparamètres (embedding_dim, k_neighbors, λ_max, exclusion de petits λ) ;
  - bootstrap et null-models.

Les 12 parties du notebook (split par blocs de 10 cellules) détaillent chacune un sous-module de cette analyse.

---

## 2. Données et préparation (Partie 1)

- **Données** : série mensuelle Sunspots (Kaggle `robervalt/sunspots` ou CSV local `data/sunspots_raw/Sunspots.csv`), taille n ≈ 3265.
- Préparation :
  - création de l’arborescence `data/`, `results/`, `logs/` ;
  - configuration d’un logger ;
  - chargement et contrôle qualité (valeurs manquantes, type, cohérence temporelle).

### 2.1 Baseline T_log avec d=1

En prenant **d = 1** (dimension minimale de la série) :

\[
T_{\log}(3265, 1) = (1 - 4) \ln(3265) \approx -3 \ln(3265) < 0.
\]

Conclusion de base :

- même dans ce cas minimal, T_log est **nettement négatif** → le système Sunspots est déjà classé en **régime de Divergence**.

Ce baseline sert de référence pour toute la suite.

---

## 3. Architecture générale du pipeline Sunspots V0.5

Les parties 2 à 12 peuvent être regroupées par blocs thématiques :

- **Bloc A – Sensibilité T_log et premiers bootstraps** (Parties 2–3) :
  - étude de T_log en fonction de n et d ;
  - premiers bootstraps de T_log ;
  - introduction du graphe k-NN, du Laplacien et du spectre.

- **Bloc B – Dimension spectrale et régimes T_log** (Parties 4–5) :
  - estimation de la dimension spectrale d_s à partir de N(λ) ;
  - propagation vers T_log ;
  - null-models (temporal shuffle, phase randomized) et comparaison statistique.

- **Bloc C – Robustesse aux hyperparamètres et dimension intrinsèque** (Parties 6–7) :
  - balayage sur (embedding_dim, k_neighbors) ;
  - estimateur de dimension intrinsèque de Levina–Bickel ;
  - comparaison Levina vs pente spectrale ;
  - diagnostics avancés sur λ_max et la qualité des fits.

- **Bloc D – Points influents, régressions robustes (Theil–Sen, RANSAC)** (Parties 8–9) :
  - étude détaillée des points à forte influence (Cook) dans les fits log‑log ;
  - OLS vs Theil–Sen vs RANSAC ;
  - top‑K bootstraps les plus discordants Levina vs spectral.

- **Bloc E – Consolidation des d_s robustes et maintenance** (Parties 10–11) :
  - pipeline `ds_remove_small_lambda` ;
  - reconstruction propre de `ds_robust_per_b.csv` à partir des fichiers paired ;
  - refits ciblés pour cas atypiques ;
  - diagnostics `top15` et gestion des fichiers counting.

- **Bloc F – Pipeline autonome `sunspots_external` et choix final** (Partie 12) :
  - cellule autonome Kaggle → embedding → Laplacien → d_s → T_log ;
  - bootstrap d_s/T_log ;
  - grille de robustesse (λ_max, exclusion des petits λ) ;
  - choix final d’une configuration de référence.

---

## 4. Dimension spectrale d_s et T_log : résultats clés

### 4.1 Dimension spectrale small‑λ (premiers résultats)

En se concentrant sur la partie small‑λ du spectre (λ ≤ λ_max, typiquement λ_max = 0.1 ou 0.2) et en utilisant des fits **OLS** sur `log N(λ)` vs `log λ` :

- les premiers résultats donnent des pentes **très faibles** (slope ≈ 0.14–0.15) ;
- donc d_s = 2·slope ≈ **0.28–0.30** ;
- pour n ≈ 3265, cela implique un T_log très négatif :

  - (d_s − 4) ≈ −3.7 → T_log ≈ −3.7·ln(3265) ≪ 0.

Ces estimations sont **cohérentes entre bootstraps** sur les `λ` considérés, mais les diagnostics de régression révèlent :

- une qualité de fit correcte (R² ≈ 0.64–0.66) ;
- **un point fortement influent** par diagnostic (Cook >> 4/n) qui pèse lourd sur la pente.

### 4.2 Dimension spectrale robuste (Theil–Sen) et influence des points

Pour traiter l’influence de ces points extrêmes, plusieurs stratégies ont été appliquées :

- refit OLS **sans** les points identifiés comme influents ;
- estimation de pente via **Theil–Sen** (robuste) ;
- RANSAC comme vérification supplémentaire.

Les résultats typiques (Parties 8–9) :

- d_s_OLS_orig médiane ≈ 0.30 ;
- d_s_OLS_sans_infl ≈ 1.1 ;
- d_s_Theil–Sen (sur λ ≤ 0.2) médiane ≈ **1.5–1.7** ;
- d_s_RANSAC ≈ 1.1–1.3 selon les diagnostics.

Les tests appariés montrent :

- des différences hautement significatives entre OLS_orig et les méthodes robustes (p de Wilcoxon ~ 10⁻³) ;
- une **multiplication de la pente** (et donc de d_s) par un facteur ≈ 3–5 dès qu’on enlève un seul point ou qu’on passe à un estimateur robuste.

Conclusion :

- la valeur **numérique** de d_s small‑λ est **très sensible** au traitement des points influents ;
- mais pour tous ces choix raisonnables (d_s ≈ 0.3–1.7), on reste strictement **en dessous de 4**, donc T_log reste **négatif**.

### 4.3 Bloc `ds_remove_small_lambda` et d_s_robust per bootstrap

Le bloc `ds_remove_small_lambda` (Parties 10–11) consolide les d_s robustes via :

- lecture des résultats paired Theil–Sen :
  - `results/paired_levina_spectral_theilsen/paired_levina_spectral_theilsen_raw.csv` ;
- sélection de λ_max ≈ 0.2 (n_points_fit ≈ 15–18) ;
- reconstruction d’un tableau propre `ds_robust_per_b.csv` (150 bootstraps) avec :
  - `d_s_robust` médiane ≈ **1.56**, 
  - écart-type ≈ 0.07,
  - valeurs dans [1.38, 1.75].

Cette table sert de base à :

- un T_log local (avec n basé sur `n_points_fit` médian, ~15) essentiellement pour comparer des bootstraps entre eux ;
- une sélection des 15 bootstraps les plus proches de T_log ≈ 0 (candidats « quasi‑équilibre ») ;
- des diagnostics graphiques détaillés pour ces cas.

À ce stade, la conclusion reste :

- **pour la dynamique observée Sunspots**, une dimension spectrale robuste d_s ~ 1.5–1.7 est raisonnable ;
- en la combinant avec n ≈ 3265, T_log ≈ (d_s−4) ln(n) reste largement **< 0**, typiquement entre −20 et −15.

### 4.4 Pipeline autonome `sunspots_external` : d_s ≈ 2 et T_log ≈ −16

La Partie 12 fournit une validation indépendante :

- Kaggle → embedding (dim=10, k=10) → graphe k-NN → Laplacien normalisé ;
- calcul des 200 plus petites valeurs propres ;
- d_s point (Theil–Sen, λ ≤ 0.2) ≈ **2.00** (19 points utilisés) ;
- bootstrap (200 samples, resampling des eigenvalues) :
  - médiane d_s_boot ≈ **2.05**, IC95% ≈ [1.07, 4.42].

Propagation vers T_log (n=3265) :

- médiane T_log ≈ **−15.77** ;
- IC95% ≈ [−23.68, +3.42], avec une queue droite due à quelques d_s > 4 (outliers dans le bootstrap).

Une petite grille de robustesse (λ_max ∈ {0.1,0.2}, exclusion de 0..3 plus petits λ) montre :

- qu’exclure trop de petits λ ou prendre un λ_max trop large peut conduire à des d_s extrêmes (>4) sur très peu de points ;
- la configuration **λ_max = 0.2, exclude_k = 0** offre un bon compromis :
  - 19 points dans le fit small‑λ ;
  - d_s ≈ 2.0 ;
  - T_log ≈ −16.19.

Cette configuration est retenue comme **choix final** pour `sunspots_external`, consignée dans :

- `results/sunspots_external/final_choice_summary.csv` ;
- plot annoté `Nlambda_loglog_fit_final.png` ;
- note `run_ready_for_commit.txt`.

---

## 5. Dimension Levina–Bickel vs dimension spectrale : incompatibilité de niveau

Les parties 6–9 comparent en détail :

- l’estimateur de dimension intrinsèque **Levina–Bickel** (m_hat, basé sur les k plus proches voisins) ;
- la **dimension spectrale** d_s (pente small‑λ de log N(λ) vs log λ).

Principaux constats :

- Levina–Bickel donne :
  - médiane m_hat ≈ **7.9–8.0** sur 150 bootstraps ;
- d_s spectral (OLS ou Theil–Sen) donne des médianes ≪ 4 :
  - OLS small‑λ → d_s ≈ 0.3 ;
  - Theil–Sen λ_max=0.1 → d_s ≈ 0.8 ;
  - Theil–Sen λ_max=0.2 → d_s ≈ 1.5–2.0.

Tests appariés Levina – d_s (pour λ_max = 0.1, 0.2, 0.4) :

- différences moyennes ≈ 7.4–7.7 (énormes) ;
- p-values Wilcoxon ~ 10⁻²⁶ (différence extrêmement significative) ;
- corrélations de Spearman faibles ou nulles ;
- tailles d’effet gigantesques.

Interprétation :

- Levina–Bickel et la dimension spectrale mesurent des **aspects différents** de la géométrie :
  - Levina–Bickel = dimension intrinsèque locale basée sur les distances dans l’espace d’embedding ;
  - d_s = dimension spectrale liée à la loi d’échelle du spectre du Laplacien sur small‑λ.
- On ne peut pas les forcer à coïncider numériquement ;
- Utiliser m_hat ≈ 8 dans T_log conduirait à un T_log très positif (régime `Saturation`), **incompatible** avec les résultats spectrales et la physique intuitive du système.

Conclusion méthodologique :

- Pour la classification T_log des Sunspots, il est plus cohérent de se baser sur **d_s small‑λ robust** (Theil–Sen, λ_max ≈ 0.2) que sur m_hat.

---

## 6. Null-models et signifiance statistique

Les null-models (Partie 5 et écho dans la Partie 12) incluent :

- **Temporal shuffle** : permutation aléatoire de la série temporelle ;
- **Phase randomized** : randomisation de phase en domaine fréquentiel (préserve spectre de puissance mais détruit la phase temporelle).

Pour chacun :

- on reconstruit embedding → graphe k-NN → Laplacien → spectre ;
- on estime d_s via la même procédure ;
- on propage vers T_log ;
- on compare la distribution T_log(observé) vs T_log(null) via tests non paramétriques.

Résultats qualitatifs :

- les nulls ont tendance à produire des d_s plus élevés ou des spectres moins réguliers ;
- T_log(null) est généralement **moins négatif** (voire proche de 0) que T_log(observé) ;
- les p-values indiquent une **différence significative** entre la dynamique observée et les nulls.

Conclusion :

- le fait que Sunspots se trouve en **régime de Divergence** (d_s < 4 et T_log < 0) n’est pas un artefact trivial d’un simple bruit ou d’un shuffle ;
- il reflète une structure temporelle spécifique de la série.

---

## 7. Robustesse globale et limites

### 7.1 Points robustes

- **Signe de T_log** :
  - pour tous les choix raisonnables de d_est basés sur la dimension spectrale small‑λ (d_s ≲ 2.5), on a T_log(n=3265, d_est) **strictement négatif** ;
  - la classification en **régime de Divergence** est donc **robuste**.

- **Ordre de grandeur** :
  - selon que l’on utilise d=1, d_s≈0.3, d_s≈1.5 ou d_s≈2.0, T_log varie typiquement entre ~−25 et ~−15 ;
  - la conclusion « divergence forte » demeure.

- **Hyperparamètres** :
  - variations de embedding_dim (4..12) et de k_neighbors (4..12) ne changent pas qualitativement la conclusion ;
  - des configurations extrêmes peuvent modifier d_s, mais restent d_s < 4 dans les plages étudiées.

### 7.2 Points délicats / limitations

- **Absence de d_s canonique** :
  - la valeur numérique de d_s dépend fortement de :
    - la plage λ_max ;
    - la gestion des plus petites valeurs propres (exclusion ou non) ;
    - le choix d’OLS vs Theil–Sen vs RANSAC ;
    - la présence de points influents (Cook) ;
  - il n’existe pas une "dimension spectrale unique" pour Sunspots, mais plutôt un **intervalle plausible**.

- **Bootstrap d_s/T_log** :
  - la queue droite (d_s > 4) dans certains bootstraps agrandit artificiellement les intervalles de confiance de T_log ;
  - ces outliers sont souvent liés à peu de points small‑λ et devraient être analysés ou filtrés avec soin.

- **Null-models** :
  - les nulls doivent être construits de manière **strictement parallèle** au pipeline observé (mêmes hyperparamètres, même nombre d’eigenvalues, etc.) pour une interprétation rigoureuse ;
  - un seul run de null (comme dans `sunspots_external`) n’est pas suffisant pour une analyse de p-value précise.

---

## 8. Synthèse finale et recommandations

### 8.1 Synthèse scientifique pour Sunspots V0.5

1. **Régime T_log** :
   - toutes les déterminations de d_est basées sur la **dimension spectrale small‑λ** mènent à **T_log < 0** pour n ≈ 3265 ;
   - Sunspots est donc classé en **régime de Divergence** de manière robuste.

2. **Échelle de la divergence** :
   - pour des choix raisonnables de configuration (embedding_dim=10, k=10, λ_max=0.2, exclude_k=0, Theil–Sen), on obtient :
     - d_s ≈ 2.0 ;
     - T_log ≈ −16 (configuration finale `sunspots_external`).

3. **Levina–Bickel vs spectral** :
   - Levina–Bickel donne m_hat ≈ 8, incompatible numériquement avec d_s spectral ;
   - ces deux dimensions mesurent des choses différentes et ne peuvent pas être identifiées naïvement ;
   - pour T_log, il est recommandé d’utiliser **d_s small‑λ robuste**, pas m_hat.

4. **Null-models** :
   - les nulls (shuffle, phase randomized) produisent des T_log moins négatifs/plus proches de 0 ;
   - la dynamique Sunspots se distingue significativement de ces nulls → la divergence observée n’est pas triviale.

### 8.2 Recommandations pratiques pour l’utilisation du pipeline

- **Documenter la configuration** :
  - toujours préciser embedding_dim, tau, k_neighbors, λ_max, éventuelle exclusion de λ, et méthode de fit (OLS vs Theil–Sen) ;
  - garder trace des manifestes (`manifest_*.json`) et des fichiers `*_summary.csv`.

- **Utilisation par défaut pour Sunspots** :
  - adopter la configuration finale `sunspots_external` :
    - embedding_dim = 10, tau = 1 ;
    - k_neighbors = 10 ;
    - λ_max = 0.2 ;
    - exclude_k = 0 ;
    - fit Theil–Sen sur N(λ) vs λ ;
    - d_s ≈ 2.0, T_log ≈ −16.

- **Pour d’autres jeux de données** :
  - répliquer la structure du pipeline (Parties 1–12) mais :
    - ajuster embedding_dim/k_neighbors en fonction de la longueur de série et de la complexité attendue ;
    - tester plusieurs λ_max et options d’exclusion de petits λ ;
    - toujours vérifier les diagnostics : spectre, N(λ) log‑log, influence de points, histogrammes bootstrap.

En résumé, Sunspots V0.5 montre qu’une mise en œuvre soigneuse de la dimension spectrale et de T_log permet d’identifier de façon robuste un **régime de Divergence** pour le signal Sunspots, tout en cartographiant explicitement les zones d’incertitude (valeur exacte de d_s, choix de λ_max, null-models). Le rapport global et les 12 rapports de partie peuvent servir de modèle pour l’analyse de futurs pipelines MUTD v0.5/v0.5.5 sur d’autres domaines.
