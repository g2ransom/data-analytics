import os
import ssl
import json
from pymongo import MongoClient
from pymongo import ReadPreference
import pandas as pd
import socket
import geoip2.database
from geoip2.errors import AddressNotFoundError


mongo_host = os.environ['MONGO_HOST']
mongo_username = os.environ['MONGO_USERNAME']
mongo_password = os.environ['MONGO_PASSWORD']

client = MongoClient(host=mongo_host,
						port=27017,
						ssl=True,
						ssl_cert_reqs=ssl.CERT_NONE,
						username=mongo_username,
						password=mongo_password,
						read_preference=ReadPreference.SECONDARY
						)

db = client['bridge']

pipeline = [
	{"$project": {"address": 1}},
	{"$group": {"_id": "$_id", "addresses": {"$addToSet": "$address"}}},
	{"$unwind": "$addresses"},
	{"$project": {"_id": 0, "node_id": "$_id", "ip_address": "$addresses"}}
]

result = db.contacts.aggregate(pipeline, allowDiskUse=True)
data = list(result)
df = pd.DataFrame(data)

def clean_address(address):
	for fmly in socket.AF_INET, socket.AF_INET6:
		try:
			socket.inet_pton(fmly, address)
			return address
		except:
			socket.error

def load_countries(address):
	try:
		response = reader.city(address.strip())
		return response.country.name
	except (ValueError, AddressNotFoundError):
		return 'N/A'


addresses = df.ip_address.tolist()
clean_addresses = filter(lambda x: x != None, map(clean_address, addresses))
df = df[df.ip_address.isin(clean_addresses)]


reader = geoip2.database.Reader('GeoLite2-City.mmdb')
countries = map(load_countries, clean_addresses)
country_series = pd.Series(countries)
df['country'] = country_series.values
df = df[df.country != 'N/A']

nodes = df.groupby('country')['node_id'].apply(list)
ips = df.groupby('country')['ip_address'].apply(list)

list_df = pd.concat([nodes, ips], axis=1)
sanctions = ['Iran', 'Iraq', 'North Korea', 'Syria', 'Cuba', 'Sudan']
sanction_df = list_df.reindex(sanctions, fill_value=0)
sanction_dict = sanction_df.to_dict('index')
with open('jan_ofac.json', 'w') as fp:
	json.dump(sanction_dict, fp, index=4)

# df.to_csv("jan_payments.csv", encoding='utf8', index=False)