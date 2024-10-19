import csv
import random
import profile
import os
from colorama import init, Fore
from telethon import TelegramClient
from telethon.tl import types
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
#from send_reactions import react
import subprocess
from functions import add_numbers_to_group, banner, Profile, clr, load_profiles, delete_profile, warmup_mode, start_msg_sending
from dotenv import find_dotenv, load_dotenv


init()
r = Fore.RED
lg = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
n = Fore.RESET
colors = [r, lg, w, ye, cy]
info = lg + '(' + w + 'i' + lg + ')' + rs
error = lg + '(' + r + '!' + lg + ')' + rs
success = w + '(' + lg + '*' + w + ')' + rs
INPUT = lg + '(' + cy + '~' + lg + ')' + rs
plus = lg + '(' + w + '+' + lg + ')' + rs



dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

profiles_file_path = 'profiles.pkl'     #load Profiles
profiles = load_profiles(profiles_file_path)

def load_proxy_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=':')
        proxy_data = next(reader)
        return {
            'hostname': proxy_data[0],
            'port': int(proxy_data[1]),
            'username': proxy_data[2],
            'password': proxy_data[3],
        }
proxy_data = load_proxy_data('proxy.csv') 


clr()
banner('TG TOOLS')

print(lg+'[1] Warm Up Numbers'+n)
print(lg+'[2] List all accounts'+n)
print(lg+'[3] Join Telegram Group'+n)
print(lg+'[4] Start Group Message'+n)
print(lg+'[5] Send Reactions to messages🔥'+n)
print(lg+'[6] Exit')
a = int(input(f'\nSelect a option: {r}'))

if a == 1: #WARMUP NUMBERS
    try:
        with TelegramClient(StringSession(profiles[0].session_string), api_id, api_hash) as client:
            warmup_mode(client, profiles)
    except Exception as e:
        print(e)

elif a == 2: #PRINT ALL PROFILES
    pass
    # clr()
    # banner()
    # print("\nActive Phone Numbers: \n")
    # for i, profile in enumerate(profiles):
    #     print(f"{i + 1}. Phone: {profile.phone_number}, User ID: {profile.user_id}\n")
    # input('\nPress enter to go in main menu')

elif a == 3: # Add New Numbers to Telegram Script
    add_numbers_to_group(profiles)  

elif a == 4: # Start Sending Messages
    start_msg_sending()

elif a == 5: # Send Reactions
    print ("Reactions")
    #react()
    
    # try:
    # # Replace 'python3' with 'python' if using Python 2
    #     subprocess.run(['python3', 'send_reactions.py'])
    # except Exception as e:
    #     print(f"Failed to launch the other script: {e}")

elif a == 6: # EXIT
    pass