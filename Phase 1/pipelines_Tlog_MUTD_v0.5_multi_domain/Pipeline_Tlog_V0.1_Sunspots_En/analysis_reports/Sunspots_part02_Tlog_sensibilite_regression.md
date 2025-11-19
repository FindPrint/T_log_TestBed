# Sunspots V0.5 – Partie 2 (cellules 10–19) : Sensibilité de T_log, balayage en n et régression

## 1. Périmètre de la partie

Cette deuxième partie correspond aux cellules **10–19** du notebook `Sunspots_part02.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle couvre trois blocs principaux :

- **Block 4 — Sensitivity of T_log as a function of the dimension d** ;
- **Block 5 — Sweeping of T_log(n) for d = 3 and d = 5** ;
- **Block 6 — Linear Regression of T_log(n) vs ln(n)**.

Une dernière cellule introduit le **Block 8 — Validation by subsampling (bootstrap on Sunspots)**, dont le code se trouve dans la partie suivante.

L’objectif de cette partie est de **tester la structure analytique** de la formule :

\[
T_{\log}(n,d) = (d - 4)\,\ln(n)\quad (\text{biais = 0}),
\]

avant d’attaquer des tests plus avancés (bootstrap, dimension spectrale, null‑models).

---

## 2. Block 4 – Sensibilité de T_log en fonction de d

### 2.1 Paramétrage

- Taille du système fixée à **n = 3265** (nombre de mois dans Sunspots.csv, déjà vérifié dans la Partie 1) ;
- dimensions effectives testées : `d_values = 1, 2, 3, 4, 5, 6` ;
- calcul de `T_log = (d−4)*ln(n_const)` pour chaque d (biais=0) ;
- classification des régimes :
  - `T_log > 0` → *Saturation* ;
  - `T_log ≈ 0` (tolérance stricte) → *Équilibre* ;
  - `T_log < 0` → *Divergence*.

### 2.2 Résultats numériques

Un tableau `Tlog_vs_d_table.csv` est sauvegardé dans `results/` avec les colonnes `d, n, T_log, regime`. Exemple :

- d = 1 : T_log ≈ −24.27 → Divergence ;
- d = 2 : T_log ≈ −16.18 → Divergence ;
- d = 3 : T_log ≈ −8.09 → Divergence ;
- d = 4 : T_log = 0 → Équilibre ;
- d = 5 : T_log ≈ +8.09 → Saturation ;
- d = 6 : T_log ≈ +16.18 → Saturation.

Une figure `results/Tlog_vs_d_plot.png` affiche :

- les points (d, T_log) colorés selon le régime (rouge = divergence, orange = équilibre, vert = saturation) ;
- une ligne horizontale T_log = 0 et une ligne verticale d = 4, marquant le point critique.

### 2.3 Interprétation

- Pour **d < 4**, T_log est **strictement négatif** → régime de **Divergence**.
- À **d = 4**, T_log = 0 → **Équilibre**.
- Pour **d > 4**, T_log est **strictement positif** → régime de **Saturation**.

La dépendance est **strictement linéaire en (d−4)** (pente constante en fonction de d), ce qui confirme le comportement critique prévu par la définition de T_log.

---

## 3. Block 5 – Balayage de T_log(n) pour d = 3 et d = 5

### 3.1 Paramétrage

On fait varier la taille du système `n` dans l’intervalle `[10, 10000]` :

- 50 valeurs de n, espacées linéairement entre 10 et 10000 ;
- deux dimensions fixées :
  - d = 3 (zone de divergence) ;
  - d = 5 (zone de saturation).

On calcule :

- `Tlog_d3 = (3−4)*ln(n)` ;
- `Tlog_d5 = (5−4)*ln(n)` ;

puis on sauvegarde `Tlog_vs_n_d3_d5.csv` et une figure `Tlog_vs_n_d3_d5_plot.png`.

### 3.2 Résultats

- Pour **d = 3** :
  - T_log est **toujours négatif** ;
  - sa valeur diminue (en valeur) avec `ln(n)` : plus n augmente, plus le régime de divergence est prononcé.

- Pour **d = 5** :
  - T_log est **toujours positif** ;
  - sa valeur augmente avec `ln(n)` : plus n augmente, plus la saturation est marquée.

- Symétrie :
  - `T_log(n, d=5) = − T_log(n, d=3)` pour tout n ;
  - c’est une conséquence directe de la formule `(d−4)·ln(n)` avec d=3 et d=5.

La figure montre deux courbes symétriques par rapport à T_log = 0, l’une en rouge (d=3), l’autre en vert (d=5).

### 3.3 Interprétation

- Le **signe** de (d−4) contrôle le **type de régime** (divergence vs saturation) ;
- la **magnitude** |T_log| croît comme `|d−4|·ln(n)` :
  - systèmes plus grands (n élevé) → T_log plus extrême (plus négatif en divergence, plus positif en saturation) ;
- le modèle ne montre **aucune anomalie numérique** : pas de NaN, pas de comportements erratiques.

Ce bloc démontre que la formule T_log est **log‑linéaire en n**, avec une symétrie structurée entre d=3 et d=5.

---

## 4. Block 6 – Régression linéaire T_log(n) vs ln(n)

### 4.1 Objectif

Ce bloc teste empiriquement la relation :

\[
T_{\log}(n,d) = (d-4)\,\ln(n) \quad\Rightarrow\quad T_{\log} \text{ linéaire en } \ln(n) \text{ avec pente } d-4.
\]

Pour cela :

1. On charge `results/Tlog_vs_n_d3_d5.csv` ;
2. On ajoute la colonne `ln_n = ln(n)` ;
3. On fait une régression OLS (statsmodels) **T_log(n) = a + b·ln(n)** séparément pour :
   - `T_log_d3` (d=3) ;
   - `T_log_d5` (d=5).

### 4.2 Résultats

Les paramètres estimés sont stockés dans `results/regression_Tlog_ln_n.csv` et affichés dans le notebook :

- Pour **d = 3** :
  - pente estimée ≈ **−1.0000** ;
  - pente théorique = **d−4 = −1** ;
  - intercept ≈ 0 ;
  - R² = 1.0 ;
  - p‑value (pente) = 0.

- Pour **d = 5** :
  - pente estimée ≈ **+1.0000** ;
  - pente théorique = **d−4 = +1** ;
  - intercept ≈ 0 ;
  - R² = 1.0 ;
  - p‑value (pente) = 0.

Les deux régressions donnent donc **un fit parfait** (à la précision numérique près), avec une pente exactement égale à d−4.

### 4.3 Interprétation

- La relation **T_log vs ln(n)** est confirmée empiriquement comme **strictement linéaire**, sans dérive ni biais caché ;
- la pente dépend uniquement de d (d−4), comme le prévoit la théorie ;
- `R² = 1` et `p_value ≈ 0` montrent que **toute la variance** de T_log est expliquée par ln(n) dans ce cadre.

Ce bloc valide que la partie "T_log V0.1" du pipeline se comporte comme une **loi analytique exacte** sur ce jeu de tests.

---

## 5. Préparation pour la suite (Block 8 – Bootstrap)

La dernière cellule de cette tranche introduit le **Block 8 — Validation by subsampling (bootstrap on Sunspots)** :

- l’idée est de tester la **stabilité de T_log** lorsque l’on perturbe l’échantillon (bootstrap) ;
- on utilise d=1 et des sous‑échantillons de taille 1000 tirés avec remise ;
- on enregistrera la distribution de T_log (moyenne, écart‑type, histogramme).

Le code de ce bootstrap se trouve dans la tranche suivante (Partie 3). Cette Partie 2 a pour rôle de **valider la structure théorique** de T_log avant d’examiner sa stabilité numérique sous rééchantillonnage.

---

## 6. Rôle de la Partie 2 dans le pipeline Sunspots V0.5

Cette deuxième partie :

- confirme que la formule **T_log(n,d) = (d−4)ln(n)** se comporte exactement comme prévu en fonction de `d` et de `n` ;
- montre que la classification en **Divergence / Équilibre / Saturation** est contrôlée uniquement par :
  - le signe de (d−4) ;
  - la taille logarithmique du système (ln n) ;
- fournit des **fichiers de référence** (`Tlog_vs_d_table.csv`, `Tlog_vs_n_d3_d5.csv`, `regression_Tlog_ln_n.csv`, et les plots associés) qui serviront de base à la comparaison avec :
  - les bootstraps (Parties 3–4) ;
  - les estimations de dimension effective via graphes de Takens et spectre de Laplacien (Parties ultérieures).

En résumé, la Partie 2 verrouille le fait que le pipeline Sunspots V0.5 implémente bien **la loi analytique T_log V0.1**, et qu’il le fait de manière numériquement propre avant de passer à des tests plus sophistiqués (spectre, d_s, null‑models).
