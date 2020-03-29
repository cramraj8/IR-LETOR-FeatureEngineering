
import os
import glob
import numpy as np
import shutil
import pandas as pd
import re

pd.options.mode.chained_assignment = None  # default='warn'

SOURCE_PATH = "../S_csvs/"
FILE_NAME = "extractedData_S*.csv"
VERBOSE = False

SRC_DIR = ""
# SRC_DIR="../../../project_2/MQ2007/"
DATA_SETS = ["train", "vali", "test"]

# MODELS = ["MART", "RankNet", "RankBoost", "AdaRank", "CoordinateAscent", "LambdaMART", "ListNet", "RandomForests"]
# MODELS = ["MART", "RankNet"] # TODO: remove this and keep above
N_FOLDS = 5
CONST_COL = 3

SAVE_BEST_MODEL_DIR = "best_model"

DST_NEW_DATASET_DIR = "./feat_added_dataset/"



# ========================
SRC_MSR_DATA = "./MQ2007_CSVs/"
SRC_MSR_FILENAMES = "extractedData_S*.csv"

RERANKED_SCORES_FOLDER = "./model_selection/"
FOLD_S_DICT = {"S1": 2, "S2": 3, "S3": 4, "S4": 5, "S5": 1}
MODELS = ["MART"]
EXTRA_FEAT_INDEX = 46
# ========================




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


def adding_features(source_path, file_name):
    S_files = glob.glob(os.path.join(source_path, file_name))
    for S_file in S_files[:1]:
        S_ID = S_file.split("/")[-1].split("_")[-1][:-4][-2:]
        fold_num = FOLD_S_DICT[S_ID]
        # print(S_ID, fold_num)

        df_raw = pd.read_csv(S_file)
        df_raw = df_raw.set_index("docID")
        df = df_raw.iloc[:5, :]

        feature_index = EXTRA_FEAT_INDEX
        for model_var in MODELS:

            feature_name = "feature_%d" % feature_index
            reranked_score_file = os.path.join(RERANKED_SCORES_FOLDER,
                                               model_var,
                                               "Fold%s" % fold_num,
                                               "reranked_scores.%s.fold%s.%s.txt" % (model_var, fold_num, "test"))

            # ["rerankedScore", "queryID", "docID"]
            reranked_df = load_rerankedscore_file(reranked_score_file)
            reranked_df = reranked_df.set_index("docID")
            # print(reranked_df)

            for index, row in df.iterrows():
                docID = index
                queryID = str(int(row["queryID"]))

                matched_row = reranked_df.loc[docID]
                print("================================")
                # print(matched_row[matched_row["queryID"] == queryID])
                matched_row = matched_row[matched_row["queryID"] == queryID]
                print(matched_row)
                print("============")

                matched_reranked_score = matched_row["rerankedScore"].iloc[0]
                print(queryID, docID, matched_reranked_score)

                df.loc[index, feature_name] = matched_reranked_score

            feature_index += 1
        print(df)
        #
        # df = df.reset_index(drop=True)
        # df.to_csv("feat_add_data_v2.csv", index=False)


if __name__ == "__main__":
    adding_features(SRC_MSR_DATA, SRC_MSR_FILENAMES)

