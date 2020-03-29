import pandas as pd
import os
import re
import glob


MQ_SRC_PATH = "../../project_2/MQ2007/S*.txt"


def load_each_file(file):
    with open(file) as f:
        data = f.read()
        raw_data = data.split("\n")
        raw_data = [e for e in raw_data if e != ".DS_Store"]
        raw_data = [e for e in raw_data if e != ""]
        # print("S1 sample size : ", len(raw_data))

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

            docID = row_data.split("#docid = ")[1].split(" inc =")[0]

            extrated_list = [rel_label, queryID, docID]
            pandas_data_collection.append(extrated_list)

        return pandas_data_collection


def collect_corpus_stats(path):
    split_files = glob.glob(path)
    corpus_collection = []
    for split_file in split_files:
        each_file_data = load_each_file(split_file)
        corpus_collection += each_file_data

        df = pd.DataFrame(each_file_data, columns=["relLabels", "queryID", "docID"])
        unique_queries = list(set(df["queryID"]))
        unique_docs = list(set(df["docID"]))
        print("MQ2007 %s Data : num. queries : %s num. docs : %s" % (split_file, len(unique_queries), len(unique_docs)))

    df = pd.DataFrame(corpus_collection, columns=["relLabels", "queryID", "docID"])
    unique_queries = list(set(df["queryID"]))
    unique_docs = list(set(df["docID"]))
    print("MQ2007 Whole Data : num. queries : %s num. docs : %s" % (len(unique_queries), len(unique_docs)))


if __name__ == "__main__":
    collect_corpus_stats(MQ_SRC_PATH)