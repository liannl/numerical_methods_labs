# Задача 10; Вариант 4
"""
Решение задачи Коши с заданной точностью
y' = f(x,y) : x ∈ [a,b]
y(c) = y_c : c ∈ [a,b]
"""
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np

filename = 'data.txt'


def get_data(name: str) -> list:
    with open(name) as f:
        lines = f.readlines()[2:]
    first, second = lines
    parameters = [None]*2
    parameters[0] = list(map(lambda x: float(x), first.split(" ")))
    parameters[1] = list(map(lambda x: float(x), second.split(" ")))
    return parameters


def give_data(X: list, Y: list, count_good_dots: int):
    with open('output.txt', "w+") as f:
        for i in range(len(X)):
            f.write('f({}) = {}\n'.format(X[i], Y[i]))
        f.write('{},  {}'.format(
            len(X), len(X) - count_good_dots))


def estimate(f: Callable, h: float, x: float, y) -> float:
    k1 = h * f(x, y)
    k2 = h * f(x + h, y + k1)
    return y + 0.5*(k1 + k2)


def optimize(f: Callable, h: float, x: float, y) -> float:
    k1 = h * f(x, y)
    k2 = h * f(x + h/2, y + k1/2)
    k3 = h * f(x + h, y - k1 +2*k2)
    return y + (k1 + 4*k2 + k3) / 6


def calculation(x: float, h: float, eps: float, X: list, Y: list, Eps: list, count: int):
    X.append(x)
    y = Y[-1]
    Y.append(estimate(f, h, x, y))
    y_hat = optimize(f, h, x, y)
    Eps.append(abs(Y[-1] - y_hat))
    if abs(Eps[-1]) > eps:
        h = h / 2
    elif Eps[-1] == eps / (2 ** 3):
        h = h * 2
    x = x + h
    return x, h, X, Y, Eps, count + int(Eps[-1] == eps)


def solve(a, b, c, y_c, h_min, eps) -> list:
    count_good_dots = 0
    h = (b - a) / 10
    X = []
    Y = [y_c]
    Eps = []
    x = c
    while a <= x <= b:
        x, h, X, Y, Eps, count_good_dots = calculation(x, h, eps, X, Y, Eps, count_good_dots)
        if b - (x + h) < h_min:
            if b - x >= 2*h_min:
                x, h, X, Y, Eps, count_good_dots = calculation(x, h, eps, X, Y, Eps, count_good_dots)
                x, h, X, Y, Eps, count_good_dots = calculation(b-h_min, h, eps, X, Y, Eps, count_good_dots)
            elif b - x <= 1.5*h_min:
                x, h, X, Y, Eps, count_good_dots = calculation(x, h, eps, X, Y, Eps, count_good_dots)
            elif 1.5*h_min < b-x < 2*h_min:
                x, h, X, Y, Eps, count_good_dots = calculation(x, h, eps, X, Y, Eps, count_good_dots)
                x, h, X, Y, Eps, count_good_dots = calculation(x + (b - x)/2.0, h, eps, X, Y, Eps, count_good_dots)

    return X, Y[:-1], count_good_dots, Eps


def unsolve(a, b, c, y_c, h_min, eps) -> list:
    count_good_dots = 0
    h = (a - b) / 10
    X = []
    Y = [y_c]
    Eps = []
    x = c
    while a <= x <= b:
        x, h, X, Y, Eps, count_good_dots = calculation(x, h, eps, X, Y, Eps, count_good_dots)
        if b - (x + h) <h_min:
            if b - x >= 2*h_min:
                x, h, X, Y, Eps, count_good_dots = calculation(x, h, eps, X, Y, Eps, count_good_dots)
                x, h, X, Y, Eps, count_good_dots = calculation(-h_min, h, eps, X, Y, Eps, count_good_dots)
            elif b - x <= 1.5*h_min:
                x, h, X, Y, Eps, count_good_dots = calculation(x, h, eps, X, Y, Eps, count_good_dots)
            elif 1.5*h_min < b-x < 2*h_min:
                x, h, X, Y, Eps, count_good_dots = calculation(x, h, eps, X, Y, Eps, count_good_dots)
                x, h, X, Y, Eps, count_good_dots = calculation(x + (x)/2.0, h, eps, X, Y, Eps, count_good_dots)

    return X, Y[:-1], count_good_dots, Eps


def f(x: float, y=1) -> float:

    return y+3*x**2


def F(x: float, y=1) -> float:
    return x**3


def main():
    data = get_data(filename)
    a, b, c, y_c = data[0]
    h_min, eps = data[1]
    if c == a:
        X, Y, count_good_dots, Eps = solve(a, b, c, y_c, h_min, eps)
    else:
        X, Y, count_good_dots, Eps = unsolve( a, b, c, y_c, h_min, eps)

    x = np.linspace(a, b, len(X))
    y = F(x, 1)
    plt.plot(x, y, "k-", label='Точное решение')
    plt.plot(X, Y, "r--", label='Численное решение')
    plt.legend(loc='best')
    plt.title('График заданной функции')
    plt.savefig('graphs.png')
    plt.show()

    for i in range(len(X)):
        print('f({}) = {},  eps = {}'.format(X[len(X)-i-1], y[i], Eps[i]))
    give_data(X, Y, count_good_dots)


if __name__ == "__main__":
    main()

