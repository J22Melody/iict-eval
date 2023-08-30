#!/usr/bin/env bash -x

APPRAISE_PYTHON=~/appraise/Appraise/venv/bin/python3

mkdir -p batches


# the final XML testset with the reference and primary submissions
$APPRAISE_PYTHON scripts/combine.py \
    -i submissions/slttest2023.dsgs-de.src-ref.xml \
    -o slttest2023.dsgs-de.all.xml \
    submissions/slttest2023.dsgs-de.dsgs-de.*.xml


prefix=batches/batches.slttest2023.sgg-deu.doclvl

# only document-level documents
$APPRAISE_PYTHON scripts/combine.py \
    -i submissions/slttest2023.dsgs-de.src-ref.xml \
    --rm-docs signsuisse -o slttest2023.dsgs-de.doclvl.xml \
    submissions/slttest2023.dsgs-de.dsgs-de.*.xml

$APPRAISE_PYTHON ./scripts/create_wmt22_tasks.py \
    -f slttest2023.dsgs-de.doclvl.xml -o $prefix -s sgg -t deu --rng-seed 1111 \
    --max-segs 10 --static-context 5 --no-qc \
    | tee $prefix.log


prefix=batches/batches.slttest2023.sgg-deu.seglvl

# only segment-level documents
$APPRAISE_PYTHON scripts/combine.py \
    -i submissions/slttest2023.dsgs-de.src-ref.xml \
    --rm-docs srf -o slttest2023.dsgs-de.seglvl.xml \
    submissions/slttest2023.dsgs-de.dsgs-de.*.xml

$APPRAISE_PYTHON ./scripts/create_wmt22_tasks.py \
    -f slttest2023.dsgs-de.seglvl.xml -o $prefix -s sgg -t deu --rng-seed 1111 \
    --max-segs 10 --static-context 1 --no-qc \
    | tee $prefix.log
