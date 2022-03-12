import imaplib
import os.path
from pynotifier import Notification
import json
import time

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
cache_file_path = os.path.join(os.path.expanduser('~'), '.cache', 'gmailnotipy.json')
accounts_file_path = os.path.join(os.path.expanduser('~'), '.config', 'gmailnotipy.json')
icon_path = '/usr/share/icons/Papirus/48x48/apps/gmail.svg'#os.path.join(os.path.dirname(__file__), 'gmail.svg')

def listen_new_email(username, password):

  last_msg_ids = {}
  if os.path.exists(cache_file_path):
    last_msg_ids = json.load(open(cache_file_path, 'r'))

  server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
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
  config = json.load(open(accounts_file_path, 'r'))
  interval = config['interval']
  accounts = config['accounts']
  while True:
    try:
      for i in accounts:
        print('checking', i['username'])
        listen_new_email(i['username'], i['password'])
      print('sleep', interval)
      time.sleep(interval)
    except Exception as ex:
      print(ex)

if __name__=="__main__":
  main()