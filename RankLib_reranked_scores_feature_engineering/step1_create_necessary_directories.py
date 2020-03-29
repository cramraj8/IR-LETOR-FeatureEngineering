
import os

MODEL_SELECTION_ROOT = "./model_selection/"

MODELS = ["MART", "RankNet", "RankBoost", "AdaRank", "CoordinateAscent", "LambdaMART", "ListNet", "RandomForests"]
N_FOLDS = 5


def setup_the_folder():
    if not os.path.exists(MODEL_SELECTION_ROOT):
        os.makedirs(MODEL_SELECTION_ROOT)

    for model in MODELS:
        model_selection_path = os.path.join(MODEL_SELECTION_ROOT, model)
        for i in range(N_FOLDS):
            fold_model_selection_path = os.path.join(model_selection_path, "Fold%d" % (i+1))
            if not os.path.exists(fold_model_selection_path):
                os.makedirs(fold_model_selection_path)


if __name__ == "__main__":
    setup_the_folder()