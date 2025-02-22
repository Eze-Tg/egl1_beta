'''
This Holds Functions Used in these scripts
'''

import profile
import re
from colorama import init, Fore
import pickle
import pyfiglet
import random
from colorama import init, Fore
import time
import os
import socks
from dotenv import find_dotenv, load_dotenv
import csv
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon import functions, types
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import SendReactionRequest, GetStickerSetRequest, ImportChatInviteRequest
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError, ChatWriteForbiddenError, PeerIdInvalidError, UserDeactivatedBanError, AuthKeyDuplicatedError, AuthKeyInvalidError, InviteHashExpiredError, UserAlreadyParticipantError
from telethon.tl.types import ReactionCustomEmoji, ReactionEmoji, InputPeerUser, InputStickerSetShortName
from telethon.tl.types import InputPeerChat, InputPeerChannel, PeerChannel


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
# STICKER_NAME = os.getenv('STICKER_NAME')


STICKER_NAME = 'AskAnyGPT'

project_group_link = 'https://t.me/+Ut8V2sWebOY0ZGE1'
# project_group_link = os.getenv('PROJECT_GROUP_LINK')

# project_short_name = os.getenv('PROJECT_GROUP_LINK_SHORT')
project_short_name = 'Ut8V2sWebOY0ZGE1'

# project_group_id  = os.getenv('GROUP_ID')
# project_group_id = -1002172471915



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

# GlObal variables
profiles_file_path = 'profiles.pkl'


def banner(name: str):
    f = pyfiglet.Figlet()
    logo = f.renderText(name)
    print(random.choice(colors) + logo + rs)
    print(f'{r}   Version: {w}1.1 {r}| Author: {w}@Eze{rs}\n')


class Profile:
    def __init__(self, phone_number, session_string, my_name):
        self.phone_number = phone_number
        self.session_string = session_string
        self.my_name = my_name


def countdown(character='⌛', initial_count=10):
    for i in range(initial_count, 0, -1):
        print(character * i)
        time.sleep(1)


def processing_dots(num_dots, delay=1):
    for _ in range(num_dots):
        # Print a dot without newline and flush output
        print("$ ", end='', flush=True)
        time.sleep(delay)  # Wait for the specified delay


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


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
proxy_set = (socks.SOCKS5, proxy_data['hostname'], int(
    proxy_data['port']), True, proxy_data['username'], proxy_data['password'])


def get_group_from_user():
    '''Gets the group information from the user
        Returns the group as Either Public, Private or Chat_ID
    '''

    print(lg+'[1] PUBLIC Group\n'+n)
    print(lg+'[2] PRIVATE Group\n'+n)
    print(lg+'[3] GROUP CHAT_ID'+n)

    g = int(input(f'\nSelect a option: '))
    time.sleep(1)
    if g == 1:  # PUBLIC group
        time.sleep(0.5)
        print(
            f'\n{plus}{lg} Enter the exact username of the PUBLIC group [Without @] ')
        g = input(f'{INPUT} Username[Eg: Techmedies_Hub]: ')
        group = 't.me/' + str(g)

    elif g == 2:  # PRIVATE Group
        time.sleep(0.5)
        # Using Group ID which is gotten on group url .. ie https://t.me/+EMOMKgHjTHBkZDc0 // https://t.me/z7abad0dbgy/-1000000
        print(f'{plus}{lg} Enter the Telegram LINK of the PRIVATE Group')
        g = input(
            f'{INPUT}{lg} Group ID[Eg: https://t.me/+EMOMKgHjTHBkZDc0]: ')
        group = g

    elif g == 3:  # Group CHAT ID
        time.sleep(0.5)
        # Using Group ID which is gotten on group url .. ie https://t.me/+EMOMKgHjTHBkZDc0 // https://t.me/z7abad0dbgy/-1000000
        print(f'{plus}{lg} Enter the CHAT ID of your Group')
        g = int(input(f'{INPUT}{lg} CHAT ID[Eg: -100234544281]: '))
        group = g
    return group


def read_messages_from_txt(file_path, encoding="UTF-8", errors='ignore'):
    messages = []
    with open(file_path, 'r', encoding=encoding, errors=errors) as txtfile:
        for line in txtfile:
            messages.append(line.strip())
    return messages


