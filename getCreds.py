#!/bin/python3
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth


blink = Blink()
auth = Auth()
blink.auth = auth
blink.start()
blink.save("./blink.credsave")
