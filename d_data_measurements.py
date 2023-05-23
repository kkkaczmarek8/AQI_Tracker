import requests
import sqlite3
import json


def d_data_measurements(id):
    """
        Funkcja pobiera listę danych pomiarowych z serwisu GIOŚ i zapisuje je do tabeli 'measuremennts' w pamięci
        SQLlite. W przypadku błędu podczas pobierania danych, funkcja pobiera dane z pliku 'measurements.json',
        jeśli taki istnieje, w przeciwnym wypadku użytkownik zostanie o tym poinforowany.

        Args:
            id (int): Numer ID stanowiska pomiarowego.

        Returns:
            None.

        Raises:
            requests.exceptions.RequestException: W przypadku błędu podczas pobierania danych z serwisu GIOS.

        Example:
            d_data_measurements(id)

        Output:
            LISTA DANYCH ZEBRANYCH ZE STANOWISKA NR 52:
            ('2023-05-16 20:00:00', 3.13515)
            ('2023-05-16 19:00:00', 4.59624)
            ('2023-05-16 18:00:00', 4.53728)
            ('2023-05-16 17:00:00', 6.98358)
            ('2023-05-16 16:00:00', 5.34032)
            ...
        """

    # Tworzenie połączenia z bazą danych, a następnie utworzenie kursora:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tworzenie tabeli 'measurements':
    conn.execute('''CREATE TABLE IF NOT EXISTS measurements (
                    values_date DATETIME NOT NULL,
                    values_value FLOAT)''')

    # Pobieranie listy wszystkich danych pomiarowych stanowiska i zapisywanie pobranych danych do pliku measurements.json:
    try:
        measurements = requests.get(('https://api.gios.gov.pl/pjp-api/rest/data/getData/') + str(id)).json()
        with open('measurements.json', 'w') as f:
            json.dump(measurements, f)

    # W przypadku błędu wczytywanie danych z pliku:
    except requests.exceptions.RequestException:
        print('BŁĄD POBIERANIA. WCZYTUJĘ DANE HISTORYCZNE...')
        try:
            with open('measurements.json', 'r') as f:
                measurements = json.load(f)
        except FileNotFoundError:
            print('Nie znaleziono pliku "measurements.json" ')

    # Wypełnianie tabeli 'measurements':
    for measurement in measurements['values']:
        conn.execute('''INSERT OR REPLACE INTO measurements (values_date, values_value)
                        VALUES (?, ?)''',
                     (measurement['date'], measurement['value']))

    # Wykonanie zapytania SELECT i wydrukowanie wyniku:
    print(f"LISTA DANYCH ZEBRANYCH ZE STANOWISKA NR {id}:")
    cursor.execute("SELECT * FROM measurements")
    for row in cursor.fetchall():
        print(row)

    # Zatwierdzenie i zamknięcie połączenia z bazą danych:
    conn.commit()
    conn.close()

