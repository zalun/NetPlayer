import logging
import logging.config
import logging.handlers

#logging.config.fileConfig('logging.conf')
logging.raiseExceptions = False
logging.basicConfig(filename='netplayer.log',level=logging.DEBUG)
logger = logging.getLogger('playerButtons')
logger.setLevel(logging.DEBUG)
#logger.addHandler(logging.handlers.SysLogHandler())

# Pins
RADIO_PIN = 17
MPC_PIN = 23
STOP_PIN = 22
HALT_PIN = 4


# Radio stations
RADIO_STATIONS = [
    ['http://stream.polskieradio.pl/program3', 'Polskie Radio Trojka'],
    ['http://lodz.radio.pionier.net.pl:8000/pl/roxyfm.ogg', 'Roxy FM'],
    ['http://audio.radiownet.pl:8000/stream64', 'Radio Wnet']
]
