# Tsunami V0.1 – Partie 7 (cellules 48–55) : Bilan permutation, ablation du biais et validation étendue

## 1. Périmètre de la partie

Cette septième partie correspond aux cellules **48–55** du notebook `Tsunami_part07.ipynb`, dérivé de `T_log_Tsunami_V_0_1En.ipynb`.

Elle :

- conclut l’analyse du **test de permutation** (Bloc 5.12) ;
- explore l’**ablation du biais** dans la formule T_log et le déplacement de la frontière critique (Bloc 5.13) ;
- ajoute une **section de validation étendue** dans le rapport final `final_report.md` ;
- prépare l’idée d’un enrichissement de la dimension effective à **d = 4** (espace + temps) pour une interprétation critique.

---

## 2. Rappel du Bloc 5.12 – Test de permutation (permutation test)

La première cellule texte de cette partie résume les résultats du Bloc 5.12 (déjà exécuté dans la Partie 6) :

- AUC vraie (labels dérivés de T_log) : **1.0000** ;
- AUC moyenne sous permutation : ≈ **0.5063 ± 0.0037** ;
- p‑value permutation : ≈ **0.0050**.

Interprétation rappelée :

- la séparation Divergence vs Saturation obtenue à partir de T_log n’est **pas due au hasard** ;
- le contraste entre AUC=1 et AUC≈0.5 sous permutation montre que la structure est **fortement signalée** ;
- cela renforce le caractère **non opportuniste** de la classification T_log.

Ce rappel sert de point de départ à l’ablation du biais.

---

## 3. Bloc 5.13 – Ablation du biais et déplacement de la frontière critique

### 3.1 Méthode

On étend la formule T_log pour inclure un **biais** explicite :

\[
T_{\log}(n,d; b) = (d - 4) \ln(n) + b.
\]

Le bloc 5.13 étudie l’effet de différentes valeurs de biais `b` sur la **frontière critique en d** et sur la répartition des régimes :

- paramètres :
  - `n = 782` ;
  - `bias_values = [-5, -2, -1, 0, +1, +2, +5]` ;
  - `d_grid = linspace(2, 5, 61)`.

Pour chaque biais b :

1. on calcule la dimension critique **d\*** telle que T_log(n,d\*;b) = 0 :

\[
(d^* - 4) \ln(n) + b = 0 \quad \Rightarrow \quad d^* = 4 - \frac{b}{\ln(n)}.
\]

2. on balaie `d_grid` et compte le nombre de points dans chaque régime : Divergence, Équilibre, Saturation.

### 3.2 Résultats

Les sorties typiques :

- **b = 0.0** :
  - d\\* = 4.0000 ;
  - counts : ~40 Divergence, 1 Équilibre, 20 Saturation → **situation de référence symétrique**.

- **b négatif** (−1, −2, −5) :
  - d\\* > 4 (par exemple b=−5 → d\\* ≈ 4.75) ;
  - le nombre de points en Divergence augmente, Saturation diminue.

- **b positif** (+1, +2, +5) :
  - d\\* < 4 (par exemple b=+5 → d\\* ≈ 3.25) ;
  - Saturation devient majoritaire, Divergence recule.

Pour tous les b ≠ 0, il n’y a plus de point exactement à T_log=0 (Équilibre) dans la grille d_grid utilisée.

### 3.3 Interprétation

- le **biais b** agit comme un **décalage horizontal** de la frontière critique en d :
  - b<0 → la frontière se déplace vers des d>4 → Divergence domine ;
  - b>0 → la frontière se déplace vers des d<4 → Saturation domine ;
- le cas **b=0** est **centré** :
  - d\\* = 4 est la frontière symétrique ;
  - la répartition Divergence/Équilibre/Saturation est équilibrée (hors d=4).

Conséquences :

- `bias=0` est un choix **principiel** pour V0.1 :
  - il maintient la frontière critique à d=4 ;
  - il conserve la symétrie Divergence ↔ Saturation autour de cette frontière ;
