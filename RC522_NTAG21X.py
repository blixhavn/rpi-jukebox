#!/usr/bin/env python

import time
import pigpio
import RC522
import logging
import os

class RC522_NTAG21X:
   """ Wrapper for the RC522 nfc reader class."""

   def __init__(self, spi_channel=0, speed=106e3, debug=False):

      current_dir = os.path.dirname(os.path.realpath(__file__))

      log_level = logging.DEBUG if debug else logging.ERROR
      logging.basicConfig(filename=os.path.join(current_dir, 'debug.log'), level=log_level)
      
      self.pi = pigpio.pi()
      if not self.pi.connected:
         msg = "Could not connect to GPIO (pigpio error)"
         logging.error(msg)
         raise Exception(msg)

      self.pcd = RC522.PCD(self.pi, spi_channel, speed)


   def card_present(self):
      ATQA=0
      UID=[]
      SAK=0

      status = RC522.ERR_NO_TAG

      while status != RC522.OK:
         self.pcd.ISO_StopCrypto()
         status, ATQA = self.pcd.ISO_Request()

         if status == RC522.OK:
            logging.debug("Card request, ATQA={}".format(ATQA))
            status, UID = self.pcd.ISO_Anticollision() # Get the UID of the card
            if status == RC522.OK:
               logging.debug("Card anticollision, UID=[{}, {}, {}, {}]".
                  format(UID[0], UID[1], UID[2], UID[3]))
               status, SAK = self.pcd.ISO_Select(UID)
               if status == RC522.OK:
                  logging.debug("Card select, SAK={}".format(SAK))
               else:
                  logging.debug("Card select failed,")
            else:
               logging.debug("Card anticollision failed,")
      logging.debug(status)

      return status, ATQA, UID, SAK


   def read_blocking(self):

      status, ATQA, UID, SAK = self.card_present()
      reply = []
      end_of_message = False

      # NTAG READ command takes page address and reads the following four pages.
      # Therefore, we only address every fourth page of the NTAG21X, stopping
      # after a completed NDEF message
      addr_range = [i*4 for i in range(1,222)]

      if status == RC522.OK:        
         for i in addr_range:
            if end_of_message:
               break

            status, block = self.pcd.MF_ReadBlock(i)
            if status != RC522.OK:
               return status, ''

            read_bytes = []
            for byte in block:
               # Byte value 254 indicates end of NDEF record
               if byte != 254:
                  reply.append(hex(byte)[2:])
               else:
                  end_of_message = True
                  break

      return_string = ''
      _, message = self.split_ndef_message(reply)
      for hex_byte in message:
         try:
            ascii_char = bytes.fromhex(hex_byte).decode('ascii')
         except ValueError:
            ascii_char = '?'
         return_string += ascii_char
      return status, return_string

   def split_ndef_message(self, message):
      # TODO: handle the NDEF header
      ndef_header = message[:12]
      data = message[12:]
      return ndef_header, data


if __name__ == '__main__':
   reader = RC522_NTAG21X()
   print("Waiting for card...")
   status, msg = reader.read_blocking()
   print(msg)