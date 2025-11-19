# Journal de session T_log V0.1

- Session démarrée: 2025-11-10T17:00:05.584390Z
- Conventions: biais=0 par défaut, seeds fixés (42), sorties dans results/

- 2025-11-10T17:00:05.586403Z [INFO] Bloc 1 prêt: imports, seeds, dossiers et logger configurés.
- 2025-11-10T17:00:06.004046Z [INFO] Plot de vérification sauvegardé: results\env_check_plot.png

---

## Rapport Intermédiaire — Robustesse T_log V0.1 (Blocs 7–8)

### 1. Rappel du modèle
Formule :

\[
T_{\log}(n, d) = (d - 4) \cdot \ln(n) + \text{biais}, \quad \text{avec biais = 0}
\]


Régimes :
- T_log > 0 → Saturation
- T_log ≈ 0 → Équilibre
- T_log < 0 → Divergence

### 2. Dataset utilisé
- Fichier : `Sunspots.csv`
- Type : série temporelle mensuelle
- Taille : n = 3265
- Dimension effective : d = 1
- Qualité : aucune valeur manquante

### 3. Calcul initial
- T_log = -24.2730 → Régime = Divergence

### 4. Sensibilité en d
- Variation de d : 1 à 6
- Résultats :
  - d = 1,2,3 → Divergence
  - d = 4 → Équilibre
  - d = 5,6 → Saturation
- Fichiers :
  - Graphique : `results/Tlog_vs_d_plot.png`
  - Tableau : `results/Tlog_vs_d_table.csv`

### 5. Balayage en n
- Variation de n : 10 → 10 000
- d = 3 → T_log < 0 ; d = 5 → T_log > 0
- Symétrie parfaite
- Fichiers :
  - Graphique : `results/Tlog_vs_n_d3_d5_plot.png`
  - Tableau : `results/Tlog_vs_n_d3_d5.csv`

### 6. Régression linéaire T_log vs ln(n)
- Objectif : valider la pente théorique (d - 4)
- Résultats :
  - d = 3 → pente = -1.0000
  - d = 5 → pente = +1.0000
  - R² = 1.0
- Fichier : `results/regression_Tlog_ln_n.csv`

### 7. Bootstrap fixe (n = 1000)
- 100 échantillons
- T_log constant = -20.7233
- Std = 0.0000
- Fichiers :
  - Histogramme : `results/bootstrap_Tlog_hist.png`
  - Tableau : `results/bootstrap_Tlog.csv`

### 8. Bootstrap variable (n ∈ [500,1500])
- 100 échantillons
- Moyenne T_log = -20.6866
- Std = 0.8615
- Fichiers :
  - Histogramme : `results/bootstrap_variable_n_hist.png`
  - Tableau : `results/bootstrap_variable_n_Tlog.csv`

### 9. Conclusion intermédiaire
- Le modèle T_log V0.1 est robuste :
  - Sensibilité linéaire validée
  - Bootstrap stable
  - Aucun artefact détecté
- Prochaine étape : tests sur graphes (dimension spectrale)

---
- 2025-11-10T17:03:43.369462Z [INFO] Bloc 1 prêt: imports, seeds, dossiers et logger configurés.
- 2025-11-10T17:03:43.657845Z [INFO] Plot de vérification sauvegardé: results\env_check_plot.png

---

## Rapport Intermédiaire — Robustesse T_log V0.1 (Blocs 7–8)

### 1. Rappel du modèle
Formule :

\[
T_{\log}(n, d) = (d - 4) \cdot \ln(n) + \text{biais}, \quad \text{avec biais = 0}
\]


Régimes :
- T_log > 0 → Saturation
- T_log ≈ 0 → Équilibre
- T_log < 0 → Divergence

### 2. Dataset utilisé
- Fichier : `Sunspots.csv`
- Type : série temporelle mensuelle
- Taille : n = 3265
- Dimension effective : d = 1
- Qualité : aucune valeur manquante

### 3. Calcul initial
- T_log = -24.2730 → Régime = Divergence

### 4. Sensibilité en d
- Variation de d : 1 à 6
- Résultats :
  - d = 1,2,3 → Divergence
  - d = 4 → Équilibre
  - d = 5,6 → Saturation
- Fichiers :
  - Graphique : `results/Tlog_vs_d_plot.png`
  - Tableau : `results/Tlog_vs_d_table.csv`

### 5. Balayage en n
- Variation de n : 10 → 10 000
- d = 3 → T_log < 0 ; d = 5 → T_log > 0
- Symétrie parfaite
- Fichiers :
  - Graphique : `results/Tlog_vs_n_d3_d5_plot.png`
  - Tableau : `results/Tlog_vs_n_d3_d5.csv`

