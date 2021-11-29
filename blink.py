#!/bin/python3
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
import os
import sys
import time
import datetime
import subprocess
from blinkpy.helpers.util import json_load
#pip install Pillow
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import logging
import vardata 


pid = os.getpid()
pid = str(pid)
pidfile = "./pidfile"

if not os.path.isfile(pidfile):
  f = open(pidfile, "a")
  f.write(pid)
  f.close()
else:
  exit("PID file " + pidfile + " exists already")

interval = vardata.interval
duration_seconds = vardata.duration_seconds
duration_minutes = vardata.duration_minutes
duration_hours = vardata.duration_hours
duration_days = vardata.duration_days

duration_totalseconds = duration_seconds + (duration_minutes * 60) + (duration_hours * 60 * 60) + (duration_days * 24 * 60 * 60)


counts =  duration_totalseconds // interval
camera_name = vardata.camera_name
fontLocation = vardata.fontLocation
dir = vardata.dir
credSave = vardata.credSave

sec_value = counts * interval  % (24*3600)
day_value = counts * interval  // (24*3600)
hour_value = sec_value // 3600
sec_value %= 3600
min = sec_value // 60
sec_value %= 60

min = str(min)
sec_value = str(sec_value)
hour_value = str(hour_value)
send_prowls = vardata.send_prowls
send_emails = vardata.send_emails
send_twilio = vardata.send_twilio
logPath = vardata.logPath
logging.basicConfig(filename=logPath, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.info("This will take " + str(counts) + " pictures, waiting " + str(interval) + " seconds between them, that's a total of " + str(day_value) + "  days, " + hour_value + " hours, " + min + " minutes and " + sec_value + " seconds" )
print("This will take " + str(counts) + " pictures, waiting " + str(interval) + " seconds between them, that's a total of " + str(day_value) + " days, " + hour_value + " hours, " + min + " minutes and " + sec_value + " seconds" )
exit("now")

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
  print("Directory " + dirName +  " Created ")
  logging.info("Directory " + dirName +  " Created ")
else:
  print("Directory " + dirName +  " already exists")
  logging.info("Directory " + dirName +  " already exists")
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
   logging.info(fileName)
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
   logging.info("number " + str_i + " out of " + str(counts))
   time.sleep(interval)
ffmpeg_location = vardata.ffmpeg_location
if not os.path.exists(ffmpeg_location):
  logging.info("Can't find ffmpeg location at " + ffmpeg_location + "\nExiting now")
  os.remove(pidfile)
  exit("Can't find ffmpeg location at " + ffmpeg_location)
cmd = ffmpeg_location + ' -i ' + dirName + "/image%05'd'.jpg -r 60 -s 640x480 -vcodec libx264 -b 1000k " + dirName + "/" + date + '.output.mp4'
sp = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)

# Store the return code in rc variable
rc=sp.wait()

# Separate the output and error.
# This is similar to Tuple where we store two values to two different variables
out,err=sp.communicate()

print('Return Code: ',rc)
print('output is: \n', out)
print('error is: \n', err)

logging.info('\nReturn Code: ' + str(rc))
logging.info('\noutput is: \n' +  out)
logging.info('\nerror is: \n' + err)
if send_emails:                                               
  import smtplib, ssl
  sender_email = vardata.sender_email                         
  smtp_password = vardata.smtp_password                       
  receiver_email = vardata.receiver_email                     
  smtp_server = vardata.smtp_server                           
  smtp_port = vardata.smtp_port                               
  if not [x for x in (sender_email,smtp_password,receiver_email,smtp_server,smtp_port) if x is None]:                                         
    pass
  else:
    logging.warn("a smtp variable wasn't set")

def SendTwilio(info):
  from twilio.rest import Client
  twilio_to = vardata.twilio_to 
  twilio_from = vardata.twilio_from
  twilio_sid = vardata.twilio_sid
  twilio_token = vardata.twilio_token
  if not [x for x in (twilio_to,twilio_sid,twilio_token) if x is None]:
    pass
  else:
    logging.warm("twilio variable wasn't set")
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
  logging.info("sending email to " + receiver_email + " with this info " + info)
 except:
  print("Error sending email: " + str(sys.exc_info()[0])) 
  logging.warn("Error sending email: " + str(sys.exc_info()[0])) 
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
     logging.warn(res)
if send_prowls:
  SendProwl("Finished " +  dirName + "/" + date + '.output.mp4')
if send_emails:
  SendEmail("Finished " +  dirName + "/" + date + '.output.mp4')
if send_twilio:
  SendTwilio("Finished " +  dirName + "/" + date + '.output.mp4')

#cleanup pid
os.remove(pidfile)
