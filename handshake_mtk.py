import serial
from serial import *
import sys
import struct
import time
import glob
import os.path
import serial.tools.list_ports

magic = b'\xa0\x0a\x50\x05\xa0\x0a\x50\x05\xa0\x0a\x50\x05' # magic

hwid_list = {
   "MT65xx" : "2000",
   "MT6627" : "0003"
}

def main():
     """
        USAGE:
           handshake_mtk.py -d /dev/ttyACM* (if you're in win use COMX)
     """
     if sys.argv[1] == "-d":
          print("\n[?] Waiting for the device...\n")
          while os.path.exists(sys.argv[2]) != True:
               sys.stdout.write("."); sys.stdout.flush()
               time.sleep(0.1)
          ports = list(serial.tools.list_ports.comports())
          for port in ports:
              portHwid = port.hwid
          if hwid_list.get("MT6627") in portHwid:
             print("\n\n[?] BootROM connected? {}".format(portHwid))
             device = "bootROM"
          elif hwid_list.get("MT65xx") in portHwid:
             print("\n\n[?] Preloader connected? {}".format(portHwid))
             device = "Preloader"
          else:
             print("\n\n[?] Unknown device connected? {}".format(portHwid))
             device = "Unknown"          
          print("[?] Opening {}...".format(sys.argv[2]))
          s = serial.Serial(sys.argv[2])
          time.sleep(0.10)
          print("[+] Port Opened correctly (yay!)")
          print("[?] Try to handshake the device...")
          if device is "Unknown":
              print("[!] Attempt to write to an unknown device...")
          s.write(magic) # Write magic
          s.write(magic) # Complete the sequence
          bytes = s.read(5)
          if device is "bootROM":
             print("[?] Device returns: {}".format(bytes))
             print("[+] Handshake Complete!")
             print("[?] {} closed succsesfully!\n".format(sys.argv[2]))
             s.close()
             sys.exit(0)
          else:
              print("[?] Checking recieved bytes...")
              if bytes == b'READY':
                 print("[?] Device returns: {}".format(bytes))
                 print("[+] Handshake Complete!")
                 print("[?] {} closed succsesfully!\n".format(sys.argv[2]))
                 s.close()
                 sys.exit(0)
              else:
                 raise RuntimeError("ERROR: Device returned {} instead of expected data. Maybe the device is already handshaked?\n".format(bytes))
                 s.close()
                 sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
       raise RuntimeError("[-] Expected more arguments")
    main()
