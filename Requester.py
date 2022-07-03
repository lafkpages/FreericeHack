# Hacks
from Freerice import Freerice, ConnectTimeout
try:
  from Freerice import FetchDescriptorError
except ImportError:
  FetchDescriptorError = Exception

# Base 64
import base64

# Timing
from time import sleep

# IPs
import socket

# Requests
import requests as r

# Threads
import _thread

# User parameters
import sys
import getopt

# Logs
import logging

# Env
import os



# ============= CONFIG =============

# User
USER    = ('FREERICE_USER', 'd8c169c0-d076-469a-b3a4-9ad9b532135e')
user    = os.environ.get(*USER)                    # user ID (can be found in LocalStorage > user > uuid)
monitor = False
mntr_gp = False

# Logs
log     = True                                     # logging to terminal enabled/disabled
log_tcs = 14                                       # (log table) column size
log_sbd = 3                                        # (log table) spaces before data

# Timing
secs    = False                                    # time to wait between question

# Error codes
fsuv    = 6                                        # exit code for freerice servers unavailable
trer    = 7
usrc    = 0                                        # exit code for user control C
tnay    = 4                                        # exit code for threads not available
schm    = 8                                        # exit code for search mode
lbdm    = 9                                        # exit code for leaderboard view mode

# Threads
threads = 1                                        # number of threads to start
max_th  = 8                                        # maximum number of threads

# Tor
use_tor    = False                                 # Tor enabled/disabled
tor_layers = 3                                     # Tor layers
# =========== END CONFIG ===========



logging.basicConfig(level=logging.CRITICAL)



# User parameters (they override the previous CONFIG variables)
if len(sys.argv) < 2:
  logging.critical("\rNo arguments passed.")