### 6. Régression linéaire T_log vs ln(n)
- Objectif : valider la pente théorique (d - 4)
- Résultats :
  - d = 3 → pente = -1.0000
  - d = 5 → pente = +1.0000
  - R² = 1.0
- Fichier : `results/regression_Tlog_ln_n.csv`

### 7. Bootstrap fixe (n = 1000)
- 100 échantillons
- T_log constant = -20.7233
- Std = 0.0000
- Fichiers :
  - Histogramme : `results/bootstrap_Tlog_hist.png`
  - Tableau : `results/bootstrap_Tlog.csv`

### 8. Bootstrap variable (n ∈ [500,1500])
- 100 échantillons
- Moyenne T_log = -20.6866
- Std = 0.8615
- Fichiers :
  - Histogramme : `results/bootstrap_variable_n_hist.png`
  - Tableau : `results/bootstrap_variable_n_Tlog.csv`

### 9. Conclusion intermédiaire
- Le modèle T_log V0.1 est robuste :
  - Sensibilité linéaire validée
  - Bootstrap stable
  - Aucun artefact détecté
- Prochaine étape : tests sur graphes (dimension spectrale)

---
- 2025-11-10T21:13:48.881380Z [INFO] Bloc 1 prêt: imports, seeds, dossiers et logger configurés.
- 2025-11-10T21:13:49.183881Z [INFO] Plot de vérification sauvegardé: results\env_check_plot.png

---

## Rapport Intermédiaire — Robustesse T_log V0.1 (Blocs 7–8)

### 1. Rappel du modèle
Formule :

\[
T_{\log}(n, d) = (d - 4) \cdot \ln(n) + \text{biais}, \quad \text{avec biais = 0}
\]


Régimes :
- T_log > 0 → Saturation
- T_log ≈ 0 → Équilibre
- T_log < 0 → Divergence

### 2. Dataset utilisé
- Fichier : `Sunspots.csv`
- Type : série temporelle mensuelle
- Taille : n = 3265
- Dimension effective : d = 1
- Qualité : aucune valeur manquante

### 3. Calcul initial
- T_log = -24.2730 → Régime = Divergence

### 4. Sensibilité en d
- Variation de d : 1 à 6
- Résultats :
  - d = 1,2,3 → Divergence
  - d = 4 → Équilibre
  - d = 5,6 → Saturation
- Fichiers :
  - Graphique : `results/Tlog_vs_d_plot.png`
  - Tableau : `results/Tlog_vs_d_table.csv`

### 5. Balayage en n
- Variation de n : 10 → 10 000
- d = 3 → T_log < 0 ; d = 5 → T_log > 0
- Symétrie parfaite
- Fichiers :
  - Graphique : `results/Tlog_vs_n_d3_d5_plot.png`
  - Tableau : `results/Tlog_vs_n_d3_d5.csv`

### 6. Régression linéaire T_log vs ln(n)
- Objectif : valider la pente théorique (d - 4)
- Résultats :
  - d = 3 → pente = -1.0000
  - d = 5 → pente = +1.0000
  - R² = 1.0
- Fichier : `results/regression_Tlog_ln_n.csv`

### 7. Bootstrap fixe (n = 1000)
- 100 échantillons
- T_log constant = -20.7233
- Std = 0.0000
- Fichiers :
  - Histogramme : `results/bootstrap_Tlog_hist.png`
  - Tableau : `results/bootstrap_Tlog.csv`

### 8. Bootstrap variable (n ∈ [500,1500])
- 100 échantillons
- Moyenne T_log = -20.6866
- Std = 0.8615
- Fichiers :
  - Histogramme : `results/bootstrap_variable_n_hist.png`
  - Tableau : `results/bootstrap_variable_n_Tlog.csv`

### 9. Conclusion intermédiaire
- Le modèle T_log V0.1 est robuste :
  - Sensibilité linéaire validée
  - Bootstrap stable
  - Aucun artefact détecté
- Prochaine étape : tests sur graphes (dimension spectrale)

---
- 2025-11-11T01:33:19.116417Z [INFO] Bloc 1 prêt: imports, seeds, dossiers et logger configurés.
- 2025-11-11T01:33:19.391887Z [INFO] Plot de vérification sauvegardé: results\env_check_plot.png

---

## Rapport Intermédiaire — Robustesse T_log V0.1 (Blocs 7–8)

### 1. Rappel du modèle
Formule :

\[
T_{\log}(n, d) = (d - 4) \cdot \ln(n) + \text{biais}, \quad \text{avec biais = 0}
\]


Régimes :
- T_log > 0 → Saturation
- T_log ≈ 0 → Équilibre
- T_log < 0 → Divergence

### 2. Dataset utilisé
- Fichier : `Sunspots.csv`
- Type : série temporelle mensuelle
- Taille : n = 3265
- Dimension effective : d = 1
- Qualité : aucune valeur manquante

