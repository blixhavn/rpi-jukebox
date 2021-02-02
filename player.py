import RC522
import requests
import time
import threading
import flicklib

from RC522_NTAG21X import RC522_NTAG21X

volume = 11
vol_delta = 0

def read_album():
    reader = RC522_NTAG21X()

    while True:
        nfc_status = -1
        while nfc_status != RC522.OK:
            nfc_status, msg = reader.read_blocking()

        print("Playing from NFC")
        requests.get(f'http://192.168.0.181:5005/Stue/clearqueue')
        requests.get(f'http://192.168.0.181:5005/Stue/spotify/now/{msg}')

@flicklib.airwheel()
def volume_ctrl(delta):
    global vol_delta

    # Divide the delta value by a magic number, to get a reasonable rate of change
    vol_delta += round(delta/100, 2)

@flicklib.flick()
def next_prev(start, finish):
    print(start + ' - ' + finish)
    if start == 'east' and finish == 'west':
        requests.get(f'http://192.168.0.181:5005/Stue/next')
    elif start == 'west' and finish == 'east':
        requests.get(f'http://192.168.0.181:5005/Stue/previous')


def update_volume():
    global volume
    global vol_delta

    old_vol = int(volume)
    volume += vol_delta
    new_vol = int(volume)
    if old_vol != new_vol:
        requests.get(f'http://192.168.0.181:5005/Stue/volume/{new_vol}')
        print(f"Volume: {new_vol}")
    vol_delta = 0


def main():
    try:
        nfc_thread = threading.Thread(target=read_album)
        nfc_thread.start()

        while True:
            update_volume()
            sleep(0.2)
    finally:
        nfc_thread.join()

if __name__ == '__main__':
    main()
