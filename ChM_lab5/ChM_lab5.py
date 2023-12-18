# Задача 10; Вариант 4
"""
Решение задачи Коши с заданной точностью
y' = f(x,y) : x ∈ [a,b]
y(c) = y_c : c ∈ [a,b]
"""

filename = 'data.txt'


def get_data(name: str) -> list:
    with open(name) as f:
        lines = f.readlines()[2:]
    first, second = lines
    parameters = [None]*2
    parameters[0] = list(map(lambda x: float(x), first.split(" ")))
    parameters[1] = list(map(lambda x: float(x), second.split(" ")))
    return parameters


def RK2(x0, y0, h):
    k1 = h * f(x0, y0)
    k2 = h * f(x0 + h / 2, y0 + k1 / 2)
    k3 = h * f(x0 + h, y0 - k1 + 2 * k2)
    eps = abs((k1 - 2.0 * k2 + k3) / 6.0)
    return y0 + k2, eps


def f(x: float, y) -> float:

    return y+x


def printF(x: float, y:float, eps: float):
    print('f({}) = {}, eps = {}'.format(x, y, eps))


def RungeKutt(a, b, c, y0, h_min, eps_max):
    h_n = (b - a) / 10.0
    y_start = y0
    eps = 0
    n = 1
    cnt = cnt_no_eps = 0
    cnt_min_h =0

    if c == a:
        x_curr = x_start = a
    else:
        h_min = -h_min
        h_n = -h_n
        x_curr = x_start = b
    with open('output.txt', "w+") as f:

        while (c == a and x_curr < b) or (c == b and x_curr > a):
            if abs(h_n) < abs(h_min):
                h_n = h_min
            if (c == a and b - (x_curr + h_n) >= h_min) or (c == b and a - (x_curr + h_n) <= h_min):
                x_curr += h_n
                y_curr, eps = RK2(x_start, y_start, h_n)
                while (abs(h_n) > abs(h_min) and (eps > eps_max or eps < eps_max / 8.0) and (
                        (c == a and x_curr + h_n < b) or (c == b and x_curr + h_n > a))):
                    if eps > eps_max:
                        h_n /= 2.0
                    if abs(h_n) < abs(h_min):
                        h_n = h_min
                    if eps < eps_max / 8.0:
                        h_n *= 2.0
                    x_curr = x_start + h_n
                    y_curr, eps = RK2(x_start, y_start, h_n)
            else:
                end = 0.0
                if c == a:
                    end = b
                else:
                    end = a
                if (c == a and b - x_curr >= 2 * h_min) or (c == b and a - x_curr <= 2 * h_min):
                    y_start, eps = RK2(x_start, y_start, (end - h_min) - x_start)
                    printF(end - h_min, y_start,  eps)
                    if eps_max != eps:
                        cnt_no_eps += 1
                    if h_min == h_n:
                        cnt_min_h += 1

                    fir, eps = RK2(end - h_min, y_start, h_min)
                    printF(end, fir, eps)
                    if eps_max != eps:
                        cnt_no_eps += 1
                    if h_min == h_n:
                        cnt_min_h += 1
                    cnt += 2

                elif (c == a and b - x_curr <= 1.5 * h_min) or (c == b and a - x_curr >= 1.5 * h_min):
                    fir, eps = RK2(x_start, y_start, end + x_start)
                    printF(end, n, fir, eps)
                    if eps_max != eps:
                        cnt_no_eps += 1
                    if h_min == h_n:
                        cnt_min_h += 1
                    cnt += 1
                else:
                    y_start, eps = RK2(x_start, y_start, x_curr + (end - x_curr) / 2.0 - x_start)
                    printF(x_curr + (end - x_curr) / 2.0, y_start, eps)
                    if eps_max != eps:
                        cnt_no_eps += 1
                    if h_min == h_n:
                        cnt_min_h += 1
                    fir, eps = RK2(x_curr + (end - x_curr) / 2.0, y_start, end - (x_curr + (end - x_curr) / 2.0))
                    printF(end, fir, eps)
                    if eps_max != eps:
                        cnt_no_eps += 1
                    if h_min == h_n:
                        cnt_min_h += 1
                    cnt += 2
                x_curr = end
            if (c == a and x_curr < b) or (c == b and x_curr > a):
                printF(x_curr, y_curr, eps)
                if eps_max == eps:
                    cnt_no_eps += 1
                if h_min == h_n:
                    cnt_min_h += 1
                x_start = x_curr
                y_start = y_curr
                cnt += 1
    print("count = {}, count no eps = {}, count min h = {}".format( cnt, cnt_no_eps, cnt_min_h))


def main():
    data = get_data(filename)
    a, b, c, y0 = data[0]
    h_min, eps_max = data[1]
    RungeKutt(a, b, c, y0, h_min, eps_max)


if __name__ == "__main__":
    main()

