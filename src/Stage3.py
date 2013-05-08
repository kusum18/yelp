from Constants import Constants
from bson import Code
from nltk import bigrams
from nltk.util import trigrams
from pymongo import MongoClient
import sys
import nltk
import pymongo
import re
from Stage2 import Stage2
class TopNUnigrams():
    const = Constants
    
    def getListWithThreshold(self,min_count):
        DB = self.db # Client[self.const.DB_YELP_MONGO]
        Collection = DB[self.const.COLLECTION_UNIGRAMS]
        Words = []
        WC_Cursor = Collection.find({"value": { "$gte" : min_count  }})
        for wc in WC_Cursor:
            word = wc["_id"]
            value = wc["value"]
            Words.append(word)
        return Words
        

class Stage3():
    
    const = Constants();
    
    def string_found(self,word):
        if (word[0] in self.topUnigrams) or (word[1] in self.topUnigrams):
            return True
        return False
    
    def processReview_bigram(self,review):
        review_text = self.stage2.removePunctuations(review["review"])
        if self.const.GENERATE_BIGRAMS_WITH_STOP_WORDS:
            pass
        else:
            review_text = self.removeStopWordsFromReview(review_text)
        review_text = review_text.lower()
        tokens = review_text.split(" ")
        bigram_list = bigrams(tokens)
        lst =[]
        for bigram in bigram_list:# if self.string_found(bigram)]
            first_word = bigram[0].strip()
            second_word = bigram[1].strip()
            if ""==first_word or ""==second_word:
                pass
            else:
                lst.append({"word":first_word+" "+second_word})
        return lst
    
    def processReview_trigram(self,review):
        review_text = self.stage2.removePunctuations(review["review"])
        if self.const.GENERATE_TRIGRAMS_WITH_STOP_WORDS:
            pass
        else:
            review_text = self.removeStopWordsFromReview(review_text)
        review_text = review_text.lower()
        tokens = review_text.split(" ")
        trigram_list = trigrams(tokens)
        lst =[]
        for trigram in trigram_list:# if self.string_found(bigram)]
            first_word = trigram[0].strip()
            second_word = trigram[1].strip()
            third_word = trigram[2].strip()
            if ""==first_word or ""==second_word or ""==third_word:
                pass
            else:
                lst.append({"word":first_word+" "+second_word+" "+third_word})
        return lst
        
    def generateBigrams(self):
        print("generating bigrams from trainset ")
        DB = self.db
        Collection = DB[self.const.COLLECTION_TRAINSET]
        DestCollection = DB[self.const.COLLECTION_TEMP_BIGRAMS]
        try:
            for review in Collection.find():
                list = self.processReview_bigram(review)
                if list==[]:
                    pass
                else:
                    DestCollection.insert(list);
        except:
            print "Bigrams Error",sys.exc_info()
        print("bigrams generated. they do not have freq as of now.")

    def generateTrigrams(self):
        print("generating trigrams combined. sit back this will take time")
        DB = self.db
        Collection = DB[self.const.COLLECTION_TRAINSET]
        #DestCollection = DB[self.const.COLLECTION_TEMP_BIGRAMS]
        print "processing.."
        try:
            for review in Collection.find():
                list = self.processReview_trigram(review)
                if list==[]:
                    pass
                else:
                    DB.Trigrams_no_freq.insert(list);
        except:
            print "Trigrams Error",sys.exc_info()
        print "processing done! trigrams generated in Trigrams_no_freq collection"

    def generateTrigramsPerClass(self):
        print "generating trigrams per class. Note. no freq as of now"
        DB = self.db
        Collection = DB[self.const.COLLECTION_TRAINSET]
        #DestCollection = DB[self.const.COLLECTION_TEMP_BIGRAMS]
        try:
            for review in Collection.find():
                list = self.processReview_trigram(review)
                if list==[]:
                    pass
                else:
                    if review['Food']==1:
                        DB.Food_trigrams_temp.insert(list)
                    if review['Service']==1:
                        DB.Service_trigrams_temp.insert(list)
                    if review['Ambiance']==1:
                        DB.Ambiance_trigrams_temp.insert(list)
                    if review['Deals']==1:
                        DB.Deals_trigrams_temp.insert(list)
                    if review['Price']==1:
                        DB.Price_trigrams_temp.insert(list)
        except:
            print "Trigrams Error",sys.exc_info()
        print "DONE!! generating trigrams per class. Note. no freq as of now"

    def generateBigramsPerClass(self):
        print("generating bigrams per class")
        DB = self.db
        Collection = DB[self.const.COLLECTION_TRAINSET]
        #DestCollection = DB[self.const.COLLECTION_TEMP_BIGRAMS]
        try:
            for review in Collection.find():
                list = self.processReview_bigram(review)
                if list==[]:
                    pass
                else:
                    if review['Food']==1:
                        DB.Food_bigrams_temp.insert(list)
                    if review['Service']==1:
                        DB.Service_bigrams_temp.insert(list)
                    if review['Ambiance']==1:
                        DB.Ambiance_bigrams_temp.insert(list)
                    if review['Deals']==1:
                        DB.Deals_bigrams_temp.insert(list)
                    if review['Price']==1:
                        DB.Price_bigrams_temp.insert(list)
        except:
            print "Bigrams Error",sys.exc_info()
        print ("bigrams per class generated, they do not have freq as of now.")

    def generateUnigrams(self):
        print ("generate unigrams from Review_no_punctuations collection...")
        map = Code("""
            function(){
                review_text = this.review.toLowerCase();
                tokens = review_text.split(" ")
                tokens.forEach(function(word){ 
                    emit(word,1)
                });
            }
            """)
        reduce = Code("""
            function(word,count){
                return Array.sum(count)
            }
        """)
        self.db.Review_no_punctuations.map_reduce(map, 
                                                 reduce,
                                                 "Unigrams_with_freq")
        print "clean now"
        self.cleanUnigramsStopwords("Unigrams_with_freq", "Unigrams_with_freq_no_stopwords", "Unigrams_with_freq_withStopwords")
        print ("generating unigrams done")
    
    def generateClassWiseUnigrams(self):
        print ("generating class  wise unigrams")
        classes = ["Food","Service","Ambiance","Deals","Price"]
        for each_class in classes:
            mapFunction = Code("""
                function(){
                    if(this.%s==1){
                        review_text = this.review.toLowerCase();
                        tokens = review_text.split(" ")
                        tokens.forEach(function(word){ 
                            emit(word,1)
                        });
                    }
                }
            """%each_class)
            
            reduce = Code("""
                function(word,count){
                    return Array.sum(count)
                }
            """)
            print("generating unigrams for %s"%each_class)
            self.db.Review_no_punctuations.map_reduce(mapFunction,
                                                     reduce,
                                                     "%s_Unigrams"%each_class)
            self.cleanUnigramsStopwords("%s_Unigrams"%each_class, "%s_Unigrams_no_stopwords"%each_class, "%s_Unigrams_with_stopwords"%each_class)
            
        print("generating unigrams done")
    
    def genBigramsWithFreq(self):
        print("generating bigrams with frequency")
        map = Code("""
                function(){
                    bigram_word = this.word.toLowerCase();
                    emit(bigram_word,1)
                }
            """)
        reduce = Code("""
                function(word,count){
                    return Array.sum(count)
                }
            """)

        self.db[self.const.COLLECTION_TEMP_BIGRAMS].map_reduce(map,
                                                               reduce,
                                                               "Bigrams_With_Freq")
        print ("generating bigrams with freq done")
    
    def genClassWiseBigramsWithFreq(self):
        #class wise bigrams
        print("generating bigrams per class with freq now")
        classes = ["Food","Service","Ambiance","Deals","Price"]
        for each_class in classes:
            map = Code("""
                    function(){
                        bigram_word = this.word.toLowerCase();
                        emit(bigram_word,1)
                    }
                """)
    
            reduce = Code("""
                    function(word,count){
                        return Array.sum(count)
                    }
                """)

            print("generating %s bigrams"%each_class)
            self.db["%s_bigrams_temp"%each_class].map_reduce(map,
                                                reduce,
                                                "%s_Bigrams_with_freq"%each_class)
        
        print ("generating bigrams per class with freq done")

    def genTrigramsWithFreq(self):
        print("generating trigrams with frequency for combined classes")
        map = Code("""
                function(){
                    trigram_word = this.word.toLowerCase();
                    emit(trigram_word,1)
                }
            """)
        reduce = Code("""
                function(word,count){
                    return Array.sum(count)
                }
            """)

        self.db.Trigrams_no_freq.map_reduce(map,
                                            reduce,
                                            "Trigrams_With_Freq")
        print ("generating trigrams with freq done")

    def genClassWiseTrigramsWithFreq(self):
        #class wise trigrams
        print "generating trigrams per class with freq "
        classes = ["Food","Service","Ambiance","Deals","Price"]
        for each_class in classes:
            map = Code("""
                    function(){
                        trigram_word = this.word.toLowerCase();
                        emit(trigram_word,1)
                    }
                """)
    
            reduce = Code("""
                    function(word,count){
                        return Array.sum(count)
                    }
                """)
    
            print("generating %s trigrams"%each_class)
            self.db["%s_trigrams_temp"%each_class].map_reduce(map,
                                                reduce,
                                                "%s_Trigrams_with_freq"%each_class)
        print ("generating trigrams per class with freq done")
        
    
    def cleanUnigramsStopwords(self,srcCollection,destAcceptCollection,destRejectCollection):
        print "removing stop words from ", srcCollection , "and creating ", destAcceptCollection, "and", destRejectCollection
        try:
            SWC = self.db[self.const.COLLECTION_STOP_WORDS]
            swlist = [] # stop word list 
            for sw in SWC.find():
                swlist.append(sw['word'])
            Unigrams = self.db[srcCollection]
            Unigrams_Accept = self.db[destAcceptCollection]
            Unigrams_Reject = self.db[destRejectCollection]
            for unigram in Unigrams.find():
                try:
                    word = unigram['_id'];
                    if word in swlist:
                        Unigrams_Reject.insert(unigram)
                    else:
                        Unigrams_Accept.insert(unigram)
                except:
                    print "Error: Cleaning Unigrams from Stop words. \n Reason: ",sys.exc_info()
        except:
            print "Error: Cleaning Unigrams from Stopwords, \n Reason: ",sys.exc_info()
        print "stop words removed check ",destAcceptCollection 
    
    def removeStopWordsFromReview(self,review_text):
        SWC = self.db[self.const.COLLECTION_STOP_WORDS]
        swlist = [] # stop word list 
        for sw in SWC.find():
            swlist.append(sw['word'].lower())
        tokens = review_text.split(" ")
        review_tokens = []
        for token in tokens:
            if token.lower() not in swlist:
                review_tokens.append(token)
            else:
                pass
        review_text = " ".join(review_tokens)
        return review_text

    def __init__(self):
        self.client = MongoClient(self.const.Mongo_Host)
        self.db = self.client[self.const.DB_YELP_MONGO]
        self.stage2 = Stage2()
        #self.topUnigrams =TopNUnigrams().getListWithThreshold(self.const.UNIGRAM_THRESHOLD)
        #self.generateTrigramsPerClass();

    def close(self):
        self.client.close()

if __name__ == '__main__':
    obj = Stage3()
    obj.generateBigrams()