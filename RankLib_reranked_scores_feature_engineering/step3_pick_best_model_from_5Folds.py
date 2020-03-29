
import os
from glob import glob
import numpy as np
import shutil

MODEL_SELECTION_ROOT = "./model_selection/"

MODELS = ["MART", "RankNet", "RankBoost", "AdaRank", "CoordinateAscent", "LambdaMART", "ListNet", "RandomForests"]
# MODELS = ["MART"] # TODO: remove this and keep above
N_FOLDS = 5

SAVE_BEST_MODEL_DIR = "best_model"


def pick_best_fold_model():

    model_best_fold_dict = {}
    for model in MODELS:
        model_selection_path = os.path.join(MODEL_SELECTION_ROOT, model)

        model_folds_test_result_files = glob(os.path.join(model_selection_path, "Fold*/model_test_performance.NDCG@10.%s.fold*.txt" % model))

        model_scores = []
        for fold_test_file in model_folds_test_result_files:
            with open(fold_test_file, "r") as read_file:
                data = read_file.read().split("\n")
                data = [e for e in data if e != ""]
                last_line = data[-1]
                avg_NDCG_at_10_score_list = last_line.split(" ")
                avg_NDCG_at_10_score_list = [e for e in avg_NDCG_at_10_score_list if e != ""]
                if avg_NDCG_at_10_score_list[1] != "all":
                    print("Error in test score file !")
                    os.exit()
                avg_NDCG_at_10_score = float(avg_NDCG_at_10_score_list[2])
                model_scores.append(avg_NDCG_at_10_score)

        max_model_score = np.max(model_scores)
        best_model_fold = np.argmax(model_scores) + 1 # based on index-0

        model_best_fold_dict[model] = best_model_fold

        # Copy the best model into a separate folder
        best_model_dir_path = os.path.join(model_selection_path, SAVE_BEST_MODEL_DIR)
        if not os.path.exists(best_model_dir_path):
            os.makedirs(best_model_dir_path)
        best_model_src_file_path = os.path.join(model_selection_path, "Fold%d" % best_model_fold, "model.%s.fold%d.txt" % (model, best_model_fold))
        best_model_save_file_path = os.path.join(best_model_dir_path, "best_model.%s.txt" % (model))
        shutil.copyfile(best_model_src_file_path, best_model_save_file_path)

    print(model_best_fold_dict)


if __name__ == "__main__":
    pick_best_fold_model()