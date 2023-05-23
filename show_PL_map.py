from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sqlite3
import numpy as np

def show_PL_map():
    """
    Funkcja show_PL_map służy do wyświetlania mapy Polski z naniesionymi stacjami pomiarowymi,
    dodatkowo po kliknięciu wybranego punktu na mapie(stacji pomiarowej), w okienku ukazują się informacje dotyczące tej stacji
    """

    # utworzenie połączenia z bazą danych
    conn = sqlite3.connect('database.db')

    # utworzenie kursora
    cursor = conn.cursor()

    # pobranie danych stacji pomiarowych z bazy danych
    cursor.execute('SELECT id, gegr_lat, gegr_lon, city_name, address_street, province_name FROM stations')
    stations = cursor.fetchall()

    # tworzenie wykresu z większym oknem
    fig, ax = plt.subplots(figsize=(15, 10))

    # utworzenie mapy
    map = Basemap(llcrnrlon=14.0, llcrnrlat=48.8, urcrnrlon=24.4, urcrnrlat=55.0, resolution='i', ax=ax)
    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color='gray')

    # naniesienie stacji pomiarowych na mapę
    x, y = map([float(station[2]) for station in stations], [float(station[1]) for station in stations])
    sc = map.scatter(x, y, c='blue', s=10, alpha=0.5, zorder=10, picker=True)

    # dodanie tytułu, legendy i etykiet osi
    plt.title('Stacje pomiarowe w Polsce')
    plt.xlabel('Długość geograficzna')
    plt.ylabel('Szerokość geograficzna')
    plt.legend([sc], ['Stacje pomiarowe'], loc='lower left', fontsize=10)

    # dodanie siatki
    map.drawparallels(np.arange(45., 60., 2.), linewidth=0.5, labels=[1, 0, 0, 0], fontsize=10)
    map.drawmeridians(np.arange(14., 26., 2.), linewidth=0.5, labels=[0, 0, 0, 1], fontsize=10)

    def on_pick(event):
        # pobranie indeksu klikniętego punktu
        ind = event.ind[0]

        # pobranie danych stacji pomiarowej
        station_id, latitude, longitude, city_name, address_street, province_name = stations[ind]

        # wyświetlenie informacji o stacji pomiarowej w okienku
        plt.figure()
        plt.text(0.5, 0.5, f"Stacja pomiarowa: Jej numer id to - {station_id}\n"
                           f"Wybrana stacja znajduje się w - {city_name} na ulicy {address_street}\n"
                           f"w województwie {province_name}\n"
                           f"Szerokość geograficzna: {latitude}\n"
                           f"Długość geograficzna: {longitude}\n"
                           f"Informacje dotyczące mierzonych parametrów oraz\n"
                            f"ich danych możesz znaleźć w liście stacji",
                 ha='center', va='center', fontsize=12)
        plt.axis('off')
        plt.show()

        # przypisanie funkcji obsługującej zdarzenie kliknięcia do punktów

    fig.canvas.mpl_connect('pick_event', on_pick)

    # wyświetlenie mapy
    plt.show()

    # zamknięcie połączenia z bazą danych
    conn.close()