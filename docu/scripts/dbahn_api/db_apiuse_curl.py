import os
from os import listdir
from os.path import isfile, join
import json

CURRENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"./"))

import urllib2, base64

URL = 'https://api.deutschebahn.com/stada/v2/stations?offset=10&limit=10'

request = urllib2.Request( URL )


base64string = base64.encodestring('%s:%s' % ('Bearer', 'ef948a12c4051590327bc2ea5f889c70')).replace('\n', '')

request.add_header("Authorization", 'Bearer ef948a12c4051590327bc2ea5f889c70')
result = urllib2.urlopen(request)

print result.read()

'''
# curl -X GET --header "Accept: application/json" --header "Authorization: Bearer ef948a12c4051590327bc2ea5f889c70" "https://api.deutschebahn.com/stada/v2/stations?offset=1&limit=10"
URL = 'https://api.deutschebahn.com/stada/v2/stations?offset=10&limit=10'
'''
