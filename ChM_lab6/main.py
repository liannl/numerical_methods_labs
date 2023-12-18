from typing import List
import numpy as np


def p(x: float) -> float:
    return 0


def q(x: float) -> float:
    return 0


def f(x: float) -> float:
    return x


def dU(x: float, u: float, v: float) -> float:
    return p(x) * u + v


def dV(x: float, u: float) -> float:
    return q(x) * u


def dW(x: float, u: float) -> float:
    return f(x) * u


class VEC2:
    def __init__(self):
        self.dY = []
        self.Y = []


class VEC3:
    def __init__(self):
        self.U = []
        self.V = []
        self.W = []


def runge(a: float, b: float, y: float, x: List[float]) -> VEC3:
    u = a
    v = -b
    w = y
    Vec = VEC3()
    Vec.U.append(u)
    Vec.V.append(v)
    Vec.W.append(w)
    for i in range(1, len(x)):
        h = x[i] - x[i - 1]
        k1_u = h * dU(x[i - 1], u, v)
        k1_v = h * dV(x[i - 1], u)
        k1_w = h * dW(x[i - 1], u)
        k2_u = h * dU(x[i], u + k1_u, v + k1_u)
        k2_v = h * dV(x[i], u + k1_v)
        k2_w = h * dW(x[i], u + k1_w)
        k3_u = h * dU(x[i], u + k2_u, v + k2_u)
        k3_v = h * dV(x[i], u + k2_v)
        k3_w = h * dW(x[i], u + k2_w)
        k4_u = h * dU(x[i], u + k3_u, v + k3_u)
        k4_v = h * dV(x[i], u + k3_v)
        k4_w = h * dW(x[i], u + k3_w)
        u += 0.5 * (k1_u + k2_u)
        v += 0.5 * (k1_v + k2_v)
        w += 0.5 * (k1_w + k2_w)
        Vec.U.append(u)
        Vec.V.append(v)
        Vec.W.append(w)
    return Vec


def runge_reverse(a: float, b: float, y: float, x: List[float]) -> VEC3:
    u = a
    v = -b
    w = y
    Vec = VEC3()
    Vec.U = [0] * len(x)
    Vec.V = [0] * len(x)
    Vec.W = [0] * len(x)
    Vec.U[-1] = u
    Vec.V[-1] = v
    Vec.W[-1] = w
    for i in range(len(x) - 2, -1, -1):
        h = x[i] - x[i + 1]
        k1_u = h * dU(x[i + 1], u, v)
        k1_v = h * dV(x[i + 1], u)
        k1_w = h * dW(x[i + 1], u)
        k2_u = h * dU(x[i], u + k1_u, v + k1_u)
        k2_v = h * dV(x[i], u + k1_v)
        k2_w = h * dW(x[i], u + k1_w)
        k3_u = h * dU(x[i], u + k2_u, v + k2_u)
        k3_v = h * dV(x[i], u + k2_v)
        k3_w = h * dW(x[i], u + k2_w)
        k4_u = h * dU(x[i], u + k3_u, v + k3_u)
        k4_v = h * dV(x[i], u + k3_v)
        k4_w = h * dW(x[i], u + k3_w)
        u += 0.5 * (k1_u + k2_u)
        v += 0.5 * (k1_v + k2_v)
        w += 0.5 * (k1_w + k2_w)
        Vec.U[i] = u
        Vec.V[i] = v
        Vec.W[i] = w
    return Vec


def solve_system(v1: VEC3, v2: VEC3) -> VEC2:
    Vec = VEC2()
    for i in range(len(v1.U)):
        Y = (v2.W[i] * v1.U[i] - v2.U[i] * v1.W[i]) / (v2.U[i] * v1.V[i] - v2.V[i] * v1.U[i])
        dY = (v1.W[i] + v1.V[i] * Y) / v1.U[i]
        Vec.dY.append(dY)
        Vec.Y.append(Y)
    return Vec


def print_result(v: VEC2, x: List[float]) -> None:
    with open("output.txt", "w") as out:
        for i in range(len(x)):
            print(f"x = {x[i]} y = {v.Y[i]} y' = {v.dY[i]}")
            out.write(f"x = {x[i]} y = {v.Y[i]} y' = {v.dY[i]}\n")


def take_data() -> List[str]:
    with open("input.txt", "r") as f:
        data = f.read().split()
    return data


if __name__ == "__main__":
    line = take_data()
    a1 = float(line[0])
    b1 = float(line[1])
    y1 = float(line[2])
    a2 = float(line[3])
    b2 = float(line[4])
    y2 = float(line[5])
    n = int(line[8])
    x = [float(line[i + 1]) for i in range(9, n * 2 + 9, 2)]
    v1 = runge(a1, b1, y1, x)
    v2 = runge_reverse(a2, b2, y2, x)
    v = solve_system(v1, v2)
    print_result(v, x)
