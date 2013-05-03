#!/bin/bash
cp -r ../output ~/Dropbox/src

# copy result.arff to dropbox
# cp *.arff ~/Dropbox/src


#import features to mongo
# mongoimport --db yelp --collection features --type csv --file /home/saini/Dropbox/src/Features/unigrams_added.csv --fieldFile "./mongoscripts/scripts/fields_features.txt"


#./mongoimport --db yelp --collection features_new --type csv --file /home/saini/Dropbox/src/Features/unigrams_added.csv --fieldFile "./mongoscripts/scripts/fields_features.txt"
