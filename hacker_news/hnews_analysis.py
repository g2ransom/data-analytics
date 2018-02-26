from hnews_functions import *

conn = sqlite3.connect("hackernews.db")
df = pd.read_sql_query("SELECT * FROM hackernews LIMIT 5", conn)
print(df)