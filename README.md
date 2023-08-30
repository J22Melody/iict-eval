# WMT23 SignLT Human evaluation

This repository contains data and scripts for reproducing human evaluation
settings and results for WMT23 Sign Language Translation Task.

## Content

Scripts:
* `generate-batches.sh` - produces batches for Appraise
* `generate-ranking.sh` - computes ranking from scores exported from Appraise

Data:
* `slttest2023.dsgs-de.all.xml` - the final test set with references and primary submissions
* `submissions/*.xml` - the official submissions to the shared task
* `batches/*.json` - JSON batches for creating a campaign in Appraise
* `scores/*.csv` - scores exported from Appraise
* `ranking.log` - output of Appraise script for computing system rankings
