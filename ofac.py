from pymongo import MongoClient
import pandas as pd
import socket
from geoip import geolite2
import pycountry

client = MongoClient()

db = client['test']

pipeline = [
	{"$group": {"_id": None, "addresses": {"$addToSet": "$address"}}},
	{"$unwind": "$addresses"},
	{"$project": {"_id": 0, "addresses": 1}}
]

ip_addresses = list(db.contacts_test.aggregate(pipeline))

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


country_codes = []
for addr in cleaned_addresses:
	match = geolite2.lookup(addr)
	try:
		country_codes.append(match.country)
	except (AttributeError, ValueError):
		country_codes.append('N/A')


country_names = []

for code in country_codes:
	try:
		country_info = pycountry.countries.get(alpha_2=code)
		country_names.append(country_info.name)
	except KeyError:
		country_names.append('N/A')

sanctions_list = ['Balkans', "Belarus", 'Burundi', 'Cuba', 'Congo', 'Iran', 'Iraq', 'Lebanon', 'Libya', 'North Korea',
					'Somalia', 'Sudan', 'South Sudan', 'Syria', 'Ukraine', 'Venezuela', 'Yemen', 'Zimbabwe']

flag = []

for name in country_names:
	if name in sanctions_list:
		flag.append(1)
	else:
		flag.append(0)


df = pd.DataFrame({'IP Address': cleaned_addresses, 'Country Codes': country_codes, 'Country Names': country_names, 'Flags': flag})
print(df.head())

sanctioned_ip = df[df['Flags'] == 1].count()['Flags']
na_list = df[df['Country Names'] == 'N/A'].count()['Country Names']

print(sanctioned_ip)
print(na_list)
