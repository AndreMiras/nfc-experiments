# NFC Experiments

Playing with the Tikitag (PN532) reader.

## Usage example
### list_targets.py
The `list_targets.py` script sends a `InListPassivTargets` command and decodes the result.
```
python list_targets.py
Available readers: ['ACS ACR 38U-CCID 00 00']
Using reader: ACS ACR 38U-CCID 00 00
response: D5 4B 01 01 00 04 08 04 92 4C 52 27
response_header: D5 4B
tags_found: 1
target_number: 1
sens_res: 00 04
sel_res: 8
uid_length: 4
uid: 92 4C 52 27
```

## Setup requirements
Create a NFC Tools docker image from https://github.com/AndreMiras/dockerfiles/tree/master/nfc-tools.

## Documentation

Pseudo APDU format and MIFARE Classic Tags exchanges description:
http://www.proxmark.org/files/Documents/NFC/ACS_API_ACR122.pdf

PN532 Application note:
http://www.nxp.com/documents/application_note/AN133910.pdf
