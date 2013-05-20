var detectPDASClasses = function(){
	db.PDASClasses.drop();
	print("detectPDASClasses");
	db.trainset.find().forEach(function(doc){
		if ((doc['Food']==2 || doc['Food']==0) && 
        	(doc['Service']==1 || doc['Ambiance']==1 || doc['Deals']==1 || doc['Price']==1)
        	){
        	db.PDASClasses.insert(doc)
        }
	});
	print(db.PDASClasses.find().count() + " rows found");
}

var detectPDAClasses = function(){
	db.PDAClasses.drop();
	print("detectPDAClasses");
	db.trainset.find().forEach(function(doc){
		if ((doc['Food']==2 || doc['Food']==0) && 
			(doc['Service']==2 || doc['Service']==0)  &&
        	(doc['Ambiance']==1 || doc['Deals']==1 || doc['Price']==1)
        	){
        	db.PDAClasses.insert(doc)
        }
	});
	print(db.PDAClasses.find().count() + " rows found");
}

var detectServiceRev = function(){
	db.serviceRev.drop();
	print("detectSelectedClasses");
	db.PDASClasses.find().forEach(function(doc){
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

var remove_service_only_from_PDAS = function(){
	print("size of PDASClasses "+ db.PDASClasses.find().count());
	count =0;
	db.serviceRev.find().forEach(function(doc){
		db.PDASClasses.remove({reviewId:doc['reviewId']});
		count= count+1;
	});
	print("removed service only classes");
	print(count+  "  rows removed");
	print("size of PDASClasses "+ db.PDASClasses.find().count());
}

var add_PDAS_rows = function(){
	print("adding PDASClasses rows");
	db.PDASClasses.find().forEach(function(doc){
		delete doc["_id"];
		db.trainset_boosted.insert(doc);
	});
}

var add_PDA_rows = function(){
	print("adding PDAClasses rows");
	db.PDAClasses.find().forEach(function(doc){
		delete doc["_id"];
		db.trainset_boosted.insert(doc);
	});
}
var create_trainset_boosted = function(){
	print("droping existing trainset_boosted collection");
	db.trainset_boosted.drop();
	print("creating trainset replica into trainset_boosted");
	db.trainset.find().forEach(function(doc){
		db.trainset_boosted.insert(doc);
	});
	add_PDAS_rows();
	add_PDAS_rows();
	add_PDA_rows();
	add_PDA_rows();
	add_PDA_rows();
	print("trainset_boosted collection size: "+ db.trainset_boosted.find().count());
}

var create_new_trainset = function(){
	print("droping existing trainset collection");
	db.trainset.drop();
	db.trainset_boosted.find().forEach(function(doc){
		db.trainset.insert(doc);
	});
	print("trainset collection size: "+ db.trainset_boosted.find().count());
}

var removeEmptyRows = function(collection){
	print("deleting empty rows or useless rows");
	db.useless_reviews.drop();
	db.usefull_reviews.drop();
	db[collection].find().forEach(function(doc){
		if ((doc['Food']==2 || doc['Food']==0 || doc['Foods']==-1) && 
        	(doc['Ambiance']==2 || doc['Ambiance']==0 || doc['Ambiance']==-1)  &&
        	(doc['Service']==2 || doc['Service']==0 || doc['Service']==-1)  &&
        	(doc['Deals']==2 || doc['Deals']==0 || doc['Deals']==-1)  &&
        	(doc['Price']==2 || doc['Price']==0 || doc['Price']==-1)){
        	db.useless_reviews.insert(doc)
        }
        else{
        	db.usefull_reviews.insert(doc)
        }
	});
	db.useless_reviews.find().forEach(function(doc){
		db[collection].remove({"reviewId":doc["reviewId"]});
	});
	print(db.useless_reviews.find().count() + " rows deleted ");
	print(db[collection].find().count() + " size of " + collection + " collection")
}

var create_backup = function(collection){
	db[collection].find().forEach(function(doc){
		db[collection + "_bkup"].insert(doc);
	});
	print("bkup collection size: "+ db[collection + "_bkup"].find().count());
}

var retreive_from_backup = function(collection){
	db[collection].drop();
	db[collection+"_bkup"].find().forEach(function(doc){
		db[collection].insert(doc);
	});
	print("collection size: "+ db[collection].find().count());
}



var boostData = function(){
	detectPDASClasses();
	detectPDAClasses();
	detectServiceRev();
	remove_service_only_from_PDAS();
	create_trainset_boosted();
	create_new_trainset();
	//create_backup('testset')
	removeEmptyRows('trainset');

}
boostData();