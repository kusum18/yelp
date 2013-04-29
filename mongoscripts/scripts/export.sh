#bibash
# file_fields_path UservaibhavsainDocumentworkspacyelmongoscriptscripts
# output_path =UservaibhavsainDocumentworkspacyelp
#-- Unigrams---
mongoexport --db $3 --collection Unigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpuunigramunigrams_freq.csv
mongoexport --db $3 --collection Food_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpuunigramFood_Unigrams.csv
mongoexport --db $3 --collection Service_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpuunigramService_Unigrams.csv
mongoexport --db $3 --collection Price_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpuunigramPrice_Unigrams.csv
mongoexport --db $3 --collection Ambiance_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpuunigramAmbience_Unigrams.csv
mongoexport --db $3 --collection Deal_Unigrams --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpuunigramDeals_Unigrams.csv
# -- bigrams----
mongoexport --db $3 --collection Bigrams_With_Freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpubigramBigrams_With_Freq.csv
mongoexport --db $3 --collection Food_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpubigramFood_Bigrams_with_freq.csv
mongoexport --db $3 --collection Service_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpubigramService_Bigrams_with_freq.csv
mongoexport --db $3 --collection Price_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpubigramPrice_Bigrams_with_freq.csv
mongoexport --db $3 --collection Ambiance_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpubigramAmbience_Bigrams_with_freq.csv
mongoexport --db $3 --collection Deals_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outpubigramDeals_Bigrams_with_freq.csv
# -- trigrams--
mongoexport --db $3 --collection Trigrams_With_Freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outputrigramTrigrams_With_Freq.csv
mongoexport --db $3 --collection Food_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outputrigramFood_Trigrams_with_freq.csv
mongoexport --db $3 --collection Service_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outputrigramService_Trigrams_with_freq.csv
mongoexport --db $3 --collection Price_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outputrigramPrice_Trigrams_with_freq.csv
mongoexport --db $3 --collection Ambiance_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outputrigramAmbience_Trigrams_with_freq.csv
mongoexport --db $3 --collection Deals_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/outputrigramDeals_Trigrams_with_freq.csv
#-- combined--



