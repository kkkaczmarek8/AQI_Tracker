import statistics
import matplotlib.pyplot as plt
import requests
import numpy as np
from scipy import stats

def analyze_measurements_data(id):
    """
    Funkcja pobiera wartości otrzymane z danych pomiarowych ze stanowiska o podanym przez użytkownika ID i wykonuje na
    analizę statystyczną i obrazuje te dane na wykresie liniowym (funkcja pomija wartości 0) oraz zaznacza linię trendu

    Args:
        id (int): Numer ID stanowiska pomiarowego.

    Returns:
        None.

    Example:
        analyze_measurements_data(50)
    """

    # Pobranie danych z API GIOŚ dla określonego ID:
    try:
        measurements = requests.get(f"https://api.gios.gov.pl/pjp-api/rest/data/getData/{id}").json()
    except requests.exceptions.RequestException as e:
        print("Błąd podczas pobierania danych z API GIOŚ:", e)
        return

    # Wyodrębnienie dat i wartości pomiarów z otrzymanych danych:
    data = []
    dates = []
    for measurement in measurements['values']:
        if measurement['value'] is not None and measurement['value'] != 0:
            data.append(float(measurement['value']))
            dates.append(measurement['date'])

     # Odwrócenie kolejności elementów w liście dates najstarsze->najnowsze:
    dates.reverse()

    # Znalezienie indeksów minimalnej i maksymalnej wartości:
    min_index = data.index(min(data))
    max_index = data.index(max(data))

    # Tworzenie wykresu danych:
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.plot(dates, data)

    # Dodanie tekstu z wynikami analizy do wykresu:
    ax.text(0.6, 0.95, f"LICZBA POMIARÓW: {len(data)}", transform=ax.transAxes)
    ax.text(0.6, 0.90, f"MINIMALNA WARTOŚĆ: {min(data)} ({dates[min_index]})", transform=ax.transAxes)
    ax.text(0.6, 0.85, f"MAKSYMALNA WARTOŚĆ: {max(data)} ({dates[max_index]})", transform=ax.transAxes)
    ax.text(0.6, 0.80, f"ŚREDNIA WARTOŚĆ: {sum(data) / len(data):.5f}", transform=ax.transAxes)
    ax.text(0.6, 0.75, f"ODCHYLENIE STANDARDOWE: {statistics.stdev(data):.5f}", transform=ax.transAxes)

    # Dodanie linii trendu:
    x = np.arange(len(data))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
    ax.plot(dates, intercept + slope * x, 'r', label='Linia trendu')
    ax.legend()

    # Obrót etykiet osi X o 90 stopni:
    plt.xticks(rotation=90, fontsize=7)

    # Ustawienie tytułu i osi:
    ax.set_title(f"Wykres pomiarów ze stanowiska nr {id}")
    ax.set_xlabel("Data")
    ax.set_ylabel("Wartość pomiaru")

    # Wyświetlenie wykresu:
    plt.show()
