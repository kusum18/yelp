'''
Created on Apr 21, 2013

@author: kusum
'''
import sys
from MongoConfig import MongoConf
from pymongo import MongoClient
from xlrd import open_workbook,cellname,empty_cell
from Review import Review,ReviewType
import json,os
from Constants import Constants

class Xls2mongo():
    const = Constants()
    
    def insert(self,reviews):
        Db = self.db
        AnnotatedReviews = Db[self.const.COLLECTION_ANNOTATED_REVIEWS];
        RejectReviews = Db[self.const.COLLECTION_REJECTED_REVIEWS]
        for review in reviews:
            try:
                review,isValid = self.checkIfValidReview(review)
                value = json.dumps(review, default=lambda x:x.__dict__)
                value = json.loads(value)
                if isValid:
                    AnnotatedReviews.insert(value)
                else:
                    RejectReviews.insert(value);
            except:
                print "Insert Error:",sys.exc_info()

    def XlsCheckValue(self,value):
        type = ReviewType();
        if value == empty_cell.value:
            return type.UA;
        else:
            return value

    def processReviewXls(self,sheet,row):
        review = Review()
        start_col = 0
        end_col = 11 
        for col in range(start_col,end_col):
            if(col==0):
                review.reviewId = sheet.cell_value(row,col)
            elif(col==1):
                review.review = sheet.cell_value(row,col);
            elif(col==2):
                review.Food = self.XlsCheckValue(sheet.cell_value(row,col))
            elif(col==3):
                review.Drinks = self.XlsCheckValue(sheet.cell_value(row,col))
            elif(col==4):
                review.Ambiance = self.XlsCheckValue(sheet.cell_value(row,col))
            elif(col==5):
                review.Service = self.XlsCheckValue(sheet.cell_value(row,col))
            elif(col==6):
                review.Location = self.XlsCheckValue(sheet.cell_value(row,col))
            elif(col==7):
                review.Deals = self.XlsCheckValue(sheet.cell_value(row,col))
            elif(col==8):
                review.Price = self.XlsCheckValue(sheet.cell_value(row,col))
            else:
                pass #control should have never reached here as there are only 11 columns in xls
        return review;
    
    def start(self,file):
        print "Working on..",file
        try:
            book = open_workbook(file)
            sheet = book.sheet_by_index(self.const.FIRST_SHEET)
            nrows = sheet.nrows
            reviews = []
            for row in range(2,nrows):
                review = self.processReviewXls(sheet,row)
                reviews.append(review);
            return reviews
        except:
            print "error",sys.exc_info()
    
    def checkIfValidReview(self, review):
        db = self.db
        reviewCollection = db[self.const.COLLECTION_REVIEW]
        entry = reviewCollection.find_one({'review_id':review.reviewId})
        if entry:
            review.stars = entry['stars']
            return (review,True)
        else:
            return (review, False)

    def dropCollections(self):
        do_not_delete = ['review','system.indexes','user',
                         'checkin','business','annotated_reviews',
                         'Reject_reviews','trainset','testset']
        for name in self.db.collection_names():
            
            if name in do_not_delete:
                pass
            else:
                print "droping collection ", name
                self.db[name].drop()

    def __init__(self):
        #usage python Xls2mongo.py <file1> <file2>
        self.config = MongoConf();
        self.client = MongoClient(self.const.Mongo_Host)
        self.db = self.client[self.const.DB_YELP_MONGO]
        #numberOfFiles = len(sys.argv)
        
    
    def load(self):
        print ("loading files to mongo. This will take some time. sit back and relax")
        destinationPath = sys.argv[1]
        try:
            for file in os.listdir(destinationPath):
                if file.endswith(self.const.EXT_EXCEL):
                    file_path = os.path.join(destinationPath,file)
                    print file_path
                    reviews=self.start(file_path)
                    self.insert(reviews)
        except:
            print sys.exc_info()
        print ("loading files done")
    def removeUnFilledReviews(self):
        print("removing unfiled reviews. they will be inserted into non_annotated_reviews collection")
        docs = self.db[self.const.COLLECTION_ANNOTATED_REVIEWS].find()
        for doc in docs:
            if  doc['Food']==2 and \
                doc['Ambiance']==2 and \
                doc['Service']==2 and \
                doc['Deals']==2 and \
                doc['Price']==2 :
                    self.db.non_annotated_reviews.insert(doc)
            else:
                    self.db.annotated_reviews_clean.insert(doc)
        print ("non_annotated_reviews and annotated_reviews_clean created.")


if __name__ == '__main__':
    obj = Xls2mongo()
    obj.load()

