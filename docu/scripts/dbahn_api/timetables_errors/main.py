#!/usr/local/bin/python
import sys
import os
from os import listdir
from os.path import isfile, join
MODULES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append( MODULES_DIR )
from modules.simpleLoader  import Loader
CURRENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"./"))
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../.."))
sys.path.append( ROOT_DIR )
#custom imports
import json
import time
import urllib2, base64
from lxml import etree

def getTrainInfos(hour_str, s_item , station_name, station_id_str ):
    train = s_item.find('tl')
    train_code = train.get("c")
    train_num = str(train.get("n"))
    info_ar = 0
    info_dp = 0
    if s_item.find('ar') is not None:
        info_ar = 1
        ar = s_item.find('ar')
        ar_t = ar.get('pt')
        ar_date =  str(ar_t[0:6])
        ar_time =  str(ar_t[6:10])
        ar_p = ar.get('pp')
        ar_route = ar.get('ppth').encode('utf8')
    if s_item.find('dp') is not None:
        info_dp = 1
        dp = s_item.find('dp')
        dp_t = dp.get('pt')
        dp_date =  str(dp_t[0:6])
        dp_time =  str(dp_t[6:10])
        dp_p = dp.get('pp')
        dp_route = dp.get('ppth').encode('utf8')
    #COM: build json item
    train_route_infos = {}
    #COM:
    if  info_ar == 1:
        #just arr
        l_ar = {
            'dateFull': ar_t,
            'date': ar_date,
            'time': ar_time,
            'platform': ar_p,
            #'routeFull': ar_route,
            'routeStops' : loader.changeAscii_utf8(ar_route).split('|')
        }
        train_route_infos["ar"] = l_ar
    #COM:
    if  info_dp == 1:
        #just dep
        l_dp = {
            'dateFull': dp_t,
            'date': dp_date,
            'time': dp_time,
            'platform': dp_p,
            #'routeFull': dp_route,
            'routeStops' : loader.changeAscii_utf8(dp_route).split('|')
        }
        train_route_infos["dp"] = l_dp
    #COM:
    train_infos = {
        'hourSearch' : hour_str,
        'stationName' : station_name,
        'stationIdStr': station_id_str ,
        'trainCode': train_code  ,
        'trainNum': train_num ,
        'trainRefFull': train_code + "-" + train_num,
        'trainRoute' : train_route_infos
    }
    return train_infos


#REPLACE
#1 #station_json = {}
#2 #station_json[hour_str] = {}
#3 #station_json[hour_str][station_id_str] = []
#4 #station_json[hour_str][station_id_str].append( train_infos )
#5 #loader.saveJsonItemToRawFile( station_json[hour_str], FLAT_SOURCE  )


def customRoutine(FLAT_SOURCE, FLAT_PARAMETERS):

    errorItems = loader.loadJsonInputToItem( FLAT_SOURCE )
    stationCounter = 1
    limit = 20
    stationsList = loader.loadJsonExtraFieldsToItem( FLAT_SOURCE, "pathStations","fileStations"  )
    #for key, value in d.iteritems():
    for ids, station in enumerate(errorItems, start=1):
        station_id_str = station["station"]
        hour_str = station["hour"]
        date_str = station["date"]
        station_name = stationsList[station_id_str]["name"]
        #COM:
        URL = 'https://api.deutschebahn.com/timetables/v1/plan/'+ station_id_str +'/'+ date_str +'/'+ hour_str
        print URL
        try:
            request = urllib2.Request( URL )
            request.add_header("Authorization", 'Bearer ef948a12c4051590327bc2ea5f889c70')
            result = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            error_report = {
                "hour":hour_str,
                "station":station_id_str,
                "date":date_str,
                "error": str(e)
            }
            loader.saveJsonItemToRawFile( error_report , FLAT_SOURCE , date_str + '_errors' )
            e_string = e.read()
            #COM no response, no access or no trains
            errors = ['400', '404', '410', '429' , '502', '500']
            if not any(ext in str(e) for ext in errors):
                e_json = json.loads(e_string)
                if 'error' in e_json.keys():
                    if e_json['error']["code"] == '900800':
                        time.sleep(60)

        else:
            xml = etree.fromstring( result.read() )
            #COM
            if 'station' in xml.attrib:
                #station_name = loader.changeAscii( xml.get('station') )
                lineItems = xml.findall('s')
                #COM: lineas de trenes que pasan por una ciudad a una hora
                for s_item in lineItems:
                    train_infos = getTrainInfos(hour_str, s_item, station_name , station_id_str )
                    #COM:
                    loader.saveJsonItemToRawFile( train_infos , FLAT_SOURCE , date_str )
        #COM:
        if ids == limit*stationCounter:
            stationCounter += 1
            time.sleep(60)





if __name__ == '__main__':
    loader = Loader()
    #COM: load Model.json to 1 level object
    FLAT_SOURCE, FLAT_PARAMETERS = loader.loadJsonModelToFlag( ROOT_DIR , CURRENT_DIR  )
    loader.createOutputDir(FLAT_SOURCE)
    customRoutine(FLAT_SOURCE, FLAT_PARAMETERS)
    PROCESS_RESULT = loader.saveReportModel( FLAT_SOURCE, FLAT_PARAMETERS )
