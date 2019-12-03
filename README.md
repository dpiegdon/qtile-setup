dependencies: (for debian)

		python3-setuptools
		python3-mpd
		python3-keyring
		python3-pip
		python3-dbus
		libpangocairo-1.0-0
		i3lock
		xautolock
		libnotify-bin

		pip3 install xcffib
		pip3 install cairocffi

typical setup:

		cd ~
		git clone --recursive <this-repo> .qtile
		ln -s ~/.qtile/bin/xsession ~/.xsession
		ln -s ~/.qtile/bin/xsession ~/.xinitrc
		ln -s ~/.qtile/bin/xlock ~/bin/
		ln -s ~/.qtile/bin/xautolock-force ~/bin/
		cd .qtile/qtile

		# NOTE:
		# in the following two files you might want to
		# (temporarily) set the shebang to /usr/bin/python3
		# if your system still has /usr/bin/python set to python2!
		./scripts/ffibuild
		./setup.py build
		
then copy some picture to ~/.locked.png for the locking screen.

