from functools import partial
from matplotlib import pyplot as plt
import numpy as np
import sys
import random
from scipy import integrate
import math

"""
Skrypt do ulatwienia pracy nad sprawozdaniem nr. 7
Kod pozwala na processing danych, rysowanie wykresów oraz na wyliczenie odpowiednich statystyk.
Użycie:
$ python KOD_ZADANIA
KOD_ZADANIA - krótka nazwa zadania. Teraz są obsługiwane:

    1. zad_2 - zadanie 2
    2. zad_5 - zadanie 5

Przykład użycia:
$ python  zad_2
"""
AVAILABLE_COLORS = ['blue', 'red', 'green', 'black']


def analyse(*test_names, describe_data=None):
    """
    Draw plots for tests
    """
    plt.grid()
    plt.xlabel('t')
    plt.ylabel('V')
    for test_name in test_names:
        try:
            raw_data = read_raw_data(test_name)
            data = trasnform_to_data(raw_data, test_name)
        except FileNotFoundError:
            print(f"Data for test {test_name} was not found")
            continue
        else:
            if describe_data:
                describe_data(data, test_name)
            display_data(data, test_name)
    plt.legend()
    plt.show()


def read_raw_data(test_name):
    """
    Reads raw data from .raw files
    """
    with open(f"figs/{test_name}.raw", "rb") as f:
        data = []
        byte = f.read(1)
        while byte:
            data.append(byte)
            byte = f.read(1)
        data = np.array([int.from_bytes(b, 'little') for b in data])
        return data


def trasnform_to_data(raw_data, test_name):
    """
    Reads params yref, yinc, yori from tests .param file and applies
    (data - yref - yori) * yinc transformer function to them. 
    """
    with open(f"figs/{test_name}.param", "r") as f:
        params = f.readline()[1:-1]
        yref, yinc, yori, tbase = [float(p) for p in params.split(", ")]
        def transfromer(data): return (data - yref - yori) * yinc
        trasnformed_data = [*map(transfromer, raw_data)]
        time = np.arange(0, len(trasnformed_data)) * tbase
        return np.vstack([time, trasnformed_data]).T


def describe_voltage_flow(data, test_name):
    """
    Prints period and DC coefficient to stdout
    """
    t, voltage_flow = get_period_data(data)
    a_0 = get_DC_coeff(t, voltage_flow)
    print(f'Data for {test_name}: ')
    print('a_0: ', a_0)
    print('T: ', t)


def get_period_data(data):
    """
    Crops data to data from one period. 
    Period caclulated as distance between two highest picks.
    """
    time, voltage = data[:, 0], data[:, 1]
    m_voltage = max(voltage)
    occurences = np.where(voltage == m_voltage)
    indexes = occurences[0]
    start, end = indexes[0], indexes[1]
    return abs(time[start] - time[end]), data[start:end, :]


def get_DC_coeff(period, period_voltage_flow):
    """
    Calculates coefficient of DC component in data
    """
    time, voltage = period_voltage_flow[:, 0], period_voltage_flow[:, 1]
    return 1/period * integrate.simps(voltage, time)


def describe_rise_time(data, test_name):
    """
    Prints to stdout information about rise time 
    """
    t_r_osc_m = get_rise_time(data)  # zmierzony czas narastania oscyloskopu
    f_o_max = 50
    t_r_osc = to_s(350 / f_o_max)  # czas narastania przebiegu prosokatnego
    t_r_gen = math.sqrt(t_r_osc_m ** 2 - t_r_osc**2)
    print(f'{test_name}')
    print('Parametr                  | Wartość |  Jednostka')
    print('--------------------------------------')
    print(f'Czas narastania t_n_osc   | {to_ns(t_r_osc)}  | ns')
    print(f'Czas narastania zmierzony | {to_ns(t_r_osc_m)} | ns')
    print(f'Czas narastania t_n_gen   | {to_ns(t_r_gen)} | ns')


def get_rise_time(data):
    """
    Calculates rise time for data. 
    """
    time, voltage = data[:, 0], data[:, 1]
    max_value = max(voltage)
    lower_bound_ind = np.where(voltage >= 0.1 * max_value)[0][0]
    upper_bound_ind = np.where(voltage >= 0.9 * max_value)[0][0]
    return time[upper_bound_ind] - time[lower_bound_ind]


def to_s(ns):
    return ns * 10 ** -9


def to_ns(s):
    return s * 10 ** 9


def display_data(data, test_name):
    """
    Display voltage plot, maximum and minimum levels.
    """
    global AVAILABLE_COLORS
    color = random.choice(AVAILABLE_COLORS)
    AVAILABLE_COLORS = [c for c in AVAILABLE_COLORS if c != color]
    time, voltage = data[:, 0], data[:, 1]
    v_max, v_min = max(voltage), min(voltage)
    line = np.ones((len(voltage),))
    plt.plot(time, line * v_max, color=color,
             linestyle='dashed', label=f'{test_name} voltage bounds')
    plt.plot(time, line * v_min, color=color,
             linestyle='dashed')
    plt.plot(time, voltage, color, label=test_name)


def run(task_code):
    """
    Runs analysis for task with given task_code
    """
    default_callback = partial(
        print, f'Task code {task_code} is not a valid task code')
    {
        'zad_1': partial(analyse, 'SQ_DC_0V_50%', 'SQ_AC_0V_50%', describe_data=describe_voltage_flow),
        'zad_2': partial(analyse, 'SQ_DC_0V_20%', 'SQ_AC_0V_20%', describe_data=describe_voltage_flow),
        'zad_3': partial(analyse, 'SQ_DC_0V_80%', 'SQ_AC_0V_80%', describe_data=describe_voltage_flow),
        'zad_5': partial(analyse, 'Z5', describe_data=describe_rise_time)
    }.setdefault(task_code, default_callback)()


if __name__ == '__main__':
    run(sys.argv[1])
