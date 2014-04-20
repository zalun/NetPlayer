import logging
import logging.config
import logging.handlers

#logging.config.fileConfig('logging.conf')
logging.raiseExceptions = False
FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(filename='/home/volumio/netplayer.log', level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('playerButtons')
logger.setLevel(logging.DEBUG)
#logger.addHandler(logging.handlers.SysLogHandler())

# Pins
RADIO_PIN = 17
MPC_PIN = 23
STOP_PIN = 24
TEST_PIN = 22

# Radio stations
RADIO_STATIONS = [
    ['http://stream.polskieradio.pl/program3', 'Polskie Radio Trojka'],
    ['http://lodz.radio.pionier.net.pl:8000/pl/roxyfm.ogg', 'Roxy FM'],
    ['http://audio.radiownet.pl:8000/stream64', 'Radio Wnet']
]

# This dir contains test files
TEST_DIR = "/home/volumio/test_files"
