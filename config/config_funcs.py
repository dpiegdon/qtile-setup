#!/usr/bin/env python3
# coding: utf-8
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 colorcolumn=100

import subprocess
import re
import math
import os


def move_window_to_screen(screen_index):
    def cmd(qtile):
        w = qtile.current_window
        if w is not None:
            w.floating = False
            w.toscreen(screen_index)
    return cmd


def move_window_to_group(group):
    def cmd(qtile):
        w = qtile.current_window
        if w is not None:
            w.floating = False
            w.togroup(group.name)
    return cmd


def next_window_to_front_if_float(qtile):
    qtile.current_group.cmd_next_window()
    if qtile.current_window.floating:
        qtile.current_window.cmd_bring_to_front()


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
        print("Error to find DPI: {}".format(e))
        print("defaulting to 100")
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
        print("Error identifying dirty memory: {}".format(e))
        return "E"


def exec_poststart(theme):
    # set root-window background
    subprocess.call(['xsetroot', '-solid', theme['rootwindow']])
