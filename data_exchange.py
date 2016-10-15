#! /usr/bin/env python
"""
InDataExchange (0x40) command example.
"""
from __future__ import print_function
from __future__ import unicode_literals
from smartcard.System import readers
from pn532_reader import Pn532Reader


def data_exchange(pn532_reader):
    # 0x40 InDataExchange
    command_str = "40 01 00 A4 04 00 05 FF FF FF FF FF 00"
    response_str = pn532_reader.send_apdu_str(command_str)
    print("response_str:", response_str)


def main():
    # gets all the available readers
    pcsc_readers = readers()
    print("Available readers: %s" % pcsc_readers)
    reader = pcsc_readers[0]
    print("Using reader: %s" % reader)
    pn532_reader = Pn532Reader(reader)
    pn532_reader._debug = False
    pn532_reader._debug = True
    data_exchange(pn532_reader)

if __name__ == "__main__":
    main()
