#!/bin/bash

models="MART RankNet RankBoost AdaRank CoordinateAscent LambdaMART ListNet RandomForests"
#models="MART" TODO:
N_FOLDS=5
fold="Fold"
SRC_DIR="../../../project_2/MQ2007/"
SAVE_MODEL_PATH="./model_selection"
SAVE_BEST_MODEL_DIR="best_model"

# Iterate the model string variable using for loop
model_ITER=0
for model_var in $models; do

    for i in $(seq 1 $N_FOLDS); do

      # function to take best model and compute reranked scores for doc-query pairs
      # each fold train-set is our input here
      input_train_data_path="${SRC_DIR}Fold${i}/train.txt"
      input_val_data_path="${SRC_DIR}Fold${i}/vali.txt"
      input_test_data_path="${SRC_DIR}Fold${i}/test.txt"
      best_model_path="${SAVE_MODEL_PATH}/${model_var}/${SAVE_BEST_MODEL_DIR}"
      # pick the only-available file in best_model folder
      best_model_file="$best_model_path/best_model.${model_var}.txt"

#      save_score_file="$best_model_path/model_reranked_scores.NDCG@10.${model_var}.txt"
#      best_model_file=""
#      for file in "$best_model_path"/*
#      do
#        best_model_file="$file"
#      done
#      echo $best_model_file
#      echo $save_score_file

      save_score_train_file="${SAVE_MODEL_PATH}/${model_var}/Fold${i}/reranked_scores.${model_var}.fold${i}.train.txt"
      save_score_val_file="${SAVE_MODEL_PATH}/${model_var}/Fold${i}/reranked_scores.${model_var}.fold${i}.vali.txt"
      save_score_test_file="${SAVE_MODEL_PATH}/${model_var}/Fold${i}/reranked_scores.${model_var}.fold${i}.test.txt"

      # java -jar RankLib.jar -load $best_model_file -rank $input_data_path -score $save_score_file
      java -jar RankLib.jar -load $best_model_file -rank $input_train_data_path -indri $save_score_train_file
      java -jar RankLib.jar -load $best_model_file -rank $input_val_data_path -indri $save_score_val_file
      java -jar RankLib.jar -load $best_model_file -rank $input_test_data_path -indri $save_score_test_file

    done
    model_ITER=$(expr $model_ITER + 1)

done
