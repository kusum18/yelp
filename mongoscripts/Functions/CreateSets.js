var addRandom = function(){
	db.Review_no_punctuations_rand.drop();
	print("adding random number to each record");
	db.Review_no_punctuations.find().forEach(function(doc){
		doc['random']=Math.random();
		db.Review_no_punctuations_rand.insert(doc)
	});
}

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
var removeDups = function(){
	db.duplicates.drop();
	var prev = 0;
	db.Review_no_punctuations.find({},{"reviewId":1}).sort({"reviewId":1}).forEach(function(doc){
		if(doc['reviewId']==prev){
			print("dup found.. damn");
			db.duplicates.update( {"_id" : doc['reviewId']}, { "$inc" : {count:1} }, true);
			db.Review_no_punctuations.remove({"_id":doc["_id"]});
		}else{
			prev = doc["reviewId"];
		}
	});
}
var makeSets = function(){
	checkdups();
	addRandom();
	makeTestSet();
	makeTrainSet();
}

makeSets();