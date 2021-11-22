#!/bin/python3
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
import os
import sys
import time
import datetime
from blinkpy.helpers.util import json_load
#pip install Pillow
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import vardata
pid = os.getpid()
pid = str(pid)

interval = vardata.interval
counts = vardata.counts
camera_name = vardata.camera_name
fontLocation = vardata.fontLocation
dir = vardata.dir
credSave = vardata.credSave

send_prowls = vardata.send_prowls
send_emails = vardata.send_emails
send_twilio = vardata.send_twilio


now = datetime.datetime.now()
date = now.strftime('%Y-%m-%d-%H')
timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
date = str(date)
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
blink.save(credSave)
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
   I1.text((36, 36), timestamp, fill=(255, 0, 0), font=font)
   img.save(fileName)
   print("number " + str_i + " out of " + str(counts))
   time.sleep(interval)
os.system('ffmpeg -i ' + dirName + "/image%05'd'.jpg -r 60 -s 640x480 -vcodec libx264 -b 1000k " + dirName + "/" + date + '.output.mp4')
if send_emails:                                               
  import smtplib, ssl
  sender_email = vardata.sender_email                         
  smtp_password = vardata.smtp_password                       
  receiver_email = vardata.receiver_email                     
  smtp_server = vardata.smtp_server                           
  smtp_port = vardata.smtp_port                               
  if not [x for x in (sender_email,smtp_password,receiver_email,smtp_server,smtp_port) if x is None]:                                         
    pass

def SendTwilio(info):
  from twilio.rest import Client
  twilio_to = vardata.twilio_to 
  twilio_from = vardata.twilio_from
  twilio_sid = vardata.twilio_sid
  twilio_token = vardata.twilio_token
  if not [x for x in (twilio_to,twilio_sid,twilio_token) if x is None]:
    pass
  client = Client(twilio_sid, twilio_token)
  message = client.messages \
                .create(
                     body=info,
                     from_=twilio_from,
                     to=twilio_to)
def SendEmail(info):
 # For guessing MIME type
 import mimetypes

 # Import the email modules we'll need
 import email
 import email.mime.application
 from email.mime.multipart import MIMEMultipart

 # Create a text/plain message
 msg = email.mime.multipart.MIMEMultipart()

 msg['Subject'] = 'TimeLapse Video'
 msg['From'] = sender_email
 msg['To'] = receiver_email


 filename=dirName + "/" + date + '.output.mp4'
 fp=open(filename,'rb')
 att = email.mime.application.MIMEApplication(fp.read(),_subtype="video/mp4")
 fp.close()
 att.add_header('Content-Disposition','attachment',filename=filename)
 msg.attach(att)
 try:
  context = ssl.create_default_context()
  with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender_email, smtp_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
  #debug comment
  print("sending email to " + receiver_email + " with this info " + info)
 except:
  print("Error sending email: " + str(sys.exc_info()[0])) 
  raise
def SendProwl(info):
 from pushno import PushNotification
 apikey = vardata.apikey
 pn = PushNotification(
     "prowl", api_key=apikey, application="TimeLapse"
 )
 is_valid, res = pn.validate_user()
 if is_valid:
     pn.send(event="Timelapse Notification", description=info)
 else:
     print(res)
if send_prowls:
  SendProwl("Finished " +  dirName + "/" + date + '.output.mp4')
if send_emails:
  SendEmail("Finished " +  dirName + "/" + date + '.output.mp4')
if send_twilio:
  SendTwilio("Finished " +  dirName + "/" + date + '.output.mp4')
