#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import ttk
import tkinter


class MainWindow:
    def __init__(self, width, height):
        self.root = tkinter.Tk()

        self.style = ttk.Style()
        self.themes = self.style.theme_names()

        #self.root.set_theme("vista")
        self.root.title("vsol clubs viewer")
        self.hs = self.root.winfo_screenheight()
        self.ws = self.root.winfo_screenwidth()
        self.root.geometry('%dx%d+%d+%d' % (width, height, (self.ws-width)//2, (self.hs-height)//2))
        self.root.resizable(width=False, height=False)

        #self.root.iconbitmap('smoking.ico')
        self.root.mainloop()


if __name__ == "__main__":
    MainWindow(1000, 500);