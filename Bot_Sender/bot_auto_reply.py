'''
This Script Uses Created Bot to AUTO REPLY to messages if the message is found in the tsv file
'''

import requests
import pandas as pd
import time

url = './Bot_Sender/chitchat.tsv'

df = pd.read_csv(url, sep="\t")
time.sleep(2)

df.head(5)

base_url = "https://api.telegram.org/bot6203005709:AAE2UnuHWrsIRcvs2cmYQTr-c3Dv58l8fiw"
chat_id = "-1002110023895"

msg_content = ''
last_message_id = None  # Variable to store the ID of the last processed message


def read_msg(offset):
  global msg_content
  global last_message_id

  parameters = {
      "offset" : offset,
      "timeout": 60  # Long polling timeout
  }

  while True:
    resp = requests.get(base_url + "/getUpdates", params=parameters)
    updates = resp.json()["result"]
    data = resp.json()


    if updates:  # Check if there are any new updates
        # Find the highest 'update_id' among the received updates
        new_offset = max(update['update_id'] for update in updates) + 1

        # Process updates here
        # For example, print messages or do something with the updates.
        for update in updates:
            print("++++++++++++++++++++++++")
            print(update)  # Process or print the full update
        
            # Check if the message ID is the same as the last processed message
            if last_message_id == update['message']['message_id']:
                continue  # Skip processing this message and wait for the next one

            last_message_id = update['message']['message_id']  # Update the last message ID

            # Process the message
            if 'message' in update and 'text' in update['message']:
                msg_content = update['message']
                text_content = update['message']['text']
                text = msg_content["text"]

                #print(f"The TEXT content is : {str(text_content)} ")
                print("======")
                auto_reply = auto_answer(text)
                if auto_reply != False:
                    print("Found this question")
                    print(f"Matched Question : {text}")
                    send_msg(msg_content)
                    continue
                else:
                  pass
                    #print("No match found for the question.")


        # Update the offset to only request newer updates next time
        parameters["offset"] = new_offset
        print("++++++++++++++++++++++++\n\n")
    else:
      print("No New Updates\n")
      pass


def auto_answer(text_content):
    # Convert all questions to lowercase for case-insensitive comparison
    questions = df['Question'].str.lower()

    # Check if text_content matches any question
    match_index = questions[questions == text_content.lower()].index

    if not match_index.empty:
        # If a match is found, return the corresponding answer
        return df.loc[match_index[0], 'Answer']
    else:
      print("Sorry, I couldn't find an answer to your question.")
      return False

def send_msg(msg_content):
    text = msg_content["text"]
    message_id = msg_content['message_id']
    answer = auto_answer(text)

    parameters = {
        "chat_id": chat_id,
        "text": answer,
        "reply_to_message_id": message_id
    }

    resp = requests.get(base_url + "/sendMessage", data=parameters)
    #print(resp.text)

offset = 0

while True:
  offset = read_msg(offset)
