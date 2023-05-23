import requests
import sqlite3
import json

def d_data_stations():
    """
        Funkcja pobiera listę wszystkich stacji pomiarowych z serwisu GIOS i zapisuje je do tabeli 'stations'
        w pamięci SQLlite. W przypadku błędu podczas pobierania danych, funkcja pobiera dane z pliku 'stations.json',
        jeśli taki istnieje, jeśli nie zwraca informację dotyczącą jego braku.

        Args:
            Brak.

        Returns:
            None.

        Raises:
            requests.exceptions.RequestException: W przypadku błędu podczas pobierania danych z serwisu GIOS.

        Example:
            d_data_stations()

        Output:
            LISTA DOSTĘPNYCH STACJI:
            (11, 'Czerniawa', '50.912475', '15.312190', 142, 'Czerniawa', 'Świeradów-Zdrój', 'lubański', 'DOLNOŚLĄSKIE', 'ul. Strażacka 7')
            (16, 'Dzierżoniów, ul. Piłsudskiego', '50.732817', '16.648050', 198, 'Dzierżoniów', 'Dzierżoniów', 'dzierżoniowski', 'DOLNOŚLĄSKIE', 'ul. Piłsudskiego 26')
            (38, 'Kłodzko, ul. Szkolna', '50.433493', '16.653660', 368, 'Kłodzko', 'Kłodzko', 'kłodzki', 'DOLNOŚLĄSKIE', 'ul. Szkolna 8')            ...
        """

    # Tworzenie połączenia z bazą danych, a następnie utworzenie kursora:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tworzenie tabeli 'stations':
    conn.execute('''CREATE TABLE IF NOT EXISTS stations (
                    id INTEGER NOT NULL PRIMARY KEY,
                    station_name TEXT,
                    gegr_lat TEXT,
                    gegr_lon TEXT,
                    city_id INTEGER,
                    city_name TEXT,
                    commune_name TEXT,
                    district_name TEXT,
                    province_name TEXT,
                    address_street TEXT)''')
    # Pobieranie listy wszystkich stacji pomiarowych i zapisywanie pobranych danych do pliku stations.json:
    try:
        stations = requests.get('http://api.gios.gov.pl/pjp-api/rest/station/findAll').json()
        with open('stations.json', 'w') as f:
            json.dump(stations, f)

    # W przypadku błędu wczytywanie danych z plików:
    except requests.exceptions.RequestException:
        print('BŁĄD POBIERANIA. WCZYTUJĘ DANE HISTORYCZNE...')
        try:
            with open('stations.json', 'r') as f:
                stations = json.load(f)
        except FileNotFoundError:
            print('Nie znaleziono pliku "stations.json"')
            return

    # Wypełnianie tabeli 'stations':
    for station in stations:
        city = station['city']
        commune = city['commune']
        conn.execute('''INSERT OR REPLACE INTO stations (id, station_name, gegr_lat, gegr_lon, city_id, city_name, commune_name, district_name, province_name, address_street)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (station['id'], station['stationName'], station['gegrLat'], station['gegrLon'], city['id'],
                      city['name'], commune['communeName'], commune['districtName'], commune['provinceName'],
                      station['addressStreet']))

    # Wykonanie zapytania SELECT i wydrukowanie wyniku:
    print(f"LISTA DOSTĘPNYCH STACJI:")
    cursor.execute("SELECT * FROM stations")
    for row in cursor.fetchall():
        print(row)

    # Zatwierdzenie i zamknięcie połączenia z bazą danych:
    conn.commit()
    conn.close()