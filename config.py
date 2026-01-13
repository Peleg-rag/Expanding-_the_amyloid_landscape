import os

# ----------------------------------------- File Paths ----------------------------------------- #
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

LANDAU_LAB_PEPTIDES_FILEPATH = os.path.join(PROJECT_PATH, "Landau_lab_peptides_20230119.xlsx")
# TODO: see if the / after Jpred is neccery
JPRED_INPUT_FILEPATH = os.path.join(PROJECT_PATH, "Jpred/")


# ------------------------------------------ Job type  ------------------------------------------ #
RUN_ONLY_DATABASE = []
JOB_RUN = 'Uniprot_keywords'

KEY = 'Entry'


# ------------------------------- Secondary structure thresholds -------------------------------- #
MINIMAL_PEPTIDE_LENGTH = 35

MIN_SEGMENT_LENGTH = 5
MAX_GAP = 3  # Between alpha-helical and beta averaged scores
MIN_JPRED_SCORE = 7  # Minimal averaged score of a segment to be predicted as helical by Jpred

MIN_H_CONTENT = 0
MIN_SSW_B_CONTENT = 0
MIN_SSW_H_CONTENT = 0








