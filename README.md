# Network Audio Player Buttons

Buttons of a Network Player build on top of Raspberry PI and HifiBerry.

System plays music using MPD (from network drive) or mplayer (for radio).

## Install

Add buttons to pins specified in `settings.py`
Clone repository 
Run from parent directory - `python -m NetPlayer.listen`

## Logic

### MPD Button

Stop any other player
If nothing is playing call last played song from the playlist.
If MPD is in use switch the next song

### Radio Button

Stop any other player
If no radio is played play last used radio
Else switch to next radio station

### Stop Button

Switch off any player

### Shutdown Button

Halt the system (software shutdown)

## ToDo

### Storing Status

System stores status in /var/run/nas

### Display info

* Current quality used: cat /proc/asound/card0/pcm0p/sub0/hw_params
