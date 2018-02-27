'''Downloads are in bytes (bandwidth) and storage is in gigabytes per hour. Traction Stats are listed in TB.'''

debits_pipeline = [
	{
		"$group": {
		"_id": 
		{"month": {"$month": "$created"}, 
		"year": {"$year": "$created"}},
		"bandwidthBilled": {
			"$sum": {
				"$cond": [
					{"$eq": ["$type", "bandwidth"]}, "$amount", 0]
				}
			},
		"storageBilled": {
			"$sum": {
				"$cond": [
					{"$eq": ["$type", "storage"]}, "$amount", 0]
				}
			},
		"bandwidthUsed": {"$sum": "$bandwidth"}
		}
	},
	{"$sort": SON([("_id", 1)])},
	{
		"$project": {
		"_id":0, 
		"month": "$_id.month",
		"year": "$_id.year",
		"storageBilled":1,
		"bandwidthUsed":1,
		"bandwidthBilled":1
		}
	}
	
]

# def debits_df():
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
# 				{"month": {"$month": "$created"}, "year": {"$year": "$created"}},
# 				"bandwidthBilled": {"$sum": {"$cond": [{"$eq": ["$type", "bandwidth"]}, "$amount", 0]}},
# 				"storageBilled": {"$sum": {"$cond": [{"$eq": ["$type", "storage"]}, "$amount", 0]}},
# 				"bandwidthUsed": {"$sum": "$bandwidth"}
# 			}
# 		},
# 		{"$sort": SON([("_id", 1)])},
# 		{"$project": 
# 			{
# 				"_id":0, 
# 				"month": "$_id.month",
# 				"year": "$_id.year",
# 				"storageBilled":1,
# 				"bandwidthUsed":1,
# 				"bandwidthBilled":1
# 			}
# 		}
		
# 	]

	# debits = list(db.debit_test.aggregate(pipeline))

	# debitDataFrame = pd.DataFrame(debits)
	# df = debitDataFrame[['month', 'year', 'bandwidthUsed', 'bandwidthBilled', 'storageBilled']]
	# df['bandwidthUsed'] = df['bandwidthUsed'] / terabyte
	# df['bandwidthBilled'] = df['bandwidthBilled'] / 100
	# df['storageBilled'] = df['storageBilled'] / 100
	# df = df.drop(df.index[0])
	# return df