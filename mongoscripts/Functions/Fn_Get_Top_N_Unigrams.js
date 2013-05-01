var get_Top_N_Unigrams = function (min_threshold){
	var word_count_pairs_cursor = db.Unigram.find({
		"value": {$gte:min_threshold}
	 }).sort({"value":-1});
	 
	 words = []
	 while(word_count_pairs_cursor.hasNext()){
	 	var word_count_pair = word_count_pairs_cursor.next();
	 	var word = word_count_pair["_id"];
	 	var value = word_count_pair["value"]
	 	words.push(word)
	 }
	 return words;
}

var removeUnFilledReviews = function(){
	print('cleaning');
	db.AnnotatedReviews.find().forEach(function(doc){
        if (doc['Food']==2 && 
        	doc['Ambiance']==2 &&
        	doc['Service']==2 &&
        	//doc['Location']==2 &&
        	doc['Deals']==2 &&
        	doc['Price']==2 ){
        	db.non_annotated_reviews.insert(doc)
        	// not annotated. remove
        }
        else{
        	db.annotated_reviews_clean.insert(doc)
        }
    });
    print('non_annotated_reviews and annotated_reviews_clean created' );

}

var addRandom = function(){
	print("adding random number to each record");
	db.Review_no_punctuations.find().forEach(function(doc){
		doc['random']=Math.random();
		db.Review_no_punctuations_rand.insert(doc)
	});
}
addRandom()

var makeTestSet = function(){
	db.testset.drop();
	count=0;
	results = {};
	while(count<1500){
		count++;
		rand = Math.random();
		result = db.Review_no_punctuations_rand.findOne( {random : { $gte :rand } } )
		if(result == null){
			result = db.Review_no_punctuations_rand.findOne( { random : { $lte : rand } } )
		}
		if(results[result["reviewId"]]){
			print("ignore");
			count = count -1;
		}else{
			results[result["reviewId"]]=result;
			print("added");
			db.testset.insert(result);
		}
	}
	print("test set done.")
	print("test set size "+ db.testset.find().count() )
}

var makeTrainSet = function(){
	db.trainset.drop();
	print("taking a backup");
	db.Review_no_punctuations_rand.find().forEach(function(doc){
		db.trainset.insert(doc)
	});
	print("size of train set"+ db.trainset.find().count());
	db.testset.find().forEach(function(doc){
		db.trainset.remove({reviewId:doc['reviewId']});
	});
	print("trainset done")
	print("size of train set"+ db.trainset.find().count());
}

var makeSets = function(){
	makeTestSet();
	makeTrainSet();
}

makeSets()



var imp_features = function(){
	count =0;
	try{
		db.features.find().forEach(function(doc){
			db.feat.insert(doc)
			count++;
			if (count>10){
				throw BreakException;
			}
		});
	}catch(e){
			print ("caught yay!!");
	}
}

var imp_rev = function(){
	count =0;
	try{
		db.Review_no_punctuations.find().forEach(function(doc){
			db.rev_test.insert(doc)
			count++;
			if (count>9){
				throw BreakException;
			}
		});
	}catch(e){
			print ("caught yay!!");
	}
}

var checkdups = function(){
	db.duplicates.drop();
	var prev = 0;
	db.testset.find({},{"reviewId":1}).sort({"reviewId":1}).forEach(function(doc){
		if(doc['reviewId']==prev){
			print("dup found.. damn");
			db.duplicates.update( {"_id" : doc['reviewId']}, { "$inc" : {count:1} }, true);
		}else{
			prev = doc["reviewId"];
		}
	});
}
checkdups();


