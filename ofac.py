from pymongo import MongoClient
import pandas as pd
import socket
from geoip2.errors import AddressNotFoundError
from math import asin, sqrt, sin, cos, acos, radians, pi

import geoip2.database

client = MongoClient()

db = client['test']

pipeline = [
	{"$group": {"_id": None, "addresses": {"$addToSet": "$address"}}},
	{"$unwind": "$addresses"},
	{"$project": {"_id": 0, "addresses": 1}}
]

ip_addresses = list(db.contacts_11.aggregate(pipeline))

df = pd.DataFrame(ip_addresses)

addresses = df['addresses'].tolist()
cleaned_addresses = []

for address in addresses:
	for fmly in socket.AF_INET, socket.AF_INET6:
		try:
			socket.inet_pton(fmly, address)
			cleaned_addresses.append(address)
		except:
			socket.error

reader = geoip2.database.Reader('GeoLite2-City.mmdb')

country_names = []
country_codes = []
region_names = []
city_names = []
long_lat = []
for addr in cleaned_addresses:
	try:
		response = reader.city(addr.strip())
		country_names.append(response.country.name)
		country_codes.append(response.country.iso_code)
		region_names.append(response.subdivisions.most_specific.name)
		city_names.append(response.city.name)
		long_lat.append((response.location.longitude, response.location.latitude))
	except (ValueError, AddressNotFoundError):
		country_names.append('N/A')
		country_codes.append('N/A')
		region_names.append('N/A')
		city_names.append('N/A')
		long_lat.append('N/A')


df = pd.DataFrame({'IP Addresses': cleaned_addresses, 'Country Names': country_names, 'Country Codes': country_codes, 
				'Region Names': region_names, 'City Names': city_names, 'Longtitude, Latitude': long_lat})


df = df[df['Country Names'] != 'N/A']
df.to_csv("ofac.csv", encoding='utf8')