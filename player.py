import RC522
import requests
import time
import threading
import flicklib

from RC522_NTAG21X import RC522_NTAG21X

volume = 10
vol_delta = 0

def read_album():
    reader = RC522_NTAGX()

    while True:
        nfc_status = -1
        while nfc_status != RC522.OK:
            nfc_status, msg = reader.read_blocking()
            time.sleep(0.05)

        requests.get(f'http://192.168.0.181:5005/Stue/spotify/now/{msg}')

@flicklib.airwheel()
def volume_ctrl(delta):
    global vol_delta

    vol_delta += round(delta/200, 2)

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

    volume += vol_delta
    if vol_delta != 0:
        new_vol = int(volume)
        requests.get(f'http://192.168.0.181:5005/Stue/volume/{new_vol}')
        print(f"Volume: {new_vol}")
    vol_delta = 0


def main():
    try:
        nfc_thread = threading.Thread(target=read_album)
        nfc_thread.start()

        while True:
            update_volume()

            sleep(0.1)
    finally:
        nfc_thread.join()

if __name__ == '__main__':
    main()
