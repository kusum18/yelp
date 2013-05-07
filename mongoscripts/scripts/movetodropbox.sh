#!/bin/bash
cp -r ../output ~/Dropbox/src

# copy result.arff to dropbox
# cp *.arff ~/Dropbox/src/arff/may-3/


#import features to mongo
# mongoimport --db yelp --collection features --type csv --file /home/saini/Dropbox/src/Features/unigrams_added.csv --fieldFile "./mongoscripts/scripts/fields_features.txt"


# ./mongoimport --db yelp --collection features --type csv --file /Users/vaibhavsaini/Dropbox/src/Features/unigrams_added_test.csv --fieldFile "/Users/vaibhavsaini/Documents/workspace/yelp/mongoscripts/scripts/fields_features.txt"

#import a json file
#./mongoimport --db yelp --collection review --file ~/Dropbox/src/review.json
