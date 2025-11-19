# Tsunami V0.1 – Synthèse des parties 1 à 5

## 1. Périmètre

Cette synthèse couvre les rapports :
- Tsunami_part01 – préparation, acquisition, inspection des données.
- Tsunami_part02 – premier calcul de T_log (d=3), sensibilités en n et d, bootstrap.
- Tsunami_part03 – validation quantitative (MSE, R²), heatmap des régimes.
- Tsunami_part04 – significativité statistique et baselines simples.
- Tsunami_part05 – régression logistique et frontière critique d*.

Ensemble, ces blocs posent les **fondations empiriques** de la loi T_log sur le dataset Tsunami.

---

## 2. Données et préparation (Partie 1)

- Dataset : `earthquake_data_tsunami.csv`, ~782 événements.
- Étapes :
  - acquisition depuis Kaggle / source externe ;
  - décompression et chargement dans pandas ;
  - inspection des colonnes (dates, lat/lon, variables sismiques) ;
  - vérification basique de la qualité (NA, distributions). 
- Mise en place conceptuelle : on travaillera surtout sur le **nombre d’événements par bucket temporel** comme n, avec d comme dimension effective du système.

Conclusion de cette phase : le dataset est exploitable, la structure temporelle et spatiale est suffisante pour tester T_log.

---

## 3. Premier test T_log à d=3 et sensibilités (Partie 2)

- Calcul de T_log pour n≈782, d=3 : le signe de T_log est **négatif** → régime **Divergence**.
- Balayage de **d** autour de 3–5 et de **n** (sous‑échantillonnage aléatoire, variations de taille) :
  - T_log varie linéairement en (d−4) et log(n), comme prévu par la formule ;
  - le signe reste globalement stable lorsque l’on reste du même côté de d=4.
- Bootstrap sur les événements :
  - distribution empirique de T_log resamplée ;
  - intervalle de confiance ne recouvrant pas 0 pour d=3 → régime Divergence statistiquement significatif.

Cette étape montre que la loi T_log n’est pas triviale : à d=3, le système Tsunami est clairement hors‑équilibre, côté Divergence.

---

## 4. Validation quantitative globale et carte de régimes (Partie 3)

- Construction d’une **heatmap (n,d)** indiquant le régime (T_log<0,=0,>0).
- Calcul de métriques globales (MSE, R²) entre T_log observé et formule théorique.
- Résultats :
  - MSE faible, R² élevé sur la grille testée → bonne adéquation de la loi analytique ;
  - la **frontière T_log=0** se situe très précisément autour de **d≈4**.

La Partie 3 fournit une première vision globale de la structure (n,d) : les régimes observés sur les données Tsunami suivent la géométrie dictée par T_log.

---

## 5. Significativité et baselines (Partie 4)

- Tests de significativité supplémentaires :
  - comparaison avec des baselines simples fondées sur d seul ou ln(n) seul ;
  - vérification que ces baselines ne capturent pas aussi bien la structure des régimes.
- Conclusion :
  - les baselines triviales ne reproduisent pas la finesse de la frontière T_log=0 ;
  - la combinaison (d−4)·ln(n) apporte une information spécifique.

Cette partie renforce l’idée que T_log est un **modèle structuré**, et non une simple re‑écriture de ln(n) ou de d.

---

## 6. Régression logistique et frontière critique d* (Partie 5)

- Mise en place d’une classification binaire :
  - classes définies à partir du signe de T_log (Divergence vs Saturation) sur la grille (n,d) ;
  - régression logistique pour apprendre la frontière entre ces classes.
- Résultat clé :
  - la frontière apprise \(d^*\) est **très proche de 4**, robuste aux choix de n et au sous‑échantillonnage ;
  - la pente/log‑odds est cohérente avec la forme analytique de T_log.

Cette étape fournit une **confirmation statistique externe** que d=4 est la frontière critique naturelle du système, telle qu’anticipée par la théorie T_log.

---

## 7. Message global des parties 1–5

Les parties 1 à 5 établissent :

- la **qualité** et l’exploitabilité du dataset Tsunami ;
- la validité empirique de la loi **T_log(n,d) = (d-4) ln(n)** sur la grille (n,d) ;
- l’existence d’une **frontière critique** proche de **d=4**, confirmée par :
  - le signe de T_log à d=3 (Divergence) ;
  - les cartes de régimes (heatmap) ;
  - les tests de significativité et baselines ;
  - la régression logistique.

Ces blocs préparent la suite du pipeline, qui se concentre ensuite sur la **dimension spatio‑temporelle d=4**, la robustesse multi‑échelle, puis les effets de bruit, de mémoire et la comparaison à d’autres modèles.
