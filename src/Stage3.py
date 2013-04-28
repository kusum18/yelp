import sys,nltk,pymongo,re
from pymongo import MongoClient
from Constants import Constants
from nltk import bigrams
from nltk.util import trigrams

class TopNUnigrams():
    const = Constants
    
    def getListWithThreshold(self,min_count):
        Client = MongoClient(self.const.Mongo_Host)
        DB = Client[self.const.DB_YELP_MONGO]
        Collection = DB[self.const.COLLECTION_UNIGRAMS]
        Words = []
        WC_Cursor = Collection.find({"value": { "$gte" : min_count  }})
        for wc in WC_Cursor:
            word = wc["_id"]
            value = wc["value"]
            Words.append(word)
        Client.close()
        return Words
        

class Stage3():
    
    const = Constants();
    
    def string_found(self,word):
        if (word[0] in self.topUnigrams) or (word[1] in self.topUnigrams):
            return True
        return False
    
    def processReview_bigram(self,review):
        review_text = review["review"]
        tokens = review_text.split(" ")
        bigram_list = bigrams(tokens)
        list = [{"word":bigram[0]+" "+bigram[1]} for bigram in bigram_list]# if self.string_found(bigram)]
        return list
    
    def processReview_trigram(self,review):
        review_text = review["review"]
        tokens = review_text.split(" ")
        trigram_list = trigrams(tokens)
        list = [{"word":trigram[0]+" "+trigram[1]+" "+ trigram[2]} for trigram in trigram_list]# if self.string_found(bigram)]
        return list
        
    def generateBigrams(self):
        Client = MongoClient(self.const.Mongo_Host)
        DB = Client[self.const.DB_YELP_MONGO]
        Collection = DB[self.const.COLLECTION_ANNOTATED_REVIEWS_WO_PUNCTUATIONS]
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
        Client.close()

    def generateTrigrams(self):
        Client = MongoClient(self.const.Mongo_Host)
        DB = Client[self.const.DB_YELP_MONGO]
        Collection = DB[self.const.COLLECTION_ANNOTATED_REVIEWS_WO_PUNCTUATIONS]
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
        Client.close()
        print "processing done!"

    def generateTrigramsPerClass(self):
        Client = MongoClient(self.const.Mongo_Host)
        DB = Client[self.const.DB_YELP_MONGO]
        Collection = DB[self.const.COLLECTION_ANNOTATED_REVIEWS_WO_PUNCTUATIONS]
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
        Client.close()

    def generateBigramsPerClass(self):
        Client = MongoClient(self.const.Mongo_Host)
        DB = Client[self.const.DB_YELP_MONGO]
        Collection = DB[self.const.COLLECTION_ANNOTATED_REVIEWS_WO_PUNCTUATIONS]
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
        Client.close()

    def __init__(self):
        #self.topUnigrams =TopNUnigrams().getListWithThreshold(self.const.UNIGRAM_THRESHOLD)
        self.generateTrigramsPerClass();

obj = Stage3()