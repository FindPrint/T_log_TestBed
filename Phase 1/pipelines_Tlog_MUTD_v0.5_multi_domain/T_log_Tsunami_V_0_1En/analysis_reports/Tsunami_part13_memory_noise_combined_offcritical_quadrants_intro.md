# Tsunami V0.1 – Partie 13 (cellules 96–103) : Mémoire + bruit combinés et résumé hors‑critique

## 1. Périmètre de la partie

Cette treizième partie correspond aux cellules **96–103** du notebook `Tsunami_part13.ipynb`, dérivé de `T_log_Tsunami_V_0_1En.ipynb`.

Elle :

- rappelle les résultats du Bloc 20bis sur la **dynamique locale T_log(t) sous mémoire** ;
- étend les tests à la combinaison **mémoire + bruit sur n_eff** à d=4 (Bloc 21) ;
- applique la même logique **mémoire + bruit** dans le cas **hors‑critique d = 3.95 et 4.05** (Bloc 22) ;
- prépare un Bloc 23 (non encore exécuté ici) sur la robustesse spatiale (quadrants géographiques) avec mémoire + bruit.

L’objectif est de tester si mémoire + bruit peuvent altérer les régimes imposés par d, ou si la frontière critique reste structurante.

---

## 2. Rappel Bloc 20bis – Dynamique locale T_log(t) avec mémoire (d = 3.95, 4.05)

Le premier commentaire récapitule le Bloc 20bis (déjà analysé en Partie 12) :

- `results/bloc20bis_memory_local.csv` contient, pour chaque bucket temporel, les valeurs :
  - `n_eff(t)` (sous EMA α=0.5 et Boxcar W=5) ;
  - `T_log(t, d)` ;
  - le régime local (Divergence / Saturation) ;
- la figure `results/bloc20bis_memory_local.png` montre que :
  - pour d=3.95, **tous** les T_log(t) sont négatifs → Divergence locale partout ;
  - pour d=4.05, **tous** les T_log(t) sont positifs → Saturation locale partout ;
- les noyaux (EMA vs Boxcar) modulent la forme temporelle (lissage, inertie), mais jamais le **signe** de T_log.

Interprétation :

- mémoire agit **localement** mais n’inverse pas les régimes ;
- la distinction Divergence vs Saturation reste entièrement contrôlée par d (3.95 vs 4.05).

---

## 3. Bloc 21 – Mémoire + bruit sur n_eff à d = 4

### 3.1 Méthode

Bloc 21 combine mémoire et bruit, en restant sur d=4 :

- agrégation du dataset en buckets temporels (`bucket` mensuel ou annuel) ;
- calcul de `counts[bucket]` ;
- application de deux noyaux :
  - **EMA** (α=0.5) → `EMA_alpha0.5` ;
  - **Boxcar** (W=5) → `Boxcar_W5` ;
- pour chaque noyau :
  - `n_eff_series` = comptes effectifs par bucket ;
  - `n_eff_global = sum(n_eff_series)` (arrondi) ;
- puis bruit multiplicatif sur `n_eff_global` :
  - `noise_levels = [0.01, 0.05, 0.10, 0.20]` ;
  - pour chaque eps et chaque signe ± : `n_noisy = round(n_eff_global * (1 ± eps))` ;
  - calcul de `T_log(n_noisy, d=4)` et du régime.

Résultats sauvegardés dans :

- `results/bloc21_memory_noise.csv` ;
- figure `results/bloc21_memory_noise.png` : T_log vs % de bruit, pour EMA et Boxcar.

### 3.2 Résultats et interprétation

La cellule de commentaire indique :

- **quel que soit** le noyau (EMA/Boxcar) et le niveau de bruit (±1..20 %), on obtient toujours :

\[
T_{\log}(n_{noisy}, d=4) = 0.000000 \quad \Rightarrow \text{Regime = Equilibrium}.
\]

- les courbes de T_log sont plates à 0 pour tous les cas ;
- les logs sont correctement mis à jour (`logs.txt`, `logs.csv`).

Interprétation :

