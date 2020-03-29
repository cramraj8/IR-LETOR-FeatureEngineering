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


def load_sitemap_txt(sitemap_file):
    collection_data = []
    sitemap_cnt = 0
    with open(sitemap_file) as sitemap_f:
        line = sitemap_f.readline().strip()
        while line:

            # print("Line {}: {}".format(cnt, line.strip()))
            tmp_list = line.split("\t")
            tmp_newDocID = int(tmp_list[0].strip())
            tmp_depth_url = tmp_list[1]
            tmp_url_len = tmp_list[2]
            tmp_num_child_pgs = tmp_list[3]
            tmp_parent_newDocID = tmp_list[4]

            # ======================================================================
            # Lookup docID in ref-table
            found_row = False
            refTable_cnt = 0
            matched_rawDocID = ""
            with open(DOCID_REF_TABLE_large_FILE) as table_f:
                line = table_f.readline().strip()
                while line:
                    # check if this line is a match
                    if len(tmp_list) == 1: refTable_cnt += 1; line = table_f.readline().strip(); continue

                    if refTable_cnt == tmp_newDocID:
                        tmp_list = line.split("\t")
                        # matched_rawDocID = tmp_list[0]
                        matched_rawDocID = tmp_list[1]
                        break

                    line = table_f.readline().strip()
                    refTable_cnt += 1
            print("Matched Doc ID : %s : %s" % (tmp_newDocID, matched_rawDocID))

            collection_data.append([tmp_newDocID, matched_rawDocID, tmp_depth_url, tmp_url_len, tmp_num_child_pgs, tmp_parent_newDocID])

            # if sitemap_cnt == 3: break
            line = sitemap_f.readline().strip()
            sitemap_cnt += 1

    df = pd.DataFrame(collection_data, columns=["newDocID", "lookedup_docID", "depth_url", "url_len",
                                                "num_child_pgs", "parent_newDocID"])
    df.to_csv(SAVE_INTERMEDIATE_SITEMAP_CSV, index=True)
    print("\nShape of the saved sitemap csv file : ", df.shape)


if __name__ == "__main__":
    load_sitemap_txt(SITEMAP_FILE)
