#!/bin/python3
#Rename this file to vardata.py after you modify it

#prowl api key
apikey="1234123412341234123412341091a12341cdee15"

#smtp stuff
sender_email="whatever@domain.com"
smtp_password="YourSecretPassword"
receiver_email="suckerwhogetsemails@domain.com"
smtp_server="smtp.gmail.com"
smtp_port="587"
send_emails=True
send_prowls=True
#if needing twilio support: pip3 install twilio 
send_twilio=True


#Twilio SMS stuff
twilio_to="+11234523450"
twilio_from="+11234123420"
twilio_sid="adflkjadaflkjaldflkjasdflkjadsfksb"
twilio_token="asdlfjasdflkasdlfkjasdfrlslslsls"


interval = 10
counts = 2
camera_name = 'aerocam'
fontLocation = "NimbusMonoPS-Bold.t1"
dir = './time-lapses/'
credSave = "./blink.credsave"
logPath = "./blink.log"
