Network Audio Player Buttons
############################

Buttons of a Network Player build on top of Raspberry PI and HifiBerry.

System plays music using MPD (from network drive) or mplayer (for radio).

Logic
=====

MPD Button
----------

Stop any other player
If nothing is playing call last played song from the playlist.
If MPD is in use switch the next song

Radio Button
------------

Stop any other player
If no radio is played play last used radio
Else switch to next radio station

Stop Button
-----------

Switch off any player

Shutdown Button
---------------

Halt the system (software shutdown)

Storing Status
==============

System stores status in /var/run/nas


