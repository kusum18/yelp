'''
Created on Apr 21, 2013

@author: kusum
'''
import sys
from MongoConfig import MongoConf;
from pymongo import MongoClient
from xlrd import open_workbook,cellname,empty_cell
from Review import Review,ReviewType
import json
from Constants import Constants

class Xls2mongo():
    const = Constants()
    
    def insert(self,reviews):
        Db = self.client[self.const.DB_YELP_MONGO]
        AnnotatedReviews = Db[self.const.COLLECTION_ANNOTATED_REVIEWS];
        
        for review in reviews:
            try:
                value = json.dumps(review, default=lambda x:x.__dict__)
                value = json.loads(value)
                AnnotatedReviews.insert(value)
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
        
    def __init__(self):
        #usage python Xls2mongo.py <file1> <file2>
        self.config = MongoConf();
        self.client = MongoClient(self.const.Mongo_Host)
        numberOfFiles = len(sys.argv)
        try:
            for index in range(1,numberOfFiles):
                reviews=self.start(sys.argv[index])
                self.insert(reviews)
        except:
            pass
        
        
obj = Xls2mongo();

