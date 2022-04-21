#!/usr/bin/env python3
# coding: utf-8
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 colorcolumn=100

import subprocess
import re
import math
import os

import libqtile


def move_window_to_screen(screen_index):
    def cmd(qtile):
        w = qtile.current_window
        if w is not None:
            w.floating = False
            w.cmd_toscreen(screen_index)
    return cmd


def move_window_to_group(group):
    def cmd(qtile):
        w = qtile.current_window
        if w is not None:
            w.floating = False
            w.togroup(group.name)
    return cmd


def swap_active_screen_with(group):
    def cmd(qtile):
        current = qtile.current_group
        other = qtile.groups_map[group.name]
        if other is not current:
            screen = qtile.current_screen.index
            current_windows = [w for w in current.windows]
            other_windows = [w for w in other.windows]
            for w in other_windows:
                w.togroup(current.name)
            for w in current_windows:
                w.togroup(other.name)
            qtile.focus_screen(screen)
    return cmd


def next_window_to_front_if_float(qtile):
    qtile.current_group.cmd_next_window()
    if qtile.current_window.floating:
        qtile.current_window.cmd_bring_to_front()


def window_audio(what):
    def mute(src, ismuted, lvol, rvol):
        os.system("pactl set-sink-input-mute {} {}".format(src, "0" if ismuted else "1"))
    def reset(src, ismuted, lvol, rvol):
        os.system("pactl set-sink-input-mute {} 0".format(src))
        os.system("pactl set-sink-input-volume {} 65536".format(src))
    def up(src, ismuted, lvol, rvol):
        newvol = int((lvol + rvol) / 2 + 2000)
        os.system("pactl set-sink-input-volume {} {}".format(src, newvol))
    def down(src, ismuted, lvol, rvol):
        newvol = int((lvol + rvol) / 2 - 2000)
        os.system("pactl set-sink-input-volume {} {}".format(src, newvol))
    audio_funs = {"mute": mute, "reset": reset, "up": up, "down": down}

    if what not in audio_funs:
        raise ValueError("Unknown audio operation: {}".format(what))

    action = audio_funs[what]

    def fun(qtile):
        if not qtile.current_window:
            return

        pid = qtile.current_window.window.get_property("_NET_WM_PID", unpack=int)[0]
        exe = os.readlink("/proc/{}/exe".format(pid))

        sources = []
        srcdisplay = None
        srcexe = None
        srcindex = None
        srcmuted = None
        srcpid = None
        srclvol = None
        srcrvol = None
        sink_input_list = subprocess.run(["pactl", "list", "sink-inputs"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in sink_input_list.stdout.decode().split('\n') + ["Sink Input FINI"]:
            line = line.lstrip(" \t")
            if line.startswith("Sink Input"):
                if srcindex is not None:
                    if srcdisplay is not None:
                        if srcexe == exe:
                            sources.append((srcindex, srcmuted, srclvol, srcrvol))
                try:
                    srcindex = int(line.split()[2].lstrip("#"))
                except (IndexError, ValueError):
                    srcindex = None
                srcdisplay = None
                srcexe = None
                srcmuted = None
                srcpid = None
                srclvol = None
                srcrvol = None
            elif line.startswith("window.x11.display"):
                srcdisplay = line.split()[2].lstrip('"').rstrip('"')
            elif line.startswith("application.process.id"):
                srcpid = int(line.split()[2].lstrip('"').rstrip('"'))
                srcexe = os.readlink("/proc/{}/exe".format(srcpid))
            elif line.startswith("muted:") or line.startswith("Mute:"):
                srcmuted = ("yes" == line.split()[1])
            elif line.startswith("volume:") or line.startswith("Volume:"):
                line = line.split()
                srclvol = int(line[2])
                srcrvol = int(line[9])

        for source in sources:
            action(*source)

    return fun


def get_primary_display_dpi():
    xo = subprocess.run("xrandr", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for line in xo.stdout.decode().split('\n'):
            m = re.match(r'([^ ]*) connected primary ([0-9]*)x([0-9]*)\+[0-9]*\+[0-9]* ([a-z]* ?)\(.*\) ([0-9]*)mm x ([0-9]*)mm', line)
            if m is not None:
                #display = m.group(1)
                res_x = int(m.group(2))
                res_y = int(m.group(3))
                size_x_mm = int(m.group(5))
                size_y_mm = int(m.group(6))
                res_dia = math.sqrt(res_x**2 + res_y**2)
                size_dia_inch = math.sqrt(size_x_mm**2 + size_y_mm**2) / 25.4
                dpi = res_dia / size_dia_inch
                return int(round(dpi, 0))
    except Exception as e:
        print("Error to find DPI: {}".format(e), flush=True)
    print("DPI defaulting to 100")
    return 100


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
        return "?"
    except Exception as e:
        print("Error identifying dirty memory: {}".format(e), flush=True)
        return "E"


@libqtile.hook.subscribe.client_new
def float_dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True


def exec_poststart(theme):
    subprocess.call(['xsetroot', '-solid', theme['rootwindow']])
