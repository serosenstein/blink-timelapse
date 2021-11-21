#!/bin/python3
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
import os
import time
import datetime
from blinkpy.helpers.util import json_load
#pip install Pillow
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

pid = os.getpid()
pid = str(pid)

interval = 120
counts = 360
camera_name = 'aerocam'
fontLocation = "/usr/lib/plexmediaserver/Resources/Fonts/DejaVuSans-Bold.ttf"


now = datetime.datetime.now()
dir = './time-lapses/'
date = now.strftime('%Y-%m-%d-%H')
timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
#print(timestamp)
date = str(date)
credSave = "./blink.credsave"
print(date)
dirName = str(dir) + date + "." + pid
print(dirName)
blink = Blink()
# Create target Directory if don't exist
if not os.path.exists(dirName):
  os.makedirs(dirName)
  print("Directory " , dirName ,  " Created ")
else:    
  print("Directory " , dirName ,  " already exists")
auth = Auth(json_load(credSave), no_prompt=True)
blink.auth = auth
blink.start()
blink.save("./blink.credsave")
camera = blink.cameras[camera_name]
for i in range (counts):
   camera.snap_picture()       # Take a new picture with the camera
   str_i = str(i)
   blink.refresh()             # Get new information from server
   fileName = dirName + '/image' + str_i.zfill(5) + '.jpg'
   print(fileName)
   now = datetime.datetime.now()
   timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
   camera.image_to_file(fileName)
   fontsize = 36
   font = ImageFont.truetype(font=fontLocation, size=36, index=0, encoding='', layout_engine=None)
   img = Image.open(fileName)
   I1 = ImageDraw.Draw(img)
   #I1.text((36, 36), timestamp, fill=(255, 0, 0))
   I1.text((36, 36), timestamp, fill=(255, 0, 0), font=font)
   img.save(fileName)
   time.sleep(interval)
os.system('ffmpeg -i ' + dirName + "/image%05'd'.jpg -r 60 -s 640x480 -vcodec libx264 -b 1000k " + dirName + "/" + date + '.output.mp4')
