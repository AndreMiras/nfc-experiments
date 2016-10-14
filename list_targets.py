#! /usr/bin/env python
"""
InListPassivTargets (0x4A) command example.
PN532 Command (InListPassiveTarget 212Kbps) = "D4 4A 01 01"
"""
from __future__ import print_function
from __future__ import unicode_literals
from smartcard.System import readers
from pn532_reader import Pn532Reader, Pn532Modulation, NfcModulation


def decode_target_data_iso14443a(target_data):
    response_header = target_data[0:2]
    response_header_str = "%02X %02X" % (
        response_header[0], response_header[1])
    tags_found = target_data[2]
    target_number = target_data[3]
    sens_res = target_data[4:6]
    sens_res_str = "%02X %02X" % (
        sens_res[0], sens_res[1])
    sel_res = target_data[6]
    uid_length = target_data[7]
    uid = target_data[8:8+uid_length]
    uid_str = " ".join(["%02X" % x for x in uid])
    print("response_header:", response_header_str)
    print("tags_found:", tags_found)
    print("target_number:", target_number)
    print("sens_res:", sens_res_str)
    print("sel_res:", sel_res)
    print("uid_length:", uid_length)
    print("uid:", uid_str)


def decode_target_data_iso14443b(target_data):
    raise NotImplemented('')


def decode_target_data(target_data, nfc_modulation):
    if nfc_modulation == NfcModulation.NMT_ISO14443A:
        decode_target_data_iso14443a(target_data)
    elif nfc_modulation == NfcModulation.NMT_ISO14443B:
        decode_target_data_iso14443b(target_data)
    else:
        raise NotImplemented('')


def run(pn532_reader):
    # 0x32 RFConfiguration
    # Turn on the antenna power
    command_str = "32 01 01"
    response_str = pn532_reader.send_apdu_str(command_str)
    # print("response_str: %s" % response_str)

    # 0x4A InListPassivTargets
    command_str = "4A 01 %02X" % (Pn532Modulation.PM_ISO14443A_106.value)
    # command_str = "4A 01 %02X 00" % (Pn532Modulation.PM_ISO14443B_106.value)
    response_str = pn532_reader.send_apdu_str(command_str)
    response = [int(x, 16) for x in response_str.split()]
    print("response: %s" % response_str)
    decode_target_data(response, NfcModulation.NMT_ISO14443A)
    # 0x32 RFConfiguration
    # Turn off the antenna power
    command_str = "32 01 00"
    response_str = pn532_reader.send_apdu_str(command_str)
    # print("response_str: %s" % response_str)


def main():
    # gets all the available readers
    pcsc_readers = readers()
    print("Available readers: %s" % pcsc_readers)
    reader = pcsc_readers[0]
    print("Using reader: %s" % reader)
    pn532_reader = Pn532Reader(reader)
    pn532_reader._debug = False
    run(pn532_reader)

if __name__ == "__main__":
    main()
