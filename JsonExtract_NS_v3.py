__author__ = 'nsrivas3'

'''
TTD
1. Include the Hoversine Formula
2. Thresholding for Motion Detection
'''

import math
import json
from operator import itemgetter
from itertools import groupby
import numpy

def hvsne(unit,inLat,inLng,finLat,finLng):
    # Defining the Haversine formula for calculating distances between 2 pts given by Lat,Lng in decimal format
    # unit = {"M":"miles","K":"kilometers","N":"nautical miles"}
    rad_inLat = math.pi * inLat/180
    rad_finLat = math.pi * finLat/180
    rad_inLng = math.pi * inLng/180
    rad_finLng = math.pi * finLng/180
    rad_theta = rad_inLng - rad_finLng
    dist = math.sin(rad_inLat) * math.sin(rad_finLat) + math.cos(rad_inLat) * math.cos(rad_finLat) * math.cos(rad_theta)
    dist = math.acos(dist)
    dist = dist * 180/math.pi
    dist = dist * 60 * 1.1515
    if (unit== "K"):
        dist = dist * 1.609344
    if (unit=="N"):
        dist = dist * 0.8684
    return(dist)

'''
QC Done - works well!
print("Distance between BOMB KAR ->",hvsne("K",19.075984,72.877656,24.829535,67.084811))
print("Distance between BOMB Del ->",hvsne("K",19.075984,72.877656,28.613939,77.209021))
print("Distance between BOMB chi ->",hvsne("K",19.075984,72.877656,41.878114,-87.629798))
print("Distance between BOMB shanghai ->",hvsne("K",19.075984,72.877656,30.866557,121.285823))
print("Distance between BOMB tokyo ->",hvsne("K",19.075984,72.877656,35.689487,139.691706))
print("Distance between BOMB london ->",hvsne("K",19.075984,72.877656,51.507351,-0.127758))
print("Distance between BOMB sao paolo ->",hvsne("K",19.075984,72.877656,-23.550520,-46.633309))
'''

file = open('data.txt',mode='r')
json_data = json.load(file)
worker_data = []
worker_smmry = []

# Remove this when done
print("UNsorted JSON data \n")
print("###################################################################### \n")
print(json_data)
print("###################################################################### \n")

# 1. Data type formed after de-serializing JSON
print("Data Type -> ",str(type(json_data)))

# 2. Number of Rows in the DataSet(DS)
print("Num Obs -> ",json_data.__len__())

# 3. Grouping on Workers
json_data = sorted(json_data,key=itemgetter('worker','time'))
print("sorted JSON data \n")
print("###################################################################### \n")
print(json_data)
print("###################################################################### \n")
for i in  range(0,json_data.__len__()):
	temp = []
	if (i>0):
		if (json_data[i]['worker']==json_data[i-1]['worker']):
			temp.append(json_data[i]['worker'])
			delLat = abs(json_data[i]['lat'] - json_data[i-1]['lat'])
			delLng = abs(json_data[i]['lng'] - json_data[i-1]['lng'])
			temp.append(math.sqrt(delLat**2+delLng**2))
			temp.append(json_data[i]['time'])
		else:
			temp.append(json_data[i]['worker'])
			delLat = 0.0
			delLng = 0.0
			temp.append(math.sqrt(delLat**2+delLng**2))
			temp.append(json_data[i]['time'])
	else:
		temp.append(1)
		delLat = 0.0
		delLng = 0.0
		temp.append(math.sqrt(delLat**2+delLng**2))
		temp.append(5)
	worker_data.append(temp)

for k,g in groupby(worker_data,lambda x:x[0]):
	g = numpy.array(list(g))
	g = sum(g[:,1])/(numpy.count_nonzero(g[:,1])+1)
	temp = []
	temp.append(k)
	temp.append(g)
	worker_smmry.append(temp)


worker_smmry = sorted(worker_smmry,key=itemgetter(1))
print(worker_smmry)



