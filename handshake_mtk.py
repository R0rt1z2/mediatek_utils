import serial
from serial import *
import sys
import struct
import time
import os.path
import serial.tools.list_ports

GET_VERSION = b"\xff"
GET_BL_VER  = b"\xfe"
GET_HW_VER  = b"\xfc"
GET_HW_CODE = b"\xfd"

HWID_LIST = {
   "MT65xx" : "2000",
   "MT6627" : "0003"
}

class Device(serial.Serial):

    def write8(self, command):
        self.flushInput()
        self.write(command)
        self.flush()
        return self.read(len(command))

    def check8(self, bytes, len):
        if bytes and len > 1:
            raise Exception("Only can check 1 byte of data")
        b_check = self.read(1)
        if b_check != bytes:
            raise Exception("Bytes doesn't match.")

def parse_platform(platform):
     platform = hex(platform)
     platform = "".join(reversed([platform[i:i+2] for i in range(0, len(platform), 2)]))
     platform = "MT{}".format(platform[:-2])
     return platform

def manage_ports(s, action):
     # Closes and opens specified port. s = port, action = close/open #
     if action is "close":
         s.close()
         print("[?] {} closed succsesfully!\n".format(sys.argv[2]))
         sys.exit(0)
     elif action is "open":
         print("[?] Opening {}...".format(s))
         s = Device(s)
         print("[+] Port Opened correctly!")
         return s
     else:
         print("[-] Unknown action: {}".format(action))

def serial_check(s, bytes, len): # serial, bytes, int
     # Checks specified bytes with a serial read with the specified lenght #
     print("[?] Checking bytes...") 
     bytes_to_check = s.read(len)
     if bytes_to_check != bytes:
            raise RuntimeError("ERROR: Device returned {} instead of expected data.\n".format(bytes_to_check))
     else:
            print("[?] Device returns: {}".format(bytes))

def check_device(ports):
    for port in ports:
       portHwid = port.hwid
       if HWID_LIST.get("MT6627") in portHwid:
           print("\n[?] BootROM connected? {}".format(portHwid))
           device = "bootROM"
           return device
       elif HWID_LIST.get("MT65xx") in portHwid:
           print("\n[?] Preloader connected? {}".format(portHwid))
           device = "Preloader"
           return device
       else:
           print("\n[?] Unknown device connected? {}".format(portHwid))
           device = "Unknown" 
           return device

def handshake(s, device):
     # Writes the magic cmd to the specified port to handshake it #
     print("[?] Try to handshake the device...")
     if device == "Unknown":
           print("[!] Attempt to write to an unknown device...")

     s.write8(b"\xA0")
     s.write8(b"\xA0")

     print("[?] Complete the sequence...")
     s.write8(b"\x0A")
     s.write8(b"\x50")
     s.write8(b"\x05")

     print("[+] Handshake Complete!")
         
def main():

     if sys.argv[1] == "-h":
          print("\n                          MediaTek Handshake Tool\n")
          print("     preloader_tool.py -d /dev/ttyACM0 ==> Handshake the specified port\n")

     elif sys.argv[1] == "-d":
          sys.stdout.write("\n[?] Waiting for the device...")

          while os.path.exists(sys.argv[2]) != True:
               sys.stdout.write("."); sys.stdout.flush()
               time.sleep(0.1)

          ports = list(serial.tools.list_ports.comports())   
      
          device = check_device(ports)

          s = manage_ports(sys.argv[2], "open")
          time.sleep(0.10)

          handshake(s, device)

          if device is "bootROM":
              manage_ports(s, "close")

          else:
              #serial_check(s, b'READY', 5)
              s.write8(GET_HW_CODE)
              platform, response = struct.unpack('hh', s.read(4))
              print("[?] Preloader reported platform: {}".format(parse_platform(platform)))
              manage_ports(s, "close")

     else:
          print("\n[-] Invalid option: {}\n".format(sys.argv[1]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
       print("[-] Expected more arguments\n")
    main()
