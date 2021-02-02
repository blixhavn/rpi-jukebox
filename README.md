# rpi-jukebox

This is a small repo put together to run my Raspberry Pi Zero jukebox. I'm using a [RC522 NFC](https://www.ebay.com/sch/i.html?_nkw=RC522) reader for NFC tag communication, and a [Flick gesture pad](https://uk.pi-supply.com/products/flick-zero-3d-tracking-gesture-phat-pi-zero) for volume control, play/pause and skipping songs.

Although python libraries do exist for the RC522 module, I couldn't get any of them to work properly or consistently with my tags. The library provided here is copied from a [forum post](https://www.raspberrypi.org/forums/viewtopic.php?t=171570#p1098821), and is as far as I can tell without a license. Please contact me if you are the owner of this library and have something to object.

I'm using the library with NXP Mifare Ultralight NTAG213 stickers, and can't guarantee that it will work for any other tags. (I have 100 tags that I thought were NTAG213 but which mysteriously won't even respond to the wakeup signal. Feel free to help me out there.)

As mentioned in the forum post, the library requires the pigpiod daemon to run - this can be achieved easily by enabling its service:`sudo systemctl enable pigpiod`. To start it once, run `sudo pigpiod`.

### Installation
The only dependency is `flicklib`. Instructions to install can be found [here](https://github.com/PiSupply/Flick/tree/master/flick).
Then, it's a matter of running the `player.py` file. This can be done [as a service](https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6) if you want some resilience (e.g. auto restart), or simply by running it in a [screen](https://linuxize.com/post/how-to-use-linux-screen/).

### License

Apart from the borrowed RC522 library, the code is MIT licensed. Have at it!
