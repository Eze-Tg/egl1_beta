from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest, SendReactionRequest, SendMessageRequest
from telethon.tl.types import InputPeerChat
from telethon.sessions import StringSession

# GlObal variables
api_id = '28585380'
api_hash = '69f5809ab14a276b308cabf9a26db3c2'

def send_reaction():
    try:
        # Connect to Telegram
        with TelegramClient(StringSession(), api_id, api_hash) as client:
            # Get the group entity
            group = 't.me/centerfresh29'
            group_entity = client.get_entity(group)  # Replace 'YOUR_GROUP_ID' with the actual group ID
            
            if not isinstance(group_entity, InputPeerChat):
                print("Invalid group entity.")
                return
            
            group_name = group_entity.title
            
            # Get the last message in the group
            messages = client(GetHistoryRequest(peer=group_entity, limit=1))
            last_message = messages.messages[0]
            last_message_id = last_message.id
            
            # Reply to the last message
            reply_message = f"Replying to the last message in {group_name}."
            client(SendMessageRequest(peer=group_entity, message=reply_message, reply_to_msg_id=last_message_id))
            
            # Add reaction to the last message
            emoji = '👍'  # Replace with the emoji you want to use
            client(SendReactionRequest(peer=group_entity, msg_id=last_message_id, reaction=emoji))
            
            print("Reaction sent successfully!")
            
    except Exception as e:
        print(f"Failed to send reaction: {e}")

# Call the function to send the reaction
#session_string = 'reactionsession'
send_reaction()



I got the group Entity: Channel(id=2110023895, title='motivated', photo=ChatPhoto(photo_id=5911092030275174701, dc_id=4, has_video=False, stripped_thumb=b'\x01\x08\x08\xd0W\x7f8\xa9\r\x9c\xfe\x14QES%\x1f'), date=datetime.datetime(2024, 2, 5, 22, 57, 33, tzinfo=datetime.timezone.utc), creator=False, left=False, broadcast=False, verified=False, megagroup=True, restricted=False, signatures=False, min=False, scam=False, has_link=False, has_geo=False, slowmode_enabled=False, call_active=False, call_not_empty=False, fake=False, gigagroup=False, noforwards=False, join_to_send=False, join_request=False, forum=False, stories_hidden=False, stories_hidden_min=False, stories_unavailable=True, access_hash=3388658093562775025, username='centerfresh29', restriction_reason=[], admin_rights=None, banned_rights=None, default_banned_rights=ChatBannedRights(until_date=datetime.datetime(2038, 1, 19, 3, 14, 7, tzinfo=datetime.timezone.utc), view_messages=False, send_messages=False, send_media=False, send_stickers=False, send_gifs=False, send_games=False, send_inline=False, embed_links=False, send_polls=False, change_info=True, invite_users=False, pin_messages=True, manage_topics=False, send_photos=False, send_videos=False, send_roundvideos=False, send_audios=False, send_voices=False, send_docs=False, send_plain=False), participants_count=None, usernames=[], stories_max_id=None, color=None, profile_color=None, emoji_status=None, level=None)
