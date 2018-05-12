#Import Packages
import pandas as pd
import numpy as np
from uszipcode import ZipcodeSearchEngine

#Import Incident report data
df = pd.read_csv("_Change_Notice__Police_Department_Incidents.csv")
uzc = ZipcodeSearchEngine()

#Data pre-processing and reverse geocoding
df['Date'] = pd.to_datetime(df['Date'])

df.sort_values(by='Date', ascending=False, inplace=True)

df = df[(df['Date'] >= '2013-1-1')]

df1 = df.copy()

len(df1)

def info(lat, long):
    data = uzc.by_coordinate(lat, long, radius=50, returns=1)
    return data


df['info'] = np.nan
df['info'] = df.apply(lambda row: info(row['Y'],row['X']), axis=1)
df.head()

df1 = df.copy()
len(df1)

df.reset_index(inplace=True)

len(df['info'])

len(df)

df['info'].isna().sum()

df['Zipcode'] = np.nan
df['Density'] = np.nan
df['LandArea'] = np.nan
df['Population'] = np.nan
df['TotalWages'] = np.nan
df['Wealthy'] = np.nan

df1 = df.copy()


df['Zipcode'] = df.apply(lambda row: row['info']['Zipcode'], axis=1)
df['Density'] = df.apply(lambda row: row['info']['Density'], axis=1)
df['LandArea'] = df.apply(lambda row: row['info']['LandArea'], axis=1)
df['Population'] = df.apply(lambda row: row['info']['Population'], axis=1)
df['TotalWages'] = df.apply(lambda row: row['info']['TotalWages'], axis=1)
df['Wealthy'] = df.apply(lambda row: row['info']['Wealthy'], axis=1)

#df.to_csv("incidents_2013-18.csv")

#Preprocessing of Business Location dta
regb = pd.read_csv('Map_of_Registered_Business_Locations.csv')

regb.dropna(subset=['Source Zipcode'], inplace=True)

regb['Source Zipcode'].isna().sum()

regb['Source Zipcode'] = regb['Source Zipcode'].astype('int')

type(regb['Source Zipcode'][0])

regb = regb[(regb['City'] == 'San Francisco')]

regb = regb[(regb['Source Zipcode'] >= 90000)]

bus_reg = regb[['Source Zipcode', 'NAICS Code Description']].groupby(['Source Zipcode', 'NAICS Code Description']).size().reset_index(name='Counts')

bus_reg.to_csv('Business Count by Zipcode.csv')


#Preprocessing of Land Use data
luse = pd.read_csv('LandUse2016.csv')

type(luse['the_geom'][0])

luse['the_geom'] = luse['the_geom'].astype('str')

import re #Regular expressions package in python import

#Functions to Extract Latitude and Lontgitude from Polygon area data
def lat_extract (multipoly):
    lat = re.search(r"[+-]?3\d{1,3}[.]\d+", multipoly)
    if (lat is not None):
        return lat.group(0)
    else:
        return np.nan

def long_extract (multipoly):
    long = re.search(r"[+-]?1\d{1,3}[.]\d+", multipoly)
    if (long is not None):
        return long.group(0)
    else:
        return np.nan

luse['latitude'] = np.nan
luse['latitude'] = luse.apply(lambda row: lat_extract(row['the_geom']), axis=1)

luse['longitude'] = np.nan
luse['longitude'] = luse.apply(lambda row: long_extract(row['the_geom']), axis=1)

#luse['latitude'].isna().sum()


luse['latitude'] = luse['latitude'].astype('float')
luse['longitude'] = luse['longitude'].astype('float')



luse['info'] = np.nan
luse['info'] = luse.apply(lambda row: info(row['latitude'],row['longitude']), axis=1)

luse1 = luse.copy()

luse['Zipcode'] = luse.apply(lambda row: row['info'][0]['Zipcode'], axis=1)

luse.to_csv('LandUse.csv')
