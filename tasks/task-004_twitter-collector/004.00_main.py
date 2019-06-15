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

import requests
from requests.utils import quote
import urllib2
from bs4 import BeautifulSoup
# import logging
# import re
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
# from connect import *

CONFIG_FILE_NAME = '004.00_config.yml'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME, 'r'))
#yaml.dump( config, file( DIR_TASK + '\\config.yml', 'w') )

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

# _____________________________________________________________________________________ INIT

today = dt.datetime.now().strftime("%Y-%m-%d--%H-%M") 

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

class StdOutListener(StreamListener):

  def __init__(self):
    self.outputFullFile = ''

  def on_data(self, data):
    #print self.outputFullFile
    with open( self.outputFullFile , "a") as myfile:
      myfile.write(data)
      #print data
      return True

  def on_error(self, status):
    print status



if __name__ == '__main__':
  
  #STEP: output-file
  outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
  outputFilePath = outputPath + config['target']['file'].replace("$TIME$", str( today ) ).replace("$UNIQUE$", str( config['params']['unique'] ) )

  #COM: create output folder
  if not os.path.exists( outputPath ):
    os.makedirs( outputPath )


  #STEP: CAPTURE TWEETS
  #COM: Access Twitter APP
  twitterSecret = yaml.load( stream = file( DIR_TASK + '\connect.secret.yml', 'r'))

  consumer_key = twitterSecret['consumer_key']
  consumer_secret = twitterSecret['consumer_secret']
  access_token = twitterSecret['access_token']
  access_token_secret = twitterSecret['access_token_secret']

  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)

  #COM: capture parameters
  query_max_tweets= config['params']['query_max_tweets'] 
  query_words = config['params']['query_words'] 
  query_lang = config['params']['query_lang'] 

  #COM: Capture stream method 1
  listener = StdOutListener()
  listener.outputFullFile= outputFilePath
  stream = Stream( auth, listener = listener )
  stream.filter( track=query_words.split(' OR ') ) # [ '#Vandalismusschaeden','#Verspaetungen','@DB_Info ']

  # #COM: Capture stream method 2
  # searched_tweets = [ status._json for status in tweepy.Cursor( api.search, q=query_words, lang=query_lang ).items(query_max_tweets) ]
  # #json_strings = [json.dumps(json_obj) for json_obj in searched_tweets]
  # tweets = [searched_tweets]
  # with open( outputFilePath , 'a') as outfile:
  #   json.dump( tweets , outfile , indent=2, ensure_ascii=True)