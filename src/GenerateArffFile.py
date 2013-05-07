from Constants import Constants
from ReviseFeaturesFromDictionary import CleanFeatures
from Stage2 import Stage2
from Stage3 import Stage3
from pymongo import MongoClient
from sets import Set
import nltk
import sys
import arff
import time
from nltk.tag.api import FeaturesetTaggerI

class GenerateArff():
    def loadfeatureset(self,tokens,featureset):
        try:
            for token in tokens:
                if " " in token:
                    print "check token",token
                #print "testing *****",("good food" in self.features)
                #print "index **** ", self.features.index("good food")
                if token in self.features:
                    
                    index = self.features.index(token)
                    featureset[index] +=1  # gives us the frequency of each feature in the featureset.
                    #print "token",token,"featureset[index]", featureset[index]
                else:
                    pass
        except:
            print "Error: Generating feature vector. \n Reason: ",sys.exc_info()
    
    def filterTokens(self,tokens):
        try:
            fset = []
            for token in tokens:
                if(token in self.dictionary):
                    fset.append(self.dictionary[token])
                else:
                    fset.append(token)
            return fset
        except:
            print "Error filtering tokens.\n Reason: ",sys.exc_info()
    
    def checkUnigrams(self,review,featureset):
        try:
            tokens = review["review"].lower().split(self.const.whitespace)
            tokens = self.filterTokens(tokens)
            self.loadfeatureset(tokens, featureset)
        except:
            print "Error: Loading Unigrams. \n Reason: ",sys.exc_info()
    
    def checkBigrams(self,review,featureset):
        try:
            tokens = self.stage3.processReview_bigram(review)
            bigrams = []
            for token in tokens:
                bigrams.append(token['word'])
            self.loadfeatureset(bigrams, featureset)
        except:
            print "Error: Loading Bigrams. \n Reason: ",sys.exc_info()
    
    def checkTrigrams(self,review,featureset):
        try:
            tokens = self.stage3.processReview_trigram(review)
            trigrams = []
            for token in tokens:
                trigrams.append(token['word'])
            self.loadfeatureset(trigrams, featureset)
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
        featuresCollection = self.db[self.const.COLLECTION_FEATURES_CLEAN]
        try:
            for feature in featuresCollection.find():
                self.features.append(str(feature["word"]))
            print "Finished Loading Features, number of features loaded", len(self.features)
        except:
            print "Error: Loading features. \n Reason: ",sys.exc_info()
            
    def loadDictionary(self):
        cfeatures = CleanFeatures()
        self.dictionary = cfeatures.loadDictionary()
    
    def loadDataFeatures(self):
        try:
            collection=self.const.COLLECTION_TRAINSET
            if self.mode.lower() == 'test':
                collection=self.const.COLLECTION_TESTSET
            reviews = self.db[collection];
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
                #self.checkTrigrams(review, featureset)
                #step 4 - check additional features
                self.checkAdditionalFeatures(review, featureset)
                #step 5 -- apply business Logic
                self.applyBusinessLogicOnFeatureset(featureset)
                #step 6 -- set everything with freq>0 to 1
                self.makeMeOne(featureset)
                dataFeatures.append(featureset)
            return dataFeatures
        except:
            print "Error: Loading data. \n Reason: ",sys.exc_info()
    
    def applyBusinessLogicOnFeatureset(self,featureset):
        for feature in self.features:
            grams = feature.split(" ")
            if len(grams)==2:
                #its a bigram, get applylogic
                self.checkAndSetFeatureSet(feature, featureset)

    def makeMeOne(self,featureset):
        index = 0
        for featureValue in featureset:
            if featureValue >0:
                featureset[index]=1
            index +=1

    def checkAndSetFeatureSet(self,bigram,featureset):
        indexBg = self.features.index(bigram)
        bigram_freq = featureset[indexBg]
        grams = bigram.split(" ")
        indexFg = self.features.index(grams[0])
        indexSg = self.features.index(grams[1])
        fg_freq = 0
        sg_freq = 0
        if indexFg !=-1:
            fg_freq = featureset[indexFg]
        if indexSg !=-1:
            sg_freq =  featureset[indexSg]
        # check of 1st gram
        if bigram_freq>=fg_freq:
            featureset[indexBg]=1
            featureset[indexFg]=0
        if bigram_freq<fg_freq:
            featureset[indexBg]=1
            featureset[indexFg]=1
        if bigram_freq>=sg_freq:
            featureset[indexBg]=1
            featureset[indexSg]=0
        if bigram_freq<sg_freq:
            featureset[indexBg]=1
            featureset[indexSg]=1
        
    def generateArffFile(self,datafeatures):
        print "data features length",len(datafeatures)
        try:
            self.features = self.features + self.const.LABEL_FEATURES_GOOD
            # OUTPUT_FILE_TRAIN
            output_file = self.const.OUTPUT_FILE_TRAIN
            if self.mode.lower() == 'test':
                output_file=self.const.OUTPUT_FILE_TEST
            print "generating arff file ", output_file ,"this will take time. please wait. "
            arff.dump(output_file, datafeatures, relation="yelp", names=self.features)
            print "arff file generation done."
        except:
            print "Error: Generating Arff file. \n Reason: ",sys.exc_info()
    
    def __init__(self):
        self.const = Constants()
        self.client = MongoClient(self.const.Mongo_Host);
        self.db = self.client[self.const.DB_YELP_MONGO];
        self.loadDictionary()
        self.stage2 = Stage2()
        self.stage3 = Stage3()
        self.loadFeatures()
        self.mode = sys.argv[1]
        datafeatures = self.loadDataFeatures()
        self.generateArffFile(datafeatures)
        
if __name__=="__main__":
    if len(sys.argv) < 2:
        sys.exit('please specify the mode: test/train' )
    startTime = time.time()
    darff = GenerateArff();
    elapsed = (time.time() - startTime)/60
    print "arff file generation took ", elapsed, " minutes";

