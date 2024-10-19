import csv
import random
import time
import os
from colorama import init, Fore
from telethon import TelegramClient
from telethon.tl.functions.messages import GetFullChatRequest
from telethon import functions, types
from telethon.tl.types import InputPeerChat
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import pickle, pyfiglet
import profile
import socks
from functions import get_group_from_user, load_profiles, \
    countdown, send_reaction, Profile, clr, banner, project_group_link
from dotenv import find_dotenv, load_dotenv


dotenv_path = find_dotenv()

load_dotenv(dotenv_path)
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

project_group_link = project_group_link

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
proxy_set = (socks.SOCKS5, proxy_data['hostname'], int(proxy_data['port']), True, proxy_data['username'], proxy_data['password'])

def get_last_pinned_message(client, group_entity):
    try:
        result = client(functions.channels.GetFullChannelRequest(group_entity))
        # print(f'\nI got the Full Chat request: {result}')
        pinned_message = int(result.full_chat.pinned_msg_id)

        if pinned_message:
            print(f"The last pinned message in the group is: {pinned_message}")
        else:
            print("Unable to get last PINNED messages in the group.")
    except Exception as e:
        print(f"Failed to retrieve the last pinned message and sunday is today: {e}")
    return pinned_message

def start_msg_reaction():
    '''
    Function to send reactions to messages'''
    
    #Load Profiles
    profiles_file_path = 'profiles.pkl'     #load Profiles
    profiles = load_profiles(profiles_file_path)

    time.sleep(0.5)
    clr()
    banner('Send Emojis🔥')
    #  The line below will request the user for group information type. Ie. Group id or link or usernames.
    # group = get_group_from_user()

    group = project_group_link

    time.sleep(0.5)

    # print(f'\n{plus}{lg} Enter MSG ID:  ')
    # msg_id = int(input(f'{INPUT} MSG ID: '))

    print(f'\n{plus}{lg} Enter SLEEP TIME ⏱️  Inbetween Reactions in SECONDS ')
    min = int(input(f'{INPUT} MINUMUM⌛: '))
    max = int(input(f'{INPUT} MAXIMUM⏳: '))
    num_of_reactions = int(input(f'{INPUT} How many Reactions? : '))
    sleep_time = random.uniform(min, max)


    print(f'\n{success} Starting now ....\n')
    time.sleep(0.5)
    countdown('⌛', 5)
    clr()
    banner('Running')

    #Main Reaction Logic Starts here!
    try:
        with TelegramClient(StringSession(profiles[0].session_string), API_ID, API_HASH, 
                            proxy=proxy_set) as client:
            group_entity = client.get_entity(group)
            group_id = group_entity.id
            print(f'\nI got the group Entity: {group_entity}')
            print(f'\nI got the group ID: {group_id}')

            total_profiles = len(profiles)

            new_pinned_msg_id  = get_last_pinned_message(client=client, group_entity=group_id)
            print(f'STARTING PINNED MESSAGE: {new_pinned_msg_id}')


            print('\n')
            print(f'{cy}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(f"{lg}Total Profiles: {total_profiles} -- Total reactions: {num_of_reactions}  ")
            print(f'{cy}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            time.sleep(0.5)

            print(f"\nStarting EMOJI🔥 sending ....  to {w}{group_entity.title}\n")

            current_profile_index = 0

            count = 0

            for x in range(num_of_reactions):

                for profile_index, current_profile in enumerate(profiles):
                    # Iterate over each profile in the list
                    
                    sender_name = f"Profile {profile_index + 1}"
                    print(f'\n{info}{cy}Attempting from {current_profile.user_id}')
                    print(f'{info}{cy}COUNT:  {count}')
                    print(f'{info}PINNED MSG ID: {new_pinned_msg_id}')
                    
                    try: 
                        send_reaction(profiles, group, profile_index, new_pinned_msg_id)

                    except InviteHashExpiredError:
                        print(f'{ye}GROUP LINK ERROR OR GROUP DELETED{rs}')
                        return
                        
                    except Exception as e:
                        print(f"Failed to send reaction: {e}")
                        pass                        
                    
                    time.sleep(sleep_time)
                    count += 1

                print(f'\n{info}{cy}All Reactions Sent! : {count}')
                
                # Get the new pinned message ID after completing the reactions
                new_pinned_msg_id = get_last_pinned_message(client=client, group_entity=group_id)
                count = 0
                
                current_profile = profiles[current_profile_index]


    except Exception as e:
        print(f"Error occured for profile {current_profile_index + 1}: {str(e)}")
        pass

react = start_msg_reaction()