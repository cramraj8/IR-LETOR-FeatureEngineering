

import pandas as pd
import re
import os


PATH = "../MQ2007/S5.txt"
DST_CSV_FILE = "extractedData_S5.csv"

"""

0 qid:10 1:0.000000 2:0.000000 3:0.000000 4:0.000000 5:0.000000 6:0.000000 7:0.000000 
8:0.000000 9:0.000000 10:0.000000 11:0.000000 12:0.000000 13:0.000000 14:0.000000 15:0.000000 
16:0.001348 17:0.000000 18:0.222222 19:0.000000 20:0.001282 21:0.000000 22:0.000000 23:0.000000 
24:0.000000 25:0.000000 26:0.000000 27:0.000000 28:0.000000 29:0.000000 30:0.000000 31:0.000000 
32:0.000000 33:0.000000 34:0.000000 35:0.000000 36:0.000000 37:0.000000 38:0.000000 39:0.000000 
40:0.000000 41:0.000000 42:0.000000 43:0.017241 44:0.000000 45:0.000000 46:0.000000 #docid = GX000-00-0000000 inc = 1 prob = 0.0246906

"""

"""
Questions:
1. can the feature value can be (-)ve? it looks like they are poositive
2. are they normalize or they have [0, 1] values?

"""

def explore_data(data_path):
	with open(data_path) as f:
		data = f.read()
		raw_data = data.split("\n")
		raw_data = [e for e in raw_data if e != ".DS_Store"]
		raw_data = [e for e in raw_data if e != ""]
		print("S1 sample size : ", len(raw_data))

		data_collection = [] # [rel-label, queryID, feature vector, docID]
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
		df = pd.DataFrame(pandas_data_collection, columns=["relLabels", "queryID", "docID"] + ["feature_%s"%f for f in range(46)])
		df.to_csv(DST_CSV_FILE, index=True)

		print("Unique Document IDs : ", len(set(df["docID"])))
		print("Unique Query IDs : ", len(set(df["queryID"])))


if __name__ == "__main__":
	explore_data(PATH)


