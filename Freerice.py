import requests as r

class Freerice:
  def __init__(self, user_id):
    self.user = user_id
    self.game = ''

    self.new_game_url = 'https://engine.freerice.com/games'
    self.new_game_mth = 'POST'

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
      'level': 2,
      'user': self.user
    }

    req = r.request(self.new_game_mth, self.new_game_url, json=data, headers=headers)

    data = req.json()
    game = data['data']['id']

    print(data)
    print(game)

    return data