- même en combinant mémoire + bruit sur n_eff, l’équilibre à d=4 reste **strictement inaltéré** ;
- ce bloc généralise les tests précédents :
  - bruit seul (Bloc 12) ;
  - mémoire seule (Bloc 14) ;
  - bruit + mémoire (Bloc 21) ;
- dans tous les cas, à d=4, le système reste à T_log=0 → Equilibrium.

Conclusion :

- l’équilibre spatio‑temporel d=4 est **structurellement stable** vis‑à‑vis des perturbations sur n, même lorsqu’elles sont modulées par des noyaux mémoire.

---

## 4. Bloc 22 – Mémoire + bruit hors‑critique (d = 3.95 et d = 4.05)

### 4.1 Méthode

Bloc 22 reprend la même logique que Bloc 21, mais cette fois en dimension **hors‑critique** :

- d_values = {3.95, 4.05} ;
- mêmes noyaux mémoire : `EMA_alpha0.5` et `Boxcar_W5` ;
- mêmes niveaux de bruit : `noise_levels = [0.01, 0.05, 0.10, 0.20]` ;
- pour chaque d, noyau et bruit (±eps) :
  - calcul de `n_eff_global` à partir de counts ;
  - `n_noisy = round(n_eff_global * (1 ± eps))` ;
  - calcul de `T_log(n_noisy, d)` ;
  - classification du régime.

Les résultats sont stockés dans :

- `results/bloc22_memory_noise_offcritical.csv` ;
- un graphique `results/bloc22_memory_noise_offcritical.png` montrant T_log vs bruit pour EMA/Boxcar, d=3.95 et d=4.05.

### 4.2 Résultats

La cellule de résumé indique :

- pour **d=3.95** :
  - T_log reste toujours **négatif** (environ −0.32 à −0.34) pour tous les noyaux et niveaux de bruit ;
  - régime = Divergence dans tous les cas ;
- pour **d=4.05** :
  - T_log reste toujours **positif** ;
  - régime = Saturation pour toutes les combinaisons ;
- mémoire + bruit ne font que déplacer légèrement la valeur numérique de T_log, sans jamais croiser zéro.

### 4.3 Interprétation

- pour d≠4, le **signe** de T_log est entièrement contrôlé par le signe de (d−4) ;
- les perturbations sur n_eff (bruit) et la structuration via mémoire n’en changent pas la nature ;
- cela confirme que :
  - **d est la variable structurante** pour le régime ;
  - mémoire et bruit sont plutôt des termes de "texture" qui modulent l’amplitude et la dynamique, pas la phase (Divergence vs Saturation).

---

## 5. Rôle de la Partie 13 dans le pipeline Tsunami V0.1

Cette Partie 13 termine l’analyse détaillée de la mémoire et du bruit en montrant que :

- à **d=4**, même la combinaison "mémoire + bruit" sur n_eff ne peut faire quitter l’équilibre (Bloc 21) ;
- à **d≈3.95** (légèrement sous‑critique) ou **d≈4.05** (sur‑critique), la combinaison "mémoire + bruit" n’empêche pas le régime divergence/saturation d’être maintenu (Bloc 22) ;
- mémoire (EMA, Boxcar) agit localement sur la dynamique des buckets mais ne change pas le signe de T_log, comme confirmé au niveau local (Block 20bis rappelé).

En synthèse :

- pour le dataset Tsunami, le modèle `T_log(n,d) = (d-4) ln(n)` présente un **point critique d=4** :
  - exactement équilibres pour d=4, robuste à toutes les perturbations sur n (y compris sous mémoire) ;
  - régimes Divergence/Saturation stables pour d légèrement sous/sur la frontière, même avec mémoire + bruit ;
- la Partie 13 confirme donc que la dimension d, plus que les détails de la dynamique (n_eff, mémoire), est la **clé de voûte** des régimes T_log.

Cela clôt la séquence de blocs 19–22 en offrant une image complète de l’influence de la mémoire et du bruit sur le modèle V0.1, et prépare le terrain pour des versions futures où d pourrait être couplé à des effets mémoire ou à des biais calibrés pour explorer des transitions de phase contrôlées.
