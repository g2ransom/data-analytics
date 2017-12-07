from pymongo import MongoClient
import pandas as pd
from bson.son import SON
import datetime


def shards_df():
	client = MongoClient()

	db = client['test']

	pipeline = [
		{"$unwind": {"path": "$contracts"}},
		{"$project": {"_id":0, 
		"farmerID": "$contracts.contract.farmer_id",
		"storage": "$contracts.contract.data_size",
		"contractBegin": {"$add": [datetime.datetime.fromtimestamp(0), "$contracts.contract.store_begin"]},
		"contractEnd": {"$add": [datetime.datetime.fromtimestamp(0), "$contracts.contract.store_end"]}}},
		{"$project": {"_id": 0, 
						"startMonth": {"$month": "$contractBegin"},
						"startYear": {"$year": "$contractBegin"},
						"endMonth": {"$month": "$contractEnd"},
						"endYear": {"$year": "$contractEnd"},
						"farmerID": 1, "storage": 1}},
		{"$group": {"_id": {"startMonth": "$startMonth", "startYear": "$startYear", "endMonth": "$endMonth", "endYear": "$endYear"}, 
		"storageMonth": {"$sum": "$storage"},
		"farmers": {"$addToSet": "$farmerID"}}},
		{"$project": {"_id": 0, 
		"startMonth": "$_id.startMonth", 
		"startYear": "$_id.startYear", 
		"endMonth": "$_id.endMonth", 
		"endYear": "$_id.endYear",
		"storagePerMonth": "$storageMonth",
		"farmersPerMonth": {"$size": "$farmers"}}},
		{"$sort": SON([("startYear", 1), ("startMonth", 1)])}
		
	]

	shards = list(db.shards.aggregate(pipeline))

	df = pd.DataFrame(shards)


	df['storage_cumsum'] = df['storagePerMonth'].cumsum()


	storage_sum = df['storage_cumsum'].tolist()
	active_monthly_storage = get_monthly_storage(storage_sum, 3)
	storage_df = pd.DataFrame(active_monthly_storage)
	df = pd.concat([df, storage_df], axis=1)
	df = (df[['startMonth', 'startYear', 0, 'farmersPerMonth']]
		.rename(columns={'startMonth': 'month', 'startYear': 'year', 0: "monthlyStorage"}))



	df = (df.groupby(["month", "year"]).sum().reset_index()
		.sort_values(by=["year", "month"]))
	df['monthlyStorage'] = df['monthlyStorage'] / 1000000000
	return df

def get_monthly_storage(cum_month_storage, contract_length):
	active_monthly_storage = []
	total_stale_data = 0
	i = 0
	for month in cum_month_storage:
		if cum_month_storage.index(month) < contract_length:
			active_monthly_storage.append(month)
		else:
			total_stale_data = cum_month_storage[i]
			i += 1
			active_monthly_storage.append(month - total_stale_data)
	return active_monthly_storage