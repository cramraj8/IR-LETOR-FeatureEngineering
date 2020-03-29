
import os
import numpy as np

ALGORITHM_NAME = "LambdaMART"
DATASET = "MQ2007"

SETS = {"testing set": "train", "validation set": "vali", "training set": "test"}
METRIC_SET = ["NDCG", "P"]
N_FOLDS = 5
N_TOP = 10
EXTRA_COLS = 2

READ_METRIC_FILES = "./enhanced_model/"
DST_EVAL_FILE = "./sample.Algorithname.%s.txt" % DATASET


def bring_all_eval_together():
    with open(DST_EVAL_FILE, "w") as write_file:
        write_data = "Algorithm: %s" % ALGORITHM_NAME
        write_data += "\nDataset: MQ2007"

        for set_name in SETS.keys():
            write_data += "\n\nPerformance on %s\n" % set_name

            for metric_set in METRIC_SET:

                write_data += "Fold" + "".join(["\t%s@%d" % (metric_set, e+1) for e in range(N_TOP)]) + "\tMean%s"%metric_set
                # write NDCGs
                fold_values_list = []
                for fold_num in range(1, N_FOLDS+1): # todo:
                    values_list = []
                    for k in range(1, N_TOP+1): # todo

                        # with open(READ_METRIC_FILES + "%s." % para_val + "NDCG@%s.txt" % (i+1), "r") as read_file:
                        with open(os.path.join(READ_METRIC_FILES,
                                               "Fold%s" % fold_num,
                                                SETS[set_name],
                                               "LambdaMART_test_perf.fold%d.%s.%s@%d.txt" % (fold_num, SETS[set_name], metric_set, k)), "r") as read_file:
                            metric_data = read_file.read().split("\n")
                            metric_data = [e for e in metric_data if e != ""]
                            mean_metric_score_list = metric_data[-1].split(" ")
                            mean_score_list = [e for e in mean_metric_score_list if e != ""]
                            if (mean_score_list[1] != "all"):
                                print("Error in  metric file : can not find mean value !")
                                exit()
                            mean_value = mean_score_list[2]
                            values_list.append(float(mean_value))
                    # add the previously set list MEAN also
                    values_list.append(np.mean(values_list))
                    fold_values_list.append(values_list)

                    write_line = "%s" % fold_num
                    for e in values_list: write_line += "\t%.4f" % e
                    write_data += "\n" + write_line

                # ==========================================================================================
                # ==========================================================================================
                avg_score = np.mean(fold_values_list, axis=0)
                write_line = "Avg"
                for e in avg_score: write_line += "\t%.4f" % e
                write_data += "\n" + write_line
                # ==========================================================================================
                # ==========================================================================================
                write_data += "\n\n"



        print(write_data)
        write_file.write(write_data)



            # for i in range(N_EXPERIMENTS + EXTRA_COLS):
            #     if i == 1:


"""
Para	NDCG@1	NDCG@2	NDCG@3	NDCG@4	NDCG@5	NDCG@6	NDCG@7	NDCG@8	NDCG@9	NDCG@10	MeanNDCG
0.5	0.4395	0.4613	0.4561	0.4517	0.4542	0.4617	0.4665	0.4730	0.4752	0.4818	0.5278	
5	0.4002	0.3889	0.3904	0.3902	0.3950	0.4006	0.4064	0.4100	0.4174	0.4266	0.4810	
"""


if __name__ == "__main__":
    bring_all_eval_together()