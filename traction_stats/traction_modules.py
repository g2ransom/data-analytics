from bridge_functions import *
from storageevents_stats import users_pipeline
from shards_stats import shards_pipeline, active_storage_df, get_monthly_storage
from debit_stats import debits_pipeline
import calendar


client = open_client(host=mongo_host, username=mongo_username, password=mongo_password)
db = client['bridge']


shards = shards_pipeline
shards_aggregate = db.shards.aggregate(shards)
shards_list = list(shards_aggregate)
pprint(db.command('aggregate', 'shards', pipeline=pipeline, explain=True))
shards_dataframe = pd.DataFrame(shards_list)
shards_df = active_storage_df(shards_dataframe, get_monthly_storage, 3) 
shards_df = shards_df[['start_month', 'start_year', 'active_storage']]
shards_df.rename({'month': 'start_month', 'year', 'start_year'})


debits = debits_pipeline
debits_aggregate = db.debits.aggregate(debits)
debits_list = list(debits_aggregate)
pprint(db.command('aggregate', 'debits', pipeline=pipeline, explain=True))
debits_df = pd.DataFrame(debits_list)


active_users = users_pipeline
users_aggregate = db.storageevents.aggregate(active_users)
users_list = list(users_aggregate)
pprint(db.command('aggregate', 'users', pipeline=pipeline, explain=True))
users_df = pd.DataFrame(users_list)


df = shards_df.merge(debits_df, how='left', on=['month', 'year'])
df = df.merge(users_df, how='left', on=['month', 'year'])

df = df1.merge(df2, how='left', on=['month', 'year'])
df = df.merge(df3, how='left', on=['month', 'year'])

df_to_csv(df,'traction_stats', '.csv')

# df['month'] = df['month'].apply(lambda x: calendar.month_name[x])
# df['year'] = df['year'].apply(lambda x: str(x))
# df['date'] = df[['month', 'year']].apply(lambda x: ' '.join(x), axis=1)
# df = df[['date', 'userbyMonth', 'farmersPerMonth', 'bandwidthUsed', 'bandwidthBilled', 'monthlyStorage', 'storageBilled']]
# df.to_csv("traction_stats0118.csv")