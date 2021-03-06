import os.path
import sys
import urllib.request
import re
import progressbar
from urllib.error import HTTPError
from gmusicapi import Mobileclient
from time import sleep

api = Mobileclient()

mail = sys.argv[1]
psw = sys.argv[2]
device_id = sys.argv[3]

print('/full/path/to/music/ / at the end required')
path = input()

login = api.login(mail, psw, device_id)
library = api.get_all_songs()
p_iter = -100/len(library)
bar = progressbar.ProgressBar().start()

for i in range(len(library)):
    sleep(0.2)

    filename = '{}{}{}{}'.format(path,
                                     library[i].get('artist'), '-', library[i].get('title'))
    songname = library[i].get('artist') + '-' + library[i].get('title')
    p_iter = p_iter + 100/len(library)

    try:
        if os.path.exists(filename) == True:
            print('\n File {} already exist'.format(songname))
            bar.update(p_iter)
        else:
            try:
                url = api.get_stream_url(library[i].get('storeId'))
                print('\n Downloading {}'.format(songname))
                urllib.request.urlretrieve(url, filename)
                bar.update(p_iter)
            except ValueError:
                bar.update(p_iter)
                pass

    except HTTPError as e:
        if e.response.status_code == 403 or 503:
            sleep(1)
            print('\n Downloading {}'.format(songname))
            urllib.request.urlretrieve(url, filename)
            bar.update(p_iter)

bar.finish()
