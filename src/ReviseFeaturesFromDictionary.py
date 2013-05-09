from pymongo import MongoClient
from Constants import Constants
from sets import Set
import sys


class CleanFeatures:
    
    
    def GetFeatures(self):
        print "Loading Old Features"
        features = []
        featuresCollection = self.db[self.const.COLLECTION_FEATURES]
        try:
            for feature in featuresCollection.find():
                features.append(feature["word"].lower())
            print "Finished Loading Features"
            return features
        except:
            print "Error: Loading Old features. \n Reason: ",sys.exc_info()
    
    def loadDictionary(self):
        try:
            file_handle = open(self.const.SYNONYMS)
            dict = {}
            for line in file_handle.readlines():
                tokens = line.split(self.const.DELIMITER_SYNONYMS)
                key = tokens[0]
                value = tokens[1].strip()
                dict[key]=value
            return dict
        except:
            print "Error Opening Synonyms file. ", sys.exc_info()
    
    def CleanFeatures(self,features,dictionary):
        try:
            set = Set([])
            for feature in features:
                if feature.lower() in dictionary:
                    set.add(dictionary[feature])
                else:
                    set.add(feature.lower())
            return set 
        except:
            print "Error Cleaning Features. Reason: ",sys.exc_info()
    
    def loadNewFeaturesInDB(self,features):
        
        print "Loading New Features into DB"
        featuresCollection = self.db[self.const.COLLECTION_FEATURES_CLEAN]
        featuresCollection.remove()
        try:
            for feature in features:
                featuresCollection.insert({"word":feature})
            print "Finished Loading Features"
        except:
            print "Error: Loading Old features. \n Reason: ",sys.exc_info()

    def __init__(self):
        try:
            self.const = Constants()
            self.client = MongoClient(self.const.Mongo_Host);
            self.db = self.client[self.const.DB_YELP_MONGO];
            features = self.GetFeatures()
            dictionary = self.loadDictionary()
            features = self.CleanFeatures(features, dictionary)
            self.loadNewFeaturesInDB(features)
        except:
            print "Error: ",sys.exc_info()


obj = CleanFeatures()   


