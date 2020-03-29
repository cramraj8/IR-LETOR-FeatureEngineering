
import os
from glob import glob
import numpy as np
import shutil
import pandas as pd
import re


SOURCE_PATH = "../S_csvs/"
FILE_NAME = "extractedData_S*.csv"
VERBOSE = False

SRC_DIR = ""
# SRC_DIR="../../../project_2/MQ2007/"
DATA_SETS = ["train", "vali", "test"]

MODELS = ["MART", "RankNet", "RankBoost", "AdaRank", "CoordinateAscent", "LambdaMART", "ListNet", "RandomForests"]
# MODELS = ["MART", "RankNet"] # TODO: remove this and keep above
N_FOLDS = 5
CONST_COL = 3

SAVE_BEST_MODEL_DIR = "best_model"
RERANKED_SCORES_FOLDER = "./model_selection/"
DST_NEW_DATASET_DIR = "./feat_added_dataset/"

EXTRA_FEAT_INDEX = 46


def load_rerankedscore_file(data_file):
    with open(data_file) as f:
        data = f.read()
        raw_data = data.split("\n")
        raw_data = [e for e in raw_data if e != ".DS_Store"]
        raw_data = [e for e in raw_data if e != ""]

        pandas_data_collection = []
        for row_data in raw_data:
            """
            10 Q0 docid = GX016-48-5543459 inc = 1 prob = 0.775913 1 0.74521 indri
            """
            docID = row_data.split("docid = ")[1].split(" inc =")[0].strip()
            queryID = row_data.split(" ")[0]
            reranked_score = float(row_data.split(" ")[-2])
            # print(docID)
            # print(queryID)
            # print(reranked_score)
            pandas_data_collection.append([reranked_score, queryID, docID])

        df = pd.DataFrame(pandas_data_collection,
                          columns=["rerankedScore", "queryID", "docID"])

        return df


def load_fold_dataset_file(data_path):
    with open(data_path) as f:
        data = f.read()
        raw_data = data.split("\n")
        raw_data = [e for e in raw_data if e != ".DS_Store"]
        raw_data = [e for e in raw_data if e != ""]

        data_collection = []  # [rel-label, queryID, feature vector, docID]
        pandas_data_collection = []
        for row_data in raw_data:
            tmp_list = row_data.split(" ")
            query = tmp_list[1]

            rel_label = tmp_list[0]
            if query.split(":")[0] == "qid":
                queryID = query.split(":")[1]
            else:
                print("Error: query ID is not found !")
                os.exit()

            # ans = re.findall(r'\s\d{1,46}:^[0-9]+\.?[0-9]+$', row_data)
            feat_list = re.findall(r'\d{1,46}\:[0-9]+\.[0-9]+', row_data)
            if len(feat_list) == 46:
                feat_values = [float(feat.split(":")[1]) for feat in feat_list]
            else:
                print("Error: feature vector does not have length 46 !")
                os.exit()

            docID = row_data.split("#docid = ")[1].split(" inc =")[0]
            # docID = row_data.find("#docid = * inc")

            extrated_list = [rel_label, queryID, docID]
            extrated_list = extrated_list + feat_values
            pandas_data_collection.append(extrated_list)
            data_collection.append([rel_label, queryID, docID, feat_values])

        # for e in data_collection: print(e)
        df = pd.DataFrame(pandas_data_collection,
                          columns=["relLabels", "queryID", "docID"] + ["feature_%s" % f for f in range(46)])

        return df


def merge_rerankedscores_with_raw_dataset(orig_df, reranked_df, feature_index):
    # orig_df = orig_df.iloc[:3, :]

    orig_df_grouped = orig_df.groupby("queryID")
    feature_name = "feature_%d" % feature_index

    for name, group_df in orig_df_grouped:
        for index, row in group_df.iterrows():
            tmp_orig_queryID = row["queryID"]
            tmp_orig_docID = row["docID"]

            matched_row = reranked_df[(reranked_df["docID"] == tmp_orig_docID) & (reranked_df["queryID"] == tmp_orig_queryID)]
            if matched_row.shape[0] != 1:
                print("Error in matched table which has multiple rows !")
                os.exit()

            tmp_rerankedScore = matched_row["rerankedScore"].iloc[0]

            orig_df.loc[orig_df.index[index], feature_name] = tmp_rerankedScore

        print("QueryID with : %s added extra feature : %s" % (name, feature_name))

    return orig_df


def adding_features(source_path, file_name):

    for fold_num in range(1, N_FOLDS + 1): # TODO:
        dst_path = os.path.join(DST_NEW_DATASET_DIR, "Fold%s" % fold_num)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        for data_set in DATA_SETS:

            with open(os.path.join(dst_path, data_set + ".txt"), "w") as write_file:

                feature_index = EXTRA_FEAT_INDEX
                original_dataset_file = os.path.join(SRC_DIR, "Fold%s" % fold_num, "%s.txt" % data_set)
                df_orig = load_fold_dataset_file(original_dataset_file)

                for model_var in MODELS:
                    reranked_score_file = os.path.join(RERANKED_SCORES_FOLDER,
                                                       model_var,
                                                       "Fold%s" % fold_num,
                                                       "reranked_scores.%s.fold%s.%s.txt" % (model_var, fold_num, data_set))

                    df_reranked = load_rerankedscore_file(reranked_score_file)

                    df_orig = merge_rerankedscores_with_raw_dataset(df_orig, df_reranked, feature_index)

                    feature_index += 1

                df = pd.DataFrame(df_orig,
                                  columns=["relLabels", "queryID", "docID"] + ["feature_%s" % f for f in range(feature_index)])
                df.to_csv(os.path.join(dst_path, "feat_added_data.%s.csv" % data_set), index=True)

                for index, row in df.iterrows():
                    write_line = "%s qid:%s " % (row["relLabels"], row["queryID"])

                    feature_cols = ["feature_%s" % e for e in range(df.shape[1] - CONST_COL)]
                    for i, feat in enumerate(row[feature_cols]): write_line += "%d:%f " % (i + 1, feat)

                    write_line += "#docid = %s" % row["docID"]
                    write_line += " inc = 1"
                    write_line += " prob = 0.001"  # maybe random generator
                    write_line += "\n"
                    write_file.write(write_line)


if __name__ == "__main__":
    adding_features(SOURCE_PATH, FILE_NAME)
