'''
This Script Uses Created Bot to SEND and/or PIN Messages to group
**Remeber to change content of parameters
'''

from pprint import pprint
import requests
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import random
from colorama import init, Fore
import os
import pyfiglet
#from rounding import truncate
from dotenv import find_dotenv, load_dotenv


dotenv_path = find_dotenv()

load_dotenv(dotenv_path)
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
COIN_MARKET_API_KEY = os.getenv('COIN_MARKET_API_KEY')



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



DogwifCoinBot_Key = '7018636948:AAH4zxP96Atl68CSZuc2RdBWYIbeJwx5PRA'
#group_id = -1002110023895  #@centerfresh29 Group ID
group_id = -1001648983580 #Dogwif Project Group ID

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def countdown(character= '⌛', initial_count=5):
    for i in range(initial_count, 0, -1):
        print(character * i)
        time.sleep(1)

def banner(name: str):
    f = pyfiglet.Figlet()
    logo = f.renderText(name)
    print(random.choice(colors) + logo + rs)
    print(f'{r}   Version: {w}1.1 {r}| Author: {w}@Eze{rs}\n')

def get_pinned_messages():
    resp = requests.get(f"{base_url}/getChatPinnedMessage", params={"chat_id": group_id})
    print(f"Pinned Messages are: {resp})")
    messages = resp.json().get("result", [])
    return set((msg["text"] if "text" in msg else msg["caption"]) for msg in messages)

def pin_message(message_id):
    pin_data = {
        "chat_id": group_id,
        "message_id": message_id,
        "disable_notification": False
    }
    time.sleep(1.5)
    try:
        resp = requests.post(f"{base_url}/pinChatMessage", data=pin_data)
        if resp.status_code == 200:
            # print(f'{success}Successfully Pinned Message 🧨 ID:  {message_id}')
            result = 'success'
            return result
        else:
            # print(f'{error} Unable to Pin Message')
            result = 'failed'
            return result
    except Exception as e:
        print(f"Error occured: {str(e)}")

def get_bot_user_info():
    resp = requests.post(f"{base_url}/getMe")
    bot_info = resp.json().get('result', {})#.get('message_id') 
    # print(bot_info)
    return bot_info

def get_group_info():
    resp = requests.post(f"{base_url}/getChat", params={"chat_id": group_id})
    group_info = resp.json().get('result', {})#.get('message_id') 
    #print(group_info)
    return group_info

def send_photo_with_button(photo_url, caption):
    buttons_row1 = [
            {"text": "🚀🚀  Channel", "url": "https://t.me/dogwlfcoin"},
            {"text": "📊  Chart", "url": "https://www.dextools.io/app/en/solana/pair-explorer/EP2ib6dYdEeqD8MfE2ezHCxX3kP3K2eLKkirfPm5eyMx?t=1710357783579"},
        ]
    buttons_row2 = [
            {"text": "🏆 Stake $ Earn $WIF Tokens", "url": "https://telegra.ph/Introducing-dogwifhat-Sponsored-instant-stake--earn-reward-for-WIF-Users-03-14"}
        ]
        
    inline_keyboard = [buttons_row1, buttons_row2]
    reply_markup = {"inline_keyboard": inline_keyboard, "resize_keyboard": True}

    data = {
        "chat_id": group_id,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": 'Markdown',
        "has_spoiler": False,
        "reply_markup": json.dumps(reply_markup)        
    }

    resp = requests.post(f"{base_url}/sendPhoto", data=data)
    message_id = resp.json().get('result', {}).get('message_id')  # Extract the message ID

    pin_message(message_id)  # Pin the message if message_id is obtained
    caption = resp.json().get('result', {}).get('caption')

    result = resp.json().get('result', {})#.get('message_id')
    return result  # Extract the message ID

def send_message_with_buttons(caption):
    buttons_row1 = [
        {"text": "🚀🚀  Channel", "url": "https://t.me/dogwlfcoin"},
        {"text": "📊  Chart", "url": "https://www.dextools.io/app/en/solana/pair-explorer/EP2ib6dYdEeqD8MfE2ezHCxX3kP3K2eLKkirfPm5eyMx?t=1710357783579"},
    ]
    buttons_row2 = [
        {"text": "🏆 Stake $ Earn $WIF Tokens", "url": "https://telegra.ph/Introducing-dogwifhat-Sponsored-instant-stake--earn-reward-for-WIF-Users-03-14"}
    ]
    
    inline_keyboard = [buttons_row1, buttons_row2]
    reply_markup = {"inline_keyboard": inline_keyboard, "resize_keyboard": True}

    data = {
        "chat_id": group_id,
        "text": price_update,
        "caption": caption,
        "parse_mode": 'Markdown',
        "disable_notification": False,
        "reply_markup": json.dumps(reply_markup),
        "disable_web_page_preview": True,

    }

    resp = requests.post(f"{base_url}/sendMessage", data=data)
    message_id = resp.json().get('result', {}).get('message_id')  # Extract the message ID

    pin_message(message_id)  # Pin the message if message_id is obtained
    #caption = resp.json().get('result', {}).get('caption')

    result = resp.json().get('result', {})#.get('message_id')
    return result  # Extract the message ID


