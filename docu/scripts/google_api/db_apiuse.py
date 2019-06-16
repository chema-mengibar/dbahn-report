import os
from os import listdir
from os.path import isfile, join
import urllib2
import json

CURRENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"./"))

# https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&key=YOUR_API_KEY
# https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&mode=bicycling&language=fr-FR&key=AIzaSyC116ghEYpqy5oNnaKyUXEqZSozFffWLOk

YOUR_API_KEY = ''

ORIGIN      = 'Vancouver+BC|Seattle'
DESTINATION = 'San+Francisco|Victoria+BC'
MODE        = 'bicycling' #bicycling

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
  parsed_json = json.loads(json_string)
  outputDir =  CURRENT_DIR
  outputFile = 'response'+ '.json'
  with open( os.path.join( outputDir , outputFile) , 'w') as outfile:
    json.dump( parsed_json , outfile , indent=4)