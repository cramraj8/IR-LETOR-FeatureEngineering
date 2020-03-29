#!/bin/bash

N_FOLDS=5
TOP_K=10
fold="Fold"
datasets="train vali test"
SRC_DIR="../../../project_2/MQ2007/"
SAVE_MODEL_PATH="./results"

for i in $(seq 1 $N_FOLDS); do
    # LambdaMART model : 6

    # function to train model and save model
    train_path="${SRC_DIR}Fold${i}/train.txt"
    val_path="${SRC_DIR}Fold${i}/vali.txt"
    save_model_path="${SAVE_MODEL_PATH}/Fold${i}/LambdaMART.fold${i}.txt"

    java -jar RankLib.jar -silent -ranker 6 -train $train_path -validate $val_path -metric2t MAP -save $save_model_path

    # ====================== function to test model and rescore ======================
    for dataset in $datasets; do
        for k in $(seq 1 $TOP_K); do
            eval_input_path="${SRC_DIR}Fold${i}/${dataset}.txt"

            save_output_path="${SAVE_MODEL_PATH}/Fold${i}/${dataset}/LambdaMART_test_perf.fold${i}.${dataset}.NDCG@${k}.txt"
            metric_name="NDCG@${k}"
            java -jar RankLib.jar -load $save_model_path -test $eval_input_path -metric2T $metric_name -idv $save_output_path

            save_output_path="${SAVE_MODEL_PATH}/Fold${i}/${dataset}/LambdaMART_test_perf.fold${i}.${dataset}.P@${k}.txt"
            metric_name="P@${k}"
            java -jar RankLib.jar -load $save_model_path -test $eval_input_path -metric2T $metric_name -idv $save_output_path

        done
    done
    # test_path="${SRC_DIR}Fold${i}/test.txt"
    # save_test_NDCG_path="${SAVE_MODEL_PATH}/Fold${i}/LambdaMART_test_performance.NDCG@10.fold${i}.txt"
    # java -jar RankLib.jar -load $save_model_path -test $test_path -metric2T NDCG@10 -idv $save_test_NDCG_path

done