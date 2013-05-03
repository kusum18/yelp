import sys,arff
from pymongo import MongoClient
from Constants import Constants
import nltk
from Stage2 import Stage2
from Stage3 import Stage3
import time

class GenerateArff():
    
    def loadfeatureset(self,tokens,featureset):
        try:
            for token in tokens:
                if token in self.features:
                    index = self.features.index(token)
                    featureset[index]=1
                else:
                    pass
        except:
            pass
    
    def checkUnigrams(self,review,featureset):
        try:
            tokens = review["review"].lower().split(self.const.whitespace)
            self.loadfeatureset(tokens, featureset)
        except:
            print "Error: Loading Unigrams. \n Reason: ",sys.exc_info()
    
    def checkBigrams(self,review,featureset):
        try:
            tokens = self.stage3.processReview_bigram(review)
            self.loadfeatureset(tokens, featureset)
        except:
            print "Error: Loading Bigrams. \n Reason: ",sys.exc_info()
    
    def checkTrigrams(self,review,featureset):
        try:
            tokens = self.stage3.processReview_trigram(review)
            self.loadfeatureset(tokens, featureset)
        except:
            print "Error: Loading Trigrams. \n Reason: ",sys.exc_info()
    
    def checkAdditionalFeatures(self,review,featureset):
        try:
            index = len(self.features)
            categories = ["Food","Service","Ambiance","Deals","Price"]
            for category in categories:
                value = review[category]
                if value==1:
                    featureset[index]=1
                """elif value==-1:
                    featureset[index+1]=1"""
                index+=1
            rating = review["stars"]
            if rating==1 or rating==2:
                featureset[index]=1
            elif rating==3:
                featureset[index+1]=1
            elif rating==4 or rating==5:
                featureset[index+2]=1
        except:
            print "Error: Loading Additional Features. \n Reason: ",sys.exc_info()
    
    
    def loadFeatures(self):
        print "Loading Features"
        self.features = []
        featuresCollection = self.db[self.const.COLLECTION_FEATURES]
        try:
            for feature in featuresCollection.find():
                self.features.append(feature["word"])
            print "Finished Loading Features"
        except:
            print "Error: Loading Unigrams. \n Reason: ",sys.exc_info()
    
    def loadDataFeatures(self):
        try:
            reviews = self.db[self.const.COLLECTION_TRAINSET]; #COLLECTION_TRAINSET
            lengthOfFeatures = len(self.features)+self.const.ADDITIONAL_FEATURES
            print "length of features ",lengthOfFeatures
            dataFeatures = []
            for review in reviews.find():
                featureset = [0 for i in range(lengthOfFeatures)]
                #step 1 - check unigrams
                self.checkUnigrams(review, featureset)
                #step 2 - check bigrams
                self.checkBigrams(review, featureset)
                #step 3 - check trigrams
                self.checkTrigrams(review, featureset)
                #step 4 - check additional features
                self.checkAdditionalFeatures(review, featureset)
                dataFeatures.append(featureset)
            return dataFeatures
        except:
            print "Error: Loading data. \n Reason: ",sys.exc_info()
    
    def generateArffFile(self,datafeatures):
        print "data features length",len(datafeatures)
        try:
            self.features = self.features + self.const.LABEL_FEATURES_GOOD
            # OUTPUT_FILE_TRAIN
            arff.dump(self.const.OUTPUT_FILE_TRAIN, datafeatures, relation="yelp", names=self.features)
        except:
            print "Error: Generating Arff file. \n Reason: ",sys.exc_info()
    
    def __init__(self):
        self.const = Constants()
        self.client = MongoClient(self.const.Mongo_Host);
        self.db = self.client[self.const.DB_YELP_MONGO];
        self.stage2 = Stage2()
        self.stage3 = Stage3()
        self.loadFeatures()
        datafeatures = self.loadDataFeatures()
	print datafeatures
        self.generateArffFile(datafeatures)
        
if __name__=="__main__":
    startTime = time.time()
    darff = GenerateArff();
    elapsed = (time.time() - startTime)/60
    print "arff file generation took ", elapsed, " minutes";

