import csv
import os
import time
import random
import pickle, pyfiglet
from telethon.sync import TelegramClient, events, utils
from telethon.sessions import StringSession
from colorama import init, Fore
from dotenv import find_dotenv, load_dotenv
import socks


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


#GlObal variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

class Profile:
    def __init__(self, phone_number, session_string, user_id=None):
        self.phone_number = phone_number
        self.session_string = session_string
        self.user_id = user_id

def banner():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('TG Group Message Manager')
    print(f'{random.choice(colors)}{banner}{n}')
    print(r+'  Version: 2.3 | Author: @1 @iamfriendz'+n+'\n')

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


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_profiles(file_path):
    try:
        with open(file_path, 'rb') as profiles_file:
            profiles = pickle.load(profiles_file)
    except FileNotFoundError:
        profiles = []
    return profiles

def save_profiles(profiles, file_path):
    with open(file_path, 'wb') as profiles_file:
        pickle.dump(profiles, profiles_file)

def edit_profile(profiles, file_path):
    with open('profiles.pkl', 'rb') as profile_pickle:
        my_profile = pickle.load(profile_pickle)
        # pickle.dump(profiles, profile_pickle)

def add_profile(phone_number, session_string, user_id, profiles):
    new_profile = Profile(phone_number, session_string, user_id)
    profiles.append(new_profile)

def get_user_id(client, phone_number):
    try:
        user = client.get_me()
        print(f'{lg}Username : {user.username}')
        print('--------------')

        my_name = client.get_entity('me')
        print(f'{lg}Display name :  {utils.get_display_name(my_name)}{rs}\n')
        
        return(utils.get_display_name(my_name))
    except Exception as e:
        print(f"Failed to get user ID for {phone_number}: {str(e)}")
        return None

def add_phone_number(profiles):
    phone_number = input(f"{INPUT} Enter the phone number (with country code):{ye} ")

    for profile in profiles: #Check if phone number already exists
        if phone_number == profile.phone_number:
            print(f"{error}Phone number {phone_number} already exists!🛑")
            print(f"{error}Please enter a different phone number!\n")
            time.sleep(0.3)
            return

    with TelegramClient(StringSession(), api_id, api_hash, proxy=proxy_set ) as client:
        client.connect()
        print("Connected successfully!")

        if not client.is_user_authorized():
            try:
                print(f"Sending a verification code to your phone number...{phone_number}")
                client.send_code_request(phone_number)
                code = input(f"{INPUT}Enter the verification code you received: ")
                client.sign_in(phone_number, code)
            except:
                pass
        
        user_id = get_user_id(client, phone_number)
        
        session_string = client.session.save()
        profile = Profile(phone_number, session_string, user_id)
        profiles.append(profile)
        # print(f"{lg}{phone_number} added SUCCESFULLY✅!\n{rs}")
       

def delete_profile(index, profiles, file_path):
    new_index = index - 1
    profile_number = profiles[new_index]
    print(f'Profile: {profile_number.user_id} Deleted Successfully!...')
    profiles.pop(new_index)
    save_profiles(profiles, file_path)
    time.sleep(1)

    print("\n List Updated Succesfully! \n")     

while True:
    #load Profiles
    profiles_file_path = 'profiles.pkl'
    profiles = load_profiles(profiles_file_path)


    clr()
    #print(r)
    banner()
    #print(n)
    print(lg+'[1] Add account'+n)
    #print(lg+'[2] Filter banned accounts'+n)
    #print(lg+'[3] List all accounts'+n)
    print(lg+'[4] Delete specified account'+n)
    print(lg+'[5] Exit')

    a = int(input(f'\nSelect a option: {w}'))
    if a == 1: #ADD NEW USERS
        add_phone_number(profiles)
        save_profiles(profiles, profiles_file_path)
        add_another = input(f"{INPUT} Do you want to add another number? (yes/no):{ye}")
        while add_another.lower() != "no":
            add_phone_number(profiles)
            save_profiles(profiles, profiles_file_path)
            add_another = input(f"{INPUT} Do you want to add another number? (yes/no):{ye} ")

    elif a == 4:
        clr()
        print("\nActive Phone Numbers: \n")
        for i, profile in enumerate(profiles):
            print(f"{i + 1}. Phone: {profile.phone_number}, User ID: {profile.user_id}\n")
        
        print("Select a profile to delete:")
        try:
            index = int(input(f"{INPUT}Enter the index of the profile to {r}DELETE, {w}Press {lg}ENTER {w}to go to Main menu: "))
            delete_profile(index, profiles, profiles_file_path)
            input('\nPress enter to go in main menu')
        except ValueError:
            print("Please enter a valid index!")
        except Exception as e:
            print(f"Error here: {e}")
        
    else:
        print("Invalid choice. Please select a valid option.")

