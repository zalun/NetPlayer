import time
import os

from .settings import (RADIO_PIN, MPC_PIN, STOP_PIN, TEST_PIN,
                       RADIO_STATIONS, TEST_DIR,
                       logger)
from .buttons import active_buttons, MplayerButton, MPCButton, StopButton

# finding test files
files = os.listdir(TEST_DIR)
test_files = []
for f in files:
    logger.info(os.path.join(TEST_DIR, f))
    test_files.append([os.path.join(TEST_DIR, f), f])

# initiating buttons
MplayerButton(RADIO_PIN, RADIO_STATIONS)
MplayerButton(TEST_PIN, test_files)
MPCButton(MPC_PIN)
StopButton(STOP_PIN)

print "Listening to buttons:"
while True:
    for button in active_buttons:
        button.check()
    time.sleep(0.05)
