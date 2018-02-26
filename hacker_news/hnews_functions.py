import json
import requests
import pandas as pd
from pandas import ExcelWriter
from ast import literal_eval
import sqlite3
from sqlite3 import Error
'''Extract top 30 posts from Hacker News using API'''


template = "https://hacker-news.firebaseio.com/v0/{type}{id}.json?print=pretty"

def top_stories(number_of_stories, template=template):
	top_stories = template.format(type='topstories', id='')
	response = requests.get(top_stories)
	top_stories_list = literal_eval(response.content)
	return top_stories_list[:number_of_stories]


def create_news_dict(item_number, template=template):
	story_url = template.format(type='item/', id=str(item_number))
	response = requests.get(story_url)
	json_data = response.content
	py_dict = json.loads(json_data)
	return py_dict


def create_dict_slice(story_dict):
	keys = ['by', 'score', 'time', 'title', 'descendants', 'type', 'url']
	return {key: (story_dict[key] if key in story_dict else 'None') for key in keys}


def create_row(top_story):
	story_dict = create_news_dict(top_story)
	story_slice = create_dict_slice(story_dict)
	story_series = pd.Series(story_slice)
	row = pd.DataFrame(story_series)
	row = row.transpose()
	return row


def create_dataframe(function, length):
	df1 = pd.DataFrame()
	rows = map(function, top_stories(length))
	df = df1.append(rows, ignore_index=True)
	return df

def clean_dataframe(df):
	df['time'] = pd.to_datetime(df.time, unit='s' )
	df['rank'] = df.index + 1
	df['score'] = df.score.astype('int')
	df['descendants'] = df.descendants.apply(lambda x: int(x) if x != 'None' else 0)
	df['descendants'] = df.descendants.astype('int')
	return df

def update_database(dbfile, dbname, dataframe_sql_function, df):
	try:
		conn = sqlite3.connect(dbfile)
		cur = conn.cursor()
		return conn
	except Error:
		conn.close()
		print "Update Failure"
	finally:
		dataframe_sql_function(dbname, conn, df)
		print "Update Success!"
		conn.close()


def dataframe_tosql(dbname, conn, df):
	df.to_sql(name=dbname, con=conn, if_exists="append", index=False)


	





