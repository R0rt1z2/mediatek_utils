#!/usr/bin/env python3

import os
import struct
import sys
import traceback

MTK_BLOADER_INFO = b'MTK_BLOADER_INFO'
ROM_INFO = b'ROMINFO_v'
DATE_BYTES = b'Build'
HEADER_BYTES = b'EMMC_BOOT'
EMMC_FLASH_IMAGE = 0x0
MEDIATEK_BOOT_HEADER = 0x800
BOOT_SECTION_START = 0x214
MEDIATEK_FILE_INFO = 0x808

def check_emmc_boot(f):
    f.seek(0) # first byte
    header = f.read(0x9)
    print("Preloader Header: {}".format(header.decode("utf-8")))
    if header != HEADER_BYTES:
        header = False
        return header
    else:
        header = True
        return header

def read_date(f, data):
    offset = data.find(DATE_BYTES)
    f.seek(offset + 16)
    date = f.read(15)
    print("Preloader Date: {}".format(date.decode("utf-8")))

def read_bloader_info(f, data):
    offset = data.find(MTK_BLOADER_INFO)
    f.seek(offset + 17) # len(MTK_BLOADER_INFO) + '_'
    bloader_info = f.read(3)
    print("BLOADER_INFO Version: {}".format(bloader_info.decode("utf-8")))
    f.read(7) # bloader_info to pl name
    pl_name = f.read(40)
    print("Preloader Name: {}".format(pl_name.decode("utf-8")))

def read_platform(f, data):
    offset = data.find(ROM_INFO)
    f.seek(offset + 9)
    f.read(7)
    platform = f.read(6)
    print("Platform: {}".format(platform.decode("utf-8")))
    
def read_load_addr(f, header=False):
    f.seek(0)
    if header:
        f.read(MEDIATEK_BOOT_HEADER) #2048
    f.read(20) # "FILE_INFO"
    f.read(8) # file_ver, file_type, flash_dev, sig_type
    load_addr, = struct.unpack('<I', f.read(4))
    load_addr = "0x%X" % load_addr
    print("Preloader Load Address: {}".format(load_addr))
    
def main():
    data = f.read()
    header = check_emmc_boot(f)
    read_load_addr(f, header)
    read_date(f, data)
    read_bloader_info(f, data)
    read_platform(f, data)
    
if __name__ == '__main__':
    try:
        preloader = sys.argv[1]
        f = open(preloader, 'rb')
        main()
    except Exception:
        traceback.print_exc()
