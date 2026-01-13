# Expanding-_the_amyloid_landscape

This repository contains a Python pipeline for identifying and characterizing alpha-helical or secondary structure switch (SSW)
fibril-forming peptides of toxic and virulant peptides. The prediction based on biochemical features and secondary-structure
predictions (Jpred, Tango) and works on selected toxicity-related keywords form Uniprot:
- Antimicrobial (KW-0929).
- Amphibian defence peptide (KW-0878)
- Antiviral defence (KW-0051)
- Antiviral protein (KW-0930)
- Pathogenicity (KW-0568)
- Prion (KW-0640)
- Virulence (KW-0834)
- Toxin (KW-0800).

The code is designed so that **users only need to place the entire repository in the same directory and run `main.py`**.

---

## Overview

The pipeline performs the following steps:

1. Loads peptide databases (Excel format)
2. Filters sequences by length and annotation quality
3. Processes **Jpred** secondary-structure predictions (To idetify helical segmets)
4. Processes **Tango** secondary-structure predictions (To idetify SSW segments)
5. Computes biochemical features (charge, hydrophobicity, hydrophobic moment)
6. Classifies peptides as fibril-forming (helix, SSW, or both)
7. Exports:
   - Final annotated databases (Excel)
   - Summary statistics (Excel)

---

## Repository Structure

- <img width="20" height="20" alt="image" src="https://github.com/user-attachments/assets/7a17b49b-20c0-4d7e-bd40-42201de8c662" /> ▶️ **main.py**   : Entry point (run this)
- <img width="20" height="20" alt="image" src="https://github.com/user-attachments/assets/7a17b49b-20c0-4d7e-bd40-42201de8c662" /> **config.py**   : Global configuration and thresholds
- <img width="20" height="20" alt="image" src="https://github.com/user-attachments/assets/7a17b49b-20c0-4d7e-bd40-42201de8c662" /> **auxiliary.py**   : Helper and utility functions
- <img width="20" height="20" alt="image" src="https://github.com/user-attachments/assets/7a17b49b-20c0-4d7e-bd40-42201de8c662" /> **biochemCalculation.py**   : Biochemical feature calculations
- <img width="20" height="20" alt="image" src="https://github.com/user-attachments/assets/7a17b49b-20c0-4d7e-bd40-42201de8c662" /> **jpred.py**   : Jpred input generation and result parsing
- <img width="20" height="20" alt="image" src="https://github.com/user-attachments/assets/7a17b49b-20c0-4d7e-bd40-42201de8c662" /> **tango.py**   : Tango input generation, execution, and parsing
- <img width="20" height="20" alt="image" src="https://github.com/user-attachments/assets/7a17b49b-20c0-4d7e-bd40-42201de8c662" /> **Analysing_final_results.py**   : Post-analysis
- 🗂️ **Jpred**   : Jpred input/output directories (provided)
   - 🗂️ ***<database_name>***.txt_dir
      - 📁 **_output**
         - 🖹 ***Jpred output files***  
      - 📁 **_error**
- 📁 **Tango**   : Tango executable + outputs (provided)
- 🗂️ **Uniprot_keywords**   : Input databases (provided)
   - 🗂️ **Database**
      - 𓊂 ***<database_name>*.xlsx**
- 📁 **Output**   : Local results (auto-created)


---

> :bulb: **Note:**  
> Input databases and external tool outputs are **included** in this repository

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
```

#### External Tools
- **Jpred**: Jpred predictions must be generated externally and paste into the folder Jpred/*<database_name>*.text_dir/_output/.
  
- **Tango**: Tango runs locally. all files needed exists in Tango/ folder. 



---

> :memo: **Configuration and threshold setting:**  
> All user-adjustable parameters are defined in config.py. **There is no need to change anything to reproduce results described in the paper**
>
> 
> Configuration andd Threshold adjustment is possible, but **will result in different output**.
> - RUN_ONLY_DATABASE - add filepath to a specific database. Must include the columns:
>    -  Unique name (update in conig.py under KEY the column name)
>    -  Sequence under 'Sequence' column
>
> 
> - MINIMAL_PEPTIDE_LENGTH - defines the length of the sequences that will be analysed.
> - MIN_SEGMENT_LENGTH - minimum number of consecutive residues required to assign a secondary-structure segment.
> - MAX_GAP - maximum number of residues with mismatched secondary-structure prediction allowed within a predicted segment strach.
> - MIN_JPRED_SCORE - minimal averaged score of a segment to be predicted as helical by Jpred
>   
> To apply additional thresholds based on the fraction of the sequence assigned a defined secondary structure, set the following parameters to values greater than 0 and less than or equal to 100:
> - MIN_H_CONTENT: minimum percentage of residues predicted to be helical
> - MIN_SSW_B_CONTENT: minimum percentage of residues predicted to adopt β-structure within SSW sequences
> - MIN_SSW_H_CONTENT: minimum percentage of residues predicted to be helical within SSW sequences
>
   
---



## Running the Pipeline
From the project root directory:

```bash
python main.py
```
That’s it 😉 The script will:
- Automatically discover input databases 
- Run all analysis steps
- Write outputs to: Output/
   - Outputs For each input database: Final_<database_name>.xlsx → Fully annotated peptide database
   - Final_statistical_result.xlsx → Summary statistics across databases

---
> :memo: **Notes & Best Practices**
> - Do not move individual .py files out of the project root.
> - Keep the directory structure intact.
> - Paths are resolved relative to config.py.
> - The pipeline overwrites existing result files with the same name.
---

## Reading the output files
The resulted ***Final_<database_name>.xlsx*** packed with all intermidiate calculations. 

The most important columns, with the final prediction with values {-1 or 1} are: 
- **FF-Secondary structure switch** -  1 if the sequence predicted as fibril-forming secondary structure switch and -1 otherwise.
- **FF-Helix (Jpred)** - 1 if the sequence predicted as fibril-forming secondary structure switch and -1 otherwise.

The resulted ***Final_statistical_result.xlsx*** file summarizes, in a single table, all threshold values computed during execution of the code for each input database. 

## Citation and contact
If you use this code in academic work, please cite the corresponding publication
or contact the authors for citation details.

For questions, issues, or extensions, please contact, please contact pelegrag@gmail.com


## References
In this project there is a use of Jpred and Tango results, as described in: 

Fernandez-Escamilla AM, Rousseau F, Schymkowitz J, Serrano L. Prediction of sequence-dependent and mutational effects on the aggregation of peptides and proteins. Nat Biotechnol. 2004 Oct;22(10):1302-6. doi: 10.1038/nbt1012. Epub 2004 Sep 12. PMID: 15361882.

Drozdetskiy A, Cole C, Procter J, Barton GJ. JPred4: a protein secondary structure prediction server. Nucleic Acids Res. 2015 Jul 1;43(W1):W389-94. doi: 10.1093/nar/gkv332. Epub 2015 Apr 16. PMID: 25883141; PMCID: PMC4489285.




