import sys
import curses
from enum import Enum

class Opts(Enum):
    CONTINUE_INSTALL  = 1
    TERMINATE_INSTALL = 2
    SET_LANGUAGE      = 3

    def opt_to_text(opt):
        if opt == Opts.CONTINUE_INSTALL:
            return 'Continue installing'
        elif opt == Opts.TERMINATE_INSTALL:
            return 'Stop installing'
        elif opt == Opts.SET_LANGUAGE:
            return 'Set install language'

    def opt_to_action(opt):
        if opt == Opts.CONTINUE_INSTALL:
            pass
        elif opt == Opts.TERMINATE_INSTALL:
            sys.exit()
        elif opt == Opts.SET_LANGUAGE:
            pass

class Menu:
    def __init__(self, options):
        self.options = options
        self.chosen = 0
        self.w = 35

    def draw_borders(self, stdscr):
        stdscr.addstr(0, 0, "╔")
        for i in range(self.w - 1):
            stdscr.addstr(0, i + 1, "═")
        stdscr.addstr(0, self.w, "╗")

        for i in range(len(self.options)):
            stdscr.addstr(i + 1, 0, "║")
        for i in range(len(self.options)):
            stdscr.addstr(i + 1, self.w, "║")

        stdscr.addstr(len(self.options) + 1, 0, "╚")
        for i in range(self.w - 1):
            stdscr.addstr(len(self.options) + 1, i + 1, "═")
        stdscr.addstr(len(self.options) + 1, self.w, "╝")

    def display(self, stdscr):
        self.draw_borders(stdscr)

        r = 0
        for o in self.options:
            if o.value == self.options[self.chosen].value:
                stdscr.addstr(r + 1, 2, '* ' + Opts.opt_to_text(o))
            else:
                stdscr.addstr(r + 1, 4, Opts.opt_to_text(o))
            r += 1

    def choose_current(self):
        Opts.opt_to_action(self.options[self.chosen])

def main(stdscr):
    stdscr.keypad(True)
    curses.curs_set(False)
    main_menu = Menu([
        Opts.SET_LANGUAGE,
        Opts.CONTINUE_INSTALL,
        Opts.TERMINATE_INSTALL
    ])
    while True:
        curses.noecho()
        stdscr.clear()
        main_menu.display(stdscr)
        stdscr.refresh()
        i = stdscr.getch()
        if i == curses.KEY_DOWN:
            main_menu.chosen += 1
        if i == curses.KEY_UP:
            main_menu.chosen -= 1
        if i == curses.KEY_ENTER:
            main_menu.choose_current()

curses.wrapper(main)

# Terminate app
curses.nocbreak()
curses.echo()
