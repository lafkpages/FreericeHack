from Freerice import *
from time import sleep


# CONFIG
user = '14cd5145-e13c-40fe-aad0-7a2bfb31b2f1'
log  = False
secs = 0.005

# Define the hack class with your user id
# User ID can be found in LocalStorage > user > uuid
freerice = Freerice(user) # Your user ID

# Create a new game
last = freerice.newGame()

print('Initial rice (total): ' + str(last.rice_total))

try:
  while True:
    if log:
      print('Game ID:          ' + last.game)
      print('Total rice:       ' + str(last.rice_total))
      print('Next question ID: ' + last.question_id)
      print('Next question:    ' + last.question_txt)
      print('\n')

    ans = str(eval(last.question_txt.replace('x', '*')))

    last = freerice.submitAnswer(last.question_id, ans)

    sleep(secs)
except KeyboardInterrupt:
  print('User controlled C')
  print('Final rice (total): ' + str(last.rice_total))
  quit()