def read_media_captions(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as captions_file:
            captions = captions_file.readlines()
        return [caption.strip() for caption in captions]
    except FileNotFoundError:
        print(
            f"Captions file not found at {file_path}. Default captions will be used.")
        return []


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


def delete_profile(index, profiles):
    profiles_file_path = 'profiles.pkl'
    # profiles = load_profiles(profiles_file_path)
    new_index = index - 1
    profile_number = profiles[new_index]
    print(f'{r}Profile: {profile_number.user_id} to be Deleted!...{rs}')
    profiles.pop(new_index)
    save_profiles(profiles, profiles_file_path)
    time.sleep(0.3)
    print(f'{lg}This User has been DELETED Successfully!{rs}')


def invite_to_channel(client, entity, user_entity):
    try:
        client(InviteToChannelRequest(entity, [user_entity]))
        return True
    except Exception as e:
        print(f"Error inviting user to channel: {str(e)}")
        return False


def captioning(current_message):
    fixed_caption = ''
    # if current_message.endswith('med1.jpeg'):
    #     fixed_caption = random.choice(
    #         ['1,126,127 $MANEKI confirmed.🤑', 'Let me show off a little. 2024 is looking good!! THanks $MANEKI'])
    # elif current_message.endswith('med2.jpeg'):
    #     fixed_caption = random.choice(
    #         ['170,249 We go Big!.', '$MANEKI just got more interesting🤑.'])
    # elif current_message.endswith('med3.jpeg'):
    #     fixed_caption = random.choice(['$1,343,412k Done and Dusted. $MANEKI is GOAT.', 'Crypto Market giving a lot🤑.', 'love $MANEKI.🤑 ',
    #                                    'Thank you for the rewards🥳🥳🥳.'])
    # elif current_message.endswith('med7.jpeg'):
    #     fixed_caption = random.choice(
    #         ['1,122,436k $MANEKI token from this airdrop.', '🤑🤑🤑🤑🤑🤑'])
    # elif current_message.endswith('med24.jpeg'):
    #     fixed_caption = random.choice(['60,600 Succesfull. Thanks Team NFP for this .' ,'🤑🤑🤑🤑🤑🤑', 'succesful airdrop.🤑 ',
    #                                    'Thank you for the rewards🥳🥳🥳.'])
    # elif current_message.endswith('med26.jpeg'):
    #     fixed_caption = random.choice(['48,000 recieved.. Can i participate again?',
    #                                    'Thank you for the rewards🥳🥳🥳.'])
    # elif current_message.endswith('med35.jpeg'):
    #     fixed_caption = random.choice(['15k NFP reward. Its good reward earning too!! @NFP🔥'])
    # elif current_message.endswith('med32.jpeg'):
    #     fixed_caption = random.choice(['24,999.. We need to rise more 🙃'])
    # elif current_message.endswith('med33.jpeg'):
    #     fixed_caption = random.choice(['I staked 21k, This is good enough for the day., Can we participate more than one in a day'])
    # elif current_message.endswith('med8.jpeg'):
    #     fixed_caption = random.choice(['I’ve just sent 15750 to the contract   address , waiting patiently for my tokens '])
    # elif current_message.endswith('med35.jpeg'):
    #     fixed_caption = random.choice(['NFP rocks. Thanks for the token', 'Can we get more tokens🎮'])
    # elif current_message.endswith('med10.jpeg'):
    #     fixed_caption = random.choice(["I sent in 3,000 Nfp and I received 9,000 NFP within 7 mins , thanks so much team NFP"])
    # else:
        # choose a random caption from the list.
    fixed_caption = random.choice(read_media_captions('media/captions.txt'))
    # print (f'Caption is : {fixed_caption}')
    return fixed_caption


def send_media(client, entity, media_path, current_message, reply_id=None, caption=None):
    file_path = 'media/captions.txt'
    caption_id = captioning(current_message)
    try:
        sender = client.send_file(
            entity, media_path, reply_to=reply_id, caption=caption_id)
        return sender
    except ChatWriteForbiddenError as error:
        print(
            f"In this case, you are not allowed to send media from this user.. Error message: {error}")
    except Exception as p:
        print(f'The issue is from media sending; Error message: {p}')
        pass


def send_typing(client, entity):
    try:
        client(functions.messages.SetTypingRequest(
            entity, types.SendMessageTypingAction()))
    except (PhoneNumberInvalidError, UserWarning, ValueError):
        print(f'The issue is from Typing; dancing!')
        pass
    except ChatWriteForbiddenError as t:
        print(
            f'{ye}{error}Unable to SendTyping Request with this User(Check if user in Group!) {t}')
        pass


def send_uploading(client, entity):
    try:
        client(functions.messages.SetTypingRequest(
            entity, types.SendMessageUploadPhotoAction(7)))
    except (PhoneNumberInvalidError, UserWarning, ValueError):
        print(f'The issue is from Typing; dancing!')
        pass
    except ChatWriteForbiddenError as t:
        print(
            f'{ye}{error}Unable to Send Upoad Request with this User(Check if user in Group!) {t}')
        pass


def send_uploading_sticker(client, entity):
    try:
        client(functions.messages.SetTypingRequest(
            entity, types.SendMessageChooseStickerAction()))
    except (PhoneNumberInvalidError, UserWarning, ValueError):
        print(f'The issue is from Sending Uploading action')
        pass
    except ChatWriteForbiddenError as t:
        print(f'{ye}{error}Unable to SendUploadingAction Request with this User(Check if user in Group!) {t}')
        pass


def send_message(client, entity, message, reply_to_message_id=None):
    try:
        sender = client.send_message(
            entity, message, reply_to=reply_to_message_id)
        return sender
    except ChatWriteForbiddenError as h:
        print(
            f'{error}{ye}Unable to SendMessage Request with this User(Check if user in Group!: {h}\n')
        pass
    except Exception as q:
        print(f'{lg}Just gonna print this to catch you! : {q}')
        # Delete this user!
        pass


def authorize_user(detailed_assigned_client, current_profile, current_profile_index):
    profiles_file_path = 'profiles.pkl'  # load Profiles
    profiles = load_profiles(profiles_file_path)

    try:
        detailed_assigned_client.connect()
        if not detailed_assigned_client.is_user_authorized():
            print(f"{ye}This User is NOT AUTHORIZED::: {current_profile.user_id}{rs}")
            delete_profile((current_profile_index + 1), profiles)
            return "deleted"
        else:
            # print(f"This User is AUTHORIZED::: {current_profile.user_id}")
            return "authorized"
    except Exception as e:
        print(f'Error for this reason::::: {e}')


def get_group_names():
    group_number = input(
        f'{INPUT}{cy} How many groups do you want to add these numbers to? (Input Test GroupName FIRST!) (1 - 10): ')
    groups = []
    for i in range(int(group_number)):
        print(
            f'{plus}{lg}Group {i}: Enter the exact username of the public group{w}[Without @]')
        g = input(f'{INPUT}{lg} Username[Eg: Techmedies_Hub]: {r}')
        group = 't.me/' + str(g)
        new_groups = groups.append(group)
        i += 1
    return groups


def add_numbers_to_group(profiles):
    profiles_file_path = 'profiles.pkl'  # load Profiles
    profiles = load_profiles(profiles_file_path)

    clr()
    banner('Add to Group')
    print('\n')

    current_profile_index = 0
    current_profile = profiles[current_profile_index]

    client = TelegramClient(StringSession(current_profile.session_string), API_ID, API_HASH, proxy=proxy_set)

    secondary_group = None  # Initialize secondary_group

    try:
        auth_user = authorize_user(client, current_profile, current_profile_index)
        if auth_user == "deleted":
            print(f"{fg}== DELETED == \n{rs}")
        else:
            # print(f'{info}{w} Project Short Name is : {project_short_name}... {rs} \n')
            try:
                print(f'Group link is : {project_short_name}')
                secondary_group = client(ImportChatInviteRequest(hash=project_short_name))
            except UserAlreadyParticipantError:
                secondary_group = client.get_entity(project_group_link)

            except InviteHashExpiredError:
                print(f'{ye}GROUP LINK ERROR OR GROUP DELETED{rs}')
                return
            except Exception as e:
                print(f'\nError Getting Group Entity!!!!: {str(e)}')
                secondary_group = None

    except Exception as e:
        print(f"\nError Authorizing User!!!!: {str(e)}")
        secondary_group = None

    if secondary_group:
        # print(f'\nI got the FULL ENTITY: {secondary_group}\n')

        # Check if the response is an Updates object (contains a list of chats)
        if hasattr(secondary_group, 'chats') and len(secondary_group.chats) > 0:
            chat = secondary_group.chats[0]  # Assuming the first chat is the one you are interested in
            group_id = chat.id  # Extract the group ID
            group_title = chat.title  # Extract the group title
            print(f'\n{info}{w}METHOD1 -- Channel ID is {group_id} and Title is {group_title}{rs}')  # Print the group ID and title

        # Check if the response is a direct Chat object
        else:
            # elif isinstance(secondary_group, Chat):
            group_id = secondary_group.id  # Extract the group ID
            group_title = secondary_group.title  # Extract the group title
            print(f'\n{info}{w}Method2 - Channel ID is {group_id} and Title is {group_title}{rs}')  # Print the group ID and title

        # else:
        #     print(f'{error}{r} No valid chat information found {rs}')

        total_profiles = len(profiles)

        print('\n')
        print(f'{cy}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(f" Total Profiles: {total_profiles} ::::: JOINING PROJECT : {lg}{group_title}")
        print(f'{cy}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{rs}')
        time.sleep(0.5)

        print(f'\n{info}{w} Joining from all accounts... {rs} \n')
        for current_profile_index in range(len(profiles)):
            current_profile = profiles[current_profile_index]
            try:
                client = TelegramClient(StringSession(current_profile.session_string), API_ID, API_HASH, proxy=proxy_set)
                auth_user = authorize_user(client, current_profile, current_profile_index)
                if auth_user == "deleted":
                    print(f"{lg}== DELETED!!\n{rs}")
                    continue

                client.connect()
                print('**********')
                print(f'{info}{w} {current_profile.user_id} JOINING... {lg}{group_title}')

                try:
                    client(ImportChatInviteRequest(hash=project_short_name))
                    print(f'{success}{lg} {current_profile.user_id} JOINED {lg}{group_title}{rs}')
                except UserAlreadyParticipantError:
                    print(f'This user is already a participant of the project group.')
                except InviteHashExpiredError as e:
                    print(f'This user hash is invalid :::: {e}')
                    try:
                        client(JoinChannelRequest(project_short_name))
                        print(f'{success}{lg} {current_profile.user_id} JOINED {lg}{group_title}{rs}')
                    except Exception as e:
                        print(f'The rugcall error is {e}')
                except Exception as e:
                    print(f'{ye}An error occurred: {e} :::::: Trying SECOND JOINING METHOD{rs}')

                print('**********\n')
                client.disconnect()
                time.sleep(1)

            except Exception as e:
                print(f"\nError adding {current_profile.phone_number} to group: {str(e)}")
                continue

        print(f'{info}{lg} Successfully Joined From All Accounts... {lg}{group_title}{rs} \n')
    else:
        print(f'{error}{r} Group not found {rs}')
    client.disconnect()


def get_usernames():
    # Get usernames from the user
    usernames_input = input("Enter a comma-separated list of usernames: ")
    usernames = [username.strip() for username in usernames_input.split(',')]
    return usernames


def send_messages_to_usernames(client, usernames, profiles):
    # Sends messages to list of usernames provided by the user for warming up

    print(f'{info}{cy} Sending Messages to ... {usernames}{rs} \n')

    # Get messages from private message csv
    messages = read_messages_from_csv('private_messages.csv')
    current_message_index = 0
    total_messages = len(messages)

    for profile in profiles:
        while current_message_index < len(profiles):
            current_message = messages[current_message_index]
            print(current_message)
            with TelegramClient(StringSession(profile.session_string), API_ID, API_HASH, proxy=("socks5", proxy_data['hostname'],
                                                                                                proxy_data['port'], proxy_data['username'],
                                                                                                proxy_data['password'])) as user_client:
                user_client.connect()
                try:
                    user = random.choice(usernames)
                    user_entity = user_client.get_entity(user)

                    # Send the message
                    send_message(user_client, user_entity, current_message)

                    print(
                        f"Message sent from {profile.phone_number} to {user} \n")
                    # time.sleep(3)
                    user_client.disconnect()
                except Exception as e:
                    print(
                        f"Error sending message from {profile.phone_number} to {user}: {str(e)}")
            current_message_index += 1


def warmup_mode(client, profiles):
    print(f'{plus}{lg} ***WARM-UP NUMBERS MODE*** \n')

    # groups = get_group_names()
    users = get_usernames()

    # add_numbers_to_group(client, profiles, groups)
    send_messages_to_usernames(client, users, profiles)
    clr()


def sending_status(current_profile, current_message_index, current_message):
    print(f'{cy}=====================')
    # print(f"{info}Phone: {current_profile.phone_number}")
    # print(f'{cy}{info}User ID: {current_profile.user_id}')
    print(f'{info}{w}Message {current_message_index + 1}: {current_message} => {lg}SENT SUCCESFULLY!')
    print(f'{cy}=====================\n')


def get_user_id(message: str):
    '''
    This function captures and returns user_id of given message
    '''
    user_id_match = re.search(r'user_id=(\d+)', message)
    if user_id_match:
        user_id = int(user_id_match.group(1))
        # print("User ID:", user_id)
    else:
        print("User ID not found.")

    return user_id


def responders(profiles, current_profile_index, current_message, group, alpha_message_id, sticker_set):
    '''
    This Function sends a responce message and reaction to the specified alpha_message_id(the message that gets the response) \n
    Args:
    profiles (list): list of profiles
    current_profile_index (int): index of current profile
    current_message (str): current message
    group (str): group name
    alpha_message_id (int): alpha_message_id of the message that gets the response
    '''
    try:
        responder_client = TelegramClient(StringSession(profiles[current_profile_index].session_string), API_ID, API_HASH,
                                          proxy=proxy_set)
        print(f'Phone number here is {profiles[current_profile_index].phone_number}')
        responder_client.connect()
        try:
            if not responder_client.is_user_authorized:
                print(f'{error}{r} {profiles[current_profile_index].phone_number} is Unauthorized {rs} \n')
                print(f'You need TO RELOGIN THIS USER, DELETING THIS USER NOW')
                print(f'Phone number here is {profiles[current_profile_index].phone_number}')
                delete_profile((current_profile_index + 1), profiles)
                print("== RELOGIN THIS USER!!\n")
                pass
            else:
                group_entity = responder_client.get_entity(group)
                # run check to see the media number
                if current_message.startswith('media'):
                    caption_string = captioning(current_message)
                    media_path = current_message[6:]
                    send_uploading(responder_client, group_entity)
                    time.sleep(4)
                    send_media(responder_client, group_entity, media_path,
                               current_message, reply_id=alpha_message_id, caption=caption_string)
                elif current_message.startswith('sticker'):
                    sticker_number = int(current_message[8:])
                    print(f'STICKER NUMBER IS : {sticker_number}')
                    send_uploading_sticker(responder_client, group_entity)
                    time.sleep(4)
                    responder_client.send_file(
                        group_entity, sticker_set.documents[sticker_number], reply_id=alpha_message_id)
                else:
                    send_typing(responder_client, group_entity)
                    time.sleep(4)  # Sleep for 2 seconds to simulate typing
                    send_message(responder_client, group_entity,
                                 current_message, reply_to_message_id=alpha_message_id)
                send_reaction(profiles, group,
                              current_profile_index, alpha_message_id)
                responder_client.disconnect()
        except UserDeactivatedBanError as e:
            print("User Deactivated ===== Deleting User...")
            delete_profile((current_profile_index + 1), profiles)
            pass
        except InviteHashExpiredError:
            print(f'{ye}GROUP LINK ERROR OR GROUP DELETED{rs}')
            return
        except AuthKeyInvalidError as e:
            print("Relogin this user ===== Deleting User...")
            delete_profile((current_profile_index + 1), profiles)
            print("== RELOGIN THIS USER!!\n")
            pass

        except Exception as e:
            print(f'The night bath; Error Message is: {e}')
            print("== check on this user\n")
            pass
    except AuthKeyDuplicatedError as authkeyerror:
        print(f'Error here is :::: {authkeyerror}')
        print(f'You need TO RELOGIN THIS USER, DELETING THIS USER NOW')
        print(
            f'Phone number here is {profiles[current_profile_index].phone_number}')
        delete_profile((current_profile_index + 1), profiles)
        print("== RELOGIN THIS USER!!\n")
        pass

    except Exception as e:
        print(f'The Lamp Curprit is user ; Error Message is: {e}')
        print("== Just gonna skip this user\n")
        pass
    finally:
        responder_client.disconnect()


def alpha_senders(profiles, current_profile_index, current_message, group, sticker_set):
    try:
        sender_client = TelegramClient(StringSession(profiles[current_profile_index].session_string), API_ID, API_HASH,
                                       proxy=proxy_set)
        print(f'Phone Number : {profiles[current_profile_index].phone_number}')
        sender_client.connect()
        try:
            if not sender_client.is_user_authorized():
                print(f'{error}{r} {profiles[current_profile_index].phone_number} is Unauthorized {rs} \n')
                print(f'You need TO RELOGIN THIS USER, DELETING THIS USER NOW')
                print(f'Phone number here is {profiles[current_profile_index].phone_number}')
                delete_profile((current_profile_index + 1), profiles)
                print("== RELOGIN THIS USER!!\n")
                pass
            else:
                group_entity = sender_client.get_entity(group)
                if current_message.startswith('media'):
                    # run check to see the media number
                    caption_string = captioning(current_message)
                    media_path = current_message[6:]
                    send_uploading(sender_client, group_entity)
                    time.sleep(5)  # Sleep for 5 seconds to simulate Uploading
                    msg_resp = send_media(sender_client, group_entity, media_path,
                                          current_message=current_message, caption=caption_string)
                    msg_id = msg_resp.id
                elif current_message.startswith('sticker'):
                    sticker_number = int(current_message[8:])
                    print(f'STICKER NUMBER IS : {sticker_number}')
                    send_uploading_sticker(sender_client, group_entity)
                    time.sleep(5)
                    msg_resp = sender_client.send_file(
                        group_entity, sticker_set.documents[sticker_number])
                    msg_id = msg_resp.id
                else:
                    send_typing(sender_client, group_entity)
                    time.sleep(6)  # Sleep for 7 seconds to simulate typing
                    msg_resp = send_message(
                        sender_client, group_entity, current_message)
                    msg_id = msg_resp.id
                    # print(f"*** ALPHA SENDER; MESSAGE ID: {msg_id} ***")
                sender_client.disconnect()
                return int(msg_id)

        except PeerIdInvalidError as e:
            print(f'Hope i catch you finnessing here : {e}')
            print(f'The Bed Curprit is user ; Error Message is: {e}')
            pass
        except InviteHashExpiredError:
            print(f'{ye}GROUP LINK ERROR OR GROUP DELETED{rs}')
            return
        except Exception as e:
            print(f'The Curprit is {e}')
            print(f'Naija film na trash, Got to del this user!')
            # delete_profile(current_profile_index, profile, profiles_file_path)
            pass
    except AuthKeyDuplicatedError as authkeyerror:
        print(f'Error here is :::: {authkeyerror}')
        print(f'You need TO RELOGIN THIS USER, DELETING THIS USER NOW')
        delete_profile((current_profile_index + 1), profiles)
        print("== RELOGIN THIS USER\n")
    except Exception as e:
        print(f'The Biggy fishy caught here) : {e}')
    finally:
        sender_client.disconnect()


def send_reaction(profiles, group, current_profile_index, msg_id):
    '''Sends different reactions to a given msg id \n
    Args:
        profiles (list): List of profiles
        group_id (int): ID of the group
        current_profile_index (int): Index of the current profile
        msg_id (int): ID of the message
    '''

    try:
        client = TelegramClient(StringSession(profiles[current_profile_index].session_string), API_ID, API_HASH,
                                proxy=proxy_set)
        client.connect()
        if not client.is_user_authorized:
            print(
                f'{error}{r} {profiles[current_profile_index].phone_number} is Unauthorized {rs} \n')
            print(f'You need TO RELOGIN THIS USER, DELETING THIS USER NOW')
            print(
                f'Phone number here is {profiles[current_profile_index].phone_number}')
            delete_profile((current_profile_index + 1), profiles)
            print("== RELOGIN THIS USER!!\n")
            pass
        else:
            user = client.get_entity(group)
            group_entity = client.get_entity(
                InputPeerChannel(user.id, user.access_hash))
            # Not allowed Emojis : 🥳, 💸
            random_emojis = random.choice(['🔥', '👍', '😎', '🐳'])  # '👌'  '😎',
            # print(f'Reaction is {random_emojis}')
            reaction = client(SendReactionRequest(peer=group_entity, msg_id=msg_id, reaction=[
                              types.ReactionEmoji(emoticon=random_emojis)]))
            print(f"{info}{lg}Reaction {random_emojis} sent successfully!")
            # return reaction
        client.disconnect()
    except Exception as e:
        print(f"Failed to send reaction: {e}")
        pass
    finally:
        client.disconnect()


def get_sticker_sets(client, sticker_name: str = None):
    sticker_name = STICKER_NAME
    sticker_sets = client(GetStickerSetRequest(InputStickerSetShortName(sticker_name), 0))
    # print(f"Sticker SET Here is :: {sticker_sets}")
    return sticker_sets


def start_msg_sending():
    profiles_file_path = 'profiles.pkl'  # load Profiles
    profiles = load_profiles(profiles_file_path)
    csv_file_path = 'messages.csv'
    message_file_path = 'msg.txt'

    # messages = read_messages_from_csv(csv_file_path)

    messages = read_messages_from_txt(message_file_path)

    time.sleep(0.5)
    clr()
    banner('MultiUser Group Messaging')

    # The line below will request the user for group information type. Ie. Group id or link or usernames.
    # group = get_group_from_user()

    group = project_group_link


    time.sleep(0.5)
    print(f'\n{plus}{lg} Enter SLEEP TIME ⏱️  Inbetween messages in SECONDS ')
    min = int(input(f'{INPUT} MINUMUM⌛: '))
    max = int(input(f'{INPUT} MAXIMUM⏳: '))
    sleep_time = random.uniform(min, max)

    print(f'\n{success} Starting now ....')

    countdown('⏳', 5)
    clr()
    banner('Running')

    # Main Group messaging Logic Starts here!
    try:
        client = TelegramClient(StringSession(profiles[0].session_string), API_ID, API_HASH, proxy=proxy_set)
        print(f'{info}Phone Number here is {profiles[0].phone_number}')
        client.connect()
        if not client.is_user_authorized:
            print(f'{error}{r} {profiles[0].phone_number} is Unauthorized {rs} \n')
            print(f'You need TO RELOGIN THIS USER, DELETING THIS USER NOW')
            print(f'Phone number here is {profiles[current_profile_index].phone_number}')
            delete_profile((current_profile_index + 1), profiles)
            print("== RELOGIN THIS USER!!\n")
            pass
        else:
            # print(f'NOW WE ARE HERE!')
            group_entity = client.get_entity(group)
            sticker_set = get_sticker_sets(client)
            # print(f'\nI got the STICKER SET: {sticker_set}')

            total_profiles = len(profiles)
            total_messages = len(messages)

            print('\n')
            print(f'{cy}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(
                f"{lg}Total Profiles: {total_profiles} -- Total messages: {total_messages} ")
            print(f'{cy}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            time.sleep(0.5)

            print(
                f"\nStarting Message sending ....  to {w}{group_entity.title}\n")
            client.disconnect()

            current_profile_index = 0
            current_message_index = 0

            while current_message_index < total_messages:
                current_profile = profiles[current_profile_index]
                current_message = messages[current_message_index]

                print(f'\n{info}{cy}Attempting from {current_profile.user_id}')
                try:
                    if current_profile_index == 1:  # ALPHA SENDER PROFILE 1 WITH 5 RESPONCE
                        alpha_msg_id = alpha_senders(profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile, current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 4 REPLIEs****")
                        for x in range(4):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(f'\n{info}{cy}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')
                            responders(profiles, current_profile_index,
                                       current_message, group, alpha_msg_id, sticker_set)

                            sending_status(
                                current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 4 Replies')

                    elif current_profile_index == 10:  # ALPHA SENDER PROFILE 10 WITH 8 RESPONCE
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile,
                                       current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (
                            current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 5 REPLIEs\n")
                        for x in range(5):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(
                                f'\n{info}{cy}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')
                            responders(profiles, current_profile_index,
                                       current_message, group, alpha_msg_id, sticker_set)

                            sending_status(
                                current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 5 Replies')

                    elif current_profile_index == 20:  # ALPHA SENDER PROFILE 24 WITH 7 RESPONCE
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile,
                                       current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (
                            current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 4 REPLIEs\n")
                        for x in range(4):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(
                                f'\n{info}{cy}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')

                            responders(profiles, current_profile_index,
                                       current_message, group, alpha_msg_id, sticker_set)

                            sending_status(
                                current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 4 Replies')

                    elif current_profile_index == 26:  # ALPHA SENDER PROFILE 40 WITH 9 RESPONCE
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile,
                                       current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (
                            current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 3 REPLIEs\n")
                        for x in range(3):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(
                                f'\n{info}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')

                            responders(profiles, current_profile_index,
                                       current_message, group, alpha_msg_id, sticker_set)

                            sending_status(
                                current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 3 Replies')

                    elif current_profile_index == 32:  # ALPHA SENDER PROFILE 50 WITH 6 RESPONCE
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile,
                                       current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (
                            current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 4 REPLIEs\n")
                        for x in range(4):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(
                                f'\n{info}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')

                            responders(profiles, current_profile_index,
                                       current_message, group, alpha_msg_id, sticker_set)

                            sending_status(
                                current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 4 Replies')

                    elif current_profile_index == 40:  # ALPHA SENDER PROFILE 61 WITH 10 RESPONCE
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile,
                                       current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (
                            current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 5 REPLIEs\n")
                        for x in range(5):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(
                                f'\n{info}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')

                            responders(profiles, current_profile_index,
                                       current_message, group, alpha_msg_id, sticker_set)

                            sending_status(
                                current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 5 Replies')

                    elif current_profile_index == 47:  # ALPHA SENDER PROFILE 61 WITH 10 RESPONCE
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile,
                                       current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (
                            current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 3 REPLIEs\n")
                        for x in range(3):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(
                                f'\n{info}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')

                            responders(profiles, current_profile_index,
                                       current_message, group, alpha_msg_id, sticker_set)

                            sending_status(
                                current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 3 Replies')

                    elif current_profile_index == 53:  # ALPHA SENDER PROFILE 61 WITH 10 RESPONCE
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile,
                                       current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (
                            current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 4 REPLIEs\n")
                        for x in range(4):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(
                                f'\n{info}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')

                            responders(profiles, current_profile_index,
                                       current_message, group, alpha_msg_id, sticker_set)

                            sending_status(
                                current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 4 Replies')

                    elif current_profile_index == 61:  # ALPHA SENDER PROFILE 61 WITH 10 RESPONCE
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile,
                                       current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (
                            current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 3 REPLIEs\n")
                        for x in range(3):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(
                                f'\n{info}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')

                            responders(profiles, current_profile_index, current_message, group, alpha_msg_id, sticker_set)

                            sending_status(current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 3 Replies')
                    
                    elif current_profile_index == 71:  # ALPHA SENDER PROFILE 61 WITH 10 RESPONCE
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile,
                                       current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (
                            current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 4 REPLIEs\n")
                        for x in range(4):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(
                                f'\n{info}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')

                            responders(profiles, current_profile_index, current_message, group, alpha_msg_id, sticker_set)

                            sending_status(current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 4 Replies')
                    
                    elif current_profile_index == 81:  # ALPHA SENDER PROFILE 61 WITH 10 RESPONCE
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        print(f'{info}{lg}ALPHA SENDER MSG ID {alpha_msg_id}')
                        sending_status(current_profile,
                                       current_message_index, current_message)

                        current_message_index += 1
                        current_profile_index = (
                            current_profile_index + 1) % total_profiles

                        print(f"{info}{ye}****SENDING 5 REPLIEs\n")
                        for x in range(5):
                            time.sleep(sleep_time)
                            current_message = messages[current_message_index]
                            current_profile = profiles[current_profile_index]

                            print(
                                f'\n{info}REPLYING TO Message ID {alpha_msg_id} from {current_profile.user_id}')

                            responders(profiles, current_profile_index, current_message, group, alpha_msg_id, sticker_set)

                            sending_status(current_profile, current_message_index, current_message)
                            x += 1
                            current_message_index += 1
                            current_profile_index = (
                                current_profile_index + 1) % total_profiles
                        print(f'{ye}***FNISH 5 Replies')

                    else:  # Normal profile sends a message
                        alpha_msg_id = alpha_senders(
                            profiles, current_profile_index, current_message, group, sticker_set)
                        sending_status(current_profile,
                                       current_message_index, current_message)

                except PeerIdInvalidError as e:
                    print(f'Hope i catch you here : {e}')
                except Exception as b:
                    print(f"The Bad guy is {current_profile.user_id} and error is {b}")
                    # delete_profile(current_profile_index, profile, profiles_file_path)
                    pass

                current_message_index += 1
                current_profile_index = (current_profile_index + 1) % total_profiles

                # sleep_time = random.uniform(10, 15)
                time.sleep(sleep_time)

        print("\nAll Messages Sent!")

    except UserDeactivatedBanError as e:
        print("User Deactivated ===== Deleting User...")
        delete_profile((current_profile_index + 1), profiles)
        print('This user has been removed from the database using delete_profile function')
        pass
    except InviteHashExpiredError:
        print(f'{ye}GROUP LINK ERROR OR GROUP DELETED{rs}')
        return
    except AuthKeyInvalidError as e:
        print("Relogin this user ===== Deleting User...")
        delete_profile((current_profile_index + 1), profiles)
        print("== RELOGIN THIS USER!!\n")
        pass

    except Exception as e:
        print(
            f"Error occured for profile {current_profile_index + 1}: {str(e)}")
        pass
    finally:
        client.disconnect()
