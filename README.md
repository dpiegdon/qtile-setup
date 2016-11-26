typical setup:

		cd ~
		git clone --recursive <this-repo> .qtile
		ln -s .qtile/xsession ~/.xsession
		ln -s .qtile/xsession ~/.xinitrc
		cd .qtile/qtile
		python ./libqtile/ffi_build.py