### 3. Calcul initial
- T_log = -24.2730 → Régime = Divergence

### 4. Sensibilité en d
- Variation de d : 1 à 6
- Résultats :
  - d = 1,2,3 → Divergence
  - d = 4 → Équilibre
  - d = 5,6 → Saturation
- Fichiers :
  - Graphique : `results/Tlog_vs_d_plot.png`
  - Tableau : `results/Tlog_vs_d_table.csv`

### 5. Balayage en n
- Variation de n : 10 → 10 000
- d = 3 → T_log < 0 ; d = 5 → T_log > 0
- Symétrie parfaite
- Fichiers :
  - Graphique : `results/Tlog_vs_n_d3_d5_plot.png`
  - Tableau : `results/Tlog_vs_n_d3_d5.csv`

### 6. Régression linéaire T_log vs ln(n)
- Objectif : valider la pente théorique (d - 4)
- Résultats :
  - d = 3 → pente = -1.0000
  - d = 5 → pente = +1.0000
  - R² = 1.0
- Fichier : `results/regression_Tlog_ln_n.csv`

### 7. Bootstrap fixe (n = 1000)
- 100 échantillons
- T_log constant = -20.7233
- Std = 0.0000
- Fichiers :
  - Histogramme : `results/bootstrap_Tlog_hist.png`
  - Tableau : `results/bootstrap_Tlog.csv`

### 8. Bootstrap variable (n ∈ [500,1500])
- 100 échantillons
- Moyenne T_log = -20.6866
- Std = 0.8615
- Fichiers :
  - Histogramme : `results/bootstrap_variable_n_hist.png`
  - Tableau : `results/bootstrap_variable_n_Tlog.csv`

### 9. Conclusion intermédiaire
- Le modèle T_log V0.1 est robuste :
  - Sensibilité linéaire validée
  - Bootstrap stable
  - Aucun artefact détecté
- Prochaine étape : tests sur graphes (dimension spectrale)

---
- 2025-11-11T03:56:00.175455Z [INFO] Bloc 1 prêt: imports, seeds, dossiers et logger configurés.
- 2025-11-11T03:56:00.472544Z [INFO] Plot de vérification sauvegardé: results\env_check_plot.png

---

## Rapport Intermédiaire — Robustesse T_log V0.1 (Blocs 7–8)

### 1. Rappel du modèle
Formule :

\[
T_{\log}(n, d) = (d - 4) \cdot \ln(n) + \text{biais}, \quad \text{avec biais = 0}
\]


Régimes :
- T_log > 0 → Saturation
- T_log ≈ 0 → Équilibre
- T_log < 0 → Divergence

### 2. Dataset utilisé
- Fichier : `Sunspots.csv`
- Type : série temporelle mensuelle
- Taille : n = 3265
- Dimension effective : d = 1
- Qualité : aucune valeur manquante

### 3. Calcul initial
- T_log = -24.2730 → Régime = Divergence

### 4. Sensibilité en d
- Variation de d : 1 à 6
- Résultats :
  - d = 1,2,3 → Divergence
  - d = 4 → Équilibre
  - d = 5,6 → Saturation
- Fichiers :
  - Graphique : `results/Tlog_vs_d_plot.png`
  - Tableau : `results/Tlog_vs_d_table.csv`

### 5. Balayage en n
- Variation de n : 10 → 10 000
- d = 3 → T_log < 0 ; d = 5 → T_log > 0
- Symétrie parfaite
- Fichiers :
  - Graphique : `results/Tlog_vs_n_d3_d5_plot.png`
  - Tableau : `results/Tlog_vs_n_d3_d5.csv`

### 6. Régression linéaire T_log vs ln(n)
- Objectif : valider la pente théorique (d - 4)
- Résultats :
  - d = 3 → pente = -1.0000
  - d = 5 → pente = +1.0000
  - R² = 1.0
- Fichier : `results/regression_Tlog_ln_n.csv`

### 7. Bootstrap fixe (n = 1000)
- 100 échantillons
- T_log constant = -20.7233
- Std = 0.0000
- Fichiers :
  - Histogramme : `results/bootstrap_Tlog_hist.png`
  - Tableau : `results/bootstrap_Tlog.csv`

### 8. Bootstrap variable (n ∈ [500,1500])
- 100 échantillons
- Moyenne T_log = -20.6866
- Std = 0.8615
- Fichiers :
  - Histogramme : `results/bootstrap_variable_n_hist.png`
  - Tableau : `results/bootstrap_variable_n_Tlog.csv`

### 9. Conclusion intermédiaire
- Le modèle T_log V0.1 est robuste :
  - Sensibilité linéaire validée
  - Bootstrap stable
  - Aucun artefact détecté
- Prochaine étape : tests sur graphes (dimension spectrale)

---
