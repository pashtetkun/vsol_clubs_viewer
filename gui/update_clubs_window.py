#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import queue
import threading
from services import data_explorer
from parsers import vsol_parser


class ThreadedClientUpdateAll(threading.Thread):

    def __init__(self, queue, data_explorer, vsol_parser, is_test=False):
        threading.Thread.__init__(self)
        self.queue = queue
        self.de = data_explorer
        self.parser = vsol_parser
        self.is_test = is_test

    def run(self):
        if not self.is_test:
            self.queue.put({'done': False, 'message': "Получение списка стран начато"})
            countries = self.de.get_all_countries()
            self.queue.put({'done': False, 'message': "Получение списка стран завершено"})
            #clubs = self.exporter.get_clubs(countries)
            all_clubs = []
            for idx, country in enumerate(countries):
                self.queue.put({'done': False, 'message': "Обрабатывается страна %d из %d" % (idx + 1, len(countries))})
                clubs = self.parser.get_clubs(country.vsol_id)
                all_clubs.extend(clubs)
            self.queue.put({'done': False, 'message': "Обрабатываются скрытые клубы"})
            hidden_clubs_dict = self.parser.get_hidden_clubs()
            count = 0
            for key, value in hidden_clubs_dict.items():
                country = next((x for x in countries if x.name == key), None)
                if country:
                    for id in value:
                        club = self.parser.get_club(id)
                        club['is_hidden'] = True
                        club['country_vsol_id'] = country.vsol_id
                        all_clubs.append(club)
                        count += 1
                        self.queue.put({'done': False, 'message': "Обработано скрытых клубов %d" % count})

            self.de.update_clubs(all_clubs)
            self.queue.put({'done': True, 'message': ""})
        else:
            self.queue.put({'done': False, 'message': "Ля-ля-ля"})


class ThreadedClientUpdateHiddens(threading.Thread):

    def __init__(self, queue, data_explorer, vsol_parser, is_test=False):
        threading.Thread.__init__(self)
        self.queue = queue
        self.de = data_explorer
        self.parser = vsol_parser
        self.is_test = is_test

    def run(self):
        if not self.is_test:
            self.queue.put({'done': False, 'message': "Получение списка стран начато"})
            countries = self.de.get_all_countries()
            self.queue.put({'done': False, 'message': "Получение списка стран завершено"})
            #clubs = self.exporter.get_clubs(countries)
            all_clubs = []
            self.queue.put({'done': False, 'message': "Обрабатываются скрытые клубы"})
            hidden_clubs_dict = self.parser.get_hidden_clubs()
            count = 0
            for key, value in hidden_clubs_dict.items():
                country = next((x for x in countries if x.name == key), None)
                if country:
                    for id in value:
                        club = self.parser.get_club(id)
                        club['is_hidden'] = True
                        club['country_vsol_id'] = country.vsol_id
                        all_clubs.append(club)
                        count += 1
                        self.queue.put({'done': False, 'message': "Обработано скрытых клубов %d" % count})

            self.de.update_clubs(all_clubs)
            self.queue.put({'done': True, 'message': ""})
        else:
            self.queue.put({'done': False, 'message': "Ля-ля-ля"})


class ThreadedClientUpdateSelectedCountry(threading.Thread):

    def __init__(self, queue, data_explorer, vsol_parser, country_vsol_id, is_test=False):
        threading.Thread.__init__(self)
        self.queue = queue
        self.de = data_explorer
        self.parser = vsol_parser
        self.is_test = is_test
        self.country_vsol_id = country_vsol_id

    def run(self):
        if not self.is_test:
            self.queue.put({'done': False, 'message': "Получение списка стран начато"})
            countries = self.de.get_all_countries()
            self.queue.put({'done': False, 'message': "Получение списка стран завершено"})
            #clubs = self.exporter.get_clubs(countries)
            all_clubs = self.parser.get_clubs(self.country_vsol_id)
            self.de.update_clubs(all_clubs)
            self.queue.put({'done': True, 'message': ""})
        else:
            self.queue.put({'done': False, 'message': "Ля-ля-ля"})


class UpdateClubsWindow(tk.Toplevel):
    def __init__(self, width, height, data_explorer, vsol_parser, is_test, callback=None):
        tk.Toplevel.__init__(self, height=height, width=width)

        self.height = height
        self.width = width
        self.offsetx = (self.winfo_screenwidth() - self.width) // 2
        self.offsety = (self.winfo_screenheight() - self.height) // 2

        self.title("Обновление...")
        self.transient(self.master)
        self.grab_set()
        self.geometry('%dx%d+%d+%d'
                      % (self.width, self.height, self.offsetx, self.offsety))
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.frame = ttk.Frame(self)
        self.frame.pack()

        self.frame_account = ttk.Frame(self.frame)
        self.frame_account.pack(fill="x", expand=1)

        self.var_message = tk.StringVar()
        self.label_message = ttk.Label(self.frame_account, textvariable=self.var_message, width=100)
        self.label_message.grid(row=0, column=0, columnspan=2, sticky="ew")
        #self.label_message.grid_remove()
        self.progressbar = ttk.Progressbar(self.frame_account, mode='indeterminate', orient=tk.HORIZONTAL)
        self.progressbar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.progressbar.grid_remove()

        self.is_test = is_test
        self.de = data_explorer
        self.parser = vsol_parser
        self.queue = queue.Queue(1)
        self.thread = None

    def update_all(self):
        self.var_message.set("")
        self.progressbar.grid(row=1, column=0)
        self.progressbar.start()
        self.thread = ThreadedClientUpdateAll(self.queue, self.de, self.parser, self.is_test)
        self.thread.start()
        self.master.after(1000, self.listen_queue)

    def update_hiddens(self):
        self.var_message.set("")
        self.progressbar.grid(row=1, column=0)
        self.progressbar.start()
        self.thread = ThreadedClientUpdateHiddens(self.queue, self.de, self.parser, self.is_test)
        self.thread.start()
        self.master.after(1000, self.listen_queue)

    def update_selected_country(self, country_id):
        self.var_message.set("")
        self.progressbar.grid(row=1, column=0)
        self.progressbar.start()
        self.thread = ThreadedClientUpdateSelectedCountry(self.queue, self.de, self.parser, country_id, self.is_test)
        self.thread.start()
        self.master.after(1000, self.listen_queue)

    def close_window(self):
        if self.thread:
            self.thread.join()
            pass
        self.destroy()

    def listen_queue(self):
        try:
            resp = self.queue.get()
            self.process_message(resp)
            self.queue.task_done()
            self.queue.queue.clear()
            self.master.after(1000, self.listen_queue)
        except queue.Empty:
            self.master.after(1000, self.listen_queue)

    def process_message(self, resp):
        if resp['done']:
            self.progressbar.stop()
            self.progressbar.grid_remove()
            self.var_message.set(resp['message'])
            #self.label_message.grid()
            self.thread.join()
            self.destroy()
        else:
            self.var_message.set(resp['message'])


if __name__ == "__main__":
    root = tk.Tk()
    width = 1000
    height = 500
    hs = root.winfo_screenheight()
    ws = root.winfo_screenwidth()
    root.geometry('%dx%d+%d+%d' % (width, height, (ws - width) // 2, (hs - height) // 2))
    explorer = data_explorer.DataExplorer()
    parser = vsol_parser.VsolParser()
    update_clubs_window = UpdateClubsWindow(800, 160, explorer, parser, False)
    update_clubs_window.update_all()
    root.mainloop()