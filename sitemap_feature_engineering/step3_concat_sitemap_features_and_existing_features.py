import pandas as pd
import re
import os
import glob
import xml.etree.ElementTree as ET
import numpy as np
from sklearn.preprocessing import normalize

# os.chdir("/Users/ramc/ResearchSpace/2020_Spring_semester/CS-572_IR/homework_2/feature_selection/feat1_sitemap")
# TODO: remove above line


SOURCE_PATH = "./MQ2007_CSVs/"
FILE_NAME = "extractedData_S*.csv"

SAVE_INTERMEDIATE_SITEMAP_CSV = "./sitemap_secondary_pandas.csv"


def adding_sitemap_meta_features(source_path, file_name):

    sitemap_df = pd.read_csv(SAVE_INTERMEDIATE_SITEMAP_CSV)

    unmatched_document_query_pairs = []
    S_files = glob.glob(os.path.join(source_path, file_name))
    for S_file in S_files: # TODO: remove slicing
        df = pd.read_csv(S_file)
        # df = df_raw.iloc[:3, :] # TODO: remove slicing

        depth_url_list = []
        url_len_list = []
        num_child_pgs_list = []
        unmatched_document_query_pair = 0
        for index, row in df.iterrows():
            queryNum = row["queryID"]
            docID = row["docID"]

            # ======================================================================
            # Given docID & queryID, extract the sitemap meta-data
            # sitemap_data = sitemap_df[sitemap_df["lookedup_docID"] == docID]
            # print(docID)
            # if sitemap_data.shape[0] == 0:
            #     print("Matching sitemap data is not found !!!!")
            #     continue
            # print(docID, sitemap_data["lookedup_docID"].iloc[0], sitemap_data["newDocID"].iloc[0])

            sitemap_data = sitemap_df[sitemap_df["lookedup_docID"] == docID]
            depth_url = 0
            url_len = 0
            num_child_pgs = 0
            parent_newDocID = -1
            if sitemap_data.shape[0] == 0:
                print("Matching sitemap data is not found !!!!")
            else:
                depth_url = int(sitemap_data["depth_url"])
                url_len = int(sitemap_data["url_len"])
                num_child_pgs = int(sitemap_data["num_child_pgs"])
                parent_newDocID = sitemap_data["parent_newDocID"]
            print("Collecting additional features for : queryID = %s : docID = %s" % (queryNum, docID))
            # =================>>> process a feature
            depth_url_list.append(depth_url)
            url_len_list.append(url_len)
            num_child_pgs_list.append(num_child_pgs)
            # if index == 2: break # TODO: remove this

        # =================>>> Normalize the added features
        depth_url_list = np.asarray(depth_url_list).reshape(1, -1)
        url_len_list = np.asarray(url_len_list).reshape(1, -1)
        num_child_pgs_list = np.asarray(num_child_pgs_list).reshape(1, -1)

        depth_url_vector = normalize(depth_url_list, axis=1, norm='max')
        url_len_vector = normalize(url_len_list, axis=1, norm='max')
        num_child_pgs_vector = normalize(num_child_pgs_list, axis=1, norm='max')

        print(depth_url_vector)
        print(url_len_vector)
        print(num_child_pgs_vector)

        print(depth_url_vector.ravel())
        print(url_len_vector.ravel())
        print(num_child_pgs_vector.ravel())

        df["feature_46"] = depth_url_vector.ravel()
        df["feature_47"] = url_len_vector.ravel()
        df["feature_48"] = num_child_pgs_vector.ravel()

        df = df.reset_index(drop=True)
        df.to_csv("MQ2007_CSV_addedSitemapMeta.csv", index=False)


if __name__ == "__main__":
    adding_sitemap_meta_features(SOURCE_PATH, FILE_NAME)