from hnews_functions import *

df1 = create_dataframe(create_row, 30)
df = clean_dataframe(df1)
update_database("hackernews.db", "hackernews", dataframe_tosql, df)
