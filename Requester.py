from Freerice import *
from time import sleep


# CONFIG
user = '14cd5145-e13c-40fe-aad0-7a2bfb31b2f1'
log  = False
secs = False
fsuv = 6      # exit code for freerice servers unavailable
ucnc = 0      # exit code for user control C

# Define the hack class with your user id
# User ID can be found in LocalStorage > user > uuid
freerice = Freerice(user) # Your user ID

# Create a new game
last = freerice.newGame()

if last.error:
  print('Freerice servers are unavailable. Try changing your IP (via VPN)')
  quit(fsuv)

try:
  while True:
    if not (last.rice_total == 0 or last.rice_total == ''):
      print(str(last.rice_total), end='')

    if log:
      print('Game ID:          ' + last.game)
      print('Total rice:       ' + str(last.rice_total))
      print('Next question ID: ' + last.question_id)
      print('Next question:    ' + last.question_txt)
      print('\n')

    if last.error:
      last = freerice.newGame()
    
    ans = str(eval(last.question_txt.replace('x', '*')))

    last = freerice.submitAnswer(last.question_id, ans)

    if type(secs) == type(0):
      sleep(secs)

    print('\r', end='')
except KeyboardInterrupt:
  print('\r\nUser controlled C')
  quit(ucnc)