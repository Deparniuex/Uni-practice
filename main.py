from math import pow
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def f1(x):
    return 4 * pow(x, 3) - 7 * x + 3


def f3(x):
    return pow(x, 2) - 9


def f2(x):
    return pow(x, 4) - 4 * pow(x, 3) - 12 * x * x


window = tk.Tk()
errmsg = tk.StringVar()

var = tk.IntVar()
var.set(0)
var_extrem = tk.IntVar()
var_extrem.set(0)


def tk_window():
    window.title("Метод перебора. Поиск локального экстремума")
    window.geometry("1000x600")
    combo_label = ttk.Label(text="Выберите формулу")
    radiobutton_1 = ttk.Radiobutton(image=one_function, variable=var, value=0, command=click_radio)
    radiobutton_2 = ttk.Radiobutton(image=two_function, variable=var, value=1, command=click_radio)
    radiobutton_3 = ttk.Radiobutton(image=three_function, variable=var, value=2, command=click_radio)
    radio_min = ttk.Radiobutton(text="Минимум", variable=var_extrem, value=0)
    radio_max = ttk.Radiobutton(text="Максимум", variable=var_extrem, value=1)
    button = ttk.Button(text="Решить", command=solve)
    start_segment_label.place(height=100, width=100, x=40)
    start_segment_entry.place(height=20, width=100, x=40, y=70)
    end_segment_label.place(height=20, width=100, x=40, y=100)
    end_segment_entry.place(height=20, width=100, x=40, y=130)
    eps_label.place(height=20, width=100, x=40, y=160)
    eps_entry.place(height=20, width=100, x=40, y=190)
    error_label = tk.Label(foreground='red', textvariable=errmsg)
    error_label.place()
    combo_label.place(height=40, width=120, x=40, y=240)
    radiobutton_1.place(height=60, width=160, x=40, y=270)
    radiobutton_2.place(height=60, width=160, x=40, y=340)
    radiobutton_3.place(height=60, width=160, x=40, y=410)
    radio_min.place(height=30, width=160, x=40, y=480)
    radio_max.place(height=30, width=160, x=40, y=510)
    button.place(height=30, width=160, x=40, y=540)
    window.mainloop()


def entry_check(input):
    result = is_valid(input)
    if not result:
        errmsg.set("Ошибка ввода данных. Введите число.")
    else:
        errmsg.set("")
    return result


def is_valid(input: str):
    if input.isdigit() or input.__contains__(".") or input.__contains__("-") or input.__contains__(" "):
        return True
    else:
        return False


def graf():
    fig = plt.figure(figsize=(8, 5), facecolor='#eee')
    plt.title(label='Метод перебора', fontsize=14)
    ax = fig.add_subplot()
    ax.grid()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=150, y=5)


def delete_entry():
    start_segment_entry.delete(0, 'end')
    end_segment_entry.delete(0, 'end')
    eps_entry.delete(0, 'end')


def get_start():
    return float(start_segment_entry.get())


def get_end():
    return float(end_segment_entry.get())


def get_eps():
    return float(eps_entry.get())


def find_local_extremum(function, start, end, type, eps=1e-6):
    # Инициализируем начальные значения
    x_min = start
    y_min = function(start)
    x_max = start
    y_max = function(start)
    # Определяем шаг
    step = (end - start) / 1000
    # Перебираем все значения аргумента в заданном диапазоне
    x = start + step
    while x < end:
        # Обновляем минимумы
        if abs(x - x_min) > eps and function(x) < y_min and type == "min":
            plt.axvline(x=x, color='red', linestyle='-')
            x_min = x
            y_min = function(x)
        # Обновляем максимумы
        if abs(x - x_max) > eps and function(x) > y_max and type == "max":
            plt.axvline(x=x, color='red', linestyle='-')
            x_max = x
            y_max = function(x)
        # Увеличиваем шаг
        if function(x) < y_min:
            step /= 1.1
        elif function(x) > y_max:
            step /= 1.1
        else:
            step = min(step, abs(x - x_min) / 10)
            step = min(step, abs(x - x_max) / 10)
        step = max(step, eps / 10000)
        x += step
    # Возвращаем результаты
    return x_min, y_min, x_max, y_max