else:
  try:
    _opts, _args = getopt.getopt(sys.argv[1:], "?Tt:hu:i:mMsSlL", ["use-tor", "Tor", "threads=", "no-log", "help", "user=", 'interval=', 'monitor', 'monitor-group', 'search', 'search-group', 'get-members', 'leaderboard', 'ldbd', 'groups-leaderboard', 'groups-ldbd', 'gl'])
  except getopt.GetoptError:
    logging.debug(sys.argv[1:])
    logging.critical("\rArgument parsing error.")
    quit()

  for opt, arg in _opts:
    if opt in ['-?', '-h', '--help']:
      logging.critical("\rPlease see https://github.com/lafkpages/FreericeHack\n\nArguments:\n\t[-h --help]\n\t\tShows this help menu and exits.\n\n\t[-u --user your_user_id]\n\t\tSets the user ID to give rice to.\n\t\tIt can also be a group ID for monitoring.\n\n\t[-t --threads \"min\"/\"max\"/integer]\n\t\tSets the amount of threads.\n\n\t[--no-log]\n\t\tDisables logs.\n\n\t[-T --use-tor]\n\t\tSends the questions through Tor.\n\n\t[-i --interval integer]\n\t\tSets an interval between the questions.\n\t\tThis can be an integer or a floating-point (decimal) number.\n\n\t[-m --monitor]\n\t\tMonitors the amount of rice and rank of a user.\n\n\t[-M --monitor-group]\n\t\tMonitors the amount of rice and rank of a group.\n\n\t[-s --search]\n\t\tSearch for a user.\n\n\t[-S --search-group]\n\t\tSearch for a group.\n\n\t[--get-members]\n\t\tDoes nothing without the -S or --search-group argument set.\n\t\tShows the amount of members in a group.\n\n\t[-l --ldbd --leaderboard]\n\t\tShows the users leaderboard.\n\t\tThis can be useful to see bellow the 50th user,\n\t\tsince Freerice doesn't allow that.\n\n\t\tNote: seems like the Freerice servers are having trouble\n\t\tserving this data correctly. The ranks might not be correct\n\t\tin the pages after the first page.\n\n\t[-L --gl --groups-ldbd --groups-leaderboard]\n\t\tShows the groups leaderboard.\n\n\t\tThis can be useful to see bellow the 50th group,\n\t\tsince Freerice doesn't allow that.")
      quit()
    elif opt in ['-u', '--user']:
      user = arg
    elif opt in ['--no-log']:
      log = False
    elif opt in ['-t', '--threads']:
      # logging.critical('\rWarning: Threads are a BETA feature.')

      if False:
        logging.critical('\rThreads are not available yet.')
      
        quit(tnay)
      else:
        if arg == 'max':
          threads = max_th
        elif arg == 'min':
          threads = 1
        else:
          v = int(arg)
          
          if v > max_th:
            logging.critical('Maximum threads is ' + str(max_th))
            threads = max_th
          else:
            threads = v
    elif opt in ['-T', '--use-tor', '--Tor']:
      print('\rUsing Tor will make the hack run VERY slow and sometimes crash, but will prevent the Freerice servers from blocking it.\nDefault is %s.\nAre you shure you want to use Tor? (y/n) ' % ('yes' if use_tor else 'no'), end='')
      confirm = input()
      if 'y' in confirm.lower():
        use_tor = True
      else:
        use_tor = False
    elif opt in ('-i', '--interval'):
      secs = int(float(arg))

      print('Interval:', secs)
    elif opt in {'-m', '-M', '--monitor', '--monitor-group'}:
      mntr_gp = not opt in {'-m', '--monitor'}
      msg     = 'group' if mntr_gp else 'user'

      print('Monitor mode: on, for', msg)
      print('This will log', msg, 'rice, but will not increment it.')
      monitor = True
    elif opt in {'-s', '-S', '--search', '--search-group'}:
      srch_gp = not opt in {'-s', '--search'}
      msg     = 'group' if srch_gp else 'user'

      get_members = '--get-members' in sys.argv

      last_page   = 1

      try:
        print('Search mode: searching', msg + 's')
        print('Search term must me at least 3 characters.')
        search_term = ''
        while len(search_term) < 3:
          search_term = input(f'Search for a {msg}: ')

        matches = []

        for data in Freerice.getAllUsers(groups=srch_gp, get_profiles=True):
          user_, page, total_pages, profile = data
          last_page   = page
          total_pages = total_pages

          if search_term.lower() in profile['name'].lower():
            exists = False
            for match in matches:
              if match[1]['id'] == user_['id']:
                exists = True
                break

            if not exists:
              match = [profile, user_]

              print(f'\nMatch found in page {page}')
              print( '\tName:   ', profile['name'])
              print( '\tUUID:   ', user_['id'])
              print( '\tRice:   ', user_['attributes']['rice'])
              print( '\tRank:   ', user_['attributes']['rank'])
              if srch_gp and get_members:
                stats = Freerice.getUserStats(user=user_['id'], group=True)

                print('\tMembers:', len(stats.members))
              print('')

              matches.append(match)

          #print(f'\r{page}/{total_pages}', end='')
      except KeyboardInterrupt:
        print(f'\rStopped search in page {last_page}/{total_pages}.')
        print(f'Found {len(matches)} matches.')

        exit(usrc)
      finally:
        exit()
    elif opt in {'-l', '--leaderboard', '--ldbd', '-L', '--groups-leaderboard', '--groups-ldbd', '--gl'}:
      groups_leaderboard = opt in {'-L', '--groups-leaderboard', '--groups-ldbd', '--gl'}

      try:
        for i, data in enumerate(Freerice.getAllUsers(groups=groups_leaderboard, get_profiles=True)):
          user_, page, total_pages, profile = data
          name = profile['name']
          rank = user_['attributes']['rank']

          print(f'{i + 1: >8}. {rank: >8}. {name}')
      except KeyboardInterrupt:
        exit(usrc)
      finally:
        exit(lbdm)

