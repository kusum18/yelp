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