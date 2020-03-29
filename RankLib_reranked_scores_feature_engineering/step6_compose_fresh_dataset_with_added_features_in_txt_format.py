import pandas as pd
import re
import os
import glob
import xml.etree.ElementTree as ET
import numpy as np

SOURCE_CSV_PATH = "./feat_added_S_folder/feat_added_data.S*.csv"
WRITE_FILE_PATH = "./features_added_LETOR_data/"
CONST_COL = 4


def convert_dataformat(source_path):
    csv_S_files = glob.glob(source_path)
    if not os.path.exists(WRITE_FILE_PATH):
        os.makedirs(WRITE_FILE_PATH)

    for csv_S_file in csv_S_files: # TODO:
        with open(os.path.join(WRITE_FILE_PATH, csv_S_file.split("/")[-1][:-4] + ".txt"), "w") as write_file:
            df = pd.read_csv(csv_S_file)
            for index, row in df.iterrows():
                write_line = "%s qid:%s " % (row["relLabels"],row["queryID"])

                feature_cols = ["feature_%s" % e for e in range(df.shape[1] - CONST_COL)]
                for i, feat in enumerate(row[feature_cols]): write_line += "%d:%f " % (i+1, feat)

                write_line += "#docid = %s" % row["docID"]
                write_line += " inc = 1"
                write_line += " prob = 0.001" # maybe random generator
                write_line += "\n"
                write_file.write(write_line)

            print("File %s.txt Written !!!" % csv_S_file.split(".")[1])


if __name__ == "__main__":
    convert_dataformat(SOURCE_CSV_PATH)