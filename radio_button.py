import os
import shlex
import subprocess
import time
import RPi.GPIO as GPIO

radio = [
  ['http://stream.polskieradio.pl/program3', 'Polskie Radio Trojka'],
  ['http://lodz.radio.pionier.net.pl:8000/pl/roxyfm.ogg', 'Roxy FM'],
  ['http://audio.radiownet.pl:8000/stream64', 'Radio Wnet']
]

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
 
prev_input = 0
toplay = 0
radio_count = len(radio)

def play(station):
  os.system("mpc stop")
  os.system("killall mplayer")
  print "Playing %s" % radio[station][1]
  args = shlex.split("mplayer -loop 0 %s" % radio[station][0])
  p = subprocess.Popen(args)
  return (station + 1) % radio_count

while True:
  input = GPIO.input(17)
  if ((not prev_input) and input):
    toplay = play(toplay)
  prev_input = input
  #slight pause to debounce
  time.sleep(0.05)
