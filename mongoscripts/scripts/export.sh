#!/bin/bash
# file_fields_path =/Users/vaibhavsaini/Documents/workspace/yelp/mongoscripts/scripts
# output_path = /Users/vaibhavsaini/Documents/workspace/yelp
#-- Unigrams---
./mongoexport --db yelp_new --collection Unigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigrams/unigrams_freq.csv
./mongoexport --db yelp_new --collection Food_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigrams/Food_Unigrams.csv
./mongoexport --db yelp_new --collection Service_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigrams/Service_Unigrams.csv
./mongoexport --db yelp_new --collection Price_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigrams/Price_Unigrams.csv
./mongoexport --db yelp_new --collection Ambiance_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigrams/Ambience_Unigrams.csv
./mongoexport --db yelp_new --collection Deal_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigrams/Deals_Unigrams.csv
# -- bigrams----
./mongoexport --db yelp_new --collection Bigrams_With_Freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigrams/Bigrams_With_Freq.csv
./mongoexport --db yelp_new --collection Food_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigrams/Food_Bigrams_with_freq.csv
./mongoexport --db yelp_new --collection Service_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigrams/Service_Bigrams_with_freq.csv
./mongoexport --db yelp_new --collection Price_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigrams/Price_Bigrams_with_freq.csv
./mongoexport --db yelp_new --collection Ambiance_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigrams/Ambience_Bigrams_with_freq.csv
./mongoexport --db yelp_new --collection Deals_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigrams/Deals_Bigrams_with_freq.csv
# -- trigrams--
./mongoexport --db yelp_new --collection Trigrams_With_Freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigrams/Trigrams_With_Freq.csv
./mongoexport --db yelp_new --collection Food_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigrams/Food_Trigrams_with_freq.csv
./mongoexport --db yelp_new --collection Service_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigrams/Service_Trigrams_with_freq.csv
./mongoexport --db yelp_new --collection Price_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigrams/Price_Trigrams_with_freq.csv
./mongoexport --db yelp_new --collection Ambiance_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigrams/Ambience_Trigrams_with_freq.csv
./mongoexport --db yelp_new --collection Deals_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigrams/Deals_Trigrams_with_freq.csv
#-- combined--



