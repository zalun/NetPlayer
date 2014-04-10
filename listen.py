import time

from .buttons import RadioButton, MPCButton, StopButton

radio = RadioButton()
mpc = MPCButton()
stop = StopButton()

print "Listening to buttons:"
while True:
    radio.check()
    mpc.check()
    stop.check()
    time.sleep(0.05)