def click_radio():
    label_extrem['text'] = "Экстремум: "
    label_position['text'] = "Точка экстремума: "
    label_extrem.place(x=300, y=500)
    label_position.place(x=300, y=540)
    a = get_start()
    b = get_end()
    eps = get_eps()
    f = get_formula()
    x_min, y_min, x_max, y_max = make_plot(a, b, eps, f, "Nonе")
    # print(x_min, y_min, x_max, y_max)
    # label_min['text'] = "Минимум в точке: " + str(x_min)
    # label_max['text'] = "Максимум в точке: " + str(x_max)
    # label_min.place(x=40, y=500)
    # label_max.place(x=40, y=540)


def get_formula():
    if var.get() == 0:
        return f1
    elif var.get() == 1:
        return f2
    elif var.get() == 2:
        return f3


def get_type():
    if var_extrem.get() == 0:
        return "min"
    elif var_extrem.get() == 1:
        return "max"


def solve():
    a = get_start()
    b = get_end()
    eps = get_eps()
    type = get_type()
    f = get_formula()
    x_min, y_min, x_max, y_max = make_plot(a, b, eps, f, type)
    if type == "min":
        label_extrem['text'] = "Минимум: " + str(y_min)
        label_position['text'] = "Точка минимума: " + str(x_min)
        label_extrem.place(x=300, y=500)
        label_position.place(x=300, y=540)
    else:
        label_extrem['text'] = "Максимум: " + str(y_max)
        label_position['text'] = "Точка максимума: " + str(x_max)
        label_extrem.place(x=300, y=500)
        label_position.place(x=300, y=540)


label_extrem = tk.Label(window)
label_position = tk.Label(window)


def make_plot(a, b, eps, f, type: str):
    fig = plt.figure(figsize=(8, 5), facecolor='#eee')
    ax = fig.add_subplot()
    ax.grid()
    plt.title(label='Метод перебора', fontsize=14)
    X = np.arange(int(a) - 4, int(b) + 2, 0.1)
    Y = [f(x) for x in X]
    ax.plot(X, Y, linewidth=3)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=205, y=5)
    toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
    toolbar.update()
    toolbar.place(x=290, y=450)
    plt.axvline(x=a, color='red', linestyle='-')
    plt.axvline(x=b, color='red', linestyle='-')
    ax.text(a, -2, 'a', fontsize=11, color='red')
    ax.text(b, -2, 'b', fontsize=11, color='red')

    count = 0
    x_min = a
    y_min = f(a)
    x_max = a
    y_max = f(a)
    n = 5
    x = a
    step = eps
    x_min, y_min, x_max, y_max = find_local_extremum(f, a, b, type, eps)
    delete_entry()
    return x_min, y_min, x_max, y_max


one_function = tk.PhotoImage(file='1.png')
two_function = tk.PhotoImage(file='2.png')
three_function = tk.PhotoImage(file='3.png')
reg_entries = (window.register(entry_check), "%P")
reg_combo = (window.register(entry_check), "%P")
start_segment_label = tk.Label(text='Начало отрезка')
start_segment_entry = tk.Entry(justify='left', validate="key", validatecommand=reg_entries)
start_segment_entry.insert(0, "0.5")
end_segment_label = tk.Label(text="Конец отрезка")
end_segment_entry = tk.Entry(justify='left', validate="key", validatecommand=reg_entries)
end_segment_entry.insert(0, "2.5")
eps_label = tk.Label(text='Погрешность')
eps_entry = tk.Entry(justify='left', validate="key", validatecommand=reg_entries)
eps_entry.insert(0, "0.01")


def main():
    graf()
    tk_window()
    ...


if __name__ == '__main__':
    main()
