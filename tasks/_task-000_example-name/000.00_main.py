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

import math
import re

CONFIG_FILE_NAME = '000.00_config.yml'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME, 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

# _____________________________________________________________________________________ INIT

# today = dt.datetime.now().strftime("%Y-%m-%d--%H-%M") 

# if __name__ == '__main__':
# raise ValueError('Not all required parameters')
'''
args = sys.argv[1:]
params = { }
for arg in args:
  param = arg.split("=")
  argKey = param[0]
  argValue = str( param[1] )
  params[ argKey ]= argValue
'''

#DEF:
def getSourceFile( _sourceKey, _fileIdx ):
  sourceName = config['sources'][ _sourceKey ]
  sourcePathFile = router.getRoute( sourceName['route'] ) + sourceName['dir'] + sourceName['files'][ _fileIdx ]
  return open( sourcePathFile , 'r')


#STEP: modify version?
configVersion = config['version']
config['version'] =  round( float(configVersion) + .1, 1 ) if config['options']['increment-version'] == True else configVersion


#STEP: load file json
rawContent = getSourceFile( 'source_langs', 0 )  
fileJsonContent = json.load( rawContent )

#COM: read in your format here
#HELP: JSON   -> fileJsonContent = json.load( rawFile )
#HELP: DF-CSV -> df_Data = pd.read_csv( filepath_or_buffer=sourcePathFile, sep=";", quoting=3, decimal="," )
#HELP: TXT    -> listLines = fileLinesRaw = [line.rstrip('\n') for line in rawFile]


#STEP: output-file
outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
outputFilePath = outputPath + config['target']['file'].replace("$VERSION$", str( config['version'] ) )

#COM: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )

#HELP: save example 
#COM: save taks-data file
outputCollection = {}
with open( outputFilePath , 'w') as outfile:
  json.dump( outputCollection , outfile , indent=2, ensure_ascii=False)


#STEP: update config file

yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME, 'w'), indent=2, default_flow_style=False )
