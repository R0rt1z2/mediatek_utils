#!/usr/bin/env python3
##############################################
# Searches and cuts off the header of the LK #
##############################################

import sys
import os.path

HEADER = b'\x07\x00\x00\xea'

def get_offset(data):
    offset = data.find(HEADER)
    if offset == -1:
        print("[-] Cannot find the end of the header! Is this an LK?")
        exit(1)
    print("[?] Header size is {} bytes.".format(offset))
    return offset

def cut_header(in_file, out_file, offset):
    with open(in_file, 'rb') as in_file:
        with open(out_file, 'wb') as out_file:
           out_file.write(in_file.read()[offset:])
    print("[+] Header Remove Complete. Output: cutted_lk.img!")

def main():
    if os.path.isfile(file):
        with open(file, "rb") as lk:
            data = lk.read()
        offset = get_offset(data)
        cut_header(file, "cutted_lk.img", offset)
    else:
        print("[-] Cannot open {}!".format(file))
        exit(1)

if __name__ == '__main__':
    file = sys.argv[1]
    main()
