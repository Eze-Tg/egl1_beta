import os
import random
from dotenv import find_dotenv, load_dotenv
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetShortName
from colorama import init, Fore
import socks
import csv
import pickle
import time



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
            print(f'{r}{profiles[0].phone_number} is Unauthorized {rs}\n')
            print('You need TO RELOGIN THIS USER, DELETING THIS USER NOW')
            pass
        else:
            print(f'{lg}Client is successfully authenticated.{rs}')
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
    sticker_name = input(f"{ye}Please enter the name or link of the sticker set: ")
    return sticker_name

# Step 3: Ask user for the number of messages to be sent
def get_number_of_messages():
    number_of_messages = int(input(f"\n{ye}How many messages do you want to send? : "))
    return number_of_messages

# Step 4: Extract the length of sticker set using the client
def get_sticker_set_length(client, sticker_name):
    try:
        sticker_set = client(GetStickerSetRequest(InputStickerSetShortName(sticker_name), 0))
        stickers = sticker_set.documents
        return len(stickers)
    except Exception as e:
        print(f"Error retrieving sticker set: {e}")
        return 0

# Step 5: Randomly add "sticker:1 - sticker:n" to the msg.txt file with each appearing 3 times
def add_stickers_to_file(file_path, sticker_length):
    # Create a list of stickers, each repeated up to 50 times
    stickers = [f"sticker:{i}\n" for i in range(1, sticker_length + 1)] * 40
    random.shuffle(stickers)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    total_stickers = len(stickers)
    print(f'Total sticker : {total_stickers}')
    interval = max(1, total_lines // total_stickers)

    new_lines = []
    sticker_index = 0

    for i, line in enumerate(lines):
        new_lines.append(line)
        # Insert stickers at regular intervals
        if sticker_index < total_stickers and (i + 1) % interval == 0:
            new_lines.append(stickers[sticker_index])
            sticker_index += 1

    # Add any remaining stickers at the end, if not inserted
    while sticker_index < total_stickers:
        new_lines.append(stickers[sticker_index])
        sticker_index += 1

    with open(file_path, 'w') as file:
        file.writelines(new_lines)



# Step 6: Find out the number of mp4/jpg in the media folder
def count_media_files(media_path):
    jpg_files = [f for f in os.listdir(media_path) if f.endswith('.jpg')]
    mp4_files = [f for f in os.listdir(media_path) if f.endswith('.mp4')]
    return len(jpg_files), len(mp4_files)

# Step 7: Rename jpg files to "med1.jpg - (medN.jpg)"
def count_media_files(media_path):
    jpg_files = [f for f in os.listdir(media_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    mp4_files = [f for f in os.listdir(media_path) if f.endswith('.mp4')]
    return len(jpg_files), len(mp4_files)

def rename_jpg_files(media_path):
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png']:
        image_files.extend(sorted([f for f in os.listdir(media_path) if f.lower().endswith(ext)]))
    
    for i, filename in enumerate(image_files, start=1):
        # Preserve original extension
        original_ext = os.path.splitext(filename)[1]
        new_name = f"med{i}{original_ext}"
        os.rename(os.path.join(media_path, filename), os.path.join(media_path, new_name))
    
    return len(image_files)

# Step 8: Rename mp4 files continuing from the last number from jpg files
def rename_mp4_files(media_path, start_number):
    mp4_files = sorted([f for f in os.listdir(media_path) if f.endswith('.mp4')])
    for i, filename in enumerate(mp4_files, start=start_number + 1):
        new_name = f"med{i}.mp4"
        os.rename(os.path.join(media_path, filename), os.path.join(media_path, new_name))

# Step 9: Add media files to msg.txt
def add_media_to_file(file_path, media_path, jpg_count, mp4_count):
    media_entries = []

    # Add image files with their respective extensions
    for i in range(1, jpg_count + 1):
        # Check which extension exists for this media number
        for ext in ['.jpg', '.jpeg', '.png']:
            if os.path.exists(os.path.join(media_path, f"med{i}{ext}")):
                media_entries.append(f"media:./media/med{i}{ext}\n")
                break
    
    # Add mp4 files
    for i in range(jpg_count + 1, jpg_count + mp4_count + 1):
        media_entries.append(f"media:./media/med{i}.mp4\n")

    # Multiply and shuffle media entries
    media_entries *= 80
    random.shuffle(media_entries)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    total_media = len(media_entries)
    print(f"{lg}Total Media : {total_media}{rs} ")
    interval = max(1, total_lines // total_media)

    new_lines = []
    media_index = 0

    for i, line in enumerate(lines):
        new_lines.append(line)
        if media_index < total_media and (i + 1) % interval == 0:
            new_lines.append(media_entries[media_index])
            media_index += 1

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

    return total_media
    return total_media


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


def clean_text_file(file_path):
    """
    This function checks each line of a text file for the presence of "" (empty quotes).
    If found, it removes the double quotes at the beginning and end of the line.
    :param file_path: Path to the text file to clean
    """
    cleaned_lines = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            stripped_line = line.strip()
            if '""' in stripped_line:  # Check if the line contains empty quotes
                # Remove double quotes at the beginning and end if they exist
                if stripped_line.startswith('"') and stripped_line.endswith('"'):
                    stripped_line = stripped_line[1:-1]
            cleaned_lines.append(stripped_line + '\n')  # Add cleaned line
    
    # Rewrite the file with cleaned lines
    with open(file_path, 'w') as file:
        file.writelines(cleaned_lines)

# Example usage




# Main script execution
def main():
    profiles_file_path = 'profiles.pkl'  # Load Profiles
    profiles = load_profiles(profiles_file_path)
    if profiles is None:
        print("Failed to load profiles. Exiting.")
        return

    file_path = 'msg.txt'
    media_path = './media/'

    print(f'{w}CHECKING FOR """')
    clean_text_file(file_path)

    print(f"\n{w}Stage 1: Removing empty lines from msg.txt.")
    remove_empty_lines(file_path)
    # input(f"{lg}Press Enter to proceed to the next step...{rs}")

    print("\nStage 2: Getting sticker information from user.")
    sticker_name = get_sticker_info()
    # input(f"{lg}Press Enter to proceed to the next step...{rs}")

    # print("\nStage 3: Asking user for the number of messages.")
    number_of_messages = get_number_of_messages()
    # input(f"\nPress Enter to proceed to the next step...")

    print(f"\n{w}Stage 4: Extracting sticker set length.")
    client = authenticated_client(profiles)
    if client is None:
        print("Failed to authenticate client. Exiting.")
        return
    sticker_length = get_sticker_set_length(client, sticker_name)
    time.sleep(0.5)
    # input("Press Enter to proceed to the next step...")

    print(f"\n{w}Stage 5: Adding stickers to msg.txt file.")
    add_stickers_to_file(file_path, sticker_length)
    print("Stickers added successfully.")
    time.sleep(0.5)
    # input("Press Enter to proceed to the next step...")

    print(f"\n{w}Stage 6: Counting media files in the media folder.")
    jpg_count, mp4_count = count_media_files(media_path)
    print(f"{lg}Found {jpg_count} JPG files and {mp4_count} MP4 files.{rs}")
    time.sleep(0.5)
    # input("Press Enter to proceed to the next step...")

    print(f"\n{w}Stage 7: Renaming JPG files.")
    last_jpg_number = rename_jpg_files(media_path)
    print(f"{lg}Renamed JPG files up to med{last_jpg_number}.jpg{rs}")
    time.sleep(0.5)
    # input("Press Enter to proceed to the next step...")

    print(f"\n{w}Stage 8: Renaming MP4 files starting from med{last_jpg_number + 1}.")
    rename_mp4_files(media_path, last_jpg_number)
    print(f"{lg}MP4 files renamed successfully.{rs}")
    time.sleep(0.5)
    # input("Press Enter to proceed to the next step...")

    print(f"\n{w}Stage 9: Adding media files to msg.txt.")
    media_count = add_media_to_file(file_path, media_path, jpg_count, mp4_count)
    print(f"{lg}{media_count} Media files added successfully.{rs}")
    # input("Press Enter to proceed to the next step...")

    print(f"\n{w}Stage 10: Duplicating messages in msg.txt.")
    duplicate_messages(file_path, number_of_messages)
    print(f"{lg}Messages duplicated successfully\n{rs}.")

if __name__ == "__main__":
    main()