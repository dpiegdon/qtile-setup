#!/usr/bin/env python3
# coding: utf-8
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 colorcolumn=100

import libqtile
from libqtile import widget

import config_funcs

import socket

class LayoutIcon(widget.CurrentLayoutIcon):
    """Like CurrentLayoutIcon, but shows layout for *current* group, not screen of this bar. """
    def _setup_hooks(self):
        def hook_update_layout(*args, **kwargs):
            g = libqtile.qtile.current_group
            layout = g.layouts[g.current_layout]
            new_layout = layout.name
            if self.current_layout != new_layout:
                self.current_layout = new_layout
                self.bar.draw()

        libqtile.hook.subscribe.layout_change(hook_update_layout)
        libqtile.hook.subscribe.current_screen_change(hook_update_layout)


def init_widgets(theme, fontsize, iconsize):
    widgets = [
            widget.GroupBox(disable_drag=True,
                       use_mouse_wheel=False,
                       highlight_method=theme['highlight_method'],
                       hide_unused=False,
                       this_current_screen_border=theme['foreground'],
                       this_screen_border=theme['screenblur'],
                       other_current_screen_border=theme['foreground'],
                       other_screen_border=theme['screenblur'],
                       urgent_alert_method='text',
                       fontsize=fontsize,
                       borderwidth=2,
                      ),
            LayoutIcon(background=theme['rootwindow']),
            widget.WindowName(foreground=theme['text'], background=theme['rootwindow'], for_current_screen=True),
            widget.Prompt(foreground=theme['textprompt'],
                          cursor_color=theme['foreground'],
                          bell_style='visual',
                          visual_bell_time=0.1,
                          visual_bell_color='#ffffff',
                          font="DejaVu Sans Mono",
                         ),
        ]
    hostname = socket.gethostname()
    if hostname in ("onyx", ):
        widgets += [
                widget.Battery(battery_name='BAT0',
                               foreground=theme['textbattery'],
                               charge_char='+',
                               discharge_char='–',
                               format='{char}{percent:2.0%} {hour:d}:{min:02d} ',
                              ),
            ]
    widgets += [
            widget.GenPollText(func=config_funcs.get_net_diag, update_interval=30, foreground='#880088'),
            widget.GenPollText(func=config_funcs.get_dirty_mem_M, update_interval=15, foreground='#ff4400'),
            widget.Clock(format='%Z %H:%M', timezone="EST5EDT", foreground='#3030a0'),
            widget.Clock(format='%Z %H:%M', timezone="Europe/Berlin", foreground='#805000'),
            widget.Clock(format='%Z %H:%M'),
            widget.Clock(format='%a %Y-%m-%d', foreground='#888888'),
            widget.Systray(icon_size=iconsize),
        ]
    return widgets
