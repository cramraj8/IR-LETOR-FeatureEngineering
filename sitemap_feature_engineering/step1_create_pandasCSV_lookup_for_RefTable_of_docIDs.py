import pandas as pd
import re
import os
import glob
import xml.etree.ElementTree as ET
import numpy as np

SOURCE_PATH = "./MQ2007_CSVs/"
FILE_NAME = "extractedData_S*.csv"
SITEMAP_FILE = "./SITEMAP_DATA/sitemap.txt"
# DOCID_REF_TABLE_FILE = "./SITEMAP_DATA/RefTable_small.txt"
DOCID_REF_TABLE_large_FILE = "./SITEMAP_DATA/RefTable_large.txt"

SAVE_INTERMEDIATE_SITEMAP_CSV = "sitemap_secondary.csv"
# SAVE_INTERMEDIATE_REFTABLE_CSV = "docID_refTable_secondary.csv"
SAVE_INTERMEDIATE_REFTABLE_CSV = "docID_refTable_LARGE_secondary.csv"


def load_reftable(ref_table_file):
    ref_tabe_data = []
    cnt = 1
    with open(ref_table_file) as table_f:
        line = table_f.readline().strip()
        while line:
            tmp_list = line.split("\t")
            if len(tmp_list) == 1: cnt += 1; line = table_f.readline().strip(); continue
            tmp_rawDocID = tmp_list[0]
            tmp_newDocID = tmp_list[1]
            ref_tabe_data.append([tmp_rawDocID, tmp_newDocID])

            # if cnt == 40: break
            line = table_f.readline().strip()
            cnt += 1
            if cnt % 1000 == 0: print("Ref Table Loaded Upto : %s ...." % cnt)
            # if cnt == 1002: break

        df = pd.DataFrame(ref_tabe_data, columns=["rawDocID", "newDocID"])
        df.to_csv(SAVE_INTERMEDIATE_REFTABLE_CSV, index=True)
        print("Shape of the saved ref-table csv file : ", df.shape)

        return df


if __name__ == "__main__":

    if os.path.exists(SAVE_INTERMEDIATE_REFTABLE_CSV):
        print("Loading Ref Table CSV file ... ")
        ref_table_df = pd.read_csv(SAVE_INTERMEDIATE_REFTABLE_CSV)
    else:
        print("Creating Ref Table CSV file ... ")
        ref_table_df = load_reftable(DOCID_REF_TABLE_large_FILE)
