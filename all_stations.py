from d_data_stations import d_data_stations
from d_data_sensors import d_data_sensors
from d_data_measurements import d_data_measurements
from d_data_aqi import d_data_aqi

from tkinter import *
import tkinter as tk
import sqlite3

def all_stations():
    """
        Funkcja wyświetla listę wszytskich stacji pomiarowych, następnie umożliwia filtrowanie po nazwie
        miejscowości, po czym wyświetla dane, które dotyczą stacji/stanowisk.

        """
    def show_measurements_data():
        # usunięcie zawartości listboxa:
        listbox.delete(0, END)

        # Pobieranie danych pomiarowych wybranego stanowiska:
        id = int(entry_id.get())
        d_data_measurements(id)

        # wykonanie zapytania SQL:
        cursor.execute('SELECT * FROM measurements')

        # pobranie wyników zapytania:
        result3 = cursor.fetchall()

        # Dodanie etykiet do listboxa:
        listbox.insert(tk.END, "data | dane dotyczące stacji")

        # dodanie wyników zapytania do listboxa:
        for row in result3:
            listbox.insert(tk.END, row)

    def show_sensors_data():
        # Usunięcie zawartości listboxa:
        listbox.delete(0, tk.END)

        # Pobranie ID stacji z pola Entry:
        station_id = int(entry_staionId.get())
        d_data_sensors(station_id)

        # Wykonanie zapytania SQL na bazie danych dla danej stacji:
        cursor.execute('SELECT * FROM sensors WHERE station_id = ?', (station_id,))
        result = cursor.fetchall()

        # Dodanie etykiet do listboxa:
        listbox.insert(tk.END, "station_id | param_name | param_formula | param_code | id_param")

        # Dodanie wyników zapytania do listboxa:
        for row in result:
            listbox.insert(tk.END, row)

    def show_city():
        # usunięcie zawartości listboxa:
        listbox.delete(0, END)

        # Pobieranie nazwy miejscowości:
        city_name = str(entry_city.get())

        # wykonanie zapytania SQL:
        cursor.execute('SELECT * FROM stations WHERE city_name = ?', (city_name,))

        # pobranie wyników zapytania:
        result = cursor.fetchall()

        # Dodanie etykiet do listboxa:
        listbox.insert(tk.END, "station_id | dane dotyczące stacji (lokalizacja)")

        # dodanie wyników zapytania do listboxa:
        for row in result:
            listbox.insert(tk.END, row)

    def show_air_quality():
        # usunięcie zawartości listboxa:
        listbox.delete(0, END)

        # Pobieranie id stacji:
        station_id = int(entry_aqi.get())
        aqi = d_data_aqi(station_id)

        # wykonanie zapytania SQL:
        cursor.execute('SELECT * FROM air_quality_index WHERE id = ?', (station_id,))

        # Dodanie etykiet do listboxa:
        listbox.insert(tk.END, "Indeks jakości powietrza")

        # dodanie wyników zapytania do listboxa:
        result = cursor.fetchall()
        for row in result:
            listbox.insert(tk.END, row)


    # Utworzenie okna i wyznaczenie jego rozmiaru:
    root = tk.Tk()
    root.title("AQI TRACKER")
    root.geometry('1100x800')

    tk.Label(root, text="FILTROWANIE STACJI ORAZ DANYCH ICH DOTYCZĄCYCH", fg='red', font=("Arial", 16)).pack()

    # Utworzenie ramki:
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=NO)

    # # Utworzenie listboxa:
    listbox = Listbox(root)
    listbox.pack(side=TOP, fill=BOTH, expand=YES)

    # Utworzenie suwaka i przypisanie go do listboxa:
    scrollbar = Scrollbar(listbox, orient=VERTICAL, command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # wprowadzamy elementy interfejsu:
    label_city = Label(frame, text="Podaj nazwę miejscowości dla której chcesz zobaczyć dostepne stacje:", font=("Arial", 10))
    label_staionId = Label(frame, text="Podaj ID stacji dla której chcesz otrzymać informacje dotyczące jej stanowisk pomiarowych:", font=("Arial", 10))
    label_id = Label(frame, text="Podaj ID stanowiska stacji dla którego chcesz otrzymać informacje dotyczące danych pomiarowych:", font=("Arial", 10))
    label_aqi = Label(frame, text="Podaj ID stacji dla której chcesz otrzymać informacje dotyczące jakości powietrza:", font=("Arial", 10))

    entry_city = Entry(frame, bd=5)
    entry_staionId = Entry(frame, bd=5)
    entry_id = Entry(frame, bd=5)
    entry_aqi = Entry(frame, bd=5)

    button_city = Button(frame, text="Szukaj", command=show_city)
    button_stationId = Button(frame, text="Szukaj", command=show_sensors_data)
    button_id = Button(frame, text="Szukaj", command=show_measurements_data)
    button_aqi = Button(frame, text="Szukaj", command=show_air_quality)

    # rozmieszczenie elementów:
    label_city.grid(row=0, column=0, padx=10)
    label_staionId.grid(row=1, column=0, padx=10)
    label_id.grid(row=2, column=0, padx=10)
    label_aqi.grid(row=3, column=0, padx=10)

    entry_city.grid(row=0, column=1, padx=10)
    entry_staionId.grid(row=1, column=1, padx=10)
    entry_id.grid(row=2, column=1, padx=10)
    entry_aqi.grid(row=3, column=1, padx=10)

    button_city.grid(row=0, column=2, padx=10)
    button_stationId.grid(row=1, column=2, padx=10)
    button_id.grid(row=2, column=2, padx=10)
    button_aqi.grid(row=3, column=2, padx=10)


    # Wywołanie funkcji w celu zapisu w bazie danych:
    d_data_stations()

    # utworzenie połączenia z bazą danych:
    conn = sqlite3.connect('database.db')

    # utworzenie kursora:
    cursor = conn.cursor()

    # wykonanie zapytania SQL
    cursor.execute('SELECT * FROM stations')

    # pobranie wyników zapytania:
    result = cursor.fetchall()

    # dodanie wyników zapytania do listboxa:
    for row in result:
        listbox.insert(tk.END, row)

    root.mainloop()