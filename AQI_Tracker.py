import tkinter as tk
from analyze_data import analyze_measurements_data
from show_PL_map import show_PL_map
from all_stations import all_stations
from filter_by_location import filter_by_location

class AnalysisWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Analiza danych")

        self.id_label = tk.Label(self, text="ID stanowiska:")
        self.id_entry = tk.Entry(self)
        self.analyze_button = tk.Button(self, text="Analizuj", command=self.analyze_data)
        self.result_label = tk.Label(self, text="")

        self.id_label.pack()
        self.id_entry.pack()
        self.analyze_button.pack()
        self.result_label.pack()

    def analyze_data(self):
        id = int(self.id_entry.get())
        results = analyze_measurements_data(id)  # wykonaj analizę i pobierz wyniki
        self.result_label.config(text=results)  # ustaw wyniki jako tekst etykiety


class App:
    def __init__(self, master):
        self.master = master
        master.title("AQI TRACKER")
        master.geometry('640x500')
        tk.Label(master, text="Cześć przed tobą AQI TRACKER!", font=("Arial", 16)).pack()
        tk.Label(master, text="Aplikacja, która za zadanie ma pokazać Ci informację dotyczące stacji pogodowych",
                 font=("Arial", 12)).pack()
        tk.Label(master, text="Aby przejść dalej wybierz jedną z dostepnych opcji:", wraplength=250,
                 font=("Arial", 10), anchor="center").place(x=25, y=100)

        tk.Button(master, text="Lista stacji i ich filtrowanie", font=("Arial", 10), command=self.show_all_stations).place(x=25, y=150, width=250, height=30)
        tk.Button(master, text="Znajdź stację w pobliżu!", font=("Arial", 10), command=self.show_filter_by_location).place(x=300, y=150, width=250, height=30)
        tk.Button(master, text="Pokaż mapę stacji pomiarowych w Polsce", font=("Arial", 10), command=self.show_PL_map).place(x=25, y=200, width=250, height=30)
        tk.Button(master, text="Analiza danych", font=("Arial", 10), command=self.show_analysis_window).place(x=300, y=200, width=250, height=30)

    def show_all_stations(self):
        all_stations()

    def show_filter_by_location(self):
        filter_by_location()

    def show_PL_map(self):
        show_PL_map()

    def show_analysis_window(self):
        analysis_window = AnalysisWindow(self.master)


root = tk.Tk()
myapp = App(root)
root.mainloop()

