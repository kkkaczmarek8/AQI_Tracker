import unittest
import sqlite3
import json
import os
from d_data_stations import d_data_stations



class TestDownloadStationsData(unittest.TestCase):
    """
        Klasa testuje funkcję pobierającą dane odnośnie stacji pomiarowych ze strony internetowej GIOŚ i zapisującą je
    do pliku 'stations.json'.
    """


    @classmethod
    def setUpClass(cls):
        """
        Przygotowuje stan przed wykonaniem testów dla całej klasy.
        Tworzy tymczasową bazę danych w pamięci, nawiązuje połączenie i tworzy tabelę 'stations' z odpowiednimi kolumnami.
        """
        cls.conn = sqlite3.connect(':memory:')  # Nawiązanie połączenia z bazą danych w pamięci
        cls.cursor = cls.conn.cursor()  # Utworzenie kursora do wykonywania poleceń SQL
        cls.cursor.execute('''
            CREATE TABLE stations (
                id INTEGER NOT NULL PRIMARY KEY,
                station_name TEXT,
                gegr_lat TEXT,
                gegr_lon TEXT,
                city_id INTEGER,
                city_name TEXT,
                commune_name TEXT,
                district_name TEXT,
                province_name TEXT,
                address_street TEXT
            )''')  # Utworzenie tabeli 'stations' z odpowiednimi kolumnami


    @classmethod
    def tearDownClass(cls):
        """
        Działa po zakończeniu testów dla całej klasy.
        Zamyka połączenie z bazą danych.
        """
        cls.conn.close()  # Zamknięcie połączenia z bazą danych


    def read_stations_json(self, file_path):
        """
            Odczytuje dane z pliku JSON.
            Otwiera wskazany plik JSON i odczytuje jego zawartość. Jak argument pobiera ścieżkę pliku .json a zwraca
        dane z tego pliku.
        """

        with open(file_path, 'r') as f:
            data = json.load(f)
        return data


    def create_test_data(self):
        """
            Tworzy testowe dane stacji pomiarowych w formie słowników i zapisuje je do pliku stations.json.
        """

        stations = [
            {
                "id": 1,
                "stationName": "Station 1",
                "gegrLat": "11.1111",
                "gegrLon": "11.1111",
                "city": {
                    "id": 1,
                    "name": "City 1",
                    "commune": {
                        "communeName": "Commune 1",
                        "districtName": "District 1",
                        "provinceName": "Province 1"
                    }
                },
                "addressStreet": "Address 1"
            },
            {
                "id": 2,
                "stationName": "Station 2",
                "gegrLat": "22.2222",
                "gegrLon": "22.2222",
                "city": {
                    "id": 2,
                    "name": "City 2",
                    "commune": {
                        "communeName": "Commune 2",
                        "districtName": "District 2",
                        "provinceName": "Province 2"
                    }
                },
                "addressStreet": "Address 2"
            }
        ]

        with open('stations.json', 'w') as f:
            json.dump(stations, f)


    def test_d_data_stations(self):
        """
            Testuje funkcję pobierającą dane ze strony internetowej GIOŚ i zapisującą je do pliku 'stations.json'.
        """


        d_data_stations()

        self.assertTrue(os.path.exists('stations.json'))

        with open('stations.json', 'r') as f:
            json_data = json.load(f)

        self.cursor.execute("SELECT * FROM stations")
        db_data = self.cursor.fetchall()

        for json_station, db_station in zip(json_data, db_data):
            self.assertSequenceEqual(json_station, db_station)
            self.assertEqual(json_station['id'], db_station[0])
            self.assertEqual(json_station['stationName'], db_station[1])
            self.assertEqual(json_station['gegrLat'], db_station[2])
            self.assertEqual(json_station['gegrLon'], db_station[3])
            self.assertEqual(json_station['city']['id'], db_station[4])
            self.assertEqual(json_station['city']['name'], db_station[5])
            self.assertEqual(json_station['city']['commune']['communeName'], db_station[6])
            self.assertEqual(json_station['city']['commune']['districtName'], db_station[7])
            self.assertEqual(json_station['city']['commune']['provinceName'], db_station[8])
            self.assertEqual(json_station['addressStreet'], db_station[9])


    def test_create_stations_table(self):
        """
            Testowanie, czy funkcja poprawnie utworzyła tabelę 'stations' i czy tabela zawiera właściwe kolumny.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        d_data_stations()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stations'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

        cursor.execute("PRAGMA table_info(stations)")
        result = cursor.fetchall()
        expected_result = [
            (0, 'id', 'INTEGER', 1, None, 1),
            (1, 'station_name', 'TEXT', 0, None, 0),
            (2, 'gegr_lat', 'TEXT', 0, None, 0),
            (3, 'gegr_lon', 'TEXT', 0, None, 0),
            (4, 'city_id', 'INTEGER', 0, None, 0),
            (5, 'city_name', 'TEXT', 0, None, 0),
            (6, 'commune_name', 'TEXT', 0, None, 0),
            (7, 'district_name', 'TEXT', 0, None, 0),
            (8, 'province_name', 'TEXT', 0, None, 0),
            (9, 'address_street', 'TEXT', 0, None, 0),
            (10, 'distance', 'FLOAT', 0, None, 0 )
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()