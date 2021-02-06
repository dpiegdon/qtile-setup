#!/usr/bin/env python3
# coding: utf-8
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 colorcolumn=100

# default config is in qtile repo in:
#   libqtile/resources/default_config.py
# when default-config is used due to config error, type:
#   WIN+CTRL+R  to restart qtile
#   WIN+R       to execute something

from libqtile.command import lazy
from libqtile.config import Key, Drag, Click

import config_funcs


def get_keys_and_mouse(groups):
    modkey = "mod4"
    shiftkey = "shift"
    controlkey = "control"
    altkey = "mod1"
    modeswitchkey = "mod5"

    keys = [
        Key([modkey], "h", lazy.layout.left()),
        Key([modkey], "j", lazy.layout.down()),
        Key([modkey], "k", lazy.layout.up()),
        Key([modkey], "l", lazy.layout.right()),

        Key([modkey], "n", lazy.layout.next()),
        Key([modkey], "p", lazy.layout.previous()),

        Key([modkey], "Tab", lazy.group.next_window()),
        Key([modkey, shiftkey], "Tab", lazy.window.bring_to_front()),

        Key([modkey, shiftkey], "h", lazy.layout.shuffle_left()),
        Key([modkey, shiftkey], "j", lazy.layout.shuffle_down()),
        Key([modkey, shiftkey], "k", lazy.layout.shuffle_up()),
        Key([modkey, shiftkey], "l", lazy.layout.shuffle_right()),

        Key([modkey, controlkey], "h", lazy.layout.grow_left()),
        Key([modkey, controlkey], "j", lazy.layout.grow_down()),
        Key([modkey, controlkey], "k", lazy.layout.grow_up()),
        Key([modkey, controlkey], "l", lazy.layout.grow_right()),

        Key([modkey, controlkey, shiftkey], "h", lazy.layout.swap_left()),
        Key([modkey, controlkey, shiftkey], "j", lazy.layout.swap_down()),
        Key([modkey, controlkey, shiftkey], "k", lazy.layout.swap_up()),
        Key([modkey, controlkey, shiftkey], "l", lazy.layout.swap_right()),

        Key([modkey], "y", lazy.layout.shrink()),
        Key([modkey], "u", lazy.layout.grow()),
        Key([modkey], "i", lazy.layout.normalize()),
        Key([modkey], "o", lazy.layout.maximize()),

        Key([modkey, shiftkey], "space", lazy.layout.flip()),

        # Swap panes of split stack
        Key([modkey, shiftkey], "n", lazy.layout.rotate()),

        Key([modkey], "Up", lazy.hide_show_bar()),
        Key([modkey], "Return", lazy.window.toggle_fullscreen()),
        # Toggle between split and unsplit sides of stack.
        # Split = all windows displayed
        # Unsplit = 1 window displayed, like Max layout, but still with
        # multiple stack panes
        Key([modkey, shiftkey], "Return", lazy.layout.toggle_split()),

        # Handle floating windows
        Key([modkey], "t", lazy.window.toggle_floating()),

        # Toggle between different layouts as defined below
        Key([modkey], "space", lazy.next_layout()),

        Key([modkey], "q", lazy.window.kill()),
        Key([modkey, shiftkey], "q", lazy.restart()),
        Key([modkey, controlkey, shiftkey], "q", lazy.shutdown()),
        Key([modkey], "BackSpace", lazy.spawncmd()),
        Key([modkey], "Escape", lazy.spawn("xautolock-force")),
        Key([modkey, modeswitchkey], "Escape", lazy.spawn("xautolock -toggle")),
        Key([modkey, controlkey], "Return", lazy.spawn("/usr/bin/xterm -u8 -e tmux -2 attach")),

        Key([modkey], "Left",  lazy.screen.prev_group(skip_empty=True, skip_managed=True)),
        Key([modkey], "Right", lazy.screen.next_group(skip_empty=True, skip_managed=True)),
        Key([modkey, shiftkey], "Left",  lazy.screen.prev_group(skip_managed=True)),
        Key([modkey, shiftkey], "Right", lazy.screen.next_group(skip_managed=True)),

        Key([modkey], "s", lazy.spawn("/usr/bin/gnome-screenshot")),
        Key([modkey, shiftkey], "s", lazy.spawn("/usr/bin/gnome-screenshot --window")),
    ]

    # Multi-Display setup
    for screen, key in enumerate("wer"):
        keys += [
                Key([modkey], key, lazy.to_screen(screen)),
                Key([modkey, shiftkey], key, lazy.function(config_funcs.move_window_to_screen(screen))),
                ]

    # map function keys to special_keys script
    for _modifier in ( ("", "NONE")
                     , (shiftkey, "SHIFT")
                     , (controlkey, "CTRL")
                     , (altkey, "ALT")
                     , (modeswitchkey, "MODESWITCH")
                     ):
        for _fkey in range(1,13):
            _fkey_name = "F{}".format(_fkey)
            _mod = [modkey]
            if("" != _modifier[0]):
                _mod.append(_modifier[0])
            keys.append( Key(_mod, _fkey_name, lazy.spawn("special_keys {} {}".format(_fkey_name, _modifier[1])) ) )

    for _fkey in ( "XF86MonBrightnessDown"
                 , "XF86MonBrightnessUp"
                 , "XF86LaunchA"
                 , "XF86LaunchB"
                 , "XF86KbdBrightnessDown"
                 , "XF86KbdBrightnessUp"
                 , "XF86AudioPrev"
                 , "XF86AudioNext"
                 , "XF86AudioPlay"
                 , "XF86AudioStop"
                 , "XF86AudioMute"
                 , "XF86AudioMicMute"
                 , "XF86AudioLowerVolume"
                 , "XF86AudioRaiseVolume"
                 , "XF86Favorites"
                 , "XF86Eject"
                 , "XF86Display"
                 ):
        keys.append( Key([], _fkey, lazy.spawn("special_keys {} NONE".format(_fkey))) )

    for i in groups:
        try:
            keyname = { '`': "grave", '-': "minus", '=': "equal" }[i.name]
        except KeyError:
            keyname = i.name
        keys += [
                Key([modkey],           keyname, lazy.group[i.name].toscreen(toggle=False)),
                Key([modkey, shiftkey], keyname, lazy.function(config_funcs.move_window_to_group(i))),
                ]


    mouse = [
        Click([], "Button9", lazy.spawn("special_keys MOUSE9 NONE")),
        Click([shiftkey], "Button9", lazy.spawn("special_keys MOUSE9 SHIFT")),
        Click([controlkey], "Button9", lazy.spawn("special_keys MOUSE9 CTRL")),
        Click([altkey], "Button9", lazy.spawn("special_keys MOUSE9 ALT")),
        Click([modeswitchkey], "Button9", lazy.spawn("special_keys MOUSE9 MODESWITCH")),
        Drag([modkey], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
        Drag([modkey, shiftkey], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
        Drag([modkey], "Button3", lazy.window.set_size_floating(),     start=lazy.window.get_size()),
        #Drag([modkey], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position(True), finish=lazy.window.reset_mouse_focus()),
        #Drag([modkey], "Button3", lazy.window.set_size_floating(),     start=lazy.window.get_size(True), finish=lazy.window.reset_mouse_focus()),
    ]

    return keys, mouse
