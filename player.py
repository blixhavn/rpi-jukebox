import RC522
import requests
import time
import flicklib

from RC522_NTAG21X import RC522_NTAG21X

def main():
    reader = RC522_NTAG21X()

    while True:
        status = -1
        while status != RC522.OK:
            status, msg = reader.read_blocking()
            sleep(0.01)

        
        requests.get(f'http://192.168.0.181:5005/Stue/spotify/now/{msg}')

@flicklib.airwheel()
def volume_ctrl(delta)
    print(delta)

if __name__ == '__main__':
    main()