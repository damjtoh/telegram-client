# from telethon import TelegramClient

# # These example values won't work. You must get your own api_id and
# # api_hash from https://my.telegram.org, under API Development.
# api_id = 105158
# api_hash = '9eeea2ab5df259875d174dbddce9223d'
# phone = '+541150184194'

# client = TelegramClient('session_name', api_id, api_hash)
# client.connect()

# # # If you already have a previous 'session_name.session' file, skip this.
# # client.sign_in(phone=phone)
# # me = client.sign_in(code=36946)  # Put whatever code you received here.
# me = client.get_me()
# print(me.stringify())

# client.send_message('IFTTT', 'Hello! Talking to you from Telethon')
# # client.send_file('username', '/home/myself/Pictures/holidays.jpg')

# channel_from = client.get_entity("https://t.me/Cryptotguide")
# channel_to = client.get_entity("https://t.me/Cryptotguide")

# total, messages, senders = client.get_message_history(channel_from)
# for message in messages:
#   print(str(message))


#!/usr/bin/env python3
# A simple script to print all updates received

from getpass import getpass
from os import environ
# environ is used to get API information from environment variables
# You could also use a config file, pass them as arguments,
# or even hardcode them (not recommended)
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import UpdateNewChannelMessage, PeerChannel
from telethon.tl.functions.messages import ForwardMessagesRequest


def main():
    api_id = 105158
    api_hash = '9eeea2ab5df259875d174dbddce9223d'
    phone = '+541150184194'
    client = TelegramClient('session_name', api_id, api_hash, proxy=None, update_workers=4)

    print('INFO: Connecting to Telegram Servers...', end='', flush=True)
    client.connect()
    print('Done!')

    if not client.is_user_authorized():
        print('INFO: Unauthorized user')
        client.send_code_request(phone)
        code_ok = False
        while not code_ok:
            code = input('Enter the auth code: ')
            try:
                code_ok = client.sign_in(phone, code)
            except SessionPasswordNeededError:
                password = getpass('Two step verification enabled. Please enter your password: ')
                code_ok = client.sign_in(password=password)
    print('INFO: Client initialized succesfully!')

    CHANNEL_FROM = client.get_entity("https://t.me/TrdAR")
    # CHANNEL_FROM = client.get_entity("https://t.me/Cryptotguide")
    CHANNEL_TO = client.get_entity("telegram.me/joinchat/AAAAAEGV4HnGlRNMhIBnBw")
    peers_from = [
      client.get_input_entity("https://t.me/joinchat/AAAAAEqa813uKBVUOvVMhw"), 
      client.get_input_entity("https://t.me/joinchat/AAAAAEGV4HnGlRNMhIBnBw"),
      client.get_input_entity("https://t.me/edwardmorra_btc"),
      client.get_input_entity("https://t.me/Cryptotguide"),
      client.get_input_entity("https://t.me/Mrcryptoindia"),
      client.get_input_entity("https://t.me/coindetector"),
      client.get_input_entity("https://t.me/cryptobullet")
    ]
    print(str(peers_from))
    def update_handler(update):
      print(type(update))
      print(update)
      print("------------------")
      if isinstance(update, UpdateNewChannelMessage):
        # message_from = client.get_entity(PeerChannel(update.message.to_id))
        # print("From: "+str(update.message.to_id))
        try:
          for peer_from in peers_from:
            if update.message.to_id.channel_id != peer_from.channel_id:
              continue
            if "http" in str(update.message.message):
              continue
            peer_to = client.get_input_entity(PeerChannel(CHANNEL_TO.id))
            print("Message comming from channel id: "+str(update.message.to_id.channel_id))
            print("To: "+str(peer_from.channel_id))
            print("From: "+str(peer_to.channel_id))
            print("########\nMessage:")
            print(str(update.message.message))
            print("########\nMessage id:")
            print(str(update.message.id))
            print("########:")
            client(ForwardMessagesRequest(
                from_peer=peer_from,  # who sent these messages or what channel sent in?
                id=[update.message.id],  # which are the messages?
                to_peer=peer_to  # who or what channel are we forwarding them to?
            ))
        except Exception as ex:
          print("Error: "+str(ex))
      # client(ForwardMessagesRequest(
      #   from_peer=CHANNEL_FROM,  # who sent these messages or what channel sent in?
      #   id=[msg.id for msg in update.messages],  # which are the messages?
      #   to_peer=CHANNEL_TO  # who or what channel are we forwarding them to?
      # ))
      # print('Press Enter to stop this!')
    
    client.add_update_handler(update_handler)
    input('Press Enter to stop this!\n')

  


if __name__ == '__main__':
    main()
