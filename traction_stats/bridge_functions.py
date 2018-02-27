import os
import ssl
from pymongo import MongoClient
from pymongo import ReadPreference
from pprint import pprint
import datetime
import pandas as pd
from bson.son import SON
from pprint import pprint

mongo_host = os.environ['MONGO_HOST']
mongo_username = os.environ['MONGO_USERNAME']
mongo_password = os.environ['MONGO_PASSWORD']


def open_client(host=None, port=27017, ssl=True, ssl_cert_reqs=ssl.CERT_NONE, username=None, password=None, read_preference=ReadPreference.SECONDARY):
	client = MongoClient(host=host, port=port, ssl=ssl, 
						ssl_cert_reqs=ssl_cert_reqs,
						username=username, password=password, 
						read_preference=read_preference)
	return client


# def aggregate_pipeline(db, collection, pipeline):
# 	collection_pipeline = db.collection.aggregate(pipeline)
# 	collection_results = list(collection_pipeline)
# 	print(db.command('aggregate', collection, pipeline=pipeline, explain=True))
# 	return collection_results


def pipeline_to_df(collection_results): return pd.DataFrame(collection_results)


def df_to_csv(df, pipeline_name, filetype): 
	date = datetime.datetime.today().strftime('%m%d%Y')
	filename = pipeline_name + date + filetype
	df.to_csv(filename, index=False)