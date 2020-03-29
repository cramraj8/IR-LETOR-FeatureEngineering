import pandas as pd
import os
import re


MQ2007_PATH = "../../project_2/MQ2007/"
MQ2008_PATH = "../../project_2/MQ2008/"
DST_CSV_FILE = "./extractions_data/"
TXT_FILENAMES = ["S%s.txt" % (e+1) for e in range(5)]
COMB_SAVE_DATA = "./combined_2007_and_2008/"
CONST_COL = 3


def load_and_extract(path):
    with open(path) as f:
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

            feat_list = re.findall(r'\d{1,46}\:[0-9]+\.[0-9]+', row_data)
            if len(feat_list) == 46:
                feat_values = [float(feat.split(":")[1]) for feat in feat_list]
            else:
                print("Error: feature vector does not have length 46 !")
                os.exit()

            docID = row_data.split("#docid = ")[1].split(" inc =")[0]

            extrated_list = [rel_label, queryID, docID]
            extrated_list = extrated_list + feat_values
            pandas_data_collection.append(extrated_list)

        return pandas_data_collection


def verify(path2007, path2008):
    for TXT_FILENAME in TXT_FILENAMES:
        data_collection_2007 = load_and_extract(os.path.join(path2007, TXT_FILENAME))
        data_collection_2008 = load_and_extract(os.path.join(path2008, TXT_FILENAME))

        combined_data_collection = data_collection_2007 + data_collection_2008

        df = pd.DataFrame(combined_data_collection, columns=["relLabels", "queryID", "docID"] + ["feature_%s"%f for f in range(46)])
        df.to_csv(os.path.join(COMB_SAVE_DATA, "%s.csv" % TXT_FILENAME[:-4]), index=True)
        print("%s shape : " % TXT_FILENAME, df.shape)

        # Write txt file
        with open(os.path.join(COMB_SAVE_DATA, TXT_FILENAME), "w") as write_file:
            for index, row in df.iterrows():
                write_line = "%s qid:%s " % (row["relLabels"], row["queryID"])

                feature_cols = ["feature_%s" % e for e in range(df.shape[1] - CONST_COL)]
                for i, feat in enumerate(row[feature_cols]): write_line += "%d:%f " % (i + 1, feat)
                # print(write_line)
                # break

                write_line += "#docid = %s" % row["docID"]
                write_line += " inc = 1"
                write_line += " prob = 0.001"  # maybe random generator
                write_line += "\n"
                write_file.write(write_line)


if __name__ == "__main__":
    verify(MQ2007_PATH, MQ2008_PATH)