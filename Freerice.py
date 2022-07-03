import requests as r
from requests.exceptions import ConnectTimeout
try:
  from torpy.http.requests import do_request as tor_request
  from torpy.documents.network_status import FetchDescriptorError
except ImportError:
  print('The TorPy library could not be found.\nPlease install it to use Tor with \'pip3 install torpy\' or \'python3 -m pip install torpy\'.')
import json
import logging

'''
  Error IDs | Description
------------------------------------
   1        | JSON decode error
   2        | 'rice_total' KeyError
'''

logging.basicConfig(level=logging.CRITICAL)

DEFAULT_TIMEOUT = 5

class Data:
  def __init__(self):
    '''
    The Data class is used for parsing responses from the Freerice API
    '''
    
    self.error      = False
    self.error_id   = 0
    self.error_info = []

    self.game = ''

    self.name = ''
    self.rank = 0
    self.avtr = ''

    self.members = []

    self.rice_total = 0
    self.streak     = 0

    self.question_id  = ''
    self.question_txt = ''

class Freerice:
  # ============== URLS ==============
  new_game_url   = 'https://engine.freerice.com/games?lang=en'
  new_game_mth   = 'POST'

  answer_url     = '' # will be autocompleted by newGame()
  answer_url2    = '/answer?lang=en'
  answer_mth     = 'PATCH'

  stats_url      = 'https://engine.freerice.com/gamestats/rice-totals'
  stats_mth      = 'GET' # or 'OPTIONS'

  ads_url        = 'https://accounts.freerice.com/api/ads'
  ads_mth        = 'GET' # or 'OPTIONS'

  favicon_url    = 'https://freerice.com/favicon.ico'
  favicon_mth    = 'GET'

  eyecatcher_url = 'https://accounts.freerice.com/api/eye-catcher?_lang=en'
  eyecatcher_mth = 'OPTIONS'

  badges_url     = 'https://engine.freerice.com/badges/?limit=50&lang=en'
  badges_mth     = 'GET'

  announce_url   = 'https://accounts.freerice.com/api/announcements?lang=en'
  announce_mth   = 'GET'

  levels_url     = 'https://engine.freerice.com/levels?lang=en'
  levels_mth     = 'GET' # or 'OPTIONS'

  manifest_url   = 'https://freerice.com/manifest.json'
  manifest_mth   = 'GET'

  user_url       = 'https://engine.freerice.com/users/'
  user_mth       = 'GET'

  group_url      = 'https://engine.freerice.com/groups/'
  group_mth      = 'GET'

  ldbd_usrs_url  = 'https://engine.freerice.com/users?current=' # page number
  ldbd_usrs_url2 = '&limit=50&_format=json'
  ldbd_usrs_mthd = 'GET'

  ldbd_grps_url  = 'https://engine.freerice.com/groups?current=' # page number
  ldbd_grps_url2 = '&limit=50&_format=json'
  ldbd_grps_mthd = 'GET'

  prfl_usrs_url  = 'https://accounts.freerice.com/public/users?uuids=' # comma-sepparated user IDs
  prfl_usrs_url2 = '&_format=json'
  prfl_usrs_mthd = 'GET'

  prfl_grps_url  = 'https://accounts.freerice.com/public/groups?uuids=' # comma-sepparated user IDs
  prfl_grps_url2 = '&_format=json'
  prfl_grps_mthd = 'GET'
  # ============ END URLS ============

  def __init__(self, user_id, timeout=DEFAULT_TIMEOUT):
    '''
    The main hack class to use
    '''
    
    self.user       = user_id # user ID
    self.game       = ''      # game ID
    self.n_games    = 0       # number of games created
    self.init_level = 1       # level to start at
    self.timeout    = timeout

    self.default_headers = {
      'Content-type': 'application/json',
      'Origin'      : 'https://freerice.com',
      'User-Agent'  : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
      'Accept'      : 'application/vnd.api+json;version=2'
    }

    self.tor        = False
    self.tor_onions = 3                 # number of Tor layers

    self.last_ret_v = None

    self.categories = {
      'multiplication-table': '66f2a9aa-bac2-5919-997d-2d17825c1837'
    }
  
  def __getitem__(self, item):
    return getattr(self, item)

  def newGame(self):
    data = {
      'category': self.categories['multiplication-table'],
      'level': self.init_level,
      'user': self.user
    }

    req = r.request(
      self.new_game_mth,
      self.new_game_url,
      json=data,
      headers=self.default_headers,
      timeout=self.timeout
    )

    ret = Data()

    try:
      data = req.json()
    except json.JSONDecodeError:
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
      'answer': 'a' + str(A),
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
      req = r.request(
        self.answer_mth,
        url,
        json=data,
        headers=self.default_headers,
        timeout=self.timeout
      )

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
  
  @classmethod
  def getUserStats(cls, user=None, group=False):
    # if user is None:
    #   user = cls.user

    URL = ''
    if group:
      URL = cls.group_url + user
    else:
      URL = cls.user_url + user

    req = r.request(
      cls.group_mth if group else cls.user_mth,
      URL,
      timeout=DEFAULT_TIMEOUT
    )

    data = Data()
    json = {}

    try:
      json = req.json()
    except:
      data.error = True

      cls.last_ret_v = data

      return data

    data.rice_total = json['data']['attributes']['rice']
    data.rank       = json['data']['attributes']['rank']
    if group:
      data.members = json['data']['attributes']['members']
    
    return data
  
  @classmethod
  def getUserProfile(cls, user, group=False):
    # if user is None:
    #   user = cls.user

    URL = ''
    if group:
      URL = cls.prfl_grps_url + user + cls.prfl_grps_url2
    else:
      URL = cls.prfl_usrs_url + user + cls.prfl_usrs_url2

    req  = r.request(
      cls.prfl_grps_mthd if group else cls.prfl_usrs_mthd,
      URL,
      timeout=DEFAULT_TIMEOUT
    )
    json = {}
    data = Data()
    
    '''
    {
      "...user-id...":{
        "uuid": "...user-id...",
        "name": "...user-name...",
        "avatar": "avatar-..."
      }
    }
    '''

    try:
      json = req.json()
    except:
      data.error = True

      cls.last_ret_v = data

      return data

    fk = user
    
    try:
      data.name = json[fk]['name']
    except KeyError:
      fk += cls.prfl_usrs_url2
      data.name = json[fk]['name']
    data.avtr = json[fk]['avatar']

    return data
  
  @classmethod
  def getAllUsers(cls, groups=False, get_profiles=False):
    # data = {}

    url = ''
    if groups:
      url = cls.ldbd_grps_url + '1' + cls.ldbd_grps_url2
    else:
      url = cls.ldbd_usrs_url + '1' + cls.ldbd_usrs_url2
    page = 1

    while True:
      req  = r.request(
        cls.ldbd_usrs_mthd,
        url,
        timeout=DEFAULT_TIMEOUT
      )
      json = req.json()

      # data.update(json)
      users       = json['data']
      page        = json['meta']['pagination']['current_page']
      total_pages = json['meta']['pagination']['total_pages']

      profiles      = {}
      profiles_list = []

      if get_profiles:
        uuids = list(
          map(
            lambda user: user['id'],
            users
          )
        )
        uuids = ','.join(uuids)
        
        url2 = ''
        if groups:
          url2 = cls.prfl_grps_url + uuids + cls.prfl_grps_url2
        else:
          url2 = cls.prfl_usrs_url + uuids + cls.prfl_usrs_url2

        req2 = r.request(
          cls.prfl_grps_mthd if groups else cls.prfl_usrs_mthd,
          url2,
          timeout=DEFAULT_TIMEOUT
        )

        profiles = req2.json()

        for user_id in profiles:
          user_ = profiles[user_id]

          data_ = Data()

          data_.name = user_['name']
          data_.avtr = user_['avatar']

          profiles_list.append(data_)

      for user in users:
        if get_profiles:
          yield user, page, total_pages, profiles[user['id']]
        else:
          yield user, page, total_pages, {}

      try:
        #print('Old URL:', url)

        #url = json['links']['next']# + cls.ldbd_grps_url2
        page += 1
        if groups:
          url = cls.ldbd_grps_url + str(page) + cls.ldbd_grps_url2
        else:
          url = cls.ldbd_usrs_url + str(page) + cls.ldbd_usrs_url2

        #print('New URL:', url)
      except KeyError:
        # No more data
        break
    
    # return data