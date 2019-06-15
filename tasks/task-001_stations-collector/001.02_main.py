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

import io
from os import listdir
from os.path import isfile, join

CONFIG_FILE_NAME = '001.02_config.yml'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME, 'r'))

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

# _____________________________________________________________________________________ INIT

#STEP: modify version?
configVersion = config['version']
config['version'] =  round( float(configVersion) + .1, 1 ) if config['options']['increment_version'] == True else configVersion

#STEP: output-file
outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 

#COM: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )


#STEP: Load Data

configSourceElement = config['sources']['source_stations']
sourceFile = router.getRoute( configSourceElement['route'] ) + configSourceElement['dir'] + configSourceElement['file']
rawContent = open( sourceFile , 'r') 
fileJsonContent = json.load( rawContent )

#STEP: Filter the stations

selectedFilterKey = config['params']['selectedFilterKey']['value']

objFilteredStations = {}

for idx, item in enumerate( fileJsonContent ):
    
  PLZ = item["mailingAddress"]["zipcode"]
  NAME = item["name"].encode('utf-8')

  #COM: Filters
  filters = {
    'nrw': (PLZ.startswith("5") and 'Hbf' in NAME),
    'main':  ('Hauptbahnhof' in NAME or 'Hbf' in NAME),
    'all' : True
  }

  if selectedFilterKey not in filters:
    break

  if filters[ selectedFilterKey ]:
    buf = {
      "name"      : NAME,
      "city"      : item["mailingAddress"]["city"].encode('utf-8'),
      "zipcode"   : item["mailingAddress"]["zipcode"],
      "number"    : item["number"]
    }
    
    evaNumber = '0'

    if len( item["evaNumbers"]) > 0:
      if len( item["evaNumbers"]) == 1:
        evaNumber =  str(item["evaNumbers"][0]["number"])
        if "geographicCoordinates" in item["evaNumbers"][0]:
          coord = item["evaNumbers"][-1]["geographicCoordinates"]["coordinates"]
        else:
          coor = '0'
        buf["evaNumber"] = evaNumber
        buf["coord"] = coord
      else:
        for evas in item["evaNumbers"]:
          if evas["isMain"] == True:
            evaNumber =  str(evas["number"])
            if "geographicCoordinates" in evas:
              coord = evas["geographicCoordinates"]["coordinates"]
            else:
              coor = '0'
            buf["evaNumber"] = evaNumber
            buf["coord"] = coord

    objFilteredStations[ evaNumber ] = buf


outputFilePath = outputPath + config['target']['file'].replace("$UNIQUE$", selectedFilterKey )
with open( outputFilePath , 'w') as outfile:
  json.dump( objFilteredStations , outfile , indent=2, ensure_ascii=False)

