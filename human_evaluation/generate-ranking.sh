#!/usr/bin/env bash
cat scores/*csv > scores/aggregated/all.csv
../venv/bin/python scripts/ComputeWMTSLT23Results.py --separate-domains --task-type Document --csv-file scores/aggregated/all.csv foo | tee ranking.log
