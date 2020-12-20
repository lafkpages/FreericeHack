# Hacks
from Freerice import Freerice  

# Timing
from time import sleep

# IPs
import socket

# Threading
import threading

# User parameters
import sys
import getopt



# ============= CONFIG =============
# User
user    = '14cd5145-e13c-40fe-aad0-7a2bfb31b2f1'   # user ID (can be found in LocalStorage > user > uuid)

# Logs
log     = True                                     # logging to terminal enabled/disabled
log_tcs = 14                                       # (log table) column size
log_sbd = 3                                        # (log table) spaces before data

# Timing
secs    = False                                    # time to wait between question

# Error codes
fsuv    = 6                                        # exit code for freerice servers unavailable
usrc    = 0                                        # exit code for user control C

# Threads
threads = 1                                        # number of threads to start
max_th  = 4                                        # maximum number of threads
daemon  = True                                     # daemon enabled/disabled

# Tor
use_tor    = False                                 # Tor enabled/disabled
tor_layers = 3                                     # Tor layers
# =========== END CONFIG ===========



# User parameters (they override the previous CONFIG variables)
if len(sys.argv) < 2:
  print("No arguments passed.")
else:
  try: 
    _opts, _args = getopt.getopt(sys.argv[1:], "Tt:hu:", "use-tor threads no-log help user=")   
  except getopt.GetoptError: 
    print(sys.argv[1:])
    print("Argument parsing error.")
    quit()

  for opt, arg in _opts:
    if opt in ['-h', '--help']:
      print("Usage: \n  Requester.py [-h --help] \n  Requester.py [-u --user your_user_id] \n  Requester.py [-t --threads min/max/a_integer] \n  Requester.py [--no-log] \n  Requester.py [-T --use-tor]")
      quit()
    elif opt in ['-u', '--user']: 
      user = arg
    elif opt in ['--no-log']: 
      log = False
    elif opt in ['-t', '--threads']:
      if arg == 'max':
        threads = max_th
      elif arg == 'min':
        threads = 1
      else:
        v = int(arg)
        
        if v > max_th:
          print('Maximum threads is ' + str(max_th))
          threads = max_th
        else:
          threads = v
    elif opt in ['-T', '--use-tor']:
      use_tor = True

# Define the hack class with your user id
freerice = Freerice(user) # Pass your user ID

freerice.tor        = use_tor
freerice.tor_onions = tor_layers

print('Using Tor: ' + ('yes' if use_tor else 'no') + ' with %s layers.' % tor_layers)

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

def TC(log_=log):
  if log_:
    print('    User      |  Total rice  |    Streak    |Games created ')
    print('--------------|--------------|--------------|--------------')

def MainHack(log=False, i=0):
  try:
    global freerice

    # Create a new game if none created
    last = False
    '''
    if freerice.game in [[], {}, '', 0, None, False]:
      last = freerice.newGame()
    else:'''
    last = freerice.last_ret_v

    print('Thread %s game ID: %s' % (i + 1, last.game))

    sleep(0.2)

    TC(log)

    while True:
      # Logs
      if log and not (last.rice_total == 0 or last.rice_total == ''):
        log_data = ['You', str(last.rice_total), str(last.streak), str(freerice.n_games)]
        log_data_formatted = '|'.join(str((' ' * log_sbd) + x).ljust(log_tcs) for x in log_data)

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

freerice.newGame()

if threads > 1:
  try:
    for i in range(threads - 1):
      (threading.Thread(target=MainHack, args=(False, i), daemon=daemon)).start()

      #print('Threads started: ' + str(i + 1), end='\r')  

      sleep(0.5)
    
    #print('\nStarting thread %s in main program.' % threads)
    
    MainHack(log, threads - 1)
  except KeyboardInterrupt:
    USRC()
else:
  MainHack(log)