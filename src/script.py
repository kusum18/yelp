'''
Created on Apr 27, 2013

@author: vaibhavsaini
'''
from Constants import Constants
from Stage2 import Stage2
from Stage3 import Stage3
from Xls2mongo import Xls2mongo
import sys
import time

if __name__ == '__main__':
    print "running the script. this will take time."
    startTime = time.time()
    xls2mg = Xls2mongo()
    stage2 = Stage2()
    stage3 = Stage3()
    const = Constants()
    
    message = """
    please pay attention
    script will be run with following configuration. To stop enter 's'
    GENERATE_TRIGRAMS = {0}
    GENERATE_BIGRAMS = {1}
    GENERATE_UNIGRAMS = {2}
    GENERATE_BIGRAMS_WITH_STOP_WORDS = {3}
    GENERATE_TRIGRAMS_WITH_STOP_WORDS = {4}
    LOAD_ANNOTATED_REVIEWS_FROM_FILE_TO_MONGO ={5}
    """.format(const.GENERATE_TRIGRAMS, const.GENERATE_BIGRAMS,
               const.GENERATE_UNIGRAMS,const.GENERATE_BIGRAMS_WITH_STOP_WORDS,
               const.GENERATE_TRIGRAMS_WITH_STOP_WORDS,const.LOAD_ANNOTATED_REVIEWS_FROM_FILE_TO_MONGO)
    print message
    user_input = raw_input("To stop the script press 's', else press anything like 'c'")
    if user_input.lower() == 's':
        print("exiting..")
        sys.exit()
        print ("exited safely")

    if const.GENERATE_UNIGRAMS:
        print "xls2mg created"
        xls2mg.dropCollections()
        #load files to mongo
        if const.LOAD_ANNOTATED_REVIEWS_FROM_FILE_TO_MONGO:
            t1 =time.time()
            xls2mg.load()
            elapsed = (time.time() -t1)
            print "load took",elapsed, "seconds" 
        # clean up. create non_annotated_reviews and create annotated_reviews_clean
        t1 =time.time()
        xls2mg.removeUnFilledReviews()
        elapsed = (time.time() -t1)
        print "removing unfilled reviews took ",elapsed, "seconds" 
        #remove punctuations
        t1 =time.time()
        stage2.loadTable()
        elapsed = (time.time() -t1)
        print "removing punctuations took ",elapsed, "seconds"
        print "Loading Stopwords"
        stage2.loadStopWords()
        print "Done loading Stopwords" 
        # map reduce to create unigrams mongo 
        # *******Unigrams ************
        # generage unigrams with freq - combined
        t1 =time.time()
        stage3.generateUnigrams()
        elapsed = (time.time() -t1)
        print "generating unigrams took ",elapsed, "seconds" 
        # generate class wise unigrams with freq
        t1 =time.time()
        stage3.generateClassWiseUnigrams()
        elapsed = (time.time() -t1)
        print "generating classwise unigrams took ",elapsed, "seconds" 
        # ********** Bigrams ***********
    if const.GENERATE_BIGRAMS:
        # generate bigrams with out freq
        t1 =time.time()
        xls2mg.dropBigramCollections()
        stage3.generateBigrams()
        elapsed = (time.time() -t1)
        print "generating bigrams took ",elapsed, "seconds" 
        # generate bigrams with frequency - combined classes.
        t1 =time.time()
        stage3.genBigramsWithFreq()
        elapsed = (time.time() -t1)
        print "generating bigrams with freq took ",elapsed, "seconds" 
        #generate bigrams per class without frequency
        t1 =time.time()
        stage3.generateBigramsPerClass() 
        elapsed = (time.time() -t1)
        print "generating bigrams per class took ",elapsed, "seconds" 
        # generate bigrams with freq class wise
        t1 =time.time()
        stage3.genClassWiseBigramsWithFreq()
        elapsed = (time.time() -t1)
        print "generating classwise bigrams with freq took ",elapsed, "seconds" 
    #************* Trigrams*****************
    # generate trigrams without freq
    if const.GENERATE_TRIGRAMS:
        t1 =time.time()
        xls2mg.dropTrigramCollections()
        stage3.generateTrigrams()
        elapsed = (time.time() -t1)
        print "generating trigrams took ",elapsed, "seconds" 
        # generate trigrams with frequency - combined classes
        t1 =time.time()
        stage3.genTrigramsWithFreq()
        elapsed = (time.time() -t1)
        print "generating trigrams with freq took ",elapsed, "seconds" 
        #generate trigrams per class without frequency
        t1 =time.time()
        stage3.generateTrigramsPerClass() 
        elapsed = (time.time() -t1)
        print "generating trigrams per class ",elapsed, "seconds"
        # generate Trigrams with freq class wise
        t1 =time.time()
        stage3.genClassWiseTrigramsWithFreq()
        elapsed = (time.time() -t1)
        print "generating trigrams per class with freq took ",elapsed, "seconds"
    elapsed = (time.time() - startTime)/60
    print "Script completed. script took ", elapsed, " minutes"
