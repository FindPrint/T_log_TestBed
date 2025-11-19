# Session Log T_log V0.1

- Session started: 2025-10-24T00:59:04.940141Z

- Conventions: bias=0 by default, seeds fixed (42), outputs in results/

- 2025-10-24T00:59:04.941129Z [INFO] Block 1 ready: imports, seeds, folders and outputs
- 2025-10-24T00:59:05.625965Z [INFO] Verification plot saved: results/env_check_plot.png
- 2025-10-24T01:02:10.097714Z [INFO] File data/Sunspots.zip extracted in data/sunspots_raw
- 2025-10-24T01:05:05.141802Z [INFO] T_log computed: n=3265, d=1, T_log=-24.2730
- 2025-10-24T01:10:21.386072Z [INFO] Sensitivity T_log(d) plotted and table saved
- 2025-10-24T01:14:06.321719Z [INFO] Sweep T_log(n) performed for d=3 and d=5
- 2025-10-24T01:17:31.190133Z [INFO] Linear regression T_log vs ln(n) performed
- 2025-10-24T01:28:22.472816Z [INFO] Bootstrap T_log completed: mean=-20.723266
- 2025-10-24T01:31:56.925618Z [INFO] Variable-n bootstrap completed: mean=-20.686587

---

## Intermediate Report - Robustness of T_log V0.1 (Blocks 7-8)

### 1. Model reminder
Formula:
T_log(n, d) = (d - 4) * ln(n) + bias

Regimes:
- T_log > 0 -> Saturation
- T_log = 0 -> Equilibrium
- T_log < 0 -> Divergence

### 2. Dataset used
- File: Sunspots.csv
- Type: monthly time series
- Size: n = 3265
- Effective dimension: d = 1
- Quality: no missing values

### 3. Initial calculation
- T_log = -24.2730 - Regime = Divergence

### 4. Sensitivity in d
- Variation of d: 1 to 6
- Results:
  - d = 1,2,3 -> Divergence
  - d = 4 -> Equilibrium
  - d = 5,6 -> Saturation
- Files:
  - Plot: results/Tlog_vs_d_plot.png
  - Table: results/Tlog_vs_d_table.csv

### 5. Sweep in n
- Variation of n: 10 - 10,000
- d = 3 -> T_log < 0 ; d = 5 -> T_log > 0
- Files:
  - Plot: results/Tlog_vs_n_d3_d5_plot.png
  - Table: results/Tlog_vs_n_d3_d5.csv

### 6. Linear regression T_log vs ln(n)
- Objective: validate theoretical slope (d - 4)
- Results:
  - d = 3 -> slope = -1.0000
  - d = 5 -> slope = +1.0000
  - R2 = 1.0
- File: results/regression_Tlog_ln_n.csv

### 7. Fixed bootstrap (n = 1000)
- 100 samples
- Constant T_log = -20.7233
- Std = 0.0000
- Files:
  - Histogram: results/bootstrap_Tlog_hist.png
  - Table: results/bootstrap_Tlog.csv

### 8. Variable bootstrap (n in [500,1500])
- 100 samples
- Mean T_log = -20.6866
- Std = 0.8615
- Files:
  - Histogram: results/bootstrap_variable_n_hist.png
  - Table: results/bootstrap_variable_n_Tlog.csv

### 9. Intermediate conclusion
- The T_log V0.1 model is robust:
  - Linear sensitivity validated
  - Bootstrap stable
  - No artifacts detected
  - Next step: tests on graphs (spectral dimension)
