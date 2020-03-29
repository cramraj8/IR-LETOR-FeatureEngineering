
import os
import glob
import numpy as np
import shutil
import pandas as pd
import re

pd.options.mode.chained_assignment = None  # default='warn'


# ========================
SRC_MSR_DATA = "./MQ2007_CSVs/"
SRC_MSR_FILENAMES = "extractedData_S*.csv"

RERANKED_SCORES_FOLDER = "./model_selection/"
FOLD_S_DICT = {"S1": 2, "S2": 3, "S3": 4, "S4": 5, "S5": 1}
MODELS = ["MART", "RankNet", "RankBoost", "AdaRank", "CoordinateAscent", "LambdaMART", "ListNet", "RandomForests"]
EXTRA_FEAT_INDEX = 46
DST_NEW_DATASET_DIR = "./feat_added_S_folder/"
# ========================


def adding_features(source_path, file_name):
    S_files = glob.glob(os.path.join(source_path, file_name))
    for S_file in S_files[1:]: # TODO:
        S_ID = S_file.split("/")[-1].split("_")[-1][:-4][-2:]
        fold_num = FOLD_S_DICT[S_ID]
        if not os.path.exists(DST_NEW_DATASET_DIR):
            os.makedirs(DST_NEW_DATASET_DIR)
        # print("Fold and SFile : ", S_ID, fold_num)

        df = pd.read_csv(S_file)
        # df = df_raw.iloc[:5, :] # TODO:

        feature_index = EXTRA_FEAT_INDEX
        for model_var in MODELS:

            feature_name = "feature_%d" % feature_index
            reranked_score_path = os.path.join(RERANKED_SCORES_FOLDER,
                                               model_var,
                                               "Fold%s" % fold_num,
                                               "reranked_scores_noID.%s.fold%s.%s.txt" % (model_var, fold_num, "test"))

            with open(reranked_score_path, "r") as reranked_score_file:

                for index, row in df.iterrows():
                    docID = row["docID"]
                    queryID = str(int(row["queryID"]))

                    rerankedScore = 0.0
                    rerankedScore_line = reranked_score_file.readline().strip().split("\t")
                    rerankedScore_line_queryID = str(int(rerankedScore_line[0]))

                    if rerankedScore_line_queryID != queryID:
                        print("Error in matching queryID in both reranked score file and input S file !")
                    else:
                        rerankedScore = float(rerankedScore_line[2])

                    df.loc[df.index[index], feature_name] = rerankedScore

            feature_index += 1

        df = df.reset_index(drop=True)
        df.to_csv(os.path.join(DST_NEW_DATASET_DIR, "feat_added_data.%s.csv" % S_ID), index=False)
        print("Done saving new features added dataset !")


if __name__ == "__main__":
    adding_features(SRC_MSR_DATA, SRC_MSR_FILENAMES)

