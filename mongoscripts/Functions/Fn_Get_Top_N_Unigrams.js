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
		db.Review_no_punctuations_rand.insert()
	});
}
