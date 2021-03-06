import ConfigParser
import requests
import json
from pprint import pprint
import io


import psycopg2
import sys

class FacebookDataIngestSource:
  """Ingest data from Facebook"""
  
  def __init__(self, config, term):
    self.config = config
    self.term = term
    self.page_id = []
    self.page_name = []
    self.video_json = []
  
  def __iter__(self):

#### Retrieve the consumer key and secret
    consumer_key = 210412405693448
    consumer_secret = '177fe950d29470dcee451a384636b787'
#### Define url for http request for access token
    auth_url = 'https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(consumer_key,consumer_secret)
#### Get authorization token from Facebook and store it for future use
    token_req = requests.get(auth_url)
    self.access_token = token_req.text.split('=')[1]

#### Retrieve term to search    
    page_search_term = self.term

#### Request id for pages associated to search term    
    page_search_request='page&fields=id,name'

#### Define url for http request to get pages id associated to search term    
    page_search_url = 'https://graph.facebook.com/search?q=%s&type=%s&access_token=%s'%(page_search_term, page_search_request, self.access_token)

#### Get a list of pages id associated to search term    
    self.page_search = requests.get(page_search_url)
    self.page_json = self.page_search.json()
#### Initialize page index to zero 
    self.page_index = 0
    self.index = 0
    return self

  def next(self):
#### Request all videos associated to each of the pages found to be relevant for the search
    
    if self.page_index < len(self.page_json['data']):

      self.page_id = self.page_json['data'][self.page_index]['id']
      self.page_name = self.page_json['data'][self.page_index]['name']
      self.page_index = self.page_index + 1
      video_url = 'https://graph.facebook.com/v2.5/%s/videos?&fields=permalink_url,sharedposts,likes,comments&access_token=%s'%(self.page_id,self.access_token)
      video_search = requests.get(video_url)
      self.video_json = video_search.json()
 ##     with io.open('/data/w205/shoot2top/w205-data-ingest/results.txt', 'a',encoding='utf8') as f:
 ##         f.write("%s\n %s\n %s\n" %(page_id,page_name, video_json))
    # Log the count - just t    
      
    else:
      raise StopIteration()


    
    return self
    

term = str(sys.argv)

ven = FacebookDataIngestSource('.w205-data-ingest.cfg', 'Venezuela')

for i in ven:
    pprint (i.page_id)
    pprint (i.page_name)
    pprint (i.video_json[data][comments][created_time])
    print'_____________________'
    





