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
    target_number = target_data[3]
    sens_res = target_data[4:6]
    sens_res_str = "%02X %02X" % (
        sens_res[0], sens_res[1])
    sel_res = target_data[6]
    uid_length = target_data[7]
    uid = target_data[8:8+uid_length]
    uid_str = " ".join(["%02X" % x for x in uid])
    print("target_number:", target_number)
    print("sens_res:", sens_res_str)
    print("sel_res:", sel_res)
    print("uid_length:", uid_length)
    print("uid:", uid_str)


def decode_target_data_iso14443b(target_data):
    target_number = target_data[3]
    # Store the PUPI (Pseudo-Unique PICC Identifier)
    pupi = target_data[5:9]
    pupi_str = " ".join(["%02X" % x for x in pupi])
    # Store the Application Data
    application_data = target_data[9:13]
    application_data_str = " ".join(["%02X" % x for x in application_data])
    # Store the Protocol Info
    protocole_info = target_data[13:16]
    protocole_info_str = " ".join(["%02X" % x for x in protocole_info])
    # TODO: handle the Card IDentifier just like the pn53x.c
    """
    // We leave the ATQB field, we now enter in Card IDentifier
    szAttribRes = *(pbtRawData++);
    if (szAttribRes) {
      pnti->nbi.ui8CardIdentifier = *(pbtRawData++);
    }
    """
    print("target_number:", target_number)
    print("pupi:", pupi_str)
    print("application_data:", application_data_str)
    print("protocole_info:", protocole_info_str)


def decode_target_data_header(target_data):
    response_header = target_data[0:2]
    response_header_str = "%02X %02X" % (
        response_header[0], response_header[1])
    tags_found = target_data[2]
    print("response_header:", response_header_str)
    print("tags_found:", tags_found)
    return tags_found


def decode_target_data(target_data, nfc_modulation):
    tags_found = decode_target_data_header(target_data)
    if tags_found < 1:
        return
    if nfc_modulation == NfcModulation.NMT_ISO14443A:
        decode_target_data_iso14443a(target_data)
    elif nfc_modulation == NfcModulation.NMT_ISO14443B:
        decode_target_data_iso14443b(target_data)
    else:
        raise NotImplementedError('')


def pn_to_nfc_modulation(pn532_modulation):
    if pn532_modulation == Pn532Modulation.PM_ISO14443A_106:
        return NfcModulation.NMT_ISO14443A
    elif pn532_modulation == Pn532Modulation.PM_ISO14443B_106:
        return NfcModulation.NMT_ISO14443B
    raise NotImplementedError(
        '%s modulation not implemented' % pn532_modulation)


def list_target(pn532_reader, pn532_modulation):
    print("pn532_modulation:", pn532_modulation)
    # Turns on the antenna power
    # 0x32 RFConfiguration
    command_str = "32 01 01"
    response_str = pn532_reader.send_apdu_str(command_str)
    # Sets the Retry Time to one
    # 0x32 RFConfiguration
    command_str = "32 05 00 00 00"
    response_str = pn532_reader.send_apdu_str(command_str)

    # 0x4A InListPassivTargets
    command_str = "4A 01 %02X" % (pn532_modulation.value)
    # command_str = "4A 01 %02X 00" % (Pn532Modulation.PM_ISO14443B_106.value)
    if pn532_modulation == Pn532Modulation.PM_ISO14443B_106:
        # optional initiator data (used for Felica, ISO14443B,
        # Topaz Polling or for ISO14443A selecting a specific UID)
        command_str += " 00"
    response_str = pn532_reader.send_apdu_str(command_str)
    response = [int(x, 16) for x in response_str.split()]
    nfc_modulation = pn_to_nfc_modulation(pn532_modulation)
    decode_target_data(response, nfc_modulation)
    # Turns off the antenna power
    # 0x32 RFConfiguration
    command_str = "32 01 00"
    response_str = pn532_reader.send_apdu_str(command_str)


def list_targets(pn532_reader):
    """
    List targets for all supported modulations.
    """
    pn532_modulations = [
        Pn532Modulation.PM_ISO14443A_106,
        Pn532Modulation.PM_ISO14443B_106,
    ]
    for pn532_modulation in pn532_modulations:
        list_target(pn532_reader, pn532_modulation)


def main():
    # gets all the available readers
    pcsc_readers = readers()
    print("Available readers: %s" % pcsc_readers)
    reader = pcsc_readers[0]
    print("Using reader: %s" % reader)
    pn532_reader = Pn532Reader(reader)
    pn532_reader._debug = False
    list_targets(pn532_reader)

if __name__ == "__main__":
    main()
