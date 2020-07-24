import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


def der_alpha(t, alpha, e):
    return (2 * np.pi / (1 - e * e)**1.5) * (1 + e * np.cos(alpha))**2


def alpha_wrt_time(e=0.0, split=1000):
    t_span = (0.0, 1.0)
    t = np.linspace(0.0, 1.0, split + 1)
    y0 = np.array([0])
    sol = solve_ivp(der_alpha, t_span, y0, t_eval=t, args=(e,))
    alpha_array = sol.y[0]

    # return lambda time : alpha_array[int((time%1) * split)]
    def alphas(time):
        nonlocal split, alpha_array
        time = time % 1.0
        n = time * split
        if int(n) < split:
            return alpha_array[int(n)]

    return alphas


if __name__ == '__main__':
    try:
        split = 1000
        e = 0.0
        if len(sys.argv) == 2:
            e = float(sys.argv[1])
        elif len(sys.argv) == 3:
            e, split = float(sys.argv[1]), int(sys.argv[2])
        func = alpha_wrt_time(e, split)
    except:
        raise NameError('Check the params again!')

    t = np.linspace(0, 1, split + 1)
    alphas = [func(time) for time in t]

    fig = plt.figure(figsize=(12, 16))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ax1.scatter(t, alphas, s=1)
    ax1.set_xlabel('t')
    ax1.set_ylabel('aplha')
    ax1.set_title('time')
    ax1.grid(True)

    ax2.scatter(t, np.sin(alphas), s=1)
    ax2.set_xlabel('t')
    ax2.set_ylabel('sin(aplha)')
    ax2.set_title('time')
    ax2.grid(True)

    plt.show()
