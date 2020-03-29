import pandas as pd
import re
import os
import glob
import xml.etree.ElementTree as ET
import numpy as np


SOURCE_PATH = "./MQ2007_CSVs/"
FILE_NAME = "extractedData_S*.csv"
SITEMAP_FILE = "./SITEMAP_DATA/sitemap.txt"

SAVE_INTERMEDIATE_SITEMAP_CSV = "sitemap_secondary_pandas.csv" # TODO: different from step2_*py file

SAVE_INTERMEDIATE_REFTABLE_CSV = "docID_refTable_LARGE_secondary.csv"


def load_sitemap_txt(sitemap_file):
    ref_table_df = pd.read_csv(SAVE_INTERMEDIATE_REFTABLE_CSV)

    collection_data = []
    sitemap_cnt = 0
    with open(sitemap_file) as sitemap_f:
        line = sitemap_f.readline().strip()
        while line:

            # print("Line {}: {}".format(cnt, line.strip()))
            tmp_list = line.split("\t")
            if len(tmp_list) == 5:
                tmp_newDocID = int(tmp_list[0].strip())
                tmp_depth_url = tmp_list[1]
                tmp_url_len = tmp_list[2]
                tmp_num_child_pgs = tmp_list[3]
                tmp_parent_newDocID = tmp_list[4]
            else:
                tmp_newDocID = int(tmp_list[0].strip())
                tmp_depth_url = tmp_list[1]
                tmp_url_len = tmp_list[2]
                tmp_num_child_pgs = tmp_list[3]
                tmp_parent_newDocID = "-1"

            # ======================================================================
            # Lookup docID in ref-table
            # matched_rawDocID = ref_table_df.loc[tmp_newDocID]["rawDocID"]
            matched_rawDocID = ref_table_df.loc[tmp_newDocID]["newDocID"]
            print("Matched Doc ID : %s : %s" % (tmp_newDocID, matched_rawDocID))

            collection_data.append([tmp_newDocID, matched_rawDocID, tmp_depth_url, tmp_url_len, tmp_num_child_pgs, tmp_parent_newDocID])

            # if sitemap_cnt == 3: break # TODO: remove
            line = sitemap_f.readline().strip()
            sitemap_cnt += 1

            if sitemap_cnt % 1000 == 0: print("Sitmap Data Loaded Upto : %s ...." % sitemap_cnt)

            if sitemap_cnt % 100000 == 0:
                df = pd.DataFrame(collection_data, columns=["newDocID", "lookedup_docID", "depth_url", "url_len",
                                                            "num_child_pgs", "parent_newDocID"])
                df.to_csv(SAVE_INTERMEDIATE_SITEMAP_CSV, index=True)

    df = pd.DataFrame(collection_data, columns=["newDocID", "lookedup_docID", "depth_url", "url_len",
                                                "num_child_pgs", "parent_newDocID"])
    df.to_csv(SAVE_INTERMEDIATE_SITEMAP_CSV, index=True)
    print("\nShape of the saved sitemap csv file : ", df.shape)


if __name__ == "__main__":
    load_sitemap_txt(SITEMAP_FILE)
