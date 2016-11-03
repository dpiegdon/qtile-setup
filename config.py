#!/usr/bin/env python
# coding: utf-8
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 colorcolumn=100

import socket

from libqtile import layout, widget, bar, hook
from libqtile.widget import base
from libqtile.manager import Screen, Drag, Click
from libqtile.command import lazy
from libqtile.config import Key, Screen, Group, Drag, Click


from libqtile.widget.groupbox import _GroupBase

class MyGroupBox(_GroupBase):
    """A widget that graphically displays the current group"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("active", "FFFFFF", "Active group font colour"),
        ("inactive", "404040", "Inactive group font colour"),
        (
            "highlight_method",
            "border",
            "Method of highlighting ('border', 'block', 'text', or 'line')"
            "Uses \*_border color settings"
        ),
        ("rounded", True, "To round or not to round box borders"),
        (
            "this_current_screen_border",
            "215578",
            "Border or line colour for group on this screen when focused."
        ),
        (
            "this_screen_border",
            "215578",
            "Border or line colour for group on this screen when unfocused."
        ),
        (
            "other_current_screen_border",
            "215578",
            "Border or line colour for group on other screen when focused."
        ),
        (
            "other_screen_border",
            "404040",
            "Border or line colour for group on other screen."
        ),
        (
            "highlight_color",
            ["000000", "282828"],
            "Active group highlight color when using 'line' highlight method."
        ),
        (
            "urgent_alert_method",
            "border",
            "Method for alerting you of WM urgent "
            "hints (one of 'border', 'text', 'block', or 'line')"
        ),
        ("urgent_text", "FF0000", "Urgent group font color"),
        ("urgent_border", "FF0000", "Urgent border or line color"),
        (
            "disable_drag",
            False,
            "Disable dragging and dropping of group names on widget"
        ),
        ("invert_mouse_wheel", False, "Whether to invert mouse wheel group movement"),
        (
            "visible_groups",
            None,
            "Groups that will be visible "
            "(if set to None or [], all groups will be visible)"
        )
    ]

    def __init__(self, **config):
        _GroupBase.__init__(self, **config)
        self.add_defaults(MyGroupBox.defaults)
        self.clicked = None

    @property
    def groups(self):
        return self.qtile.groups if not self.visible_groups else \
            [g for g in self.qtile.groups if g.name in self.visible_groups]

    def get_clicked_group(self, x, y):
        group = None
        new_width = 0
        width = 0
        for g in self.groups:
            new_width += self.box_width([g])
            if width <= x <= new_width:
                group = g
                break
            width = new_width
        return group

    def button_press(self, x, y, button):
        self.clicked = None
        group = None
        curGroup = self.qtile.currentGroup

        if button == (5 if not self.invert_mouse_wheel else 4):
            i = itertools.cycle(self.qtile.groups)
            while next(i) != curGroup:
                pass
            while group is None or group not in self.groups:
                group = next(i)
        elif button == (4 if not self.invert_mouse_wheel else 5):
            i = itertools.cycle(reversed(self.qtile.groups))
            while next(i) != curGroup:
                pass
            while group is None or group not in self.groups:
                group = next(i)
        else:
            group = self.get_clicked_group(x, y)
            if not self.disable_drag:
                self.clicked = group

        if group:
            self.bar.screen.setGroup(group)

    def button_release(self, x, y, button):
        if button not in (5, 4):
            group = self.get_clicked_group(x, y)
            if group and self.clicked:
                group.cmd_switch_groups(self.clicked.name)
                self.clicked = None

    def calculate_length(self):
        width = 0
        for g in self.groups:
            width += self.box_width([g])
        return width

    def group_has_urgent(self, group):
        return len([w for w in group.windows if w.urgent]) > 0

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)

        offset = 0
        for i, g in enumerate(self.groups):
            to_highlight = False
            is_block = (self.highlight_method == 'block')
            is_line = (self.highlight_method == 'line')

            bw = self.box_width([g])

            if self.group_has_urgent(g) and self.urgent_alert_method == "text":
                text_color = self.urgent_text
            elif g.windows:
                text_color = self.active
            else:
                text_color = self.inactive

            if g.screen:
                if self.highlight_method == 'text':
                    border = self.bar.background
                    text_color = self.this_current_screen_border
                else:
                    if self.bar.screen.group.name == g.name:
                        if self.qtile.currentScreen == self.bar.screen:
                            border = self.this_current_screen_border
                            to_highlight = True
                        else:
                            border = self.this_screen_border
                    else:
                        if self.qtile.currentScreen == g.screen:
                            border = self.other_current_screen_border
                        else:
                            border = self.other_screen_border
            elif self.group_has_urgent(g) and \
                    self.urgent_alert_method in ('border', 'block', 'line'):
                border = self.urgent_border
                if self.urgent_alert_method == 'block':
                    is_block = True
                elif self.urgent_alert_method == 'line':
                    is_line = True
            else:
                border = self.background or self.bar.background

            self.drawbox(
                self.margin_x + offset,
                g.name,
                border,
                text_color,
                highlight_color=self.highlight_color,
                width=bw - self.margin_x * 2 - self.padding_x * 2,
                rounded=self.rounded,
                block=is_block,
                line=is_line,
                highlighted=to_highlight
            )
            offset += bw
        self.drawer.draw(offsetx=self.offset, width=self.width)






from libqtile import hook, bar
from libqtile.widget import base

class MyWindowName(base._TextBox):
    """Displays the name of the window that currently has focus"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('show_state', True, 'show window status before window name'),
        ('for_current_screen', False, 'instead of bars screen use currently active screen')
    ]

    def __init__(self, width=bar.STRETCH, **config):
        base._TextBox.__init__(self, width=width, **config)
        self.add_defaults(MyWindowName.defaults)

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        hook.subscribe.window_name_change(self.update)
        hook.subscribe.focus_change(self.update)
        hook.subscribe.float_change(self.update)
        # Clear the widget if group has no window
        @hook.subscribe.client_killed
        def on_client_killed(window):
            if ((not self.for_current_screen and window == self.bar.screen.group.currentWindow) or
                (self.for_current_screen and window == self.qtile.currentScreen.group.currentWindow)):
                self.text = ""
                self.bar.draw()
        @hook.subscribe.current_screen_change
        def on_screen_changed():
            if self.for_current_screen:
                self.update()

    def update(self):
        if self.for_current_screen:
            w = self.qtile.currentScreen.group.currentWindow
        else:
            w = self.bar.screen.group.currentWindow
        state = ''
        if self.show_state and w is not None:
            if w.maximized:
                state = '[] '
            elif w.minimized:
                state = '_ '
            elif w.floating:
                state = 'V '
        self.text = "%s%s" % (state, w.name if w and w.name else " ")
        self.bar.draw()







