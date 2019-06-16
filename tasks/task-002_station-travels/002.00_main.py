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

reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from requests.utils import quote
import urllib2
from bs4 import BeautifulSoup
import logging
import re
import time

CONFIG_FILE_NAME = '002.00_config.yml'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME, 'r'))

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

# _____________________________________________________________________________________ INIT


today = dt.datetime.today()

def getTravels( station_code, station_id_str, l_time, l_day, direction ):
  # https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=15082&country=DE&protocol=https:&seqnr=4&ident=fi.0865482.1497188234&rt=1&input=8000001&time=08:00&date=14.06.17&ld=15082&productsFilter=1111100000&start=1&boardType=dep&rtMode=DB-HYBRID
  global log
  filtro = '1111100000'
  url = {
    "a": "https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?",
    "b": "ld=15082",
    "c": "&country=DE",
    "d": "&protocol=https:",
    "e": "&seqnr=4",
    "f": "&ident=fi.0865482.1497188234&rt=1",
    "g": "&input=" + station_code,
    "h": "&time=" +  l_time  + "&date=" +  l_day  + "&ld=15082",
    "i": "&productsFilter=" + filtro,
    "j": "&start=1&boardType="+ direction + "&rtMode=DB-HYBRID"
  }
  compossed_url = "".join(url.values())
  # print compossed_url
  rsp = requests.get( compossed_url)
  log.debug( 'START_PARSE_URL' )
  html = rsp.text.encode("utf8")   #html = rsp.content
  soup = BeautifulSoup(html, "lxml") # html.parser
  travelRows = soup.findAll('tr', id=re.compile('^journeyRow_'))
  
  for linebreak in soup.find_all('br'):
    linebreak.extract()

  if len(travelRows) > 0 :
    for row in travelRows:

      if len(row.find_all("td", class_="platform")) > 0 :
        platform_int =  row.find_all("td", class_="platform")[0].text.replace('\n', '')
      else:
        platform_int = '-'

      alerts = []
      statusActual = ''

      if len(  row.find_all("td", class_="ris") ) > 0 :
        delayItems = row.find_all("td", class_="ris")[0].find_all('span',class_=re.compile('^delay'))
        if len( delayItems ) > 0:
          statusActual = delayItems[0].text

        alertItems = row.find_all("td", class_="ris")[0].find_all('span',class_=re.compile('^red'))
        for alert in alertItems:
          alerts.append( alert.text )
  
      route = row.find_all("td", class_="route")[0]
      rem_route = route.find(class_="bold")

      trainInfo = {
        "trainDate" : 'TID-'+ str( l_day ),
        "trainTime" : 'TIT-'+ row.find_all("td", class_="time")[0].contents[0],
        #BUG: "trainName" : 'TIN-'+ row.find_all("td", class_="train")[-1].a.contents[0].replace('\n', ''),
        "trainName" : 'TIN-'+ row.find_all("td", class_="train")[-1].a.text.replace('\n', ''),
        "trainLink" : 'TIL-'+ row.find_all("td", class_="train")[-1].a.get('href'),
        "trainPlatform" : 'TIP-'+str(platform_int),
        "trainEnd" : 'TIRE-' + rem_route.extract().text.replace('\n', ''),
        "trainRoute" : 'TIR-'+ route.text.replace('\n', ''),
        "trainActual" : 'TA-' + statusActual,
        "trainDirection" : 'TIM-'+direction,
        "stationCode" : 'TSC-'+station_code,
        "stationId" : 'TSI-'+station_id_str,
        "alerts" : 'TAA-' + '@@'.join(alerts)
      }
      log.debug( 'RESULT_ROW ' +  '|'.join( trainInfo.values() ) )
    log.debug( 'END_PARSE_URL RESULT_ROWS_OK'   )
    return 1
  else:
    log.debug( 'END_PARSE_URL RESULT_ROWS_NULL'  )
    return 0


def mainTask( dir_data, station_number_str, station_name ):
  global log
  INTERVAL_MIN = 1 #por minuto
  DIRECTIONS = ["arr" , "dep"]
  WAIT_TIME = INTERVAL_MIN * 60
  HOUR_DIVISION = 60/INTERVAL_MIN
  today = dt.datetime.today()
  TODAY = today.strftime('%d.%m.%y')
  TODAY_NAME = today.strftime('%y.%m.%d')

  time_str_full =  today.strftime('%H')  + ":00"
  start_time =  time_str_full

  log = logging.getLogger()
  log.setLevel(logging.DEBUG)

  fh = logging.FileHandler( filename= dir_data )
  fh.setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    fmt='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
  )
  fh.setFormatter(formatter)
  log.addHandler(fh)

  station_url_code = quote( station_name + "#" + station_number_str , safe='')

  sel_direct = DIRECTIONS[0]

  log.info('ROUTINE_STARTS')
  log.info('BASE_URL-' + 'https://reiseauskunft.bahn.de' + " DATE-" + TODAY + " STATION-'" + station_name + "' NUM-" + station_number_str )
  log.info('CAPTURE_PERIOD each ' + str(INTERVAL_MIN) + ' minute/s')

  #DEBUG: rr = getTravels( station_url_code , now_time , TODAY , sel_direct )

  RUN = True

  while RUN :
    # One hour loop
    for t in range( HOUR_DIVISION ):
      rr = getTravels( station_url_code, station_number_str, time_str_full, TODAY, DIRECTIONS[0] )
      rr = getTravels( station_url_code, station_number_str, time_str_full, TODAY, DIRECTIONS[1] )
      log.warning('SLEEP ' + time_str_full)
      time.sleep(WAIT_TIME)
    last_time = time_str_full
    today = dt.datetime.today()
    time_str_full = today.strftime('%H') + ":00"
    log.warning('CHANGE_HOUR ' + time_str_full)
    if last_time == '23:00' and time_str_full  == '00:00':
      log.info('ROUTINE_ENDS')
      RUN = False


if __name__ == '__main__':

  TODAY_NAME = today.strftime('%y.%m.%d')

  # args = sys.argv[1:]
  # params = { }
  # for arg in args:
  #   param = arg.split("=")
  #   argKey = param[0]
  #   argValue = str( param[1] )
  #   params[ argKey ]= argValue


  #STEP: modify version?
  configVersion = config['version']
  
  stationNumberAsStr = str( config['params']['station_number'])
  stationName = config['params']['station_name'].encode('utf-8')

  #STEP: output-file

  outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
  outputFileName = config['target']['file'].replace("$STATION$", u''+stationName ).replace("$DATE$", str( TODAY_NAME ) )
  outputFilePath = outputPath + outputFileName

  # create output folder
  if not os.path.exists( outputPath ):
    os.makedirs( outputPath )

  mainTask( outputFilePath, stationNumberAsStr, stationName )