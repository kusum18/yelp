# This script is supposed to pick up the pruned unigrams and generate new set of bigrams and trigrams
from Constants import Constants
from Stage3 import Stage3
from pymongo import MongoClient
import pymongo
import re
import sys

class script_2():
    
    
    def loadAllUnigrams(self):
        unigramsCollection = self.db[self.const.COLLECTION_UNIGRAMS_Prune]
        self.unigrams = []
        for unigram in unigramsCollection.find():
            try:
                self.unigrams.append(unigram._id);
            except:
                print "Error: Fetching Unigrams from mongo. \n Reason: ",sys.exc_info()
    
    def isPresentInUnigram(self,bigram):
        tokens = bigram._id.split(self.const.whitespace)
        for token in tokens:
            if token in self.unigrams:
                return True
        return False
         
    def pruneBigrams(self,bigramCollectionName,bigramAcceptCollectionName,bigramRejectCollectionName):
        bigramCollection = self.db[bigramCollectionName]
        bigramAcceptCollection = self.db[bigramAcceptCollectionName]
        bigramRejectCollection = self.db[bigramRejectCollectionName]
        try:
            for bigram in bigramCollection.find():
                if self.isPresentInUnigram(bigram):
                    bigramAcceptCollection.insert(bigram)
                else:
                    bigramRejectCollection.insert(bigram)
        except:
            print "Error: Pruning Bigrams",sys.exc_info()
    
    def pruneTrigrams(self,trigramCollectionName,trigramAcceptCollectionName,trigramRejectCollectionName):
        triCollection = self.db[trigramCollectionName]
        triAcceptCollection = self.db[trigramAcceptCollectionName]
        triRejectCollection = self.db[trigramRejectCollectionName]
        try:
            for trigram in triCollection.find():
                if self.isPresentInUnigram(trigram):
                    triAcceptCollection.insert(trigram)
                else:
                    triRejectCollection.insert(trigram)
        except:
            print "Error: Pruning Trigrams",sys.exc_info()
    
    def __init__(self):
        self.const = Constants()
        self.client = MongoClient(self.const.Mongo_Host);
        self.db = self.client[self.const.DB_YELP_MONGO];
        self.loadAllUnigrams()

code = script_2();
