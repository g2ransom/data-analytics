shards_pipeline = [
	{"$unwind": {"path": "$contracts"}},
	{
		"$project": {
		"_id": 0,
		"store_begin": {"$add": [datetime.datetime.fromtimestamp(0), "$contracts.contract.store_begin"]},
		"store_end": {"$add": [datetime.datetime.fromtimestamp(0), "$contracts.contract.store_end"]},
		"storage": "$contracts.contract.data_size"
		}
	},
	{
		"$project": {
		"_id": 0,
		"start_month": {"$month": "$store_begin"},
		"start_year": {"$year": "$store_begin"},  
		"end_month": {"$month": "$store_end"}, 
		"end_year": {"$year": "$store_end"},
		"storage": 1
		}
	},
	{
		"$group": {
			"_id": {
				"start_month": "$start_month",
				"start_year": "$start_year",
				"end_month": "$end_month", 
				"end_year": "$end_year"
				},
			"storage_month": {"$sum": "$storage"},
			}
		},
	{
		"$project": {
		"_id": 0, 
		"start_month": "$_id.start_month",
		"start_year": "$_id.start_year",
		"end_month": "$_id.end_month",
		"end_year": "$_id.end_year",
		"storage_per_month": "$storage_month",
		}
	},
	{"$sort": SON([("start_year", 1), ("start_month", 1)])}
		
]


def active_storage_df(dataframe, storage_formula, contract_length):
	df = (dataframe.groupby(["start_month", "start_year"]).sum().reset_index()
		.sort_values(by=["start_year", "start_month"]))
	df.at[20, 'storage_per_month'] = 1.107143e16
	df['storage_cumsum'] = df['storage_per_month'].cumsum()
	storage_sum = df['storage_cumsum'].tolist()
	active_monthly_storage = storage_formula(storage_sum, contract_length)
	df['active_storage'] = active_monthly_storage 
	df['active_storage'] = df.active_storage / 1e12
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