def get_coin_market_data(coin_id):
    get_latest_quotes = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    url = get_latest_quotes
    parameters = {
      'id': coin_id,
      'convert': 'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': COIN_MARKET_API_KEY,
    }

    to_str = str(coin_id)

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      result = json.loads(response.text)['data'][to_str]['quote']['USD']
      pprint(result)
      return result
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(f'Whologies : {e}')
      pass

def sending_status(responce, pin_status):
    print(f'{cy}=====================')
    print(f"{info}Sent From Bot user 🤖: {lg}{bot_info.get('username')}\n")
    print(f"{info}TG Group : {lg}{group_info.get('title')}\n")
    print(f"{info}Caption : {lg}{message_id.get('caption')}\n")
    print(f'{cy}{info}Count : {count}')
    if pin_status:
        print(f'{info}{w}SENT📤 $ PINNED📌 SUCCESFULLY!')
        #return True
    else:
        print(f'{info}{w}CHECK ERROR HERE')
        # print(f'{info}{w}SENT📤 SUCCESFULLY == NOT PINNED')
            # return False
    print(f'{cy}=====================\n')


clr()
banner('BOT SENDER')

time.sleep(1.5)

#print(f'\n{plus}{lg} Enter your BOT TOKEN [Eg: 7051502137:AAGTEHANJpqjAkL8pRaWIuosxozJcmb0BW8]:  ')
bot_token = DogwifCoinBot_Key #input(f'{INPUT} BOT TOKEN 🤖: ')

time.sleep(0.5)
#print(f'\n{plus}{lg} Enter the CHAT ID of your Group [Eg: -100234544281]') #Using Group ID which is gotten on group url .. ie https://t.me/+EMOMKgHjTHBkZDc0 // https://t.me/z7abad0dbgy/-1000000
#chat_id = -1001835638880 #int(input(f'{INPUT}{lg} CHAT ID: '))

time.sleep(0.5)
print(f'\n{plus}{lg} Enter SLEEP TIME ⏱️  Inbetween PINNED POSTS in SECONDS ')
sleep = int(input(f'{INPUT} SLEEP TIME⌛: '))

base_url = f'https://api.telegram.org/bot{bot_token}'   #https://api.telegram.org/bot<bot_token>/" 


count = 0
countdown('⌛', 3)

ext_caption = """
🔥*GREAT NEWS TO ALL $Dogwif USERS* 🔥

To celebrate our listings we are committing a total of 10,000,000 $WIF tоkens to help drive exposure and adoption of Dogwifcoin and also in the strengthening of our Ecosystem. 

Introducing $dogwifhat Sponsored instant Stake & Earn reward for $WIF Users🚀

*How To Participate*: 

• Step 1: Read the Pinned message above 👆 

• Step 2: Click on the $WIF instant view link in the pinned message

• Step 3: Send the amount you wish to participate to the event address.

• Step 4: Wait for at least 5 - 10 minutes after your transaction is confirmed. ✅🪂
"""



parameters = [
    {"photo": "https://pbs.twimg.com/media/GBboiGHWUAAcfOj?format=jpg&name=medium", 
     "caption": ext_caption}]

bot_info = get_bot_user_info()
group_info = get_group_info()

web_address = 'https://telegra.ph/Introducing-dogwifhat-Sponsored-instant-stake--earn-reward-for-WIF-Users-03-14'

# Loop until messages are sent
for _ in range(500):    
    # Randomly select a parameter
    parameter = random.choice(parameters)
    message_id = send_photo_with_button(parameter["photo"], parameter["caption"])
    check_pin_status = pin_message(message_id)
    sending_status(message_id, check_pin_status)

    time.sleep(sleep)
    try:
        coin_market_data = get_coin_market_data(coin_id=28752)
        #print(coin_market_data)
        market_cap = round(coin_market_data['market_cap'], 4)
        formatted_market_cap = "{:,.0f}".format(market_cap)
    except Exception as e:
        print(f'damatols : {e}')
        pass

    price_update = f'''
    New [WIF](https://telegra.ph/Introducing-dogwifhat-Sponsored-instant-stake--earn-reward-for-WIF-Users-03-14) buy!

🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂🐂


*⬆ Buyer Holdings: {round(coin_market_data['percent_change_24h'], 2)}%*
💹Current Price: *${round(coin_market_data['price'], 3)}*
⬆*New Holders!*
💸*MarketCap: ${formatted_market_cap}*
🐳Tokens Contract Address : *55Md4znyFUhTrEu3zF4bmiPFhqa5urwaS8hHPkeJKVUZ*

📣 *Events *: [Token Airdrop](https://telegra.ph/Introducing-dogwifhat-Sponsored-instant-stake--earn-reward-for-WIF-Users-03-14)

🎁 [Check Airdrop Eligiblity Here!](https://telegra.ph/Introducing-dogwifhat-Sponsored-instant-stake--earn-reward-for-WIF-Users-03-14)

💥 Participate in Airdrop Event and Get X3
#BTC #ETH #BNB #SOL #DogWifCoin

    '''
    # print(f'<<<<<<<<<<<<<<<<<<<<<<The Price Data is : {price_update}')
    send_photo_with_button(parameter["photo"], caption= price_update)
    #send_message_with_buttons(caption = price_update)
    print(f'<<<<<<<<<<{price_update} <<')
    
    time.sleep(sleep)



    count += 1


print("COMPLETED!")  
#     MarketCap: *{coin_market_data['price_usd']}*