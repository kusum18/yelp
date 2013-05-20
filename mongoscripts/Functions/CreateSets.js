var addRandom = function(){
	db.Review_no_punctuations_rand.drop();
	print("adding random number to each record");
	db.Review_no_punctuations.find().forEach(function(doc){
		doc['random']=Math.random();
		db.Review_no_punctuations_rand.insert(doc)
	});
	print("add index on random attribute.");
	db.Review_no_punctuations_rand.ensureIndex( { random :1 } );
	print("index added");
}

var makeTestSet = function(){
	print("delete existing testset");
	db.testset.drop();
	print(" creating testset");
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
			count = count -1;
		}else{
			results[result["reviewId"]]=result;
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
var checkdups = function(){
	print("checking for duplicates ...");
	db.duplicates.drop();
	var prev = 0;
	db.Review_no_punctuations.find({},{"reviewId":1}).sort({"reviewId":1}).forEach(function(doc){
		if(doc['reviewId']==prev){
			db.duplicates.update( {"_id" : doc['reviewId']}, { "$inc" : {count:1} }, true);
			db.Review_no_punctuations.remove({"_id":doc["_id"]});
		}else{
			prev = doc["reviewId"];
		}
	});
	print(db.duplicates.find().count() + " duplicate values removed");
}

var detectEmptyRows = function(){
	print("deleting empty rows or useless rows");
	db.useless_reviews.drop();
	db.usefull_reviews.drop();
	db.Review_no_punctuations.find().forEach(function(doc){
		if ((doc['Food']==2 || doc['Food']==0) && 
        	(doc['Ambiance']==2 || doc['Ambiance']==0)  &&
        	(doc['Service']==2 || doc['Service']==0)  &&
        	(doc['Deals']==2 || doc['Deals']==0)  &&
        	(doc['Price']==2 || doc['Price']==0)){
        	db.useless_reviews.insert(doc)
        }
        else{
        	db.usefull_reviews.insert(doc)
        }
	});
	db.useless_reviews.find().forEach(function(doc){
		db.Review_no_punctuations.remove({"reviewId":doc["reviewId"]});
	});
	print(db.useless_reviews.find().count() + " rows deleted ");
}

var detectNegetiveRows = function(){
	print("deleting empty rows or useless rows");
	db.useless_neg_reviews.drop();
	db.usefull_reviews.drop();
	db.Review_no_punctuations.find().forEach(function(doc){
		if ((doc['Food']==2 || doc['Food']==0 ||doc['Food']==-1) && 
        	(doc['Ambiance']==2 || doc['Ambiance']==0  ||doc['Ambiance']==-1)  &&
        	(doc['Service']==2 || doc['Service']==0 ||doc['Service']==-1)  &&
        	(doc['Deals']==2 || doc['Deals']==0 ||doc['Deals']==-1)  &&
        	(doc['Price']==2 || doc['Price']==0 ||doc['Price']==-1)){
        	db.useless_neg_reviews.insert(doc)
        }
        else{
        	db.usefull_reviews.insert(doc)
        }
	});
	//db.useless_neg_reviews.find().forEach(function(doc){
	//	db.Review_no_punctuations.remove({"reviewId":doc["reviewId"]});
	//});
	print(db.useless_reviews.find().count() + " rows deleted ");
}

var detectSelectedClasses = function(){
	db.selectedClasses.drop();
	print("detectSelectedClasses");
	db.trainset.find().forEach(function(doc){
		if ((doc['Food']==2 || doc['Food']==0) && 
        	(doc['Service']==1 || doc['Ambiance']==1 || doc['Deals']==1 || doc['Price']==1)
        	){
        	db.selectedClasses.insert(doc)
        }
	});
	print(db.selectedClasses.find().count() + " rows found");
}


detectSelectedClasses();

var detectServiceRev = function(){
	db.serviceRev.drop();
	print("detectSelectedClasses");
	db.selectedClasses.find().forEach(function(doc){
		if ((doc['Food']==2 || doc['Food']==0) && 
        	(doc['Ambiance']==2 || doc['Ambiance']==0)  &&
        	(doc['Service']==1)  &&
        	(doc['Deals']==2 || doc['Deals']==0)  &&
        	(doc['Price']==2 || doc['Price']==0)
        	){
        	db.serviceRev.insert(doc);
        }
	});
	print(db.serviceRev.find().count() + " rows found");
}
detectServiceRev();

//detectNegetiveRows();

var makeSets = function(){
	//detectEmptyRows();
	//detectNegetiveRows();
	checkdups();
	addRandom();
	//makeTestSet();
	makeTrainSet();
}

makeSets();