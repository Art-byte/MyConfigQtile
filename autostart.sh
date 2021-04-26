#!/bin/sh

# systray battery icon
#cbatticon -u 5 &


festival --tts $HOME/.config/qtile/welcome_msg &
lxsession &
picom &
nitrogen --restore &
/usr/bin/emacs --daemon &
volumeicon &
nm-applet &
