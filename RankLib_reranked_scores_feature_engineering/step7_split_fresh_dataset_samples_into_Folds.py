

import os
import shutil


SRC_TEXT_FILES_PATH = "./features_added_LETOR_data/"
SAVE_FOLD_DIR = "./features_added_LETOR_FoldsData/"
READ_ME_FILE = "readme.txt"
N_FOLDS = 5


def create_folds():
    if os.path.exists(SAVE_FOLD_DIR):
        shutil.rmtree(SAVE_FOLD_DIR)

    with open(READ_ME_FILE, "r") as f:
        for i in range(N_FOLDS + 1):
            fold_data = f.readline()
            if i == 0: continue

            tmp_list = fold_data.split("\t")
            tmp_list = [e for e in tmp_list if e != ""]
            fold_name = tmp_list[0]
            train_set = tmp_list[1].split(",")
            train_set = [e.strip() for e in train_set]
            val_set = tmp_list[2]
            test_set = tmp_list[3]
            print(tmp_list)

            fold_path = os.path.join(SAVE_FOLD_DIR, fold_name)
            if not os.path.exists(fold_path):
                os.makedirs(fold_path)

            # write test file
            with open(os.path.join(SRC_TEXT_FILES_PATH, "feat_added_data.%s.txt" % test_set)) as read_f:
                s_data = read_f.read()
                with open(os.path.join(fold_path, "test.txt"), "w") as write_f:
                    write_f.write(s_data)

            # write val file
            with open(os.path.join(SRC_TEXT_FILES_PATH, "feat_added_data.%s.txt" % val_set)) as read_f:
                s_data = read_f.read()
                with open(os.path.join(fold_path, "vali.txt"), "w") as write_f:
                        write_f.write(s_data)

            # write train file
            with open(os.path.join(fold_path, "train.txt"), "a") as write_f:
                for train in train_set:
                    with open(os.path.join(SRC_TEXT_FILES_PATH, "feat_added_data.%s.txt" % train)) as read_f:
                        s_data = read_f.read()
                        write_f.write(s_data)


if __name__ == "__main__":
    create_folds()