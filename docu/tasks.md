# Tasks

**Python:** 2.7

## Data Extract
Selenium
APIs Reference:
- api-dbahn
- api-tiempo
- api-google



Each file has a:
- script
- config file

## Config file
**format:** yamel (.yml )
**example:**
```
options:
  increment_version: false
description: Ge the travels for a station
version: 1.0
params:
  station_number:
    value: '8000207'
  station_name:
    value: Köln
sources:
  source_name:
    dir: task-001_stations-filtered/
    files:
    - stations_filtered-all.json
    - stations_filtered-main.json
    - stations_filtered-nrw.json
    route: master
target:
  dir: task-002_station-travels/
  file: travels_$STATION$_$DATE$.log
  route: universe
```
| key | description| options |
| :------------- | :------------- | :------------- |
| options.increment_version     |         | true/false      |

---
# task 001
description ...
## Issues

# task-002_station-travels
Extract the data from the web for the gived target Station  
See in the \data\master\task-001_stations-filtered the lists of the stations.  

| Station City    | evaNumber     |
| :-------------  | :-------------|
| Koblenz         | 8000206       |
| Köln            | 8000207       |
| Bonn            | 8000044       |

## Issues

#### Api dbahn  in task-001_stations-collector
- https://data.deutschebahn.com/dataset?groups=apis

#### Encoding
- https://stackoverflow.com/questions/9942594/unicodeencodeerror-ascii-codec-cant-encode-character-u-xa0-in-position-20
- https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json
- https://stackoverflow.com/questions/46408051/python-json-load-set-encoding-to-utf-8
- https://stackoverflow.com/questions/25049962/is-encoding-is-an-invalid-keyword-error-inevitable-in-python-2-x
- https://stackoverflow.com/questions/36003023/json-dump-failing-with-must-be-unicode-not-str-typeerror

- https://stackoverflow.com/questions/24475393/unicodedecodeerror-ascii-codec-cant-decode-byte-0xc3-in-position-23-ordinal


# task-003_km-distance-stations
Get the distance between two points using the Google API - https://developers.google.com/maps/documentation/distance-matrix/intro#travel_modes
Needs a Google API KEY

# task-004_twitter-collector
Get Tweets filtered by Keywords.
Needs Twitter APP Access: https://developer.twitter.com/en.html
The access keys are defined in the **config.secret.yml** ( This file is in the git ignore list ).
The search parameters are in the task config definned:
- query_words (str): '#Vandalismusschaeden OR #BahnDown OR @DB_Info'  
- query_max_tweets (int): 100000
- query_lang (str): de en


## Capture Tweets - Stream Methods
There are two approach to get the tweets:
### Stream Method 1
The first method in Code creates a file with object, NON SEPARATED by comma. Also after the capture is needed to modify the file content.
The words search is array structured: [ 'a','b','c']
```
{ tweetsdata... }
{ tweetsdata... }
```

### Stream Method 2
The second Method in Code creates a right formed json file, but seems to be mor restricted.  
The words search is string structured with conditions: 'a OR b OR c'  

## Issues

### Encoding ascii
```
>> 'ascii' codec can't encode character u'\xf6'
```
```
 json.dump( tweets , outfile , indent=2, ensure_ascii=True)
```
