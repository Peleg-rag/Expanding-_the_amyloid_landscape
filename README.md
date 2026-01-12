# Expanding-_the_amyloid_landscape

This repository contains a Python pipeline for identifying and characterizing alpha-helical or secondary structure switch
fibril-forming peptides of toxic and virulant peptides. The prediction based on biochemical features and secondary-structure
predictions (Jpred, Tango) and works on selected toxicity-related keywords form Uniprot:
- antimicrobial (KW-0929).
- amphibian defence peptide (KW-0878)
- antiviral defence (KW-0051)
- antiviral protein (KW-0930)
- pathogenicity (KW-0568)
- prion (KW-0640)
- virulence (KW-0834)
- toxin (KW-0800).

The code is designed so that **users only need to place the required input files
in the correct directories and run `main.py`**.

---

## Overview

The pipeline performs the following steps:

1. Loads peptide databases (Excel format)
2. Filters sequences by length and annotation quality
3. Processes **Jpred** secondary-structure predictions
4. Processes **Tango** aggregation and secondary-structure-switch predictions
5. Computes biochemical features (charge, hydrophobicity, hydrophobic moment)
6. Classifies peptides as fibril-forming (helix, SSW, or both)
7. Exports:
   - Final annotated databases (Excel)
   - Summary statistics (Excel)

---

## Repository Structure

project_root/
├── main.py # Entry point (run this)
├── config.py # Global configuration and thresholds
├── auxiliary.py # Helper and utility functions
├── biochemCalculation.py # Biochemical feature calculations
├── jpred.py # Jpred input generation and result parsing
├── tango.py # Tango input generation, execution, and parsing
├── Analysing_final_results.py # Optional post-analysis utilities
│
├── Jpred/ # Jpred input/output directories (user-provided)
├── Tango/ # Tango executable + outputs (user-provided)
├── Uniprot_keywords/ # Input databases (user-provided)
│ └── Database/
│ └── *.xlsx
│
├── Output/ # Local results (auto-created)
└── results/ # Final results (auto-created)

markdown
Copy code

> **Note:**  
> Input databases and external tool outputs are **not included** in this repository
> due to size and licensing constraints.

---

## Requirements

- Python **3.8+**
- Required Python packages:
  - `pandas`
  - `numpy`
  - `openpyxl`

Install dependencies with:
```bash
pip install pandas numpy openpyxl
External Tools
Jpred
Jpred predictions must already exist or be generated externally.

The pipeline expects Jpred outputs to be located under:

php-template
Copy code
Jpred/<database_name>.txt_dir/
Tango
Tango must be installed locally.

The Tango executable (Tango_run.bat) must be placed in:

Copy code
Tango/
Configuration
All user-adjustable parameters are defined in config.py, including:

Input paths

Job type (JOB_RUN)

Length thresholds

Secondary-structure thresholds

Typical users only need to edit config.py.

Running the Pipeline
From the project root directory:

bash
Copy code
python main.py
That’s it.

The script will:

Automatically discover input databases

Run all analysis steps

Write outputs to:

Output/ (local copy)

results/ (final results)

Outputs
For each input database:

Final_<database_name>.xlsx
→ Fully annotated peptide database

Additionally:

Final_statistical_result.xlsx
→ Summary statistics across databases

Notes & Best Practices
Do not move individual .py files out of the project root.

Keep the directory structure intact.

Paths are resolved relative to config.py.

The pipeline overwrites existing result files with the same name.

Citation
If you use this code in academic work, please cite the corresponding publication
or contact the authors for citation details.

Contact
For questions, issues, or extensions, please contact the project maintainer.

yaml
Copy code

---

If you want, next I can:
- **Slim this down** for Code Ocean specifically  
- Add a **“Quick start (TL;DR)”** block  
- Add a **configuration table** explaining each parameter in `config.py`  
- Or rewrite it in a **more formal “Methods-style” tone** for publication

Just tell me 👍
