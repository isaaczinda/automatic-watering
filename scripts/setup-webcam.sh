# enable manual overrides to webcam exposure_absolute setting
v4l2-ctl -d /dev/video0 -c exposure_auto=1

# increase the exposure to 40 (default is 24)
# this mostly removes annoying horizontal black bars from the picture
v4l2-ctl -d /dev/video0 -c exposure_absolute=40

# decrease the gain from 64 to 8 to compensate for the increase in exposure
v4l2-ctl -d /dev/video0 -c gain=8 
