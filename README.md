# blink-timelapse

This is a python script that can be used with blink cameras.  You can specify the interval (time between taking snapshots) and how many iterations (counts) you want it to do.
You will need to create your credential file with the getCreds.py, then copy the example_vardata.py to vardata.py and fill it out appropriately.

1) Install requirements from requirements file: pip3 install -r requirements.txt
2) Generate your credentials with generateCreds.py, this should save to a blink.credsave file
3) Get your Camera name from getCameras.py
4) Copy example_vardata.py to vardata.py and modify all of the variables
5) run blink.py


Big thanks to fronzbot for writing the blinkpy library: https://github.com/fronzbot/blinkpy.git
And to be MattTW for writing the original BlinkMonitorProtocol: https://github.com/MattTW/BlinkMonitorProtocol
