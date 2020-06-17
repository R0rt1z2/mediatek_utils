#!/usr/bin/env python3
##############################################
# Searches and cuts off the header of the LK #
##############################################

import sys
import os.path

LK_HEADER = b'\x07\x00\x00\xea'
PL_HEADER = 0x800

def get_offset(data):
    offset = data.find(LK_HEADER)
    if offset == -1:
        print("[-] Cannot find the end of the header! Is this an LK?")
        exit(1)
    print("[?] Header size is {} bytes.".format(offset))
    return offset

def cut_header(image, out, offset):
    with open(image, 'rb') as in_file:
        with open(out, 'wb') as out_file:
           out_file.write(in_file.read()[offset:])
    print("[+] Header Remove Complete. Output: {}!".format(out))

def main():
    if os.path.isfile(file):
        with open(file, "rb") as lk:
            data = lk.read()
        if "lk" in sys.argv[1]:
            offset = get_offset(data)
            cut_header(file, "cutted_lk.img", offset)
        elif "pl" in sys.argv[1]:
            cut_header(file, "cutted_pl.img", PL_HEADER)
        else:
            print("[?] USAGE: python3 cutter.py lk/pl image.img")
            exit(1)
    else:
        print("[-] Cannot open {}!".format(file))
        exit(1)

if __name__ == '__main__':
    file = sys.argv[2]
    main()
