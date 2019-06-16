import os
from os import listdir
from os.path import isfile, join
import urllib2
import json

CURRENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"./"))


DB_AUTH = 'ef948a12c4051590327bc2ea5f889c70'

DB_CITY_NAME = 'Bonn'
DB_FREE_PLAN_URL =  'freeplan/v1/location/' + DB_CITY_NAME


URL = 'https://api.deutschebahn.com/' + DB_FREE_PLAN_URL



f = urllib2.urlopen( URL )
json_string = f.read()

parsed_json = json.loads(json_string)
#print parsed_json


#location = parsed_json['location']['city']
#temp_f = parsed_json['current_observation']['temp_f']
#print "Current temperature in %s is: %s" % (location, temp_f)
#f.close()



outputDir =  CURRENT_DIR #'./'
outputFile = 'db_report-'+ '.json'


with open( os.path.join( outputDir , outputFile) , 'w') as outfile:
    json.dump( parsed_json , outfile , indent=4)