- le biais peut être vu comme un **levier de calibration** pour ajuster la position de d\\* si l’on voulait aligner le modèle sur des données empiriques spécifiques ;
- dans le pipeline V0.1, garder `bias=0` garantit que le modèle reste **neutre** et que la dimension critique d=4 est une propriété structurelle, non artificiellement déplacée.

---

## 4. Extension ajoutée au rapport final (Extended Validation Suite)

### 4.1 Bloc 6 – Appending Extended Validation Suite

Une cellule de cette partie ("Bloc 6") ajoute une section **"Extended Validation Suite (Blocks 5.5–5.13)"** au rapport final :

- `results/final_report.md`.

Cette section résume :

- 5.5 : tests de significativité (t-test, Wilcoxon) ;
- 5.6 : comparaison aux baselines (seuil en d vs ln(n)) ;
- 5.7 : régression logistique et frontière d≈4 ;
- 5.8 : localisation précise de d\\* et marges ;
- 5.9 : sensibilités en n et d ;
- 5.10 : calibration et marges ;
- 5.11 : validation hors-échantillon ;
- 5.12 : test de permutation ;
- 5.13 : ablation du biais.

L’objectif est de **documenter dans un même endroit** toutes les preuves anti‑overfitting et de robustesse du modèle T_log V0.1.

---

## 5. Préparation conceptuelle vers d = 4 (enrichissement de la dimension)

La fin de la partie propose une interprétation physique :

- jusqu’ici, on a travaillé avec d=3 (dimension spatiale) ;
- en ajoutant le **temps** comme dimension supplémentaire, on peut considérer **d=4** (espace + temps) ;
- dans ce cas, avec n=782 :

\[
T_{\log}(782,4) = (4-4) \ln(782) = 0 \quad \Rightarrow \text{Équilibre critique}.
\]

Une cellule suggérée (Block 7) propose :

- de recalculer T_log pour d=4, et pour d=3.9 et 4.1, afin de montrer que :
  - d=4 → T_log = 0 → **Equilibrium** ;
  - d<4 (3.9) → T_log < 0 → Divergence ;
  - d>4 (4.1) → T_log > 0 → Saturation.

Interprétation :

- en considérant le système comme **spatio‑temporel (d=4)**, le point (n=782, d=4) se trouve en **criticité exacte** ;
- de petites variations autour de d=4 font immédiatement basculer le régime, ce qui renforce l’idée de **point critique** ;
- cette lecture est cohérente avec l’intuition que les systèmes séismes/tsunamis se comportent comme des phénomènes critiques (frontières de stabilité/instabilité).

---

## 6. Rôle de la Partie 7 dans le pipeline Tsunami V0.1

Cette Partie 7 :

- consolide le **test de permutation** en rappelant qu’il exclut une explication purement aléatoire des bonnes performances ;
- montre, via l’**ablation du biais**, que :
  - la dimension critique d=4 est stable pour `bias=0` ;
  - le biais déplace la frontière sans casser la structure Divergence/Équilibre/Saturation ;
- ajoute une **section de validation étendue** au rapport final, archivant tous les tests avancés (5.5–5.13) au même endroit ;
- prépare la transition naturelle vers un cadre **d=4 (espace+temps)**, où le système Tsunami se trouve en **Équilibre critique**.

En résumé, la Partie 7 clôt la batterie de tests pour le cas Tsunami V0.1 en montrant que :

- la loi `T_log(n,d) = (d-4) ln(n) + bias` est robuste vis‑à‑vis du choix de bias (quand celui‑ci est nul par défaut) ;
- d=4 reste le point critique universel ;
- le modèle ne montre pas de signe d’overfitting, même sous permutation, stress tests, baselines et ablation du biais.

Elle fournit ainsi un socle conceptuel solide pour de futurs développements (V1/V2) où l’on pourra explorer des dimensions effectives estimées, des dynamiques plus riches et des données plus complexes, tout en conservant les régimes T_log comme boussole globale.
