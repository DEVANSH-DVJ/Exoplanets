import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch


def coord(a, e, i, w):
    if a * (1 - e) <= 1.0:
        raise NameError('The planet enter the star, check the params!')

    def xy(alpha):
        angle = alpha + w
        r = a * (1 - e**2) / (1 + e * np.cos(alpha))
        x = r * np.cos(angle)
        y = r * np.sin(angle) * np.cos(i)
        return x, y

    def xyz(alpha):
        angle = alpha + w
        r = a * (1 - e**2) / (1 + e * np.cos(alpha))
        x = r * np.cos(angle)
        y = r * np.sin(angle) * np.cos(i)
        z = r * np.sin(angle) * np.sin(i)
        return x, y, z

    return xy, xyz


if __name__ == '__main__':
    a = 4.0  # in terms of Rs
    e = 0.0
    i = 0  # rad
    w = 0  # rad
    if len(sys.argv) == 2:
        a = float(sys.argv[1])
    elif len(sys.argv) == 3:
        a, e = float(sys.argv[1]), float(sys.argv[2])
    elif len(sys.argv) == 4:
        a, e, i = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    elif len(sys.argv) == 5:
        a, e, i, w = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])

    i *= (np.pi / 180)
    w *= (np.pi / 180)

    loc_2d, loc_3d = coord(a, e, i, w)

    fig = plt.figure(figsize=(10, 20))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122, projection='3d')

    for x in range(360):
        alpha = x * (np.pi / 180)
        x, y = loc_2d(alpha)
        if x**2 + y**2 < 1.0:
            ax1.scatter(x, y, c='g', s=1)
        else:
            ax1.scatter(x, y, c='k', s=1)

    ax1.set_xlim(-2 * a, 2 * a)
    ax1.set_ylim(-2 * a, 2 * a)

    c = patch.Circle((0, 0), 1.0, zorder=0, color='r', fill=None)
    ax1.add_patch(c)

    for x in range(360):
        alpha = x * (np.pi / 180)
        x, y, z = loc_3d(alpha)
        ax2.scatter(x, y, z, s=1, c='k')

    ax2.set_xlim(-2 * a, 2 * a)
    ax2.set_ylim(-2 * a, 2 * a)
    ax2.set_zlim(-2 * a, 2 * a)
    ax2.view_init(45, 45)

    plt.show()
