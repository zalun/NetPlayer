import os
import shlex
import subprocess
import time
import RPi.GPIO as GPIO

from .settings import (logger,
                       RADIO_STATIONS, TEST_DIR)


# set the BCM numbering mode
GPIO.setmode(GPIO.BCM)


status = {
    "playing": False,
    "object": None
}

active_buttons = []


class Button(object):

    prev_input = None

    def __init__(self, pin):
        """Assign pin"""
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)
        active_buttons.append(self)
        logger.info("Pin %d assigned to %s" % (self.pin, self.name()))

    def run(self):
        """Placeholder to run specific buttons"""
        logger.info("Pressed %s" % self.name())
        status['object'] = self
        status['playing'] = True

    @classmethod
    def stop(cls):
        """Method to stop playing"""
        if status['playing']:
            status['object'] = None
            status['playing'] = False

    def check(self):
        """Has the button been pressed?"""
        inp = GPIO.input(self.pin)
        if (not self.prev_input) and inp:
            self.run()
        self.prev_input = inp


class MplayerButton(Button):

    current_url = None
    next_url = None

    def __init__(self, pin, urls):
        super(MplayerButton, self).__init__(pin)
        self.urls = urls
        self.next_url = 0
        self.urls_count = len(self.urls)

    def stop(self):
        super(MplayerButton, self).stop()
        logger.info('Stopping mplayer')
        os.system("killall mplayer")

    def run(self):
        self.stop()
        self.current_url = self.next_url
        logger.info('Playing %s' % self.urls[self.current_url][1])
        command = 'mplayer -loop 0 -ao alsa:device=hw=0.0 -cache 512 -cache-min 10 "%s"'
        args = shlex.split(command % self.urls[self.current_url][0])
        subprocess.Popen(args)
        self.next_url = (self.current_url + 1) % self.urls_count
        super(MplayerButton, self).run()

    @classmethod
    def name(cls):
        return "Mplayer button"


class MPCButton(Button):

    play_next_song = None

    def __init__(self, pin):
        super(MPCButton, self).__init__(pin)
        self.next_song = False

    def stop(self):
        super(MPCButton, self).stop()
        os.system("mpc stop")

    @classmethod
    def play(cls):
        logger.info('mpc play')
        os.system("mpc play")

    @classmethod
    def next(cls):
        logger.info('mpc next')
        os.system("mpc next")

    @classmethod
    def getPureStatus(cls):
        s = subprocess.check_output(["mpc", "status"])
        logger.debug('mpc status: %s' % s)
        return s

    def getStatus(self):
        pass

    def run(self):
        """Start playing, if already playing switch to next song, if all songs
        played, start from beginning"""

        logger.info("Music button pressed")
        if status['playing']:
            logger.info('Something was playing')
            if status['object'] != self:
                logger.info('It wasn\'t MPD')
                status['object'].stop()
            else:
                logger.info('It was MPD')
                if self.play_next_song:
                    logger.info('[play next song] is on')
                    self.next()
                else:
                    logger.info('[play next song] is off')
                    self.play()
        else:
            logger.info("Nothing was playing")
            self.play()

        super(MPCButton, self).run()

        mpc_status = self.getPureStatus()
        self.play_next_song = (len(mpc_status.split("\n")) > 2)

    @classmethod
    def name(cls):
        return "MPC button"


class StopButton(Button):

    def __init__(self, pin):
        super(StopButton, self).__init__(pin)

    def stop(self):
        pass

    def stopall(self):
        """Hard stop everything"""
        for button in active_buttons:
            button.stop()

    def run(self):
        logger.info("Stop button pressed")
        self.stopall()
        # request mpc database update
        os.system("mpc update")
        # restart AirPlay
        os.system("sudo /etc/init.d/shairport stop")
        time.sleep(0.5)
        os.system("sudo /etc/init.d/shairport start")

    @classmethod
    def name(cls):
        return 'Stop Button'


class TestButton(Button):
    """Use mplayer to play some test sounds"""

    current = 0

    def __init__(self, pin):
        super(TestButton, self).__init__(pin)

    def run(self):
        logger.info("Test button pressed")

    @classmethod
    def name(cls):
        return 'Test Button'
