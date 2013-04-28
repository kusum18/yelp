// Read each trigram word as token from Mongo Trigrams_no_freq collections
// map(token,1)
// Reduce sum of trigrams


var map = function(){
	trigram_word = this.word;
	emit(trigram_word,1)
}

var reduce = function(word,count){
	return Array.sum(count)
}

db.BIGRAMS_WO_COUNT.mapReduce(
                     map,
                     reduce,
                     { out: "trigram_with_freq" }
                   )