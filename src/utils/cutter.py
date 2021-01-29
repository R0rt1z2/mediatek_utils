#!/usr/bin/env python3
######################################################
# Searches and cuts off the header of MediaTek LK/PL #
######################################################

import sys

LK_HEADER = b'\x07\x00\x00\xea'

def main():
    if sys.argv[1] == "lk":
        offset = fp.read().find(LK_HEADER)
        if offset != -1:
            with open(sys.argv[2], "rb") as in_file:
                with open("cutted_lk.img", 'wb') as out_file:
                    out_file.write(in_file.read()[offset:])
            print("[+] All done, output image is cutted_lk.img")
        else:
            print("[-] Invalid LK offset ({})".format(offset))
    elif sys.argv[1] == "pl":
            with open(sys.argv[2], "rb") as in_file:
                with open("cutted_pl.img", 'wb') as out_file:
                    out_file.write(in_file.read()[0x800:])
            print("[+] All done, output image is cutted_pl.img")
    else:
        print("[!] Invalid option: {}".format(sys.argv[1]))

if __name__ == '__main__':
    try:
        fp = open(sys.argv[2], "rb")
    except IndexError as e:
        print("[-] Missing arguments: [pl/lk].")
        exit(1)
    except FileNotFoundError as e:
        print("[-] Invalid input file: {}".format(sys.argv[2]))
        exit(1)
    main()
