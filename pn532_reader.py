#! /usr/bin/env python
"""
InListPassivTargets (0x4A) command example.
PN532 Command (InListPassiveTarget 212Kbps) = "D4 4A 01 01"
"""
from __future__ import print_function
from __future__ import unicode_literals


class Pn532Reader(object):

    def __init__(self, pcsc_reader):
        self.connection = pcsc_reader.createConnection()
        self.connection.connect()

    def transmit(self, command):
        command_str = " ".join(["%02X" % x for x in command])
        print("> %s" % command_str)
        data, sw1, sw2 = self.connection.transmit(command)
        data_str = " ".join(["%02X" % x for x in data])
        print("< [%s] %02X %02X" % (data_str, sw1, sw2))

    def transmit_str(self, command_str):
        command = [int(x, 16) for x in command_str.split()]
        self.transmit(command)

def main():
    from smartcard.System import readers
    # gets all the available readers
    pcsc_readers = readers()
    print("Available readers: %s" % pcsc_readers)
    reader = pcsc_readers[0]
    print("Using reader: %s" % reader)
    pn532_reader = Pn532Reader(reader)

if __name__ == "__main__":
    main()

