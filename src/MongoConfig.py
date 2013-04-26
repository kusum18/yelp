'''
Created on Apr 21, 2013

@author: user
'''
class MongoConf():
    
    def conf(self):
        self.host = "localhost"
        self.port = ""
        self.database = "yelpd"
        self.collection = "AnnotatedReviews"
    
    def _init__(self,host):
        self.conf()
        self.host = host 
    
    def __init__(self):
        self.conf();