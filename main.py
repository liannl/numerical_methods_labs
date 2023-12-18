import matplotlib.pyplot as plt


def smoothing(y, n):
    res = [0.0] * n
    res[0] = y[0]
    res[1] = (4*y[0] + 3*y[1] + 2*y[2] + y[3])/10
    for i in range(2, n-2):
        res[i] = sum(y[i-2:i+3])/5
    res[n-2] = (y[n-4] + 2*y[n-3] + 3*y[n-2] + 4*y[n-1])/10
    res[n-1] = y[n-1]
    return res


if __name__ == '__main__':
    y =[3,4, 4, 4, 4, 4, 3]#[2, 1, 3, 5, 2]  #[2, 2, 2, 2, 2]
    plt.plot(y)

    res = smoothing(y.copy(), y.__len__())
    print('Входные данные:', y)
    print('Выходные данные:',res)
    if y ==res:
        print("– сглаженные значения совпадают с исходными")
    else:
        print("– сглаженные значения отличаются от исходными")
    plt.plot(res)
    plt.show()