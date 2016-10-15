#! /usr/bin/env python
"""
InDataExchange (0x40) command example.
"""
from __future__ import print_function
from __future__ import unicode_literals
from smartcard.System import readers
from enum import Enum
from pn532_reader import Pn532Reader, Pn532Modulation
from list_targets import list_target


class MifareError(Enum):
    # Time out, the target has not answered
    TIME_OUT = 0x01
    # A CRC error has been detected by the contactless UART
    CRC = 0x02
    # A Parity error has been detected by the contactless UART
    PARITY = 0x03
    # During a MIFARE anticollision/select
    # operation an erroneoes Bit Count has been detected
    ANTICOLLISION = 0x04
    # Framing error during MIFARE operation
    FRAMING = 0x05
    # An abnormal bit-collision has been detected
    # during bit wise anticollision at 106 kbps"
    BIT_COLLISION = 0x06
    # Communication buffer size insufficient
    BUFFER_SIZE = 0x07
    # RF Buffer overflow has been detected by the contactless UART
    BUFFER_OVERFLOW = 0x09
    # In active communication mode, the RF field has not been
    # switched on in time the counterpart (as definied in NFCIP-1 standard)
    ERROR_0A = 0x0A
    # RF Protocol error
    ERROR_0B = 0x0B
    # Temperature error
    ERROR_0D = 0x0D
    # Internal buffer overflow
    ERROR_0E = 0x0E
    # Invalid parameter
    ERROR_10 = 0x11
    # DEP Protocol: unsupported command from the initiator
    ERROR_12 = 0x12
    # DEP Protocol/Mifare/ISO-14443-4:
    # The data format does not match the specification
    ERROR_13 = 0x13
    # Mifare: Authentification error
    ERROR_14 = 0x14
    # ISO 14443-3: UID Check byte wrong
    ERROR_24 = 0x24
    # DEP Protocol: Invalid device state
    ERROR_25 = 0x25
    # Operation not allowed in the configuration
    ERROR_26 = 0x26
    # This command is not acceptable due to the current context of the PN531
    ERROR_27 = 0x27
    # The PN531 configured as a target has been released by its initiator
    ERROR_29 = 0x29


def data_exchange_authentication(pn532_reader):
    # Turns on the antenna power
    command_str = "32 01 00"
    response_str = pn532_reader.send_apdu_str(command_str)
    print("response_str:", response_str)
    # Turns off the antenna power
    command_str = "32 01 01"
    response_str = pn532_reader.send_apdu_str(command_str)
    print("response_str:", response_str)
    # 3) InListPassivTargets (0x4A)
    command_str = "4A 01 00"
    response_str = pn532_reader.send_apdu_str(command_str)
    print("response_str:", response_str)
    # 4) Mifare auth (0x60) via InDataExchange (0x40)
    command_str = "40 01 60 07 FF FF FF FF FF FF 12 67 58 32"
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
    data_exchange_authentication(pn532_reader)

if __name__ == "__main__":
    main()
