// class wise bigrams

var mapFunction = function(){
	bigram_word = this.word;
	emit(bigram_word,1)
}

var reduceFunction = function(word,count){
	return Array.sum(count)
}


db.Food_bigrams_temp.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Food_Bigrams_with_freq" }
                   )
db.Service_bigrams_temp.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Service_Bigrams_with_freq" }
                   )
db.Deals_bigrams_temp.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Deals_Bigrams_with_freq" }
                   )
db.Ambiance_bigrams_temp.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Ambiance_Bigrams_with_freq" }
                   )
db.Price_bigrams_temp.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Price_Bigrams_with_freq" }
                   )