import math
import os
import numpy as np
import pandas as pd

import auxiliary
from config import JPRED_INPUT_FILEPATH, MIN_SEGMENT_LENGTH, KEY

JPRED_OUTPUT_DIRECTORY_ENDING = ".txt_dir/"
JPRED_PREDICTION_FILE_ENDING = ".jnet"
JPRED_PREDICTION_TITLE = "jnetpred"
JPRED_PREDICTION_CONF_TITLE = "JNETCONF"


def __create_jpred_fasta_input(database: pd.DataFrame, database_name: str):
    """
    This function creates Jpred input (fasta file) and saves it into:
        JPRED_INPUT_FILEPATH + "Jpred_input_" + database_name + ".txt"

    :param database: database containing sequences
    :param database_name: database name
    :return: Creates new .txt. file in JPRED_INPUT_FILEPATH
    """
    current_input_filepath = JPRED_INPUT_FILEPATH + "Jpred_input_" + database_name + ".txt"
    if os.path.isfile(current_input_filepath):
        os.remove(current_input_filepath)
    jpred_input_file = open(current_input_filepath, "a")
    for _, row in database.iterrows():
        jpred_input_file.write(">{}\n".format(row["Entry"].split(',')[0]))
        sequence = auxiliary.get_corrected_sequence(row["Sequence"])
        if len(sequence) < 20:
            duplications = math.ceil(20 / len(sequence))
            i = 1
            while i < duplications:
                sequence += sequence
                i += 1
        jpred_input_file.write(sequence + "\n")
    jpred_input_file.close()


def __get_predicted_peptides_by_jpred(database: pd.DataFrame, database_name: str, job_name: str) -> set:
    """
    This function return in a list all entries in the database that HAVE Jpred result saved in the files,
    in the directory named:
        JPRED_INPUT_FILEPATH + database_name + JPRED_OUTPUT_DIRECTORY_ENDING + "/"

    :param database_name: database name
    :return: set of entries
    """
    predicted_peptides = set()
    jpred_result_directory = JPRED_INPUT_FILEPATH + database_name + JPRED_OUTPUT_DIRECTORY_ENDING
    if job_name == "Uniprot_keywords":
        jpred_result_directory += '_output/'

    if not os.path.isdir(jpred_result_directory):
        return set()
    for file in os.listdir(jpred_result_directory):
        filename = os.fsdecode(file)
        if JPRED_PREDICTION_FILE_ENDING in filename:
            entry = filename.split('_')[0]
            predicted_peptides.add(entry[0:(len(entry) - 1)])

    return predicted_peptides


def get_jpred_predicted_peptide_10239_AND(database: pd.DataFrame, jpred_predicted_peptides: set):
    entries_with_jpred_result_col = []
    for i, row in database.iterrows():
        found_entry_flag = 0
        # print(row['Entry'])
        cur_entries_list = row[KEY].split(',')
        # print(cur_entries_list)
        for entry in cur_entries_list:
            if entry in jpred_predicted_peptides:
                entries_with_jpred_result_col.append(entry)
                found_entry_flag = 1
                continue
        if not found_entry_flag:
            entries_with_jpred_result_col.append("")

    assert len(entries_with_jpred_result_col) == database.shape[0]
    database["Jpred result entry"] = entries_with_jpred_result_col


def creat_jpred_input(database: pd.DataFrame, database_name: str, job_name) -> int:
    """
    This function creates Jpred input (fasta file) and saves it into
        JPRED_INPUT_FILEPATH + "Jpred_input_" + database_name + ".txt"
    to all sequences in the database that do not have Jpred results in the directory:
        JPRED_INPUT_FILEPATH + database_name + JPRED_OUTPUT_DIRECTORY_ENDING + "/"

    :param database: database containing sequences
    :param database_name: database name
    :return: Number of sequences that DO NOT have Jpred result yet
            (and will appear in the newly created jpred input file)
    """
    jpred_predicted_peptides = __get_predicted_peptides_by_jpred(database, database_name, job_name)

    not_predicted_df = database[~database.Entry.isin(jpred_predicted_peptides)]

    database.to_excel("Database_After_Searching_existent_Jpred_Results.xlsx")
    if not_predicted_df.empty:
        print("     No new sequences to run Jpred in {} database".format(database_name))
        return 0

    __create_jpred_fasta_input(not_predicted_df, database_name)
    print("     {} New sequences to run Jpred, out of {} in {} database".format(not_predicted_df.shape[0], database.shape[0], database_name))

    if database_name == "10239_UniProt":
        database.drop(not_predicted_df.index, inplace=True)

    return not_predicted_df.shape[0]


