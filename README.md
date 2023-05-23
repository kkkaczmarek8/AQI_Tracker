# AQI_Tracker
Aplikacja, która została zaprojektowana na potrzeby zaliczenia studiów podyplomowych realizowanych we współpracy Collegium Da Vinci oraz Altkom Akademii

## Instrukcja uruchomienia
W celu uruchomienia programu użytkownik powinien pobrać wszystkie pliki i po upewnieniu się że posiada zainstalowane wszystkie wykorzystane w tej aplikacji biblioteki uruchomić plik AQI_Tracker. W celu uruchomienia modułu testowego należy uruchomić plik d_data_stations_test. Po uruchomieniu pliku AQI_Tracker, pokaże się czytelny interfejs użytkownika.

## Wykorzystane biblioteki:
- tkinter - Biblioteka do tworzenia interfejsu graficznego użytkownika w języku Python.
- sqlite3 - Moduł umożliwiający interakcję z bazą danych SQLite w Pythonie.
- statistics - Moduł zawierający funkcje statystyczne, takie jak obliczanie średniej, mediany, odchylenia standardowego itp.
- matplotlib.pyplot - Biblioteka służąca do tworzenia wykresów i wizualizacji danych w języku Python.
- requests - Biblioteka umożliwiająca wysyłanie zapytań HTTP i pobieranie zawartości stron internetowych.
- numpy - Biblioteka do obliczeń naukowych w języku Python, umożliwiająca operacje na dużych tablicach i macierzach danych.
- scipy.stats - Moduł zawierający różne funkcje statystyczne i rozkłady prawdopodobieństwa w bibliotece SciPy.
- json - Moduł umożliwiający kodowanie i dekodowanie danych w formacie JSON.
- unittest - Moduł do tworzenia i uruchamiania testów jednostkowych w Pythonie.
- os - Moduł dostarczający funkcje do interakcji z systemem operacyjnym, takie jak operacje na plikach i katalogach.
- geopy.geocoders.Nominatim - Klasa z biblioteki Geopy służąca do geokodowania, czyli przekształcania adresów na współrzędne geograficzne.
- mpl_toolkits.basemap.Basemap - Narzędzie służące do tworzenia map geograficznych w bibliotece Matplotlib.

## Opis interfejsu użytkownika
Po zainicjalizowaniu pliku AQI_Tracker, pokaże się interfejs który zawiera cztery opcje:

Lista stacji i ich filtrowanie
- Po uruchomieniu użytkownik widzi pełną listę stacji, którą można przeglądać
- Użytkownik do wyboru ma 4 możliwości pokazania konkretnych danych: Nazwa miejscowości, ID Stacji - zwraca stanowiska, ID Stanowiska - zwraca dane pomiarowe, ID stacji - zwraca indeks jakości powietrza

Znajdź stację w pobliżu!
- Po uruchomieniu użytkownik widzi pełną listę stacji, którą można przeglądać
- Użytkownik do wyboru ma 3 możliwości pokazania konkretnych danych: Nazwa miejscowości + promień odległości - zwraca stacje, ID Stacji - zwraca stanowiska, ID stanowiska - zwraca dane pomiarowe

Pokaż mapę stacji pomiarowych w Polsce
- Po uruchomieniu użytkownikowi pokaże się mapa Polski wraz z naniesionymi punktami
- Po kliknięciu w wybrany punkt, użytkownikowi pokaże się okienko z wybranymi przez autora informacjami dotyczącymi danej stacji

Analiza danych
- Po uruchmieniu użytkownikowi pokaże się okienko do wpisania ID stanowiska
- Po podaniu ID stanowiska, użytkownikowi zwrócony zostanie wykres z danymi, linia trendu oraz podstawowe miary statystyczne, które dotyczą wybranego stanowiska

## Autor
Korneliusz Kaczmarek
