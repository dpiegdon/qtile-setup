#!/usr/bin/env python
# coding: utf-8
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 colorcolumn=100

# default config is in qtile repo in:
#   libqtile/resources/default_config.py
# when default-config is used due to config error, type:
#   WIN+CTRL+R  to restart qtile
#   WIN+R       to execute something

import socket
import subprocess
import os
import re
import math

from libqtile import layout, widget, bar, hook
from libqtile.widget import base
from libqtile.core.manager import Screen, Drag, Click
from libqtile.command import lazy
from libqtile.config import Key, Screen, Group, Drag, Click

def get_primary_display_dpi():
    xo = subprocess.run("xrandr", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for line in xo.stdout.decode().split('\n'):
            m = re.match(r'([^ ]*) connected primary ([0-9]*)x([0-9]*)\+0\+0 \(.*\) ([0-9]*)mm x ([0-9]*)mm', line)
            if m is not None:
                #display = m.group(1)
                res_x = int(m.group(2))
                res_y = int(m.group(3))
                size_x_mm = int(m.group(4))
                size_y_mm = int(m.group(5))
                res_dia = math.sqrt(res_x**2 + res_y**2)
                size_dia_inch = math.sqrt(size_x_mm**2 + size_y_mm**2) / 25.4
                dpi = res_dia / size_dia_inch
                return int(round(dpi, 0))
                
    except Exception:
        pass
    return 100 # sane default

redTheme = {
        'focus':       '#ff0000',
        'blur':        '#008888',
        'floatfocus':  '#ff8800',
        'floatblur':   '#004488',
        'rootwindow':  '#440000',
        'foreground':  '#cc0000',
        'screenblur':  '#007777',
        'background':  '#000000',
        'text':        '#c0c0c0',
        'textprompt':  '#44ff44',
        'textbattery': '#00aaaa',
    }

greenTheme = {
        'focus':       '#00ff00',
        'blur':        '#880088',
        'floatfocus':  '#00ff88',
        'floatblur':   '#880044',
        'rootwindow':  '#004400',
        'foreground':  '#00cc00',
        'screenblur':  '#770077',
        'background':  '#000000',
        'text':        '#c0c0c0',
        'textprompt':  '#ff44ff',
        'textbattery': '#aa00aa',
    }

blueTheme = {
        'focus':       '#0088ff',
        'blur':        '#333366',
        'floatfocus':  '#338888',
        'floatblur':   '#333366',
        'rootwindow':  '#001133',
        'foreground':  '#0077dd',
        'screenblur':  '#bb9900',
        'background':  '#000000',
        'text':        '#c0c0c0',
        'textprompt':  '#44ff44',
        'textbattery': '#00aaaa',
    }

yellowTheme = {
        'focus':       '#ffee00',
        'blur':        '#003366',
        'floatfocus':  '#ff9900',
        'floatblur':   '#0077ff',
        'rootwindow':  '#332200',
        'foreground':  '#ccbb00',
        'screenblur':  '#005588',
        'background':  '#000000',
        'text':        '#c0c0c0',
        'textprompt':  '#ff8866',
        'textbattery': '#00aaaa',
    }

theme = redTheme

def move_window_to_screen(screen):
    def cmd(qtile):
        w = qtile.current_window
        if w is not None:
            w.togroup(qtile.screens[screen].group.name)
    return cmd

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

    # Multi-Display setup
    Key([modkey], "w", lazy.to_screen(0)),
    Key([modkey, shiftkey], "w", lazy.function(move_window_to_screen(0))),
    Key([modkey], "e", lazy.to_screen(1)),
    Key([modkey, shiftkey], "e", lazy.function(move_window_to_screen(1))),
    Key([modkey], "r", lazy.to_screen(2)),
    Key([modkey, shiftkey], "r", lazy.function(move_window_to_screen(2))),

    # Execute programs and terminate/reconfig WM
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

# map function keys to special_keys script
for _modifier in [ ("", "NONE"),
                   (shiftkey, "SHIFT"),
                   (controlkey, "CTRL"),
                   (altkey, "ALT"),
                   (modeswitchkey, "MODESWITCH") ]:
    for _fkey in range(1,13):
        _fkey_name = "F{}".format(_fkey)
        _mod = [modkey]
        if("" != _modifier[0]):
            _mod.append(_modifier[0])
        keys.append( Key(_mod, _fkey_name, lazy.spawn("special_keys {} {}".format(_fkey_name, _modifier[1])) ) )

for _fkey in [  "XF86MonBrightnessDown",
                "XF86MonBrightnessUp",
                "XF86LaunchA",
                "XF86LaunchB",
                "XF86KbdBrightnessDown",
                "XF86KbdBrightnessUp",
                "XF86AudioPrev",
                "XF86AudioPlay",
                "XF86AudioNext",
                "XF86AudioMute",
                "XF86AudioLowerVolume",
                "XF86AudioRaiseVolume",
                "XF86Eject"
                ]:
    keys.append( Key([], _fkey, lazy.spawn("special_keys {} NONE".format(_fkey))) )

groups = [Group(i) for i in "1234567890-="]

for i in groups:
    try:
        keyname = { '`': "grave", '-': "minus", '=': "equal" }[i.name]
    except KeyError:
        keyname = i.name
    keys.append(Key([modkey],           keyname, lazy.group[i.name].toscreen(toggle=False)))
    keys.append(Key([modkey, shiftkey], keyname, lazy.window.togroup(i.name)))


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




layouts = [
    layout.Columns(border_focus=theme['focus'], border_normal=theme['blur'], grow_amount=2),
    #layout.MonadTall(border_focus=theme['focus'], border_normal=theme['blur']),
    #layout.Tile(ratio=0.5, border_focus=theme['focus'], border_normal=theme['blur']),
    #layout.Max(),
    #layout.Floating(border_focus=theme['floatfocus'], border_normal=theme['floatblur']),
]

dpi = get_primary_display_dpi()
barheight = max(18, int(round(dpi * 0.11, 0)))
fontsize = barheight - 4
iconsize = barheight - 4

widget_defaults = dict(font='Arial', fontsize=fontsize, padding=2)

def get_net_diag():
    try:
        with open(os.path.expanduser("~/.qtile/config/net-diag.conf")) as config:
            for line in config.readlines():
                (dst, name) = line.split()
                ping = subprocess.Popen(["ping", "-c1", dst],
                                        stdin = subprocess.PIPE,
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.STDOUT)
                if 0 == ping.wait():
                    return "+"+name
        return "-"
    except Exception:
        return "?conf"

def get_dirty_mem_M():
    try:
        with open("/proc/meminfo") as meminfo:
            while True:
                line = meminfo.readline().rstrip('\n ')
                if line.startswith('Dirty:'):
                    dirtymem_K = int(line.split()[1])
                    return "{}M".format(int(dirtymem_K / 1024))
    except Exception:
        pass
    return "?"

def init_widgets():
    global fontsize
    global iconsize
    widgets = [
            widget.GroupBox(disable_drag=True,
                       use_mouse_wheel=False,
                       highlight_method='block',
                       this_current_screen_border=theme['foreground'],
                       this_screen_border=theme['screenblur'],
                       other_current_screen_border=theme['foreground'],
                       other_screen_border=theme['screenblur'],
                       urgent_alert_method='text',
                       fontsize=fontsize,
                       borderwidth=2,
                      ),
            widget.WindowName(foreground=theme['text'], for_current_screen=True),
            widget.Prompt(foreground=theme['textprompt'],
                          cursor_color=theme['foreground'],
                          cursor_style='block',
                          bell_style='visual',
                          visual_bell_time=0.1,
                          visual_bell_color='#ffffff',
                          font="DejaVu Sans Mono",
                         ),
        ]
    hostname = socket.gethostname()
    if hostname in ["aluminumbar", "onyx"]:
        widgets += [
                widget.Battery(battery_name='BAT0',
                               foreground=theme['textbattery'],
                               charge_char='+',
                               discharge_char='–',
                               format='{char}{percent:2.0%} {hour:d}:{min:02d} ',
                              ),
            ]
    widgets += [
            widget.GenPollText(func=get_net_diag, update_interval=30, foreground='#880088'),
            widget.GenPollText(func=get_dirty_mem_M, update_interval=15, foreground='#ff4400'),
            widget.Clock(format='%Y-%m-%d %a %H:%M'),
            widget.Systray(icon_size=iconsize),
        ]
    return widgets

screens = [ Screen(top=bar.Bar(init_widgets(), barheight)) ]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(border_focus=theme['floatfocus'], border_normal=theme['floatblur'])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# set root-window background
subprocess.call(['xsetroot', '-solid', theme['rootwindow']])

