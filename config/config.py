#!/usr/bin/env python
# coding: utf-8
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 colorcolumn=100

# default config is in qtile repo in:
# libqtile/resources/default_config.py

import socket
from subprocess import call

from libqtile import layout, widget, bar, hook
from libqtile.widget import base
from libqtile.manager import Screen, Drag, Click
from libqtile.command import lazy
from libqtile.config import Key, Screen, Group, Drag, Click

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
        w = qtile.currentWindow
        # XXX: strange behaviour - w.focus() doesn't work
        # if toScreen is called after togroup...
        qtile.toScreen(screen)
        if w is not None:
            w.togroup(qtile.screens[screen].group.name)
    return cmd

mod = "mod4"

keys = [
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),

    Key([mod], "n", lazy.layout.next()),
    Key([mod], "p", lazy.layout.previous()),

    Key([mod], "Tab", lazy.group.next_window()),
    Key([mod, "shift"], "Tab", lazy.window.bring_to_front()),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),

    Key([mod, "control", "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "control", "shift"], "j", lazy.layout.swap_down()),
    Key([mod, "control", "shift"], "k", lazy.layout.swap_up()),
    Key([mod, "control", "shift"], "l", lazy.layout.swap_right()),

    Key([mod], "y", lazy.layout.shrink()),
    Key([mod], "u", lazy.layout.grow()),
    Key([mod], "i", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),

    Key([mod, "shift"], "space", lazy.layout.flip()),


    # Swap panes of split stack
    Key([mod, "shift"], "n", lazy.layout.rotate()),

    Key([mod], "Up", lazy.hide_show_bar()),
    Key([mod], "Return", lazy.window.toggle_fullscreen()),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # Handle floating windows
    Key([mod], "t", lazy.window.toggle_floating()),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout()),

    # Multi-Display setup
    Key([mod], "w", lazy.to_screen(0)),
    Key([mod, "shift"], "w", lazy.function(move_window_to_screen(0))),
    Key([mod], "e", lazy.to_screen(1)),
    Key([mod, "shift"], "e", lazy.function(move_window_to_screen(1))),
    Key([mod], "r", lazy.to_screen(2)),
    Key([mod, "shift"], "r", lazy.function(move_window_to_screen(2))),

    # Execute programs and terminate/reconfig WM
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "shift"], "q", lazy.restart()),
    Key([mod, "control", "shift"], "q", lazy.shutdown()),
    Key([mod], "BackSpace", lazy.spawncmd()),
    Key([mod], "Escape", lazy.spawn("xautolock-force")),
    Key([mod, "mod5"], "Escape", lazy.spawn("xautolock -toggle")),
    Key([mod, "control"], "Return", lazy.spawn("/usr/bin/xterm -u8 -e tmux -2 attach")),

    Key([mod], "Left",  lazy.screen.prev_group(skip_empty=True, skip_managed=True)),
    Key([mod], "Right", lazy.screen.next_group(skip_empty=True, skip_managed=True)),
    Key([mod, "shift"], "Left",  lazy.screen.prev_group(skip_managed=True)),
    Key([mod, "shift"], "Right", lazy.screen.next_group(skip_managed=True)),
]

# map function keys to special_keys script
for _modifier in [ ("", "NONE"),
                   ("shift", "SHIFT"),
                   ("control", "CTRL"),
                   ("mod1", "ALT"),
                   ("mod5", "MODESWITCH") ]:
    for _fkey in range(1,13):
        _fkey_name = "F{}".format(_fkey)
        _mod = [mod]
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

groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.append(Key([mod],          i.name, lazy.group[i.name].toscreen()))
    keys.append(Key([mod, "shift"], i.name, lazy.window.togroup(i.name)))


mouse = [
    Click([], "Button9", lazy.spawn("special_keys MOUSE9 NONE")),
    Click(["shift"], "Button9", lazy.spawn("special_keys MOUSE9 SHIFT")),
    Click(["control"], "Button9", lazy.spawn("special_keys MOUSE9 CTRL")),
    Click(["mod1"], "Button9", lazy.spawn("special_keys MOUSE9 ALT")),
    Click(["mod5"], "Button9", lazy.spawn("special_keys MOUSE9 MODESWITCH")),
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),     start=lazy.window.get_size()),
    #Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position(True), finish=lazy.window.reset_mouse_focus()),
    #Drag([mod], "Button3", lazy.window.set_size_floating(),     start=lazy.window.get_size(True), finish=lazy.window.reset_mouse_focus()),
]




layouts = [
    layout.Columns(border_focus=theme['focus'], border_normal=theme['blur'], grow_amount=2),
    #layout.MonadTall(border_focus=theme['focus'], border_normal=theme['blur']),
    #layout.Tile(ratio=0.5, border_focus=theme['focus'], border_normal=theme['blur']),
    #layout.Max(),
    #layout.Floating(border_focus=theme['floatfocus'], border_normal=theme['floatblur']),
]

widget_defaults = dict(font='Arial', fontsize=13, padding=2)

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
    widgets = [
            widget.GroupBox(disable_drag=True,
                       highlight_method='block',
                       this_current_screen_border=theme['foreground'],
                       this_screen_border=theme['screenblur'],
                       other_current_screen_border=theme['foreground'],
                       other_screen_border=theme['screenblur'],
                       urgent_alert_method='text',
                       fontsize=9,
                       borderwidth=1,
                      ),
#           widget.CurrentLayout(foreground='8b6840'),
            widget.WindowName(foreground=theme['text'], for_current_screen=True),
#           widget.CurrentScreen(),
            widget.Prompt(foreground=theme['textprompt'],
                          cursor_color=theme['foreground'],
                          cursor_style='block',
                          bell_style='visual',
                          visual_bell_time=0.1,
                          visual_bell_color='#ffffff',
                          font="DejaVu Sans Mono",
                         ),
        ]
    if "proton" == socket.gethostname():
        widgets += [
                widget.Battery(battery_name='BATC',
                               foreground=theme['textbattery'],
                               charge_char='+',
                               discharge_char='–',
                               format='{char}{percent:2.0%} {hour:d}:{min:02d} ',
                              ),
            ]
    elif "aluminumbar" == socket.gethostname():
        widgets += [
                widget.Battery(battery_name='BAT0',
                               foreground=theme['textbattery'],
                               charge_char='+',
                               discharge_char='–',
                               format='{char}{percent:2.0%} {hour:d}:{min:02d} ',
                              ),
            ]
    widgets += [
            widget.GenPollText(func=get_dirty_mem_M, update_interval=15, foreground='#ff4400'),
            widget.Clock(format='%Y-%m-%d %a %H:%M'),
            widget.Systray(icon_size=12),
        ]
    return widgets

screens = [ Screen(top=bar.Bar(init_widgets(), 18)) ]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = True
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
call(['xsetroot', '-solid', theme['rootwindow']])

