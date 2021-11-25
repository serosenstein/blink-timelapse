#!/bin/python3
from blinkpy.helpers.util import json_load
import vardata
from blinkpy.auth import Auth
from blinkpy.blinkpy import Blink
import pprint

credSave = vardata.credSave
auth = Auth(json_load(credSave), no_prompt=True)
blink = Blink()
blink.auth = auth
blink.start()

for name, camera in blink.cameras.items():
  print("Camera name is: " + name )                   # Name of the camera
  pprint.pprint(camera.attributes)      # Print available attributes of camera
  print("\n\n")
