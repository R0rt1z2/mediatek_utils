import sys
import struct
import re

# Program Version.
_VERSION_ = 1.1

# Start Offset of all the different headers.
EMMC_HDR_START = 0x0
BRLYT_HDR_START = 0x200
BROM_HDR_START = 0x800

def logi(s):
    """ Prints log info.
        :returns: nothing."""
    print("[?] {}".format(s))

def logw(s):
    """ Prints log warnings.
        :returns: nothing."""
    print("[!] {}".format(s))

def loge(s):
    """ Prints log error.
        :returns: nothing."""
    print("[-] {}".format(s))

def logs(s):
    """ Prints log succeed.
        :returns: nothing."""
    print("[+] {}".format(s))

def u32_le(x):
    """ Unpacks a Little Endian 32 bit value.
        :returns: the unpacked value."""
    return struct.unpack("<I", x)[0]

def u16_le(x):
    """ Unpacks a Little Endian 16 bit value.
        :returns: the unpacked value."""
    return struct.unpack("<H", x)[0]

def u8_le(x):
    """ Unpacks a Little Endian 8 bit value.
        :returns: the unpacked value."""
    return struct.unpack("<H", b'\x00' + x)[0]

def pchar(x):
    """ Parses and decodes a string inside given bytes.
        :returns: the parsed string."""
    return str(x.decode('ascii'))

def bfhx(x):
    """ Parses the bytes from a given hex value using
        the built-in "bytes.fromhex()" method.
        :returns: the converted bytes."""
    return bytes.fromhex(x)

def parse_gen_header(preloader):
    """ Parses and prints the header for NOR/SD/eMMC.
        :returns: nothing."""
    preloader.seek(EMMC_HDR_START)
    print("Name = {}".format(pchar(preloader.read(12))))
    print("Version = {}".format(u32_le(preloader.read(4))))
    print("Size = {}".format(u32_le(preloader.read(4))))

def parse_brlyt(preloader):
    """ Parses and prints the BootROM layout header.
        :returns: nothing."""
    preloader.seek(BRLYT_HDR_START)
    print("Name = {}".format(pchar(preloader.read(8))))
    print("Version = {}".format(u32_le(preloader.read(4))))
    print("Size = {}".format(u32_le(preloader.read(4))))
    print("Total Size = {}".format(u32_le(preloader.read(4))))
    print("Magic = {}".format(u32_le(preloader.read(4))))
    print("Type = {}".format(u32_le(preloader.read(4))))
    print("Second Size = {}".format(u32_le(preloader.read(4))))
    print("Second Total Size = {}".format(u32_le(preloader.read(4))))

def parse_gfh_common_header(preloader):
    """ Parses and prints the BootROM header definitions.
        :returns: nothing."""
    preloader.seek(BROM_HDR_START)
    print("Magic = {}".format(pchar(preloader.read(3))))
    print("Version = {}".format(u8_le(preloader.read(1))))
    print("Size = {}".format(u16_le(preloader.read(2))))
    print("Type = {}".format(u16_le(preloader.read(2))))

def parse_file_info(preloader):
    """ Parses and prints the File Info header.
        :returns: nothing."""
    preloader.seek(BROM_HDR_START + 8) # Skip the gfh common header
    print("Name = {}".format(pchar(preloader.read(12)))) # FILE_INFO
    preloader.read(4) # Skip unused bytes
    print("File Type = {}".format(u16_le(preloader.read(2))))
    print("Flash Type = {}".format(u8_le(preloader.read(1))))
    print("Sig Type = {}".format(u8_le(preloader.read(1))))
    print("Load Address = 0x%X" % u32_le(preloader.read(4)))
    print("Total Size = {}".format(u32_le(preloader.read(4))))
    print("Max Size = {}".format(u32_le(preloader.read(4))))
    print("Header Size = {}".format(u32_le(preloader.read(4))))
    print("Signature Type = {}".format(u32_le(preloader.read(4))))
    print("Jump Offset = {}".format(u32_le(preloader.read(4))))
    print("Proccessed = {}".format(u32_le(preloader.read(4))))

def main():
    print("")
    logi("MediaTek Preloader Parser - R0rt1z2 - v{}\n".format(_VERSION_))
    logi("Selected file: {}\n".format(sys.argv[1]))
    logi("Opening {}...\n".format(sys.argv[1]))
    try:
        preloader = open(sys.argv[1], "rb")
    except FileNotFoundError:
        loge("Cannot open {}!\n".format(sys.argv[1]))
        return -1
    logi("Parsing the header for NOR/SD/eMMC...") 
    parse_gen_header(preloader)
    print("")
    logi("Parsing the BootROM layout header...")
    parse_brlyt(preloader)
    print("")
    logi("Parsing the BootROM header definitions...")
    parse_gfh_common_header(preloader)
    print("")
    logi("Parsing the File Info header...")
    parse_file_info(preloader)
    print("")

main()