def __get_database_jpred_results(database_name: str, job_name) -> dict:
    """
    This function puts in a dictionary all the database_name Jpred prediction.

    :param database_name: database name
    :return: Dictionary containing Jpred prediction for all entries in the database_name in the formate of:
        {KEY: {"Jpred_prediction": , "Jpred_conf": peptide_jpred_conf}}
    """
    jpred_result_dict = {}
    jpred_result_directory = JPRED_INPUT_FILEPATH + database_name + JPRED_OUTPUT_DIRECTORY_ENDING
    if job_name == 'Uniprot_keywords':
        jpred_result_directory += '_output/'
    files_to_go_over = os.listdir(jpred_result_directory)

    for file in files_to_go_over:
        filename = os.fsdecode(file)
        if JPRED_PREDICTION_FILE_ENDING in filename:
            entry = filename.split('_')[0]
            peptide_name = entry[0:(len(entry) - 1)]

            with open(jpred_result_directory + filename) as jpred_result_file:
                line = jpred_result_file.readline()
                while line:
                    line_seperated_by_semicolon = line.split(":")
                    if JPRED_PREDICTION_TITLE in line_seperated_by_semicolon:
                        peptide_jpred_prediction = line_seperated_by_semicolon[1].split(',')
                        peptide_jpred_prediction.pop()

                    if JPRED_PREDICTION_CONF_TITLE in line_seperated_by_semicolon:
                        peptide_jpred_conf_str = line_seperated_by_semicolon[1].split(',')
                        peptide_jpred_conf_str.pop()
                        peptide_jpred_conf = list(map(int, peptide_jpred_conf_str))

                    line = jpred_result_file.readline()
            jpred_result_file.close()

            jpred_result_dict[peptide_name] = {"Jpred_prediction": peptide_jpred_prediction,
                                               "Jpred_conf": peptide_jpred_conf}
    return jpred_result_dict


def __get_only_helix_conf_score(peptide_jpred_pred: list, peptide_jpred_conf: list) -> list:
    """
    This function gets the Jpred result by twe lists of secondary structure prediction and confidence score of that
    prediction by residue and returns a list that unify that information by returning a list with Jpred confidence score
     only for residues predicted as helical

    :param peptide_jpred_pred:
    :param peptide_jpred_conf:
    :return:
    """
    assert len(peptide_jpred_pred) == len(peptide_jpred_conf), \
        "In __get_only_helix_conf_score the length of both lists is different"

    helix_scores = [0] * len(peptide_jpred_pred)
    for i in range(len(peptide_jpred_pred)):
        if peptide_jpred_pred[i] == 'H':
            helix_scores[i] = peptide_jpred_conf[i]
    return helix_scores


def __adjust_prediction_idx_to_original_length(length: int, jpred_helix_prediction_idx: list) -> list:
    """
    This function returns segments with indexes computable to original sequence rather than the longer sequence created
    for the Jpred run

    :param length: Original sequence length
    :param jpred_helix_prediction_idx: Confidence scores by residues who were predicted as helical of Jpred sequence
    :return: list of Confidence scores by residues who were predicted as helical adapted to original sequence length
    """
    assert len(jpred_helix_prediction_idx) != 0, "in __adjust_prediction_idx_to_original_length " \
                                                 "prediction indexes is empty"
    new_idxs = []
    for start, end in jpred_helix_prediction_idx:
        if end > length:
            if length - start < MIN_SEGMENT_LENGTH:
                return new_idxs
            else:
                new_idxs.append(tuple((start, int(length))))
                return new_idxs
        new_idxs.append(tuple((start, end)))
    return new_idxs


def process_jpred_output(database: pd.DataFrame, database_name: str, job_name):
    """
    This function analyses Jpred prediction and update the database with the result

    :param database: database containing sequences with unique ID as KEY
    :param database_name: database name
    :return: Update the database with columns:
        "Helix fragments (Jpred)" = list of helical fragments (start and end indexes) predicted by Jpred
        Helix score (Jpred)" = list of averaged confidence scores of fragments above
        "Helix percentage (Jpred)" = percentage of residues predicted as helical out of the original sequence
    """
    jpred_results_dict = __get_database_jpred_results(database_name, job_name)

    jpred_helix_by_residue = []
    jpred_helix_scores = []
    jpred_helix_percentage = []

    for _, row in database.iterrows():
        if database_name == "10239_AND":
            peptide_jpred_results = jpred_results_dict[row["Jpred result entry"]]
        else:
            peptide_jpred_results = jpred_results_dict[row["Entry"]]
        peptide_jpred_pred = peptide_jpred_results["Jpred_prediction"]
        peptide_jpred_conf = peptide_jpred_results["Jpred_conf"]

        helix_conf_list = __get_only_helix_conf_score(peptide_jpred_pred, peptide_jpred_conf)

        jpred_helix_percentage.append(auxiliary.check_secondary_structure_prediction_content(helix_conf_list))

        jpred_helix_prediction_idx = auxiliary.get_secondary_structure_segments(helix_conf_list, "Jpred")
        if row["Length"] < 20 and len(jpred_helix_prediction_idx) > 0:
            jpred_helix_prediction_idx = __adjust_prediction_idx_to_original_length(row["Length"],
                                                                                    jpred_helix_prediction_idx)
        helix_avg_score = auxiliary.__calc_average_score(prediction=helix_conf_list,
                                                         structure_prediction_indexes=jpred_helix_prediction_idx)

        jpred_helix_by_residue.append(jpred_helix_prediction_idx)
        jpred_helix_scores.append(helix_avg_score)

    database["Helix fragments (Jpred)"] = jpred_helix_by_residue
    database["Helix score (Jpred)"] = jpred_helix_scores
    database["Helix percentage (Jpred)"] = jpred_helix_percentage



