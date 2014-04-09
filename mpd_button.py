import os
import subprocess
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
 
prev_input = 0
next_song = False

while True:
  input = GPIO.input(23)
  if ((not prev_input) and input):
    os.system("killall mplayer")
    status = subprocess.check_output(["mpc", "status"])
    os.system("mpc play")
    if next_song:
      os.system("mpc next")
    status = subprocess.check_output(["mpc", "status"])
    next_song = (len(status.split("\n")) > 2)
  prev_input = input
  #slight pause to debounce
  time.sleep(0.05)
