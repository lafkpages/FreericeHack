import requests as r
from requests.exceptions import ConnectTimeout
try:
  import torpy
  from torpy.http.requests import do_request as tor_request
  from torpy.documents.network_status import FetchDescriptorError
except ImportError:
  print('The TorPy library could not be found. \nPlease install it to use Tor with \'pip3 install torpy\' or \'python3 -m pip install torpy\'.')
import json
import logging

'''
  Error IDs | Description
------------------------------------
   1        | JSON decode error
   2        | 'rice_total' KeyError
'''

logging.basicConfig(level=logging.CRITICAL)

class Data:
  def __init__(self):
    self.error      = False
    self.error_id   = 0
    self.error_info = []

    self.game = ''

    self.rice_total = 0
    self.streak     = 0
		
    self.question_id  = ''
    self.question_txt = ''

class Freerice:
  def __init__(self, user_id):
    self.user       = user_id # user ID
    self.game       = ''      # game ID
    self.n_games    = 0       # number of games created
    self.init_level = 1       # level to start at

    self.default_headers = {
      'Content-type': 'application/json',
      'Origin'      : 'https://freerice.com',
      'User-Agent'  : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
      'Accept'      : 'application/vnd.api+json;version=2'
    }

    # ============== URLS ==============
    self.user_url       = 'https://accounts.freerice.com/users/'
    self.user_url2      = '?_format=json'
    self.user_mth       = 'GET'

    self.new_game_url   = 'https://engine.freerice.com/games?lang=en'
    self.new_game_mth   = 'POST'

    self.answer_url     = '' # will be autocompleted by newGame()
    self.answer_url2    = '/answer?lang=en'
    self.answer_mth     = 'PATCH'

    self.stats_url      = 'https://engine.freerice.com/gamestats/rice-totals'
    self.stats_mth      = 'GET' # or 'OPTIONS'

    self.ads_url        = 'https://accounts.freerice.com/api/ads'
    self.ads_mth        = 'GET' # or 'OPTIONS'

    self.favicon_url    = 'https://freerice.com/favicon.ico'
    self.favicon_mth    = 'GET'

    self.eyecatcher_url = 'https://accounts.freerice.com/api/eye-catcher?_lang=en'
    self.eyecatcher_mth = 'OPTIONS'

    self.badges_url     = 'https://engine.freerice.com/badges/?limit=50&lang=en'
    self.badges_mth     = 'GET'

    self.announce_url   = 'https://accounts.freerice.com/api/announcements?lang=en'
    self.announce_mth   = 'GET'

    self.levels_url     = 'https://engine.freerice.com/levels?lang=en'
    self.levels_mth     = 'GET' # or 'OPTIONS'

    self.manifest_url   = 'https://freerice.com/manifest.json'
    self.manifest_mth   = 'GET'
    # ============ END URLS ============



    self.tor        = False
    try:
      self.tor_client = torpy.TorClient()
    except NameError:
      self.tor_client = None
    self.tor_onions = 3                 # number of Tor layers

    self.last_ret_v = None

    self.categories = {
      'multiplication-table': '66f2a9aa-bac2-5919-997d-2d17825c1837'
    }

  def newGame(self):
    data = {
      'category': self.categories['multiplication-table'],
      'level': self.init_level,
      'user': self.user
    }

    req = r.request(self.new_game_mth, self.new_game_url, json=data, headers=self.default_headers)

    ret = Data()

    try:
      data = req.json()
    except:
      ret.error = True
      ret.error_id = 1
      ret.error_info = 'JSON decode error.'

      self.last_ret_v = ret

      return ret

    if 'errors' in data:
      ret.error      = True
      ret.error_info = data['errors']

      self.last_ret_v = ret

      return ret
    
    self.answer_url = data['data']['links']['self']

    ret.game         = data['data']['id']
    ret.question_id  = data['data']['attributes']['question_id']
    ret.question_txt = data['data']['attributes']['question']['text']
    try:
      ret.rice_total = data['data']['attributes']['userattributes']['rice']
    except KeyError: 
      ret.rice_total = data['data']['attributes']['user_rice_total']
    
    self.game = ret.game

    self.n_games += 1

    self.last_ret_v = ret

    return ret
  
  def submitAnswer(self, qId, A):
    data = {
      'answer': 'a' + A,
      'question': qId,
      'user': self.user
    }
    
    url = self.answer_url + self.answer_url2
	
    req = False

    if self.tor:
      data = json.dumps(data)
      try:
        while True:
          try:
            req = tor_request(url, headers=self.default_headers, data=data, method=self.answer_mth, hops=self.tor_onions)
            break
          except KeyboardInterrupt:
            logging.critical("\rUser controlled C during Tor request.")
            break
      except KeyboardInterrupt:
        logging.critical('\rUser controlled C during Tor request.')
    else:
      req = r.request(self.answer_mth, url, json=data, headers=self.default_headers)

    ret = Data()

    try:
      if not self.tor:
        data = req.json()
      else:
        # Tor's request returns a string (.text), not a request object
        data = json.loads(req)
    except:
      ret.error = True
      ret.error_id = 1
      ret.error_info = 'JSON decode error.'

      self.last_ret_v = ret

      return ret

    if 'errors' in data:
      ret.error      = True
      ret.error_info = data['errors']

      self.last_ret_v = ret

      return ret
    
    try:
      ret.game         = data['data']['id']
      ret.question_id  = data['data']['attributes']['question_id']
      ret.question_txt = data['data']['attributes']['question']['text']
    except:
      pass#print(data)

    try:
      ret.streak = data['data']['attributes']['streak']
      try:
        ret.rice_total = data['data']['attributes']['userattributes']['rice']
      except KeyError:
        try:
          ret.rice_total = data['data']['attributes']['user_rice_total']
        except KeyError:
          ret.error_id = 2
          ret.rice_total = 0
    except KeyError:
      ret.error = True

    self.last_ret_v = ret

    return ret