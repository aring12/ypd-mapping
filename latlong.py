#!/usr/bin/python3
import sys
import geopy
import certifi
import ssl
import pandas as pd
import numpy as np
ctx=ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context=ctx
from geopy.geocoders import Nominatim
geolocator=Nominatim(scheme='http', user_agent='ypddatavis')

# dataframe dictionary hold all addresses for lookup and convert to dict:
address_help_df = pd.read_csv('address_help.csv', index_col=0)
address_help = address_help_df.to_dict('index')
# address_help['ABCDE'] = {'Latitude': 10, 'Longitude': 11}
# address_help_df = pd.DataFrame.from_dict(address_help, orient='index')
def get_latlong(address):
	if address in address_help:
		return (address_help[address]['Latitude'], address_help[address]['Longitude'])
	elif address[0].isdigit():
		location = geolocator.geocode(address + " New Haven CT")
		if location:
			address_help[address] = {'Latitude':location.latitude, 'Longitude':location.longitude}
			print("adding {} to address_help".format(address))
			# update the address_help.csv file after every 20 addresses added
			if len(address_help)%10 == 0:
				print("UPDATING address_help.csv")
				address_help_df = pd.DataFrame.from_dict(address_help, orient='index')
				address_help_df.to_csv('address_help.csv')
			return (location.latitude, location.longitude)
		else:
			print(address)
	else:
		print(address)

df = pd.read_csv('2015.csv', index_col=0)
print(df)
df['latlong'] = df.apply(lambda row : get_latlong(row['Location']), axis = 1)
df['Latitude'] = df.apply(lambda row : row['latlong'][0], axis = 1)
df['Longitude'] = df.apply(lambda row : row['latlong'][1], axis = 1)
df.drop('latlong', axis=1, inplace=True)
df.to_csv("2015_LL.csv")
address_help_df = pd.DataFrame.from_dict(address_help, orient='index')
address_help_df.to_csv('address_help.csv')