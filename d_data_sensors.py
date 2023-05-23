import requests
import sqlite3
import json


def d_data_sensors(stationId):
    """
        Funkcja pobiera listę stanowisk pomiarowych dla danej stacji pomiarowej z serwisu GIOŚ i zapisuje je do tabeli
        'sensors' w pamięci bazy danych SQLlite. Gdy otrzymamy bład w pobieraniu, funkcja pobierze dane z pliku sensors.json,
        gdy taki plik nie istnieje użytkownik zostanie o tym poinformowany.

        Args:
            stationId (int): Numer ID stacji pomiarowej.

        Returns:
            None.

        Raises:
            requests.exceptions.RequestException: W przypadku błędu podczas pobierania danych z serwisu GIOS lub braku
            pliku sensors.json

        Example:
            d_data_sensors(stationId)

        Output:
           LISTA DOSTĘPNYCH STANOWISK POMIAROWYCH STACJI NR 50:
            (26990, 16493, 'dwutlenek azotu', 'NO2', 'NO2', 6)
            (26995, 16493, 'tlenek węgla', 'CO', 'CO', 8)
            (26996, 16493, 'pył zawieszony PM10', 'PM10', 'PM10', 3)
            (26997, 16493, 'pył zawieszony PM2.5', 'PM2.5', 'PM2.5', 69)

        """

    # Tworzenie połączenia z bazą danych, a następnie utworzenie kursora:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tworzenie tabeli 'sensors':
    conn.execute('''CREATE TABLE IF NOT EXISTS sensors (
                        id INTEGER PRIMARY KEY,
                        station_id INTEGER REFERENCES stations(id),
                        param_name TEXT,
                        param_formula TEXT,
                        param_code TEXT,
                        id_param INTEGER)''')

    # Pobieranie listy wszystkich stanowisk pomiarowych stacji i zapisywanie pobranych danych do pliku sensors.json:
    try:
        sensors = requests.get(('https://api.gios.gov.pl/pjp-api/rest/station/sensors/') + str(stationId)).json()
        with open('sensors.json', 'w') as f:
            json.dump(sensors, f)

    # W przypadku błędu wczytywanie danych z plików:
    except requests.exceptions.RequestException:
        print('BŁĄD POBIERANIA. WCZYTUJĘ DANE HISTORYCZNE...')
        try:
            with open('sensors.json', 'r') as f:
                sensors = json.load(f)
        except FileNotFoundError:
            print('Nie znaleziono pliku "sensors.json"')
            return

    # Wypełnianie tabeli 'sensors':
    for sensor in sensors:
        conn.execute('''INSERT OR REPLACE INTO sensors (id, station_id, param_name, param_formula, param_code, id_param)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (sensor['id'], sensor['stationId'], sensor['param']['paramName'], sensor['param']['paramFormula'],
                      sensor['param']['paramCode'], sensor['param']['idParam']))

    # Wykonanie zapytania SELECT i wydrukowanie wyniku:
    cursor.execute("SELECT * FROM sensors")
    rows = cursor.fetchall()

    if len(rows) == 0:
        print(f'Nie znaleziono stanowisk pomiarowych dla stacji o numerze ID {stationId}')
    else:
        print(f'LISTA DOSTĘPNYCH STANOWISK POMIAROWYCH STACJI NR {stationId}:')
        for row in rows:
            print(row)

    # Zatwierdzenie i zamknięcie połączenia z bazą danych:
    conn.commit()
    conn.close()
