#! /usr/bin/env python
"""
InListPassivTargets (0x4A) command example.
PN532 Command (InListPassiveTarget 212Kbps) = "D4 4A 01 01"
"""
from smartcard.System import readers

# get all the available readers
r = readers()
print "Available readers:", r

reader = r[0]
print "Using:", reader

connection = reader.createConnection()
connection.connect()

def transmit(command):
    print ">", " ".join(["%02X" % x for x in command])
    data, sw1, sw2 = connection.transmit(command)
    data_str = " ".join(["%02X" % x for x in data])
    print "< [%s] %02X %02X" % (data_str, sw1, sw2)

def transmit_str(command_str):
    command = [int(x, 16) for x in command_str.split()]
    transmit(command)

COMMAND_STR = "FF 00 00 00 04 D4 32 01 00"
transmit_str(COMMAND_STR)

COMMAND_STR = "FF C0 00 00 04"
transmit_str(COMMAND_STR)

COMMAND_STR = "FF 00 00 00 04 D4 32 01 01"
transmit_str(COMMAND_STR)

COMMAND_STR = "FF C0 00 00 04"
transmit_str(COMMAND_STR)

# 4A InListPassivTargets
COMMAND_STR = "FF 00 00 00 04 D4 4A 01 00"
transmit_str(COMMAND_STR)

COMMAND_STR = "FF C0 00 00 0E"
transmit_str(COMMAND_STR)
