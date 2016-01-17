import numpy
import pandas
import json
import statsmodels.api as sm

__author__ = 'nsrivas3'

'''
TTD -
1.  regress latitude and longitude on time
    (in this case the rows are constant longitude, but that is of course not always true).
1a. Regress latitude on longitude and vice versa (using whichever regression gives you the smallest errors)
    to figure out the orientation of the row.
2.  use some p-statistics or something to figure out when the harvest has actually started.
3.  Use deviations from the regress-latitude/longitude-on-time to figure out when the worker is returning to the
    edge of the field; this will quantify when and where the harvest actually was.
4.  Use the regress-latitude/longitude-on-time and the edge of the field to estimate when the worker will finish.
'''

file = open('data_2016-01-06.txt',mode='r')
json_data = json.load(file)
json_data = pandas.DataFrame(json_data)
print(json_data,"\n")
UnqWorker = list(numpy.unique(json_data['worker']))
print(type(UnqWorker))
print(UnqWorker)

for i in UnqWorker:
    tempLat = json_data['lat'][json_data['worker'] == i]
    tempTime = json_data['time'][json_data['worker'] == i]
    tempLng = json_data['lng'][json_data['worker'] == i]

    # 1.1 Regressing Latitude on time
    modelTLat = sm.OLS(tempLat, tempTime)
    modelTLatEval = modelTLat.fit()
    resultTLat = modelTLatEval.summary()

    # 1.2 Regressing Longitude on time
    modelTLng = sm.OLS(tempLng, tempTime)
    modelTLngEval = modelTLng.fit()
    resultTLng = modelTLngEval.summary()

    # 1a.1 Regressing Lat on Long
    modelLngLat = sm.OLS(tempLat, tempLng)
    modelLngLatEval = modelLngLat.fit()
    resultLngLat = modelLngLatEval.summary()

    # 1a.2 Regressing Long on Lat
    modelTLng = sm.OLS(tempLng, tempTime)
    modelTLngEval = modelTLng.fit()
    resultTLng = modelTLngEval.summary()




