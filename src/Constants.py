import os

class Constants():
    #Strings
    COLLECTION_ANNOTATED_REVIEWS="annotated_reviews"
    COLLECTION_ANNOTATED_REVIEWS_WO_STOPWORDS = "Review_no_stopwords"
    COLLECTION_ANNOTATED_REVIEWS_WO_PUNCTUATIONS = "Review_no_punctuations"
    COLLECTION_TRAINSET = "trainset"
    COLLECTION_TESTSET = "testset"
    COLLECTION_REJECTED_REVIEWS = "Reject_reviews"
    COLLECTION_REVIEW = "review"
    COLLECTION_UNIGRAMS = "Unigrams"
    COLLECTION_UNIGRAMS_PRUNED_ACCEPT = "Unigrams_Pruned_Accept"
    COLLECTION_UNIGRAMS_PRUNED_REJECT = "Unigrams_Pruned_Reject"
    COLLECTION_TEMP_BIGRAMS = "BIGRAMS_WO_COUNT"
    COLLECTION_BIGRAMS = "Bigrams"
    COLLECTION_BIGRAMS_PRUNE_ACCEPT = "Bigrams_Prune_Accept"
    COLLECTION_BIGRAMS_PRUNE_REJECT = "Bigrams_Prune_Reject"
    COLLECTION_TRIGRAMS = "Trigrams"
    COLLECTION_TRIGRAMS_PRUNE_ACCEPT = "Trigrams_Prune_Accept"
    COLLECTION_TRIGRAMS_PRUNE_REJECT = "Trigrams_Prune_Reject"
    COLLECTION_STOP_WORDS = "Stopwords"
    COLLECTION_FEATURES = "features"
    COLLECTION_FEATURES_CLEAN = "features_clean"
    ADDITIONAL_FEATURES = 8  # IsFoodGood....,IsPriceBad,IsRatingBad,IsRatingModerate,IsRatingGood,
    FILE_STOP_WORDS = "..%sRes%sStopWords.txt"%(os.sep,os.sep)
    SYNONYMS = "..%sRes%ssynonym.txt"%(os.sep,os.sep)
    EXT_EXCEL = ".xlsx" 
    LABEL_FEATURES_ALL = ["IsFoodGood","IsFoodBad","IsServiceGood","IsServiceBad","IsAmbianceGood","IsAmbianceBad","IsDealsGood","IsDealsBad","IsPriceGood","IsPriceBad","IsRatingBad","IsRatingModerate","IsRatingGood"]
    LABEL_FEATURES_GOOD = ["IsFoodGood","IsServiceGood","IsAmbianceGood","IsDealsGood", "IsPriceGood","IsRatingBad","IsRatingModerate","IsRatingGood"]
    OUTPUT_FILE_TRAIN = "result.arff"
    OUTPUT_FILE_TEST = "test_result.arff"
    #Numbers
    FIRST_SHEET = 0
    UNIGRAM_THRESHOLD = 10
    #END
    #delimiters
    whitespace = " "
    DELIMITER_SYNONYMS = ":"
    
    #configurations for script
    GENERATE_TRIGRAMS = False
    GENERATE_BIGRAMS = True
    GENERATE_UNIGRAMS = False
    GENERATE_BIGRAMS_WITH_STOP_WORDS = False
    GENERATE_TRIGRAMS_WITH_STOP_WORDS = True
    LOAD_ANNOTATED_REVIEWS_FROM_FILE_TO_MONGO =False
    Mongo_Host = "localhost"
    DB_YELP_MONGO = "yelp"
    
