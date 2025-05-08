
# Hertz Model Fitting Workflow

This guide walks you through the complete process of fitting the Hertz model to experimental data, from raw voltage-time data to the final effective modulus (`E_eff`) collection, visualization, and combined plots.

---

## 📁 **File Structure Overview**

```plaintext
data_root_folder/
│
├── pink/
│   ├── experiment_1/
│   │   ├── 20250508_123456_data.csv
│   │   ├── 20250506_162304_chart.png
│   │   ├── 20250506_162304_fz_data.csv
│   │   ├── force_distance_plot.png
│   │   ├── cp.txt
│   │   ├── 20250508_123456_retract_data.csv
│   │   ├── 20250506_162304_retract_plot.png
│   │   ├── 20250508_123456_hertz_results.txt
│   │   └── 20250508_123456_hertz_fit.png
│   └── experiment_2/
│       └── ...
│
├── white/
│   └── experiment_1/
│       └── ...
│
├── yellow/
│   └── experiment_1/
│       └── ...
│
├── E_eff_scatter_plot.png 
├── average_E_eff_results_filtered.txt
├── low_quality_results.txt
└── combined_plots/
    ├── pink_combined.png
    ├── white_combined.png
    └── yellow_combined.png

data_root_folder/
├── data_format_transfer.py
├── retract_data_transfer.py
├── hertz_fit.py
├── fit_result_collect.py
└── combined_plots.py
```

---

## 📝 **Step 1: Transfer Voltage-Time to Force-Displacement Data**

This step converts raw voltage-time data into force-displacement data.

```bash
python data_format_transfer.py
```

### 🔄 **Generated File Structure**:

Each experiment folder under each material (e.g., `pink/experiment_1/`) will contain:

* `*_data.csv`: Original raw voltage-time data.
* `*_data_chart.png`: Original raw voltage-time plot.
* `*_fz_data.csv`: Converted force-displacement data.
* `*_force_distance_plot.png`: Converted force-displacement plot.

---

## 📝 **Step 2: Manually Choose Contact Point**

For each experiment, **manually determine the contact point** and save it in a `cp.txt` file in the same experiment folder.

### ✍️ **Instructions**:

1. Open the corresponding force-displacement plot.
2. Identify the contact point visually.
3. Write the contact point value (in the same unit as your data) in `cp.txt`.

### 🔄 **Generated File Structure**:

Each experiment folder under each material will have:

* `cp.txt`: Contains the manually selected contact point.

---

## 📝 **Step 3: Extract Retract Data**

This step extracts the retract curve data from the formatted data and saves it.

```bash
python retract_data_transfer.py
```

> **Note**: Update the root path inside the script to match your material folder (e.g., `pink`, `white`, or `yellow`).

### 🔄 **Generated File Structure**:

Each experiment folder under each material will contain:

* `*_retract_data.csv`: Contains the extracted retract curve data.
* `*_retract_plot.png`: Plot of the extracted retract curve plot.

---

## 📝 **Step 4: Fit Hertz Model**

This step fits the Hertz model to the retract data.

```bash
python hertz_fit.py
```

> **Note**: Update the root path inside the script to match your material folder (e.g., `pink`, `white`, or `yellow`).

### 🔄 **Generated File Structure**:

Each experiment folder under each material will contain:

* `*_hertz_results.txt`: Contains the effective modulus (`E_eff`), R² value, and radius used.
* `*_hertz_fit.png`: A plot showing the experimental data and the fitted curve.

---

## 📝 **Step 5: Collect the E\_eff and Plot Results**

In this step, you collect all the `E_eff` values from different experiments, filter out low-quality fits (`R² < 0.85`), and generate a summary.

```bash
python fit_result_collect.py
```

### 🔄 **Generated File Structure**:

The root folder will contain:

* `average_E_eff_results_filtered.txt`: The average `E_eff` for each material.
* `E_eff_scatter_plot.png`: A scatter plot visualizing the `E_eff` distribution for different materials.
* `low_quality_results.txt`: A list of experiments with `R² < 0.85` that were filtered out.

---

## 📝 **Step 6: Generate Combined Plots for Each Material**

This step generates combined plots for all experiments under each material for easy comparison.

```bash
python combined_plots.py
```

### 🔄 **Generated File Structure**:

A new folder called `combined_plots` will be created in the root directory, containing:

* `pink_combined.png`: All Hertz fitting curves from experiments with pink samples.
* `white_combined.png`: All Hertz fitting curves from experiments with white samples.
* `yellow_combined.png`: All Hertz fitting curves from experiments with yellow samples.

> **Note:** Low-quality fits (`R² < 0.85`) are excluded from these combined plots.

---

## 🚀 **Final Notes**

* Ensure the root paths are updated in each script before execution.
* Files with poor fits (`R² < 0.85`) are automatically filtered out and logged into `low_quality_results.txt` for review.
* The combined plots are helpful for quick visual inspection of consistency across experiments.

