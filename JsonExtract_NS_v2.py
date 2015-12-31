__author__ = 'nsrivas3'

'''
TTD
1. To read and do simple manipulations on data given as a JSON file
'''

import math
import json
from operator import itemgetter
from itertools import groupby
import numpy

file = open('data.txt',mode='r')
json_data = json.load(file)
worker_data = []
worker_smmry = []

# Remove this when done
print("###################################################################### \n")
print("UNsorted JSON data \n")
print(json_data)
print("###################################################################### \n")

# 1. Data type formed after de-serializing JSON
print("Data Type -> ",str(type(json_data)))

# 2. Number of Rows in the DataSet(DS)
print("Num Obs -> ",json_data.__len__())

# 3. Grouping on Workers
json_data = sorted(json_data,key=itemgetter('worker','time'))
print("###################################################################### \n")
print("sorted JSON data \n")
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



