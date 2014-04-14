import os
import shlex
import subprocess
import time
import RPi.GPIO as GPIO

from .settings import logger, RADIO_PIN, MPC_PIN, STOP_PIN, HALT_PIN, RADIO_STATIONS


GPIO.setmode(GPIO.BCM)


class Button(dict):

    prev_input = None

    def __init__(self, pin):
        """Assign pin"""
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def run(self):
        """Placeholder to run specific buttons"""
        pass

    def stop(self):
        os.system("mpc stop")
        os.system("killall mplayer")
        os.system("sudo /etc/init.d/shairport stop")
        time.sleep(0.5)
        os.system("sudo /etc/init.d/shairport start")

    def check(self):
        """Has the button been pressed?"""
        inp = GPIO.input(self.pin)
        if (not self.prev_input) and inp:
            self.run()
        self.prev_input = inp


class RadioButton(Button):

    current_station = None

    next_station = None

    def __init__(self):
        super(RadioButton, self).__init__(RADIO_PIN)
        self.next_station = 0
        self.stations_count = len(RADIO_STATIONS)

    def run(self):
        logger.info("Radio button pressed")
        self.stop()
        self.current_station = self.next_station
        print "Playing %s\n" % RADIO_STATIONS[self.current_station][1]
	command = "mplayer -loop 0 -ao alsa:device=hw=0.0 -cache 512 -cache-min 10 %s"
        args = shlex.split(command % RADIO_STATIONS[self.current_station][0])
        subprocess.Popen(args)
        self.next_station = (self.next_station + 1) % self.stations_count


class MPCButton(Button):

    play_next_song = None

    def __init__(self):
        super(MPCButton, self).__init__(MPC_PIN)
        self.next_song = False

    def play(self):
        os.system("mpc play")

    def next(self):
        os.system("mpc next")

    def stop(self):
        os.system("killall mplayer")
        os.system("sudo /etc/init.d/shairport stop")
        time.sleep(0.5)
        os.system("sudo /etc/init.d/shairport start")

    def getPureStatus(self):
        return subprocess.check_output(["mpc", "status"])

    def getStatus(self):
        pass

    def run(self):
        logger.info("Music button pressed")
        self.stop()
        self.play()
        if self.play_next_song:
            self.next()

        status = self.getPureStatus()
        self.play_next_song = (len(status.split("\n")) > 2)


class StopButton(Button):

    def __init__(self):
        super(StopButton, self).__init__(STOP_PIN)

    def run(self):
        logger.info("Stop button pressed")
        self.stop()
        os.system("mpc update")


class HaltButton(Button):

    def __init__(self):
        super(HaltButton, self).__init__(HALT_PIN)

    def run(self):
        logger.info("Shutdown button pressed")
        self.stop()
        os.system("sudo halt")
