// Read each review from Mongo Review_no_stopwords collections
// Split each review and map(token,1)
// Reduce sum the reviews


var mapFunction = function(){
	review_text = this.review;
	tokens = review_text.split(" ")
	tokens.forEach(function(word){ 
		emit(word,1)
	});
	
}

var reduceFunction = function(word,count){
	return Array.sum(count)
}


db.Review_no_stopwords.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Unigram" }
                   )