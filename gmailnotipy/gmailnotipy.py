import imaplib
import os.path
from pynotifier import Notification
import json

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
cache_file_path = os.path.join(os.path.expanduser('~'), '.cache', 'gmailnotipy.json')
accounts_file_path = os.path.join(os.path.expanduser('~'), '.config', 'gmailnotipy.json')
icon_path = os.path.join(os.path.dirname(__file__), 'gmail.svg')

def listen_new_email():

  last_msg_ids = {}
  if os.path.exists(cache_file_path):
    last_msg_ids = json.load(open(cache_file_path, 'r'))

  for i in json.load(open(accounts_file_path, 'r')):
    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    username = i['username']
    password = i['password']
    server.login(username, password)
    server.select(readonly=True)
    result, data = server.search(None, 'UnSeen')
    for num in data[0].split():
      if int(num) > last_msg_ids.get(username,0):
        result, data = server.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT FROM DATE)])')
        data_dict = data[0][1].decode()

        Notification(title=username, description=data_dict, duration=10,
                     icon_path=icon_path).send()
        last_msg_ids[username] = int(num)
    json.dump(last_msg_ids, open(cache_file_path, 'w'))
    server.logout()

def main():
  listen_new_email()

if __name__=="__main__":
  main()