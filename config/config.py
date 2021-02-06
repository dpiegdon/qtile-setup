#!/usr/bin/env python3
# coding: utf-8
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 colorcolumn=100

# default config is in qtile repo in:
#   libqtile/resources/default_config.py
# when default-config is used due to config error, type:
#   WIN+CTRL+R  to restart qtile
#   WIN+R       to execute something

from libqtile import layout, bar, hook
from libqtile.command import lazy
from libqtile.config import Screen, Group, ScratchPad, DropDown

import config_funcs
import config_colorthemes
import config_periphery
import config_widgets

_theme = config_colorthemes.fancyYBGtheme
_dpi = config_funcs.get_primary_display_dpi()
_barheight = max(15, int(round(_dpi * 0.11, 0)))
_fontsize = _barheight - 2
_iconsize = _barheight - 2

# fake a WM-name that is on java-whitelist so java apps work properly
wmname = "LG3D"

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"

groups = [Group(i) for i in "1234567890-="] + [
    ScratchPad("d", [DropDown("d", "/usr/bin/xterm -u8",
                              opacity=0.80, height=0.70, width=0.80, x=0.10, y=0.00)]),
    ScratchPad("f", [DropDown("f", "/usr/bin/xterm -u8 -e ~/.qtile/qtile/bin/qshell",
                              opacity=0.80, height=0.40, width=0.80, x=0.10, y=0.60)]),
    ]

keys, mouse = config_periphery.get_keys_and_mouse(groups)

layouts = [
    layout.Columns(border_focus=_theme['focus'], border_normal=_theme['blur'], grow_amount=2),
    #layout.MonadTall(border_focus=_theme['focus'], border_normal=_theme['blur']),
    #layout.Tile(ratio=0.5, border_focus=_theme['focus'], border_normal=_theme['blur']),
    #layout.Max(),
    #layout.Floating(border_focus=_theme['floatfocus'], border_normal=_theme['floatblur']),
]

floating_layout = layout.Floating(border_focus=_theme['floatfocus'], border_normal=_theme['floatblur'])

widget_defaults = dict(font='Arial', _fontsize=_fontsize, padding=2)

screens = [ Screen(top=bar.Bar(config_widgets.init_widgets(_theme, _fontsize, _iconsize), _barheight)) ]

config_funcs.exec_poststart(_theme)
