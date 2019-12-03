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
		./scripts/ffibuild
		./build.py build
		
then copy some picture to ~/.locked.png for the locking screen.

