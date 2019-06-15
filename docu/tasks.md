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

# task 002
description ...

see in the \data\master\task-001_stations-filtered the lists of the stations.

| Station         | evaNumber     |
| :-------------  | :-------------|
| Koblenz         | 8000206       |
| Köln            | 8000207       |
| Bonn            | 8000044       |

## Issues

# task 003
description ...
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
