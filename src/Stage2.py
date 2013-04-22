import nltk,sys
import pymongo,re
from pymongo import MongoClient
from Constants import Constants

#Stage 0 - loading Annotated Reviews from Excel to Mongo
#Stage 1 - Each Review be cleaned from Stopwords

class Stage2():
    const = Constants()
    
    def loadStopWords(self):
        self.stop_words = re.split('\s+',file(self.const.FILE_STOP_WORDS).read().lower())
    
    def processReview(self,review):
        punctuation = re.compile(r'[-.?,\'"%:#&+/=;()|0-9]')  # [-.?!,":;()|0-9]'
        review_text = review["review"]
        review_text = punctuation.sub("",review_text)  # Removing punctuations
        tokens = nltk.word_tokenize(review_text) # review_text.split(" ")
        tokens = [token for token in tokens if not token in self.stop_words]
        #tokens = nltk.word_tokenize()
        # Below line first reads the list of token and then checks against the list of stopwords
        # if a stopword then it just continues
        # if not a stop word then adds it to the list
        revised = [punctuation.sub("",word) for word in tokens]
        review_text = " ".join(revised)
        return review_text
        
    def loadTable(self,table):
        try:
            DB = self.client[self.const.DB_YELP_MONGO];
            srcCollection = DB[self.const.COLLECTION_ANNOTATED_REVIEWS]
            destCollection = DB[self.const.COLLECTION_ANNOTATED_REVIEWS_WO_STOPWORDS]
            reviews = []
            for review in srcCollection.find():
                review['review'] = self.processReview(review)
                reviews.append(review)
            destCollection.insert(reviews)
        except:
            print "LoadTable Error:",sys.exc_info()
    def __init__(self):
        self.client = MongoClient(self.const.Mongo_Host);
        self.loadStopWords()
        self.loadTable(self.const.COLLECTION_ANNOTATED_REVIEWS)
        
obj = Stage2();