__author__ = "seanwlk"
__copyright__ = "Copyright 2018"
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "seanwlk"
__status__ = "Beta"

import sys
import time
import signal
import requests
import json
import getpass




### CONFIG ###


### END CONFIG ###

s = requests.Session()

# Login credentials request
email = "naveenmars007@gmail.com"
password = "maxysierra911"
mnumb = 0
# Login credentials request

def login():
    # Base header
    payload = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9,it;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'s=dpr=1; amc_lang=en_US; t_0=1; _ym_isad=1',
        'DNT':'1',
        'Host':'auth-ac.my.com',
        'Origin':'https://wf.my.com',
        'Referer':'https://wf.my.com/en/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }
    # Login HTTP data for the post request
    login_data = {
        'email':email,
        'password':password,
        'continue':'https://account.my.com/login_continue/?continue=https%3A%2F%2Faccount.my.com%2Fprofile%2Fuserinfo%2F',
        'failure':'https://account.my.com/login/?continue=https%3A%2F%2Faccount.my.com%2Fprofile%2Fuserinfo%2F',
        'nosavelogin':'0'
        }
    # Login process
    while True:
        try:
            s.post('https://auth-ac.my.com/auth',headers=payload,data=login_data)
            s.get('https://auth-ac.my.com/sdc?from=https%3A%2F%2Fwf.my.com')
            s.get('https://wf.my.com/')  
            get_token = s.get('https://wf.my.com/minigames/user/info').json()
            s.cookies['mg_token'] = get_token['data']['token']
            s.cookies['cur_language'] = 'en'
        except:
            continue
        break

def get_mg_token():
    get_token = s.get('https://wf.my.com/minigames/user/info').json()
    s.cookies['mg_token'] = get_token['data']['token']

 
    
#Class for color and text customization
class tcol:
    magenta = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

def signal_handler(signal, frame):
    print ('\n'+tcol.yellow+"K.I.W.I. Manager was interrupted!"+tcol.end)
    sys.exit(0)

print (tcol.magenta+"\nK.I.W.I. Manager\n"+tcol.end)

# LOGIN AND CHECK USER
login()
user_check_json = s.get('https://wf.my.com/minigames/bp4/info/compose?methods=user.info').json()
try:
    print ("Logged in as {0}".format(user_check_json['data']['user']['info']['username']))
except KeyError:
    print ("Login failed.")
    sys.exit(0)
# LOGIN AND CHECK USER

# CHECK CHAR TASK AFTER COMPLETE
def char_done_task(stars,task):
    get_mg_token()
    data_done = {
        'task_id' : str(task),
        'is_paid' : '0',
        'stars' : str(stars)
    }
    req = s.post("https://wf.my.com/minigames/bp4/task/done-task",data=data_done).json()
    if req['data']['result'] == "success":
        print (tcol.green+"Success... "+tcol.end+req['data']['rewards']['reward']['item']['ext_name'])
        mnumb = mnumb+1
    else:
        print (tcol.red+"Task failed."+tcol.end)
        
# START TASK BOTH GAME AND CHAR
def start_task(stars,task):
    get_mg_token()
    # Game missions = 3 stars | Character missions 1/2/3 Stars
    data_start = {
        'task_id' : str(task),
        'stars' : str(stars)
    }
    req = s.post("https://wf.my.com/minigames/bp4/task/start-task",data=data_start).json()
    if req['state'] == "Success":
        print (tcol.green+"Task started."+tcol.end)
    else:
        print (tcol.red+"Failed to start task."+tcol.end)

# Configure task
global mission_index
global task_id
global chain

while (mnumb < 3):    
    
    if mnumb % 3 == 0 :
        mission_chain = "pripyat"
        mission_name = "wheel"
        mission_stars = 1
        auto_refil = True
        mission_index = 2
        task_id = 3
        chain = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=pripyat").json()
        print ("Pripyat Wheel mission set")
        usr_info = s.get("https://wf.my.com/minigames/bp4/info/compose?methods=user.info").json()
        chain = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain={0}".format(mission_chain)).json()
        if int(usr_info['data']['user']['info']['cheerfulness']) > 2 and chain['data']['tasks'][mission_index][task_id]['status'] == "open":
            start_task(mission_stars,task_id)
        if chain['data']['tasks'][mission_index][task_id]['remaining_time'] == 0 and chain['data']['tasks'][mission_index][task_id]['status'] == "progress":
            char_done_task(mission_stars,task_id)
        if int(usr_info['data']['user']['info']['cheerfulness']) < 2 and auto_refil == True:
            print ("Energy refil.")
            s.post("https://wf.my.com/minigames/bp4/user/buy-energy")
        time.sleep(10)
    
    elif mnumb % 3 == 1:
        mission_chain = "icebreaker" # Correct names of the chains: icebreaker, volcano, anubis, pripyat, shark
        mission_name = "water" # Same name as appears on site
        mission_stars = 1 # For people with Lucky and Athlete it's highly suggested to choose 1 star  to increase BP farming
        auto_refil = True # Can be either True or False
        mission_index = 5
        task_id = 59
        print ("Icebreaker Water mission set")
        usr_info = s.get("https://wf.my.com/minigames/bp4/info/compose?methods=user.info").json()
        chain = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain={0}".format(mission_chain)).json()
        if int(usr_info['data']['user']['info']['cheerfulness']) > 2 and chain['data']['tasks'][mission_index][task_id]['status'] == "open":
            start_task(mission_stars,task_id)
        if chain['data']['tasks'][mission_index][task_id]['remaining_time'] == 0 and chain['data']['tasks'][mission_index][task_id]['status'] == "progress":
            char_done_task(mission_stars,task_id)
        if int(usr_info['data']['user']['info']['cheerfulness']) < 2 and auto_refil == True:
            print ("Energy refil.")
            s.post("https://wf.my.com/minigames/bp4/user/buy-energy")
        time.sleep(10)
    else :
        mission_chain = "shark" # Correct names of the chains: icebreaker, volcano, anubis, pripyat, shark
        mission_name = "bite" # Same name as appears on site
        mission_stars = 1 # For people with Lucky and Athlete it's highly suggested to choose 1 star  to increase BP farming
        auto_refil = True # Can be either True or False
        mission_index = 5
        task_id = 74
        print ("Shark Bite mission set")
        usr_info = s.get("https://wf.my.com/minigames/bp4/info/compose?methods=user.info").json()
        chain = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain={0}".format(mission_chain)).json()
        if int(usr_info['data']['user']['info']['cheerfulness']) > 2 and chain['data']['tasks'][mission_index][task_id]['status'] == "open":
            start_task(mission_stars,task_id)
        if chain['data']['tasks'][mission_index][task_id]['remaining_time'] == 0 and chain['data']['tasks'][mission_index][task_id]['status'] == "progress":
            char_done_task(mission_stars,task_id)
        if int(usr_info['data']['user']['info']['cheerfulness']) < 2 and auto_refil == True:
            print ("Energy refil.")
            s.post("https://wf.my.com/minigames/bp4/user/buy-energy")
        time.sleep(10)
        
