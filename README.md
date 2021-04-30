dependencies: (for debian)

		i3lock
		libnotify-bin
		libpangocairo-1.0-0
		libpulse-dev
		python3-cairocffi
		python3-dbus
		python3-keyring
		python3-mpd
		python3-pip
		python3-setuptools
		python3-wheel
		python3-xcffib
		python3-xlib
		xautolock

if python packages are unavailable in your distro,
you can try to install them via pip3.

typical setup:

		cd ~
		git clone --recursive <this-repo> .qtile
		ln -s ~/.qtile/bin/xsession ~/.xsession
		ln -s ~/.qtile/bin/xsession ~/.xinitrc
		ln -s ~/.qtile/bin/xlock ~/bin/
		ln -s ~/.qtile/bin/displace ~/bin/
		ln -s ~/.qtile/bin/xautolock-force ~/bin/
		cd .qtile/qtile

		# NOTE:
		# in the following two files you might want to
		# (temporarily) set the shebang to /usr/bin/python3
		# if your system still has /usr/bin/python set to python2!
		./scripts/ffibuild
		./setup.py build
		
then copy some picture to ~/.locked.png for the locking screen.

