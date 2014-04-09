import os
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN)
 
prev_input = 0
while True:
  input = GPIO.input(22)
  if ((not prev_input) and input):
    os.system("mpc stop")
    os.system("killall mplayer")
  prev_input = input
  #slight pause to debounce
  time.sleep(0.05)
