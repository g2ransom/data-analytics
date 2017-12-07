from storage_events_stats import storage_events_df
from shards_stats import shards_df, get_monthly_storage
from debit_stats import debits_df
import calendar
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go


df1 = storage_events_df()
df2 = debits_df()
df3 = shards_df()

df = df1.merge(df2, how='left', on=['month', 'year'])
df = df.merge(df3, how='left', on=['month', 'year'])

df['month'] = df['month'].apply(lambda x: calendar.month_name[x])
df['year'] = df['year'].apply(lambda x: str(x))
df['date'] = df[['month', 'year']].apply(lambda x: ' '.join(x), axis=1)
df = df[['date', 'userbyMonth', 'farmersPerMonth', 'bandwidthUsed', 'bandwidthBilled', 'monthlyStorage', 'storageBilled']]
df.to_csv("traction_stats.csv")