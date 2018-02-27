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