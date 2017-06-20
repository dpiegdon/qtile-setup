typical setup:

		# install multiple dependencies (list missing)
		cd ~
		git clone --recursive <this-repo> .qtile
		ln -s .qtile/xsession ~/.xsession
		ln -s .qtile/xsession ~/.xinitrc
		cd .qtile/qtile
		python3 ./libqtile/ffi_build.py
		python3 ./setup.py build

