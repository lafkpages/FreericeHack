from Freerice import Freerice   
from time import sleep          # To wait 
import socket                   # To get your IP
import threading                # To do multiple threads
import sys, getopt              # For user params


# CONFIG
user    = '14cd5145-e13c-40fe-aad0-7a2bfb31b2f1'   # user ID (can be found in LocalStorage > user > uuid)
log     = True                                     # logging to terminal enabled/disabled
log_tcs = 14                                       # log table column size
secs    = False                                    # time to wait between question
fsuv    = 6                                        # exit code for freerice servers unavailable
usrc    = 0                                        # exit code for user control C
threads = 2

# User arguments (they override the previous CONFIG variables)
if len(sys.argv) < 2:
  print("No arguments passed.")
else:
  try: 
    _opts, _args = getopt.getopt(sys.argv[1:], "t:hu:", "threads no-log help user=")   
  except getopt.GetoptError: 
    print(sys.argv[1:])
    print("Argument parsing error.")
    quit()

  for opt, arg in _opts:
    if opt in ['-h', '--help']:
      print("Usage: \nRequester.py [-h --help] \nRequester.py [-u --user your_user_id] \n")
      quit()
    elif opt in ['-u', '--user']: 
      user = arg
    elif opt in ['--no-log']: 
      log = False
    elif opt in ['-t', '--threads']:
      threads = int(arg)

# Define the hack class with your user id
freerice = Freerice(user) # Pass your user ID

def get_local_ip():
  hostname = socket.gethostname()
  ip       = socket.gethostbyname(hostname)

  return ip

def get_external_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("1.1.1.1", 80))
  ip_addr = s.getsockname()[0]
  s.close()
  return ip_addr

def get_network_ip():
  ip_addr = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
  if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
  s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET,
  socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

  return ip_addr

def FSUV():
  global fsuv

  print('Freerice servers are unavailable. Try changing your IP (via VPN)')
  print('Your current IPs:')

  ips = [get_local_ip(), get_external_ip(), get_network_ip()]
  for ip in ips:
    sleep(0.1)
    print('  - ' + ip)
  
  quit(fsuv)

def USRC():
  global usrc

  print('\r\n\nUser controlled C')
  quit(usrc)

def MainHack(log=False):
  try:
    global freerice

    # Create a new game
    last = freerice.newGame()

    while True:
      # Logs
      if log and not (last.rice_total == 0 or last.rice_total == ''):
        log_data = ['  You', '  ' + str(last.rice_total), '  ' + str(last.streak), '  ' + str(freerice.n_games)]
        log_data_formatted = '|'.join(str(x).ljust(log_tcs) for x in log_data)

        print(log_data_formatted, end='')

      if last.error or len(last.question_txt) < 2:
        # If error is 'JSON decode error' => Freerice servers unavailable
        if last.error_id == 2:
          FSUV()
          break
        else:
          last = freerice.newGame()
      
      try:
        ans = str(eval(last.question_txt.replace('x', '*')))

        last = freerice.submitAnswer(last.question_id, ans)
      except SyntaxError: # Syntax error in eval()
        pass

      if type(secs) == type(0):
        sleep(secs)

      print('\r', end='')
  except KeyboardInterrupt:
    USRC()

print('Threads: ' + str(threads))

print('    User      |  Total rice  |    Streak    |Games created ')
print('--------------|--------------|--------------|--------------')

_threads = []
if threads > 1:
  for i in range(threads - 1):
    _threads.append(threading.Thread(target=MainHack, daemon=True))
    _threads[i].start()
  
  MainHack(log)
else:
  MainHack(log)