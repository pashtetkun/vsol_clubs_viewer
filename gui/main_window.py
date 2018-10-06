#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import ttk
import tkinter
import tkinter.messagebox
import os
from test_data import test_data_explorer as tde
from services import vsol_exporter, db_importer


class MainWindow:
    def __init__(self, width, height, icon_path, logo_path):
        self.root = tkinter.Tk()

        #self.style = ttk.Style()
        #self.themes = self.style.theme_names()

        #self.root.set_theme("vista")
        self.root.title("vsol clubs viewer")
        self.hs = self.root.winfo_screenheight()
        self.ws = self.root.winfo_screenwidth()
        self.root.geometry('%dx%d+%d+%d' % (width, height, (self.ws-width)//2, (self.hs-height)//2))
        self.root.resizable(width=False, height=False)
        self.root.iconbitmap(icon_path)

        self.tde = tde.TestDataExplorer()
        self.continents = self.tde.get_all_continents()
        self.clubs = []

        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label="Обновить")
        self.menu.add_command(label="Анализ")

        self.service_menu = tkinter.Menu(self.menu, tearoff=0)
        self.service_menu.add_command(label="Экспорт стран: VSOL --> csv", command=self.countries_to_csv)
        self.service_menu.add_command(label="Импорт стран: csv --> db", command=self.countries_to_db)

        self.menu.add_cascade(label="Сервис", menu=self.service_menu)

        self.draw_left_frame(logo_path)
        self.draw_right_frame()

        self.set_continents_combo(0)
        
        self.root.mainloop()
        
    def draw_left_frame(self, logo_path):
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
        self.continents_combo.configure(values=[item.name for item in self.continents])
        self.continents_combo.bind("<<ComboboxSelected>>", self.choose_continent_handler)

        self.countries_frame = ttk.LabelFrame(self.left_frame, text="Страна")
        self.countries_frame.pack(side='top', fill=tkinter.BOTH, expand=tkinter.YES)
        self.countries_listbox = ttk.Treeview(self.countries_frame,
                                              columns=("name",),
                                              displaycolumns=("name",),
                                              show="")
        self.countries_listbox.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.countries_listbox.bind("<<TreeviewSelect>>", self.choose_country_handler)

    def draw_right_frame(self):
        self.right_frame = ttk.LabelFrame(self.root, text="Клубы")
        self.right_frame.pack(side='right', fill=tkinter.BOTH, expand=tkinter.YES)

        self.tab_panel = ttk.Notebook(self.right_frame)
        self.tab_panel.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.clubs_grid = ttk.Treeview(self.tab_panel,
                                              columns=("name",),
                                              displaycolumns=("name",),
                                              show="")
        self.clubs_grid.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.tab_panel.add(self.clubs_grid, text='Активные')

        self.hidden_clubs_grid = ttk.Treeview(self.tab_panel,
                                       columns=("name",),
                                       displaycolumns=("name",),
                                       show="")
        self.hidden_clubs_grid.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.tab_panel.add(self.hidden_clubs_grid, text='Скрытые')

    def set_continents_combo(self, idx):
        if not self.continents:
            return
        self.continents_combo.current(idx)
        self.countries = self.tde.get_countries(self.continents[idx].id)
        self.refresh_countries_grid()

    def choose_continent_handler(self, event):
        idx = event.widget.current()
        self.set_continents_combo(idx)

    def refresh_countries_grid(self):
        for row in self.countries_listbox.get_children():
            self.countries_listbox.delete(row)
        if not self.countries:
            return
        for country in self.countries:
            self.countries_listbox.insert('','end', iid=country.id, values=(country.name,))
        self.countries_listbox.selection_add(self.countries[0].id)

    def choose_country_handler(self, event):
        country_id = int(event.widget.selection()[0])
        self.clubs = self.tde.get_clubs(country_id)
        self.refresh_clubs_grids()

    def refresh_clubs_grids(self):
        for row in self.clubs_grid.get_children():
            self.clubs_grid.delete(row)
        for row in self.hidden_clubs_grid.get_children():
            self.hidden_clubs_grid.delete(row)
        print(self.clubs)
        if not self.clubs:
            return
        for club in self.clubs:
            if not club.hidden:
                self.clubs_grid.insert('', 'end', iid=club.id, values=(club.name,))
            else:
                self.hidden_clubs_grid.insert('', 'end', iid=club.id, values=(club.name,))

    def countries_to_csv(self):
        exporter = vsol_exporter.VsolExporter()
        csv = exporter.countriesToCSV()
        #for windows only
        os.startfile(csv, 'open')

    def countries_to_db(self):
        importer = db_importer.DbImporter()
        importer.import_countries('countries.csv')
        tkinter.messagebox.showinfo("Сообщение", "Страны импортированы успешно!")


if __name__ == "__main__":
    MainWindow(1000, 500, '../logo.ico', '../logo.gif')
