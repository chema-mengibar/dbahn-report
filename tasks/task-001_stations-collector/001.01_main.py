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

CONFIG_FILE_NAME = '001.01_config.yml'
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

#COM: Join all the input-files
loadedDataJson = []

configSourceElement = config['sources']['source_stations']
sourcePath = router.getRoute( configSourceElement['route'] ) + configSourceElement['dir']
sourceFilesNames = [f for f in listdir( sourcePath ) if isfile(join(sourcePath , f))]

for f in sourceFilesNames:
  with io.open( os.path.join( sourcePath , f ), mode='r') as outfile:
    listResult = json.load(outfile)
    loadedDataJson.extend( listResult["result"] )

outputFilePath = outputPath + config['target']['file']
with io.open(outputFilePath, mode='w', encoding='utf-8') as outfile:
  outfile.write(unicode(json.dumps(loadedDataJson, indent=2, ensure_ascii=False)))