class MyPrompt(widget.Prompt):
    def __init__(self, name="prompt", **config):
        widget.Prompt.__init__(self, name, **config)

    def _highlight_text(self, text):
        if self.show_cursor:
            text = '<span foreground="{0}" background="{1}">{2}</span>'.format('#000000', '#ff0000', text)
        else:
            text = '<span foreground="{0}" background="{1}">{2}</span>'.format('#ff0000', '#000000', text)
        return text







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
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),

    Key([mod], "y", lazy.layout.shrink()),
    Key([mod], "u", lazy.layout.grow()),
    Key([mod], "i", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),

    Key([mod, "shift"], "space", lazy.layout.flip()),

    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Swap panes of split stack
    Key([mod, "shift"], "n", lazy.layout.rotate()),

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
    Key([mod], "Escape", lazy.spawn("xlock")),
    Key([mod, "control"], "Return", lazy.spawn("/usr/bin/xterm -u8 -e tmux -2 attach")),

    Key([mod], "Left",  lazy.screen.prev_group(skip_managed=True)),
    Key([mod], "Right", lazy.screen.next_group(skip_managed=True)),
]

# map function keys to special_keys script
for _modifier in [ ("", "NONE"),
                   ("shift", "SHIFT"),
                   ("control", "CTRL"),
                   ("mod1", "ALT"),
                   ("mod5", "MODESWITCH") ]:
    for _fkey in range(1,11):
        _fkey_name = "F{}".format(_fkey)
        _mod = [mod]
        if("" != _modifier[0]):
            _mod.append(_modifier[0])
        keys.append( Key(_mod, _fkey_name, lazy.spawn("/home/dpiegdon/bin/special_keys {} {}".format(_fkey_name, _modifier[1])) ) )

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.append(Key([mod],          i.name, lazy.group[i.name].toscreen()))
    keys.append(Key([mod, "shift"], i.name, lazy.window.togroup(i.name)))


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),     start=lazy.window.get_size()),
]




layouts = [
    layout.MonadTall(border_focus="#ff0000", border_normal="#008888"),
    layout.Stack(num_stacks=2, border_focus="#00ff00", border_normal="#008888"),
    layout.Max(),
]

widget_defaults = dict(font='Arial', fontsize=13, padding=2)

def init_widgets():
    widgets = [
            MyGroupBox(disable_drag=True,
                       highlight_method='block',
                       this_current_screen_border='#cc0000',
                       this_screen_border='#446666',
                       other_current_screen_border='#cc0000',
                       other_screen_border='#446666',
                       urgent_alert_method='text',
                       fontsize=9,
                       borderwidth=1,
                      ),
#           widget.CurrentLayout(foreground='8b6840'),
            MyWindowName(foreground='#c0c0c0', for_current_screen=True),
#           widget.CurrentScreen(),
            MyPrompt(foreground='#44ff44',
                          cursor_color='#ff4444',
                          bell_style='visual',
                          visual_bell_time=0.1,
                          font="DejaVu Sans Mono",
                         ),
        ]
    if "proton" == socket.gethostname():
        widgets += [
                widget.Battery(battery_name='BATC',
                               foreground='#00aaaa',
                               charge_char='+',
                               discharge_char='–',
                               format='{char}{percent:2.0%} {hour:d}:{min:02d} ',
                              ),
            ]
    widgets += [
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
floating_layout = layout.Floating(border_focus="#0000ff", border_normal="#333366")
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

