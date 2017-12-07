from pymongo import MongoClient
import pandas as pd
from bson.son import SON

def storage_events_df():
	client = MongoClient()

	db = client['test']

	pipeline = [
		{"$group": {"_id": {"month": {"$month": "$timestamp"}, "year": {"$year": "$timestamp"}}, 
		"user": {"$addToSet": "$user"}}},
		{"$sort": SON([("_id", 1)])},
		{"$project": {"_id": 0, "month": "$_id.month", "year": "$_id.year", "userbyMonth": {"$size": "$user"}}}
		
	]

	usersbyMonth = list(db.storageevents.aggregate(pipeline))

	storageDataFrame = pd.DataFrame(usersbyMonth)
	storageDataFrame = storageDataFrame[['month', 'year', 'userbyMonth']]
	return storageDataFrame