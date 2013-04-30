import nltk,sys
import pymongo,re
from pymongo import MongoClient
from Constants import Constants

#Stage 0 - loading Annotated Reviews from Excel to Mongo
#Stage 1 - Each Review be cleaned from Stopwords

class Stage2():

    def loadStopWords(self):
        try:
            print "Loading Stop words"
            self.stop_words = re.split('\s+',file(self.const.FILE_STOP_WORDS).read().lower())
            DB = self.client[self.const.DB_YELP_MONGO]
            collection = DB[self.const.COLLECTION_STOP_WORDS];
            for word in self.stop_words:
                collection.insert({"word":word});
        except:
            print "Error: Loading Stop words failed. \n Reason: ",sys.exc_info()
        
    
    def processReview(self,review):
        punctuation = re.compile(r'[-.?,\'"%:#&$*!+/=;~`()|0-9]')  # [-.?!,":;()|0-9]'
        review_text = review["review"]
        review_text = punctuation.sub("",review_text)  # Removing punctuations
        tokens = review_text.split(" ") # nltk.word_tokenize(review_text)
        tokens = [token for token in tokens]# if not token in self.stop_words]
        #tokens = nltk.word_tokenize()
        # Below line first reads the list of token and then checks against the list of stopwords
        # if a stopword then it just continues
        # if not a stop word then adds it to the list
        #revised = [punctuation.sub("",word) for word in tokens]
        review_text = " ".join(tokens)
        return review_text
        
    def loadTable(self):
        print("removing punctuations from reviews, sit back and relax")
        try:
            DB = self.db
            srcCollection = DB.annotated_reviews_clean
            destCollection = DB[self.const.COLLECTION_ANNOTATED_REVIEWS_WO_PUNCTUATIONS]
            reviews = []
            for review in srcCollection.find():
                review['review'] = self.processReview(review)
                reviews.append(review)
            destCollection.insert(reviews)
        except:
            print "LoadTable Error:",sys.exc_info()
        print(" punctuations removed. new clean reviews are in Review_no_punctuations collection")
    def __init__(self):
        self.const = Constants()
        self.client = MongoClient(self.const.Mongo_Host);
        self.db = self.client[self.const.DB_YELP_MONGO];
        #self.loadStopWords()
        

if __name__ == '__main__':
    obj = Stage2()
    obj.loadTable()