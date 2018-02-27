users_pipeline = [
	{
		"$group": {
		"_id": {
		"month": {"$month": "$timestamp"}, 
		"year": {"$year": "$timestamp"}
		}, 
		"users": {"$addToSet": "$user"},
		}
	},
	{"$sort": SON([("_id", 1)])},
	{
		"$project": {
		"_id": 0, 
		"month": "$_id.month", 
		"year": "$_id.year", 
		"active_users": {"$size": "$users"},
		}
	}
	
]

# def storage_events_df():
# 	client = MongoClient(host='104.196.54.95',
# 						port=27017,
# 						ssl=True,
# 						ssl_cert_reqs=ssl.CERT_NONE,
# 						username='root',
# 						password='kM8tRoRtQDBFBkN9ZOFNYR5'
# 						)

# 	db = client['bridge']

# 	pipeline = [
# 		{"$group": 
# 			{"_id": 
# 				{"month": {"$month": "$timestamp"}, 
# 				"year": {"$year": "$timestamp"}}, 
# 				"user": {"$addToSet": "$user"}
# 			}
# 		},
# 		{"$sort": SON([("_id", 1)])},
# 		{"$project": 
# 			{"_id": 0, 
# 			"month": "$_id.month", 
# 			"year": "$_id.year", 
# 			"userbyMonth": {"$size": "$user"}
# 			}
# 		}
		
# 	]

# 	# change db to correct name, if not correct
# 	usersbyMonth = list(db.storageevents.aggregate(pipeline))

# 	storageDataFrame = pd.DataFrame(usersbyMonth)
# 	storageDataFrame = storageDataFrame[['month', 'year', 'userbyMonth']]
# 	return storageDataFrame