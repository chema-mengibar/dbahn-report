# -*- coding: utf-8 -*-
import os
import sys

DIR_TASK = os.path.basename(os.getcwd())
DIR_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
DIR_TASK = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt

import urllib2

CONFIG_FILE_NAME = '003.00_config.yml'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME, 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

# _____________________________________________________________________________________ INIT

#STEP: modify version?
configVersion = config['version']
config['version'] =  round( float(configVersion) + .1, 1 ) if config['options']['increment_version'] == True else configVersion


#DEF
def getInfosAB(  station_a , station_b  ):
  global log
  YOUR_API_KEY = config['params']['api_key']
  ORIGIN      = str(station_a['coord'][1]) + ',' + str(station_a['coord'][0])
  DESTINATION = str(station_b['coord'][1]) + ',' + str(station_b['coord'][0])
  MODE        = 'transit' # 'bicycling'

  url = [
    "https://maps.googleapis.com/maps/api/",
    "distancematrix",
    "/json?",
    "origins=" + ORIGIN ,
    "&destinations=" + DESTINATION ,
    "&mode=" + MODE ,
    "&language=de-DE",
    '&key=' + YOUR_API_KEY
  ]
  URL = "".join(url)
  try:
    request = urllib2.Request( URL )
    result = urllib2.urlopen(request)
  except urllib2.HTTPError, e:
    print("404")
  else:
    json_string = result.read()
    result_json = json.loads(json_string)
    if result_json['status'] == 'REQUEST_DENIED':
      print '>> ERROR: ' + result_json['error_message']
      return {}
    filtered_result_json = {
      "duration_seconds": result_json["rows"][0]["elements"][0]["duration"]["value"],
      "distance_meters": result_json["rows"][0]["elements"][0]["distance"]["value"],
      "station_a" : station_a["evaNumber"] ,
      "station_b" : station_b["evaNumber"]
    }
  return filtered_result_json


#STEP
configSourceElement = config['sources']['source_stations']
sourcePath = router.getRoute( configSourceElement['route'] ) + configSourceElement['dir'] 
sourceFiles = sourcePath + configSourceElement['files'][2]
listStations = json.load( open( sourceFiles , 'r') )


#STEP: output-file
outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 

#COM: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )


# STEP: get data

station_a_obj = listStations[ str(config['params']['station_a_evanumber']) ]
station_b_obj = listStations[ str(config['params']['station_b_evanumber']) ]

result_json = getInfosAB( station_a_obj , station_b_obj )

suffixFIleName = str( station_a_obj["evaNumber"]) + "-" + str( station_b_obj["evaNumber"])

outputFilePath = outputPath + config['target']['file'].replace("$SUFFIX$", suffixFIleName )
with open( outputFilePath , 'w') as outfile:
  json.dump( result_json , outfile , indent=2, ensure_ascii=False)