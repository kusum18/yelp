// class wise unigrams


var food_mapFunction = function(){
	if(this.Food==1){
			review_text = this.review;
		tokens = review_text.split(" ")
		tokens.forEach(function(word){ 
			emit(word,1)
		});
	}
}

var service_mapFunction = function(){
	if(this.Service==1){
			review_text = this.review;
		tokens = review_text.split(" ")
		tokens.forEach(function(word){ 
			emit(word,1)
		});
	}
}
var ambience_mapFunction = function(){
	if(this.Ambiance==1){
			review_text = this.review;
		tokens = review_text.split(" ")
		tokens.forEach(function(word){ 
			emit(word,1)
		});
	}
}

var deal_mapFunction = function(){
	if(this.Deals==1){
			review_text = this.review;
		tokens = review_text.split(" ")
		tokens.forEach(function(word){ 
			emit(word,1)
		});
	}
}

var price_mapFunction = function(){
	if(this.Price==1){
			review_text = this.review;
		tokens = review_text.split(" ")
		tokens.forEach(function(word){ 
			emit(word,1)
		});
	}
}


var reduceFunction = function(word,count){
	return Array.sum(count)
}

db.Review_no_punctuations.mapReduce(
 food_mapFunction,
 reduceFunction,
 { out: "Food_Unigrams" }
)

db.Review_no_punctuations.mapReduce(
 service_mapFunction,
 reduceFunction,
 { out: "Service_Unigrams" }
)

db.Review_no_punctuations.mapReduce(
 ambience_mapFunction,
 reduceFunction,
 { out: "Ambiance_Unigrams" }
)

db.Review_no_punctuations.mapReduce(
 deal_mapFunction,
 reduceFunction,
 { out: "Deal_Unigrams" }
)

db.Review_no_punctuations.mapReduce(
 price_mapFunction,
 reduceFunction,
 { out: "Price_Unigrams" }
)

