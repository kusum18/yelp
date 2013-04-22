import sys,nltk,pymongo,re
from pymongo import MongoClient
from Constants import Constants
from nltk import bigrams

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
    
    def processReview(self,review):
        review_text = review["review"]
        tokens = review_text.split(" ")
        bigram_list = bigrams(tokens)
        list = [{"word":bigram[0]+" "+bigram[1]} for bigram in bigram_list if self.string_found(bigram)]
        return list
        
    def generateBigrams(self):
        Client = MongoClient(self.const.Mongo_Host)
        DB = Client[self.const.DB_YELP_MONGO]
        Collection = DB[self.const.COLLECTION_ANNOTATED_REVIEWS_WO_STOPWORDS]
        DestCollection = DB[self.const.COLLECTION_TEMP_BIGRAMS]
        try:
            for review in Collection.find():
                list = self.processReview(review)
                if list==[]:
                    pass
                else:
                    DestCollection.insert(list);
        except:
            print "Bigrams Error",sys.exc_info()
        Client.close()
    
    def __init__(self):
        self.topUnigrams =TopNUnigrams().getListWithThreshold(self.const.UNIGRAM_THRESHOLD)
        self.generateBigrams();

obj = Stage3()