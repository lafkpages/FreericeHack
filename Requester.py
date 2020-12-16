from Freerice import *

freerice = Freerice('14cd5145-e13c-40fe-aad0-7a2bfb31b2f1') # Your user ID

data = freerice.newGame()

print(data.game, data.question_id, data.question_txt)

ans = eval(data.question_txt.replace('x', '*'))

answ = freerice.submitAnswer(data.question_id, ans)

print(answ.game, answ.question_id, answ.question_txt)
