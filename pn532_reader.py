#! /usr/bin/env python
"""
InListPassivTargets (0x4A) command example.
PN532 Command (InListPassiveTarget 212Kbps) = "D4 4A 01 01"
"""
from __future__ import print_function
from __future__ import unicode_literals


class PseudoApdu(object):

    def __init__(self):
        self._cla = None
        self._ins = None
        self._p1 = None
        self._p2 = None
        self._payload = None

    def get_headers(self):
        return [
            self._cla,
            self._ins,
            self._p1,
            self._p2,
        ]

    def set_headers(self, cla, ins, p1, p2):
        self._cla = cla
        self._ins = ins
        self._p1 = p1
        self._p2 = p2

    def get_payload(self):
        return self._payload

    def set_payload(self, payload):
        """
        Args:
            payload (list of int): the APDU payload.
        """
        self._payload = payload

    def get_lc(self):
        """
        Number of bytes to send.
        """
        return len(self._payload)

    def get_raw(self):
        """
        Returns the full RAW APDU as a list of int)
        """
        raw = []
        raw += self.get_headers()
        raw += [self.get_lc()]
        raw += self.get_payload()
        return raw


class Pn532Reader(object):
    DIRECT_TRANSMIT_CLA = 0xFF
    DIRECT_TRANSMIT_INS = 0x00
    DIRECT_TRANSMIT_P1 = 0x00
    DIRECT_TRANSMIT_P2 = 0x00

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

    def send_apdu(self, payload):
        """
        Args:
            apdu (list of int): the APDU payload to be sent.
        """
        direct_transmit_lc = len(payload)
        # adds the pseudo ADPU header
        pseudo_apdu = PseudoApdu()
        pseudo_apdu.set_headers(
            Pn532Reader.DIRECT_TRANSMIT_CLA,
            Pn532Reader.DIRECT_TRANSMIT_INS,
            Pn532Reader.DIRECT_TRANSMIT_P1,
            Pn532Reader.DIRECT_TRANSMIT_P2)
        pseudo_apdu.set_payload(payload)
        raw_apdu = pseudo_apdu.get_raw()
        self.transmit(raw_apdu)

    def send_apdu_str(self, payload_str):
        """
        Args:
            apdu (str): the APDU payload to be sent.
        """
        payload = [int(x, 16) for x in payload_str.split()]
        self.send_apdu(payload)

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

