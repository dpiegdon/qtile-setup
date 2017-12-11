#!/bin/bash
# vim: fdm=marker

cd

xrdb ~/.Xdefaults
# disable screensaver
xset s off
xset -dpms
[ -e ~/bin/xscreenlayout ] && ~/bin/xscreenlayout
(~/bin/hid-reset &)

# check or pick display manager {{{

if [ -z "$WINDOWMANAGER" ]; then
	source ~/.environment
fi;

if [ -z "$WINDOWMANAGER" ]; then
	WINDOWMANAGER="python3 $HOME/.qtile/qtile/bin/qtile -c $HOME/.qtile/config/config.py"
	# or one of:
	#   /usr/bin/xterm
	#   /usr/bin/startkde
	#   /usr/bin/gnome-session
fi;

export WINDOWMANAGER

# }}}

# in case of xmonad or qtile, start all the accompanying programs {{{

start_screenlocker() {
	which xautolock > /dev/null 2>&1 && (
		KILLEROPTIONS=""

		# laptop?
		BATTERYCOUNT=$(ls -1 /sys/class/power_supply/ | grep BAT > /dev/null 2>&1 | wc -l)
		if [ $BATTERYCOUNT -ge 1 ]; then
			KILLEROPTIONS='-killtime 1 -killer "systemctl suspend"'
		fi

		xautolock -time 3 $KILLEROPTIONS &
		XAUTOLOCK_FILE="/tmp/.qtile_xautolock_$!"
		touch $XAUTOLOCK_FILE
	)
}

case `basename "$WINDOWMANAGER"` in
	xmonad)
		(trayer --edge top --align left --SetDockType true --SetPartialStrut true --expand true --widthtype pixel --width 71 --margin 1008 --transparent true --tint 0x220000 --height 12 &)
		start_screenlocker
		( (sleep 3; exec ~/bin/update-background)&)
		(exec dunst&)
		( (sleep 3; exec blueman-applet) &)
		;;
	*)
		echo $WINDOWMANAGER | grep '\<qtile\>' > /dev/null 2>&1 && {
			start_screenlocker
			(exec dunst&)
			( (sleep 3; exec blueman-applet) &)
		}
		;;
esac

# }}}

# other programs {{{

case "$(hostname)" in
	windfury)
		(~/bin/mpd &)
		;;
	proton)
		(nm-applet &)
		;;
	aluminumbar)
		(nm-applet &)
		;;
esac

#(gajim&)

# }}}

# execute display manager
exec $WINDOWMANAGER > ~/.windowmanager.log 2>&1

