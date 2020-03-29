
import os

ROOT_EVAL = "./enhanced_model/"

datasets = ["train", "vali", "test"]
N_FOLDS = 5

def setup_the_folder():
    if not os.path.exists(ROOT_EVAL):
        os.makedirs(ROOT_EVAL)

    for i in range(N_FOLDS):
        for dataset in datasets:
            dataset_selection_path = os.path.join(ROOT_EVAL, "Fold%s" % str(i+1), dataset)

            if not os.path.exists(dataset_selection_path):
                os.makedirs(dataset_selection_path)


if __name__ == "__main__":
    setup_the_folder()