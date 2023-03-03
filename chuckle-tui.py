#!/usr/bin/python3

import sys
import curses
from enum import Enum

MENU_WIDTH = 40

class Opts(Enum):
    # Main menu
    CONTINUE_INSTALL  = 1
    TERMINATE_INSTALL = 2
    SET_LANGUAGE      = 3
    MANAGE_PARTITIONS = 4

    # Set language menu
    # NOTE Language select menu needs a rewrite to scan 'n stuff to detect locales 'n shit
    KB_EN_US = 5
    KB_FI    = 6

    # PARTITIONS MENU
    USE_DEFAULT_PARTITION_SCHEME = 7
    USE_CUSTOM_PARTITION_SCHEME  = 8

    def opt_to_text(opt):
        if opt == Opts.CONTINUE_INSTALL:
            return 'Continue installing'
        elif opt == Opts.TERMINATE_INSTALL:
            return 'Stop installing'
        elif opt == Opts.SET_LANGUAGE:
            return 'Set install language'
        elif opt == Opts.MANAGE_PARTITIONS:
            return 'Manage partitions'
        elif opt == Opts.KB_EN_US:
            return 'English (US)'
        elif opt == Opts.KB_FI:
            return 'Finnish'
        elif opt == Opts.USE_DEFAULT_PARTITION_SCHEME:
            return 'Use the default partition scheme'
        elif opt == Opts.USE_CUSTOM_PARTITION_SCHEME:
            return 'Use a custom partition scheme'
        return 'UNKNOWN OPTION (SHOULD NEVER BE SEEN)'

    def opt_to_action(opt, menus):
        if opt == Opts.CONTINUE_INSTALL:
            pass
        elif opt == Opts.TERMINATE_INSTALL:
            sys.exit()
        elif opt == Opts.SET_LANGUAGE:
            menus.append(
                Menu(
                    [Opts.KB_EN_US, Opts.KB_FI], MENU_WIDTH+1, 0
                )
            )
        elif opt == Opts.MANAGE_PARTITIONS:
            menus.append(
                Menu(
                    [Opts.USE_DEFAULT_PARTITION_SCHEME, Opts.USE_CUSTOM_PARTITION_SCHEME], MENU_WIDTH+1, 0
                )
            )

class Menu:
    def __init__(self, options, x=0, y=0):
        self.options = options
        self.chosen = 0
        self.w = MENU_WIDTH
        self.x = x
        self.y = y

    def draw_borders(self, stdscr):
        stdscr.addstr(self.y, self.x, "╔")
        for i in range(self.w - 1):
            stdscr.addstr(self.y, i+self.x + 1, "═")
        stdscr.addstr(self.y, self.x+self.w, "╗")

        for i in range(len(self.options)):
            stdscr.addstr(self.y + i + 1, self.x, "║")
        for i in range(len(self.options)):
            stdscr.addstr(i + 1 + self.y, self.w + self.x, "║")

        stdscr.addstr(len(self.options) + 1 + self.y, self.x, "╚")
        for i in range(self.w - 1):
            stdscr.addstr(len(self.options) + 1 + self.y, i + 1 + self.x, "═")
        stdscr.addstr(len(self.options) + 1 + self.y, self.w + self.x, "╝")

    def display(self, stdscr):
        self.draw_borders(stdscr)

        r = 0
        for o in self.options:
            if o.value == self.options[self.chosen].value:
                stdscr.addstr(r + 1 + self.y, 2 + self.x, '* ' + Opts.opt_to_text(o))
            else:
                stdscr.addstr(r + 1 + self.y, 4 + self.x, Opts.opt_to_text(o))
            r += 1

    def choose_current(self, menus):
        Opts.opt_to_action(self.options[self.chosen], menus)

def main(stdscr):
    stdscr.keypad(True)
    curses.curs_set(False)
    menus = [Menu([
        Opts.SET_LANGUAGE,
        Opts.MANAGE_PARTITIONS,
        Opts.CONTINUE_INSTALL,
        Opts.TERMINATE_INSTALL
    ], 0, 0)]
    chosen = 0
    while True:
        curses.noecho()
        stdscr.clear()
        for m in menus:
            m.display(stdscr)
        stdscr.refresh()
        i = stdscr.getch()
        if i == curses.KEY_DOWN and (menus[chosen].chosen < len(menus[chosen].options) - 1):
            menus[chosen].chosen += 1
        elif i == curses.KEY_UP and (menus[chosen].chosen > 0):
            menus[chosen].chosen -= 1
        elif i == curses.KEY_RIGHT and chosen == 0:
            menus[0].choose_current(menus)
            chosen = 1
        elif i == curses.KEY_LEFT and chosen == 1:
            menus.remove(menus[1])
            chosen = 0

curses.wrapper(main)

# Terminate app
curses.nocbreak()
curses.echo()
