#! /usr/bin/env python
"""
InListPassivTargets (0x4A) command example.
PN532 Command (InListPassiveTarget 212Kbps) = "D4 4A 01 01"
"""
from __future__ import print_function
from __future__ import unicode_literals
from smartcard.System import readers
from pn532_reader import Pn532Reader


def run(pn532_reader):
    DIRECT_TRANSMIT_CLASS = 0xFF
    DIRECT_TRANSMIT_INS = 0x00
    DIRECT_TRANSMIT_P1 = 0x00
    DIRECT_TRANSMIT_P2 = 0x00
    DIRECT_TRANSMIT_COMMAND_PREFIX = "%s %s %s %s" % (
        DIRECT_TRANSMIT_CLASS,
        DIRECT_TRANSMIT_INS,
        DIRECT_TRANSMIT_P1,
        DIRECT_TRANSMIT_P2,
    )

    COMMAND_STR = "%s 04 D4 32 01 00" % (DIRECT_TRANSMIT_COMMAND_PREFIX)
    pn532_reader.transmit_str(COMMAND_STR)

    COMMAND_STR = "FF C0 00 00 04"
    pn532_reader.transmit_str(COMMAND_STR)

    COMMAND_STR = "%s 04 D4 32 01 01" % (DIRECT_TRANSMIT_COMMAND_PREFIX)
    pn532_reader.transmit_str(COMMAND_STR)

    COMMAND_STR = "FF C0 00 00 04"
    pn532_reader.transmit_str(COMMAND_STR)

    # 4A InListPassivTargets
    COMMAND_STR = "%s 04 D4 4A 01 00" % (DIRECT_TRANSMIT_COMMAND_PREFIX)
    pn532_reader.transmit_str(COMMAND_STR)

    COMMAND_STR = "FF C0 00 00 0E"
    pn532_reader.transmit_str(COMMAND_STR)


def main():
    # gets all the available readers
    pcsc_readers = readers()
    print("Available readers: %s" % pcsc_readers)
    reader = pcsc_readers[0]
    print("Using reader: %s" % reader)
    pn532_reader = Pn532Reader(reader)
    run(pn532_reader)

if __name__ == "__main__":
    main()
