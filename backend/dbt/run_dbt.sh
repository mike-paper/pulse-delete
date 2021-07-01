#!/bin/bash
# echo $PAPER_DBT_SCHEMA
cd dbt
# dbt --log-format json run --profiles-dir . --model plans
dbt --log-format json run --profiles-dir . 