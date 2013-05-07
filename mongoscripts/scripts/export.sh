#bibash
# file_fields_path UservaibhavsainDocumentworkspacyelmongoscriptscripts
# output/t_path =UservaibhavsainDocumentworkspacyelp
#-- Unigrams---
mongoexport --db $3 --collection Unigrams_with_freq_no_stopwords --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigram/unigrams_freq.csv
mongoexport --db $3 --collection Food_Unigrams_no_stopwords --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigram/Food_Unigrams.csv
mongoexport --db $3 --collection Service_Unigrams_no_stopwords --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigram/Service_Unigrams.csv
mongoexport --db $3 --collection Price_Unigrams_no_stopwords --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigram/Price_Unigrams.csv
mongoexport --db $3 --collection Ambiance_Unigrams_no_stopwords --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigram/Ambience_Unigrams.csv
mongoexport --db $3 --collection Deals_Unigrams_no_stopwords --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/unigram/Deals_Unigrams.csv
# -- bigrams----
mongoexport --db $3 --collection Bigrams_With_Freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigram/Bigrams_With_Freq.csv
mongoexport --db $3 --collection Food_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigram/Food_Bigrams_with_freq.csv
mongoexport --db $3 --collection Service_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigram/Service_Bigrams_with_freq.csv
mongoexport --db $3 --collection Price_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigram/Price_Bigrams_with_freq.csv
mongoexport --db $3 --collection Ambiance_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigram/Ambience_Bigrams_with_freq.csv
mongoexport --db $3 --collection Deals_Bigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/bigram/Deals_Bigrams_with_freq.csv
# -- trigrams--
mongoexport --db $3 --collection Trigrams_With_Freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigram/Trigrams_With_Freq.csv
mongoexport --db $3 --collection Food_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigram/Food_Trigrams_with_freq.csv
mongoexport --db $3 --collection Service_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigram/Service_Trigrams_with_freq.csv
mongoexport --db $3 --collection Price_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigram/Price_Trigrams_with_freq.csv
mongoexport --db $3 --collection Ambiance_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigram/Ambience_Trigrams_with_freq.csv
mongoexport --db $3 --collection Deals_Trigrams_with_freq --csv --fieldFile "$1/fields_unigrams.txt" --out $2/output/trigram/Deals_Trigrams_with_freq.csv
#-- combined--

# sample command, run from the yelp folder
# ./mongoscripts/scripts/export.sh ./mongoscripts/scripts ./output yelp

