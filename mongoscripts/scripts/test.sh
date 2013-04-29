#!/bin/bash
#-- Unigrams---
./mongoexport --db yelp_new --collection Unigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigrams/unigrams_freq.csv
./mongoexport --db yelp_new --collection Food_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigrams/Food_Unigrams.csv