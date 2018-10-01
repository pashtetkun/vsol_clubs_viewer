#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import ttk
import tkinter
import os


class MainWindow:
    def __init__(self, width, height, icon_path, logo_path):
        self.root = tkinter.Tk()

        self.style = ttk.Style()
        self.themes = self.style.theme_names()

        #self.root.set_theme("vista")
        self.root.title("vsol clubs viewer")
        self.hs = self.root.winfo_screenheight()
        self.ws = self.root.winfo_screenwidth()
        self.root.geometry('%dx%d+%d+%d' % (width, height, (self.ws-width)//2, (self.hs-height)//2))
        self.root.resizable(width=False, height=False)
        self.root.iconbitmap(icon_path)

        self.init_left_frame(logo_path)
        self.init_right_frame()
        
        self.root.mainloop()
        
    def init_left_frame(self, logo_path):
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.pack(side='left', anchor="n", fill=tkinter.Y)
        self.logo_container = ttk.LabelFrame(self.left_frame)
        self.logo_container.pack(side='top')
        image = tkinter.PhotoImage(file=os.path.join(os.getcwd(), logo_path))
        self.logo = ttk.Label(self.logo_container, image=image, compound="image")
        self.logo.image = image
        self.logo.pack(anchor=tkinter.CENTER)

        self.continents_frame = ttk.LabelFrame(self.left_frame, text="Континент")
        self.continents_frame.pack(side='top', fill=tkinter.X, anchor="n")
        self.continents_combo = ttk.Combobox(self.continents_frame)
        self.continents_combo.pack(fill=tkinter.BOTH, expand=tkinter.YES)

        self.countries_frame = ttk.LabelFrame(self.left_frame, text="Страна")
        self.countries_frame.pack(side='top', fill=tkinter.BOTH, expand=tkinter.YES)
        self.countries_listbox = ttk.Treeview(self.countries_frame,
                                              columns=("name",),
                                              displaycolumns=("name",),
                                              show="headings")
        self.countries_listbox.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    def init_right_frame(self):
        self.right_frame = ttk.LabelFrame(self.root, text="Клубы")
        self.right_frame.pack(side='right', fill=tkinter.BOTH, expand=tkinter.YES)

        self.clubs_grid = ttk.Treeview(self.right_frame,
                                              columns=("name",),
                                              displaycolumns=("name",),
                                              show="tree")
        self.clubs_grid.pack(fill=tkinter.BOTH, expand=tkinter.YES)

                                        
if __name__ == "__main__":
    MainWindow(1000, 500, '../logo.ico', '../logo.gif')
