#! /usr/bin/env python
"""
Implements the PN532 reader:
http://www.proxmark.org/files/Documents/NFC/ACS_API_ACR122.pdf

InListPassivTargets (0x4A) command example.
PN532 Command (InListPassiveTarget 212Kbps) = "D4 4A 01 01"
"""
from __future__ import print_function
from __future__ import unicode_literals


class Pn532ReaderUnknownError(Exception):
    """
    Base exception.
    """
    pass


class Pn532ReaderOperationFailedError(Exception):
    """
    The operation is failed.
    """
    pass


class Pn532ReaderTimeOutError(Exception):
    """
    The PN532 does not response.
    """
    pass


class Pn532ReaderChecksumError(Exception):
    """
    The checksum of the Contactless Response is wrong.
    """
    pass


class Pn532ReaderParameterError(Exception):
    """
    The PN532_Contactless Command is wrong.
    """
    pass

class Pn532ReaderNoResponseDataError(Exception):
    """
    No response data is available.
    """
    pass


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
    # Direct Transmit status codes
    SW1_DT_SUCCESS = 0x61
    SW1_DT_ERROR = 0x63
    SW2_DT_ERROR = 0x00
    SW2_DT_TIME_OUT_ERROR = 0x01
    SW2_DT_CHECKSUM_ERROR = 0x27
    SW2_DT_PARAMETER_ERROR = 0x7F
    # Get Reponse status codes
    SW1_GR_SUCCESS = 0x90
    SW1_GR_ERROR = 0x63

    def __init__(self, pcsc_reader):
        self.connection = pcsc_reader.createConnection()
        self.connection.connect()
        self._debug = False

    def _handle_dt_status_code(self, sw1, sw2):
        """
        Handles Direct Transmit SW1 & SW2 status code according to
        "Table 1.0C: Status Code".
        http://www.proxmark.org/files/Documents/NFC/ACS_API_ACR122.pdf
        """
        if sw1 == Pn532Reader.SW1_DT_SUCCESS:
            return
        elif sw2 == Pn532Reader.SW2_DT_ERROR:
            raise Pn532ReaderOperationFailedError('')
        elif sw2 == Pn532Reader.SW2_DT_TIME_OUT_ERROR:
            raise Pn532ReaderTimeOutError('')
        elif sw2 == Pn532Reader.SW2_DT_CHECKSUM_ERROR:
            raise Pn532ReaderChecksumError('')
        elif sw2 == Pn532Reader.SW2_DT_PARAMETER_ERROR:
            raise Pn532ReaderParameterError('')
        raise Pn532ReaderUnknownError('')

    def _handle_gr_status_code(self, sw1):
        """
        Handles Get Response SW1 & SW2 status code according to "Table 2.0B".
        http://www.proxmark.org/files/Documents/NFC/ACS_API_ACR122.pdf
        """
        if sw1 == Pn532Reader.SW1_GR_SUCCESS:
            return
        elif sw1 == Pn532Reader.SW1_GR_ERROR:
            raise Pn532ReaderNoResponseDataError('')
        raise Pn532ReaderUnknownError('')

    def _transmit(self, command):
        """
        Args:
            command (list of int): the raw APDU to be sent.
        """
        command_str = " ".join(["%02X" % x for x in command])
        if self._debug:
            print("> %s" % command_str)
        data, sw1, sw2 = self.connection.transmit(command)
        data_str = " ".join(["%02X" % x for x in data])
        if self._debug:
            print("< [%s] %02X %02X" % (data_str, sw1, sw2))
        return data, sw1, sw2

    def _direct_transmit(self, command):
        """
        Sends a pseudo APDU command, handles the response status code
        and returns the response length.
        Args:
            command (list of int): the raw APDU to be sent.
        """
        data, sw1, sw2 = self._transmit(command)
        self._handle_dt_status_code(sw1, sw2)
        # The operation is completed successfully.
        # The response data has a length of LEN bytes.
        # The APDU "Get Response" should be used to retrieve the response data.
        response_length = sw2
        return response_length

    def _get_response(self, response_length):
        """
        Sends the "0xFF 0xC0 0x00 0x00 Le" command to get the response.
        Args:
            response_length (int): the expected response length.
        """
        PSEUDO_APDU_GET_RESPONSE_PREFIX = [
            0xFF,
            0xC0,
            0x00,
            0x00,
        ]
        pseudo_apdu_get_response = PSEUDO_APDU_GET_RESPONSE_PREFIX
        pseudo_apdu_get_response += [response_length]
        data, sw1, _ = self._transmit(pseudo_apdu_get_response)
        # Data Out: Response Data, or Error Code "63 00" will be given
        # if no response data is available.
        self._handle_gr_status_code(sw1)
        return data

    def _transmit_retrieve(self, command):
        """
        Transmits the pseudo APDU command, then sends a new pseud APDU
        command to retrieve the response.
        Table 2.0A: Get Response Command Format (5 Bytes).
        """
        response_length = self._direct_transmit(command)
        response = self._get_response(response_length)
        return response

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
        response = self._transmit_retrieve(raw_apdu)
        return response

    def send_apdu_str(self, payload_str):
        """
        Args:
            apdu (str): the APDU payload to be sent.
        """
        payload = [int(x, 16) for x in payload_str.split()]
        response = self.send_apdu(payload)
        response_str = " ".join(["%02X" % x for x in response])
        return response_str


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

