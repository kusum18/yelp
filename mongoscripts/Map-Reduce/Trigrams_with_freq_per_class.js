// class wise trigrams

var mapFunction = function(){
	trigram_word = this.word;
	emit(trigram_word,1)
}

var reduceFunction = function(word,count){
	return Array.sum(count)
}


db.Food_trigrams_temp.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Food_Trigrams_with_freq" }
                   )
db.Service_trigrams_temp.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Service_Trigrams_with_freq" }
                   )
db.Deals_trigrams_temp.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Deals_Trigrams_with_freq" }
                   )
db.Ambiance_trigrams_temp.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Ambiance_Trigrams_with_freq" }
                   )
db.Price_trigrams_temp.mapReduce(
                     mapFunction,
                     reduceFunction,
                     { out: "Price_Trigrams_with_freq" }
                   )