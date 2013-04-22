// Read each bigram word as token from Mongo Bigram_WO_Count collections
// map(token,1)
// Reduce sum of bigrams


var mapFunction = function(){
	bigram_word = this.word;
	emit(bigram_word,1)
}

var reduceFunction = function(word,count){
	return Array.sum(count)
}


db.BIGRAMS_WO_COUNT.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Bigrams" }
                   )