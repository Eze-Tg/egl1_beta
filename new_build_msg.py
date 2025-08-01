import os
import random
from dotenv import find_dotenv, load_dotenv
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetShortName
import socks
import csv
import pickle


# Define the Profile class (example)
class Profile:
    def __init__(self, session_string, phone_number):
        self.session_string = session_string
        self.phone_number = phone_number

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

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

def load_profiles(profiles_file_path):
    try:
        with open(profiles_file_path, 'rb') as f:
            profiles = pickle.load(f)
        return profiles
    except Exception as e:
        print(f"Error loading profiles: {e}")
        return None

def authenticated_client(profiles):
    try:
        client = TelegramClient(StringSession(profiles[0].session_string), API_ID, API_HASH, proxy=proxy_set)
        print(f'Phone Number here is {profiles[0].phone_number}')
        client.connect()
        if not client.is_user_authorized():
            print(f'{profiles[0].phone_number} is Unauthorized \n')
            print('You need TO RELOGIN THIS USER, DELETING THIS USER NOW')
            pass
        else:
            print('Client is successfully authenticated.')
            return client
    except Exception as e:
        print(f"Error in client authentication: {e}")
        return None

# Step 1: Remove empty lines from msg.txt file
def remove_empty_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    non_empty_lines = [line for line in lines if line.strip() != ""]
    with open(file_path, 'w') as file:
        file.writelines(non_empty_lines)

# Step 2: Ask user for link to or name of sticker
def get_sticker_info():
    sticker_name = input("Please enter the name or link of the sticker set: ")
    return sticker_name

# Step 3: Ask user for the number of messages to be sent
def get_number_of_messages():
    number_of_messages = int(input("How many messages do you want to send? "))
    return number_of_messages

# Step 4: Extract the length of sticker set using the client
def get_sticker_set_length(client, sticker_name):
    try:
        # Use the logged-in client to get the sticker set details
        sticker_set = client(GetStickerSetRequest(InputStickerSetShortName(sticker_name), 0))
        stickers = sticker_set.documents
        length = len(stickers)
        # print(f"The length of Sticker set is :: {sticker_set}\n\n")
        # print(f"Sticker SET Here is :: {sticker_set}")
        return length
    except Exception as e:
        print(f"Error retrieving sticker set: {e}")
        return 0

# Step 5: Randomly add "sticker:1 - sticker:n" to the msg.txt file with each appearing 3 times
def add_stickers_to_file(file_path, sticker_length):
    stickers = [f"sticker:{i}\n" for i in range(1, sticker_length + 1)] * 3
    random.shuffle(stickers)

    with open(file_path, 'r') as file:
        existing_lines = file.readlines()
    
    combined_content = existing_lines + stickers
    random.shuffle(combined_content)

    with open(file_path, 'w') as file:
        file.writelines(combined_content)

# Step 6: Find out the number of mp4/jpg in the media folder
def count_media_files(media_path):
    jpg_files = [f for f in os.listdir(media_path) if f.endswith('.jpg')]
    mp4_files = [f for f in os.listdir(media_path) if f.endswith('.mp4')]
    return len(jpg_files), len(mp4_files)

# Step 7: Rename jpg files to "med1.jpg - (medN.jpg)"
def rename_jpg_files(media_path):
    jpg_files = sorted([f for f in os.listdir(media_path) if f.endswith('.jpg')])
    for i, filename in enumerate(jpg_files, start=1):
        new_name = f"med{i}.jpg"
        os.rename(os.path.join(media_path, filename), os.path.join(media_path, new_name))
    return len(jpg_files)

# Step 8: Rename mp4 files continuing from the last number from jpg files
def rename_mp4_files(media_path, start_number):
    mp4_files = sorted([f for f in os.listdir(media_path) if f.endswith('.mp4')])
    for i, filename in enumerate(mp4_files, start=start_number + 1):
        new_name = f"med{i}.mp4"
        os.rename(os.path.join(media_path, filename), os.path.join(media_path, new_name))


# NEW Step 9: Add media files to msg.txt
def add_media_to_file(file_path, media_path, jpg_count, mp4_count):
    media_entries = []

    # Add jpg files
    for i in range(1, jpg_count + 1):
        media_entries.append(f"media:./media/med{i}.jpg\n")
    
    # Add mp4 files
    for i in range(jpg_count + 1, jpg_count + mp4_count + 1):
        media_entries.append(f"media:./media/med{i}.mp4\n")

    # Add each media entry 4 times
    media_entries *= 4
    random.shuffle(media_entries)

    with open(file_path, 'r') as file:
        existing_lines = file.readlines()

    combined_content = existing_lines + media_entries
    random.shuffle(combined_content)

    with open(file_path, 'w') as file:
        file.writelines(combined_content)

# Step 10: Duplicate total number of messages until number is reached
def duplicate_messages(file_path, total_messages):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    original_length = len(lines)

    # Repeat the entire content until the total number of lines is greater than or equal to total_messages
    while len(lines) < total_messages:
        lines += lines[:original_length]

    # If we have exceeded the required number of messages, trim the excess
    lines = lines[:total_messages]

    with open(file_path, 'w') as file:
        file.writelines(lines)

# Main script execution
def main():
    profiles_file_path = 'profiles.pkl'  # Load Profiles
    profiles = load_profiles(profiles_file_path)
    if profiles is None:
        print("Failed to load profiles. Exiting.")
        return

    file_path = 'msg.txt'
    media_path = './media/'

    print("Stage 1: Removing empty lines from msg.txt.")
    remove_empty_lines(file_path)
    input("Press Enter to proceed to the next step...")

    print("Stage 2: Getting sticker information from user.")
    sticker_name = get_sticker_info()
    input("Press Enter to proceed to the next step...")

    print("Stage 3: Asking user for the number of messages.")
    number_of_messages = get_number_of_messages()
    input("Press Enter to proceed to the next step...")

    print("Stage 4: Extracting sticker set length.")
    client = authenticated_client(profiles)
    if client is None:
        print("Failed to authenticate client. Exiting.")
        return
    sticker_length = get_sticker_set_length(client, sticker_name)
    input("Press Enter to proceed to the next step...")

    print("Stage 5: Adding stickers to msg.txt file.")
    add_stickers_to_file(file_path, sticker_length)
    print("Stickers added successfully.")
    input("Press Enter to proceed to the next step...")

    print("Stage 6: Counting media files in the media folder.")
    jpg_count, mp4_count = count_media_files(media_path)
    print(f"Found {jpg_count} JPG files and {mp4_count} MP4 files.")
    input("Press Enter to proceed to the next step...")

    print("Stage 7: Renaming JPG files.")
    last_jpg_number = rename_jpg_files(media_path)
    print(f"Renamed JPG files up to med{last_jpg_number}.jpg")
    input("Press Enter to proceed to the next step...")

    print(f"Stage 8: Renaming MP4 files starting from med{last_jpg_number + 1}.")
    rename_mp4_files(media_path, last_jpg_number)
    print("MP4 files renamed successfully.")
    input("Press Enter to proceed to the next step...")

    print("Stage 9: Adding media files to msg.txt.")
    add_media_to_file(file_path, media_path, jpg_count, mp4_count)
    print("Media files added successfully.")
    input("Press Enter to proceed to the next step...")

    print("Stage 10: Duplicating messages in msg.txt.")
    duplicate_messages(file_path, number_of_messages)
    print("Messages duplicated successfully.")

if __name__ == "__main__":
    main()