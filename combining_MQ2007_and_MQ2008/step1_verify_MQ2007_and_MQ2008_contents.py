import pandas as pd
import os


MQ2007_PATH = "../../project_2/MQ2007/"
MQ2008_PATH = "../../project_2/MQ2008/"
DST_CSV_FILE = "./extractions_data/"
TXT_FILENAMES = ["S%s.txt" % (e+1) for e in range(5)]


def load_and_extract(path, global_pandas_data_collection):
    with open(path) as f:
        data = f.read()
        raw_data = data.split("\n")
        raw_data = [e for e in raw_data if e != ".DS_Store"]
        raw_data = [e for e in raw_data if e != ""]
        # print("S1 sample size : ", len(raw_data))

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

            docID = row_data.split("#docid = ")[1].split(" inc =")[0]

            extrated_list = [rel_label, queryID, docID]
            pandas_data_collection.append(extrated_list)
            global_pandas_data_collection.append(extrated_list)
            # data_collection.append([rel_label, queryID, docID, feat_values])

        # df = pd.DataFrame(pandas_data_collection,
        #                   columns=["relLabels", "queryID", "docID"])
        # df.to_csv(os.path.join(DST_CSV_FILE, "%s.csv" % path.split("/")[-1][:-4]), index=True)

        return global_pandas_data_collection


def verify(path2007, path2008):
    global_pandas_data_collection_2007 = []
    global_pandas_data_collection_2008 = []
    for TXT_FILENAME in TXT_FILENAMES:
        global_pandas_data_collection_2007 = load_and_extract(os.path.join(path2007, TXT_FILENAME), global_pandas_data_collection_2007)
        global_pandas_data_collection_2008 = load_and_extract(os.path.join(path2008, TXT_FILENAME), global_pandas_data_collection_2008)

        df_2007 = pd.DataFrame(global_pandas_data_collection_2007, columns=["relLabels", "queryID", "docID"])
        df_2007.to_csv(os.path.join(DST_CSV_FILE, "extractions_MQ2007.csv"), index=True)

        df_2008 = pd.DataFrame(global_pandas_data_collection_2008, columns=["relLabels", "queryID", "docID"])
        df_2008.to_csv(os.path.join(DST_CSV_FILE, "extractions_MQ2008.csv"), index=True)

    unique_2007_queries = list(set(df_2007["queryID"]))
    unique_2008_queries = list(set(df_2008["queryID"]))

    unique_2007_docs = list(set(df_2007["docID"]))
    unique_2008_docs = list(set(df_2008["docID"]))

    print("MQ2007 Data : num. queries : %s num. docs : %s" % (len(unique_2007_queries), len(unique_2007_docs)))
    print("MQ2008 Data : num. queries : %s num. docs : %s" % (len(unique_2008_queries), len(unique_2008_docs)))


    # ==================================================================================================================
    # ================================= COMPARISON STARTS HERE =========================================================
    # ==================================================================================================================
    # matched_queries_list = [q for q in unique_2007_queries if q in unique_2008_queries]
    # print("Matched QueryID list : ", matched_queries_list)

    # Taking too long
    # matched_docs_list = [d for d in unique_2008_docs if d in unique_2007_docs]
    # print("Matched docID list : ", matched_docs_list)


if __name__ == "__main__":
    verify(MQ2007_PATH, MQ2008_PATH)