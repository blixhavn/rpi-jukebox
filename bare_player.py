import datetime
import RC522
import requests
import time

from RC522_NTAG21X import RC522_NTAG21X

volume = 11
vol_delta = 0
currently_playing = ''
scan_timestamp = datetime.datetime.now()

def read_album():
    global currently_playing

    reader = RC522_NTAG21X()

    while True:
        nfc_status = -1
        while nfc_status != RC522.OK:
            nfc_status, msg = reader.read_blocking()

        scan_timestamp = datetime.datetime.now()
        if currently_playing != msg:
            print("Playing from NFC")
            currently_playing = msg

            requests.get(f'http://192.168.0.181:5005/Stue/volume/{volume}')
            requests.get(f'http://192.168.0.181:5005/Stue/clearqueue')
            requests.get(f'http://192.168.0.181:5005/Stue/spotify/now/{msg}')

def main():
    read_album()

if __name__ == '__main__':
    main()
