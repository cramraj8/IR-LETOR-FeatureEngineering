#!/bin/bash

models="MART RankNet RankBoost AdaRank CoordinateAscent LambdaMART ListNet RandomForests"
#models="MART" # TODO:
N_FOLDS=5
fold="Fold"
SRC_DIR="../../../project_2/MQ2007/"
SAVE_MODEL_PATH="./model_selection"

# Iterate the model string variable using for loop
model_ITER=0
for model_var in $models; do

    for i in $(seq 1 $N_FOLDS); do

      # function to train model and save model
      train_path="${SRC_DIR}Fold${i}/train.txt"
      val_path="${SRC_DIR}Fold${i}/vali.txt"
      save_model_path="${SAVE_MODEL_PATH}/${model_var}/Fold${i}/model.${model_var}.fold${i}.txt"
      echo $model_ITER
      java -jar RankLib.jar -silent -ranker $model_ITER -train $train_path -validate $val_path -metric2t MAP -save $save_model_path

      # function to test model and rescore
      test_path="${SRC_DIR}Fold${i}/test.txt"
      save_test_NDCG_path="${SAVE_MODEL_PATH}/${model_var}/Fold${i}/model_test_performance.NDCG@10.${model_var}.fold${i}.txt"
      java -jar RankLib.jar -load $save_model_path -test $test_path -metric2T NDCG@10 -idv $save_test_NDCG_path

    done
    model_ITER=$(expr $model_ITER + 1)

done
