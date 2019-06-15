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

import urllib2, base64

CONFIG_FILE_NAME = '001.00_config.yml'
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

#COM: the loop
def collectStations():
  TOTAL = 5363
  LIMIT = 100
  numStations = 0
  counter = 0
  while numStations < TOTAL:
    first = counter
    URL = 'https://api.deutschebahn.com/stada/v2/stations?offset='+ str(counter) + '&limit=' + str(LIMIT)
    try:
      request = urllib2.Request( URL )
      request.add_header("Authorization", 'Bearer ' + config['params']['bearer'] )
      result = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
      print( counter, e )
      return 0
    else:
      jsonStringResponse = result.read()
      time.sleep(0.3)
      counter += LIMIT
      last = counter
      rangeUnique = str(first) + '-' + str(last)
      outputFilePath = outputPath + config['target']['file'].replace("$UNIQUE$", rangeUnique )
      with open( outputFilePath , 'w') as outfile:
        json.dump( json.loads(jsonStringResponse), outfile , indent=2, ensure_ascii=False)


collectStations()