#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import ttk
import tkinter
import tkinter.messagebox
import os
#from services import test_data_explorer as de
from config_file import ConfigFile
from services import data_explorer as de
from services import vsol_exporter
from parsers import vsol_parser
from gui import update_clubs_window


class MainWindow:
    def __init__(self, width, height, icon_path, logo_path, config_file):
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
        self.config_file = config_file

        self.de = de.DataExplorer(self.config_file, 'vsol.db')
        self.continents = self.de.get_all_continents()
        self.clubs = []
        self.selected_continent_id = None
        self.selected_country_id = None

        self.exporter = vsol_exporter.VsolExporter(self.config_file)

        self.parser = vsol_parser.VsolParser(self.config_file)

        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)

        self.update_menu = tkinter.Menu(self.menu, tearoff=0)
        self.update_menu.add_command(label="Все", command=self.update_all)
        self.update_menu.add_command(label="Только скрытые", command=self.update_hiddens)
        self.update_menu.add_command(label="Выбранную страну", command=self.update_selected_country)
        self.menu.add_cascade(label="Обновить клубы", menu=self.update_menu)
        #self.menu.add_command(label="Обновить клубы", command=self.clubs_update)
        self.menu.add_command(label="Анализ")

        self.service_menu = tkinter.Menu(self.menu, tearoff=0)
        #self.service_menu.add_command(label="Экспорт стран: VSOL --> csv", command=self.countries_to_csv)
        #self.service_menu.add_command(label="Импорт стран: csv --> db", command=self.countries_to_db)
        self.service_menu.add_command(label="Получить страны", command=self.countries_to_db2)

        self.menu.add_cascade(label="Сервис", menu=self.service_menu)

        self.tab_panel = None

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
        self.countries = self.de.get_countries(self.continents[idx].id)
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
            self.countries_listbox.insert('','end', iid=country.vsol_id, values=(country.name,))
        self.countries_listbox.selection_add(self.countries[0].id)

    def choose_country_handler(self, event):
        country_vsol_id = int(event.widget.selection()[0])
        self.selected_country_id = country_vsol_id
        self.clubs = self.de.get_clubs(country_vsol_id)
        self.refresh_clubs_grids()

    def refresh_clubs_grids(self):
        actived = 0
        hiddened = 0
        for row in self.clubs_grid.get_children():
            self.clubs_grid.delete(row)
        for row in self.hidden_clubs_grid.get_children():
            self.hidden_clubs_grid.delete(row)
        print(self.clubs)
        if self.clubs:
            for club in self.clubs:
                if not club.hidden:
                    self.clubs_grid.insert('', 'end', iid=club.id, values=(club.name,))
                    actived+=1
                else:
                    self.hidden_clubs_grid.insert('', 'end', iid=club.id, values=(club.name,))
                    hiddened+=1

        self.tab_panel.tab(0, text="Активные (%d)" % actived)
        self.tab_panel.tab(1, text="Скрытые (%d)" % hiddened)

    def countries_to_csv(self):
        csv = self.exporter.countries_to_csv()
        #for windows only
        os.startfile(csv, 'open')

    def countries_to_db(self):
        self.de.import_countries('countries.csv')
        tkinter.messagebox.showinfo("Сообщение", "Страны импортированы успешно!")

    def countries_to_db2(self):
        csv = self.exporter.countries_to_csv2()
        self.de.import_countries('countries.csv')
        tkinter.messagebox.showinfo("Сообщение", "Страны загружены в БД успешно!")

    def update_all(self):
        answer = tkinter.messagebox.askyesno(title="Вопрос", message="Обновить информацию о клубах?")
        if answer:
            #countries = self.de.get_all_countries()
            #clubs = self.exporter.get_clubs(countries)
            #for club in clubs:
                #self.de.save_club(club["name"], club["vsol_id"], club["country_vsol_id"], club["stadium"],
                #club["is_hidden"])
            #tkinter.messagebox.showinfo("Сообщение", "Информация о клубах обновлена успешно!")
            upWindow = update_clubs_window.UpdateClubsWindow(800, 160, self.de, self.parser, False)
            upWindow.update_all()

    def update_hiddens(self):
        answer = tkinter.messagebox.askyesno(title="Вопрос", message="Обновить информацию о скрытых клубах?")
        if answer:
            upWindow = update_clubs_window.UpdateClubsWindow(800, 160, self.de, self.parser, False)
            upWindow.update_hiddens()

    def update_selected_country(self):
        if not self.selected_country_id:
            tkinter.messagebox.showinfo("Сообщение", "Страна не выбрана")
        answer = tkinter.messagebox.askyesno(title="Вопрос", message="Обновить клубы в выбранной стране?")
        if answer:
            upWindow = update_clubs_window.UpdateClubsWindow(800, 160, self.de, self.parser, False)
            upWindow.update_selected_country(self.selected_country_id)


if __name__ == "__main__":
    dir_gui = os.path.dirname(__file__)
    dir_root = os.path.dirname(dir_gui)
    config_path = os.path.join(dir_root, 'config.ini')
    config = ConfigFile(config_path)
    MainWindow(1000, 500, '../logo.ico', '../logo.gif', config)
