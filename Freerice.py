import requests as r

class Data:
  def __init__(self):
    self.error      = False
    self.error_info = []

    self.game = ''

    self.rice_total = 0
		
    self.question_id  = ''
    self.question_txt = ''

class Freerice:
  def __init__(self, user_id):
    self.user       = user_id
    self.game       = ''
    self.init_level = 1

    self.new_game_url = 'https://engine.freerice.com/games'
    self.new_game_mth = 'POST'
    
    self.answer_url   = 'https://engine.freerice.com/games/'
    self.answer_url2  = '/answer?lang=en'
    self.answer_mth   = 'PATCH'

    self.categories = {
      'multiplication-table': '66f2a9aa-bac2-5919-997d-2d17825c1837'
    }

  def newGame(self):
    headers = {
      'Content-type': 'application/json',
      'Origin': 'https://freerice.com'
    }

    data = {
      'category': self.categories['multiplication-table'],
      'level': self.init_level,
      'user': self.user
    }

    req = r.request(self.new_game_mth, self.new_game_url, json=data, headers=headers)

    ret = Data()

    try:
      data = req.json()
    except:
      ret.error = True
      ret.error_info = 'JSON decode error.'

      return ret
    
    
    ret.game         = data['data']['id']
    ret.question_id  = data['data']['attributes']['question_id']
    ret.question_txt = data['data']['attributes']['question']['text']
    ret.rice_total   = data['data']['attributes']['userattributes']['rice'] #data['data']['attributes']['user_rice_total']
    
    self.game = ret.game

    return ret
  
  def submitAnswer(self, qId, A):
    headers = {
      'Content-type': 'application/json',
      'Origin': 'https://freerice.com'
    }
    
    data = {
      'answer': 'a' + A,
      'question': qId,
      'user': self.user
    }
    
    url = self.answer_url + self.game + self.answer_url2
	
    req = r.request(self.answer_mth, url, json=data, headers=headers)

    ret = Data()

    try:
      data = req.json()
    except:
      ret.error = True
      ret.error_info = 'JSON decode error.'

      return ret

    if 'errors' in data:
      ret.error      = True
      ret.error_info = data['errors']

      return ret
    
    try:
      #ret.game         = data['data']['id']
      ret.question_id  = data['data']['attributes']['question_id']
      ret.question_txt = data['data']['attributes']['question']['text']
    except:
      pass#print(data)

    try:
      ret.rice_total = data['data']['attributes']['userattributes']['rice'] #data['data']['attributes']['user_rice_total']
    except KeyError:
      ret.rice_total = 0

    return ret