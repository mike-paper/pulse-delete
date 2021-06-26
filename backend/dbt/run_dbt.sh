#!/bin/bash
# export PAPER_DBT_SCHEMA=some_test_2
echo $PAPER_DBT_SCHEMA
echo $PWD
cd dbt
echo $PWD
dbt run --profiles-dir .