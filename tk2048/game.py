#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Gabriele Cirulli's 2048 puzzle game

    Python3-Tkinter port by Raphaël Seban <motus@laposte.net>

    Copyright (c) 2014+ Raphaël Seban for the present code

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

# lib imports

import random

import tkinter as TK

import tkinter.messagebox as MB

from tkinter import ttk


import src.game2048_score as GS

import src.game2048_grid as GG
from AI import *




class GabrieleCirulli2048 (TK.Tk):
    r"""
        Gabriele Cirulli's 2048 puzzle game;

        Python3-Tkinter port by Raphaël Seban;
    """

    # component disposal padding

    PADDING = 10

    # number of tiles to show at startup

    START_TILES = 2



    def __init__ (self, **kw):

        # super class inits

        TK.Tk.__init__(self)

        # widget inits

        self.init_widget(**kw)

        # prevent from accidental displaying

        self.withdraw()

    # end def



    def center_window (self, tk_event=None, *args, **kw):
        r"""
            tries to center window along screen dims;

            no return value (void);
        """

        # ensure dims are correct

        self.update_idletasks()

        # window size inits

        _width = self.winfo_reqwidth()

        _height = self.winfo_reqheight()

        _screen_width = self.winfo_screenwidth()

        _screen_height = self.winfo_screenheight()

        # make calculations

        _left = (_screen_width - _width) // 2

        _top = (_screen_height - _height) // 2

        # update geometry

        self.geometry("+{x}+{y}".format(x=_left, y=_top))

    # end def



    def init_widget (self, **kw):
        r"""
            widget's main inits;
        """

        # main window inits

        self.title("Gabriele Cirulli's 2048")

        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.resizable(width=False, height=False)

        # look'n'feel

        ttk.Style().configure(".", font="sans 10")

        # inits

        _pad = self.PADDING

        # get 2048's grid

        self.grid = GG.Game2048Grid(self, **kw)

        # hint subcomponent

        self.hint = ttk.Label(

            self, text="Hint: use keyboard arrows to move tiles."
        )

        # score subcomponents

        self.score = GS.Game2048Score(self, **kw)

        self.hiscore = GS.Game2048Score(self, label="Highest:", **kw)

        # layout inits

        self.grid.pack(side=TK.TOP, padx=_pad, pady=_pad)

        self.hint.pack(side=TK.TOP)

        self.score.pack(side=TK.LEFT)

        self.hiscore.pack(side=TK.LEFT)

        # quit button

        ttk.Button(

            self, text="Ciao!", command=self.quit_app,

        ).pack(side=TK.RIGHT, padx=_pad, pady=_pad)

        # new game button

        ttk.Button(

            self, text="New Game", command=self.new_game,

        ).pack(side=TK.RIGHT)

        # set score callback method

        self.grid.set_score_callback(self.update_score)

    # end def



    def new_game (self, *args, **kw):
        r"""
            new game inits;
        """

        # no events now

        self.unbind_all("<Key>")

        # reset score

        self.score.reset_score()

        # reset grid

        self.grid.reset_grid()
        self.grid.x=TwentyFortyEight()
        # make random tiles to appear

        for n in range(self.START_TILES):
            t1,t2,tv = self.grid.x.new_tile()
            self.grid.pop_tile(row=t1,column=t2,tile=tv)

        self.grid.x.__str__()
        # end if

        # bind events

        self.bind_all("<Key>", self.slot_keypressed)

    # end def



    def quit_app (self, **kw):
        r"""
            quit app dialog;
        """

        # ask before actually quitting

        if MB.askokcancel("Question", "Quit game?", parent=self):

            self.quit()

        # end if

    # end def

    def autoplay(self):
        print("autoplay")
        while(self.grid.x.canMove()):
            self.grid.x.__str__()
            print("Score:"+str(self.grid.x.score)+"\t Max Tile:"+str(self.grid.x.maxValue()))
            dir=eminimax(self.grid.x,2)
            print(dir)
            _slot = {

                3: self.grid.move_tiles_left,

                4: self.grid.move_tiles_right,

                1: self.grid.move_tiles_up,

                2: self.grid.move_tiles_down,

            }.get(dir)
            _slot()
            self.update()
            # self.grid.x.move(dir)
            # r1,r2=self.grid.x.new_tile()
            # print(str(r1),str(r2))

        print("GAME ENDs")
        self.grid.x.__str__()
        print(self.grid.x.get_available_moves())

    def run (self, **kw):
        print("run")
        r"""
            actually runs the game;
        """

        # show up window

        self.center_window()

        self.deiconify()

        # init new game

        self.new_game(**kw)
        print("new_game")

        # enter the loop

        self.mainloop()

    # end def



    def slot_keypressed (self, tk_event=None, *args, **kw):
        r"""
            keyboard input events manager;
        """

        # action slot multiplexer
        print("dhh")
        print(tk_event.keysym.lower())

        _slot = {

            # "left": self.grid.move_tiles_left,

            # "right": self.grid.move_tiles_right,

            # "up": self.grid.move_tiles_up,

            # "down": self.grid.move_tiles_down,

            # "escape": self.quit_app,
            "return": self.autoplay,

        }.get(tk_event.keysym.lower())

        # got some redirection?

        if callable(_slot):

            # call slot method

            _slot()

            # hints are useless by now

            self.hint.pack_forget()

        # end if

    # end def



    def update_score (self, value, mode="add"):
        r"""
            updates score along @value and @mode;
        """

        # relative mode?

        if str(mode).lower() in ("add", "inc", "+"):

            # increment score value

            self.score.add_score(value)

        # absolute mode

        else:

            # set new value

            self.score.set_score(value)

        # end if

        # update high score

        self.hiscore.high_score(self.score.get_score())

    # end def

# end class GabrieleCirulli2048



# launching the game

if __name__ == "__main__":

    GabrieleCirulli2048().run()

# end if