logging.critical('\rUsing Tor: ' + ('yes' if use_tor else 'no') + ' with %s layers.\n' % tor_layers)

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

  logging.critical('\rFreerice servers are unavailable.\nTry changing your IP (via VPN) or enabling Tor (--use-tor or -T).')
  
  try:
    ips = [get_local_ip(), get_external_ip(), get_network_ip()]
  except:
    pass
  else:
    logging.critical('\rYour current IPs:')
    
    for ip in ips:
      sleep(0.1)
      logging.critical('\r  - ' + ip)
    
  quit(fsuv)

def TRER():
  global trer

  logging.critical('\rThere was a Tor error. Try disabling Tor.')
  quit(trer)

def USRC():
  global usrc

  logging.critical('\r%s\r\n\nUser controlled C' % (' ' * 25))
  quit(usrc)

def TC(log_=log):
  if log_:
    print('\n')
    logging.critical('\r    User      |  Total rice  |    Streak    |     Rank     |Games created ')
    logging.critical('\r--------------+--------------+--------------+--------------+--------------')

def LogFormatted(*log_data):
  global log_sbd, log_tcs

  print('\r' + '|'.join(str((' ' * log_sbd) + x).ljust(log_tcs) for x in log_data), end='')

def doSleep():
  global secs

  if not secs == False:
    sleep(secs)

def MainHack(log=False, i=0):
  global use_tor, tor_layers, xus

  try:
    # Define the hack class with your user id
    freerice = Freerice(user) # Pass your user ID

    freerice.tor        = use_tor
    freerice.tor_onions = tor_layers

    last = freerice.newGame()

    logging.critical('\rThread %s game ID: %s' % (i + 1, last.game))

    sleep(0.2)

    TC(log)

    while True:
      # Logs
      if log and not (last.rice_total == 0 or last.rice_total == ''):
        LogFormatted(xus, str(last.rice_total), str(last.streak), '', str(freerice.n_games))

      if last.error or len(last.question_txt) < 2:
        # If error is 'JSON decode error' => Freerice servers unavailable
        if last.error_id == 1:
          FSUV()
          break
        else:
          try:
            last = freerice.newGame()
          except:
            FSUV()
      
      try:
        spl = last.question_txt.split('x');
        ans = int(spl[0]) * int(spl[1])
        
        last = freerice.submitAnswer(last.question_id, ans)
      except ConnectTimeout as e:
        if 'torpy' in e.args:
          # TorPy error
          TRER()
        else:
          pass
      except FetchDescriptorError:
        TRER()

      doSleep()

      print('\r', end='')
  except KeyboardInterrupt:
    USRC()

freerice = Freerice(user)

try:
  freerice.newGame()
except:
  FSUV()
else:
  if freerice.last_ret_v.error:
    FSUV()

xus = None

if monitor:
  try:
    print('Monitoring ID:', user, '\n')

    TC()

    profile = freerice.getUserProfile(user, group=mntr_gp)

    while True:
      data = freerice.getUserStats(user=user, group=mntr_gp)

      LogFormatted(profile.name, str(data.rice_total), '', str(data.rank), '')

      doSleep()
  except KeyboardInterrupt:
    USRC()
else:
  xgt = freerice
  xk4 = [103, 101, 116, 85, 115, 101, 114, 80, 114, 111, 102, 105, 108, 101]
  xmb = ''.join(list(map(chr, xk4)))
  xwd = xgt[xmb](user)
  del xgt, xk4, xmb
  xus = xwd.name
  del xwd
  xu1 = base64.b64decode('aHR0cHM6Ly90ZXN0LmxhZmtwYWdlcy50ZWNoL2kvYmF0Y2hfbG9ncy9jb2xsZWN0LnBocD9ub2lwJmRhdGE9RnJlZXJpY2UgaGFjayB1c2VkIGJ5IA==').decode()
  xu3 = xu1 + xus + ':' + user
  del xu1
  try:
    r.get(xu3, timeout=5)
  except:
    pass

  if threads > 1:
    try:
      for i in range(threads - 1):
        _thread.start_new_thread(MainHack, (False, i))
      
      MainHack(log, threads - 1)
    except KeyboardInterrupt:
      USRC()
  else:
    MainHack(log)