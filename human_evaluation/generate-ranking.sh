#!/usr/bin/env bash

set -xe

PYTHON=~/appraise/Appraise/venv/bin/python3
APPRAISE=~/appraise/Appraise

mkdir -p results

# sort scores
for idx in SegA SegB SegC DocA DocB DocC; do
    cat scores/WMT23SLT$idx.scores.csv \
        | sort -t',' -k1,1 -k2,2 -k8,8 -k11,11n \
        > scores/WMT23SLT$idx.scores.sorted.csv
done

# separate rankings for each annotator
for idx in A B C; do
    $PYTHON $APPRAISE/manage.py ComputeWMT21Results \
        --task-type Document \
        --csv-file <(cat scores/WMT23SLT???$idx.scores.sorted.csv | grep -v ',True,') foo \
        | tee results/WMT23SLT_$idx.results.log
done

# separate rankings for each document
for idx in Seg Doc; do
    $PYTHON $APPRAISE/manage.py ComputeWMT21Results \
        --task-type Document \
        --csv-file <(cat scores/WMT23SLT${idx}?.scores.sorted.csv | grep -v ',True,') foo \
        | tee results/WMT23SLT_$idx.results.log
done

# final ranking from all scores
$PYTHON $APPRAISE/manage.py ComputeWMT21Results \
    --task-type Document \
    --csv-file <(cat scores/WMT23SLT*.scores.sorted.csv | grep -v ',True,') foo \
    | tee results/WMT23SLT.results.log

tail -n7 results/*.log | column -ts $'\t' > results.txt
