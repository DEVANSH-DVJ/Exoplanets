import copy
import random
import time

import matplotlib.pyplot as plt
import numpy as np


def limb_dark_two_params(cosine):
    u = [0.1, 0.2]
    return 1 - u[0] * (1 - cosine) - u[1] * ((1 - cosine)**2)


def initialize_star(limb_func, split=1000):
    star = np.zeros((2 * split + 1, 2 * split + 1))
    total = 0
    for i in range(-split, split + 1):
        rg_j = abs(int((split**2 - i**2)**0.5))
        for j in range(-rg_j, rg_j + 1):
            x = (i) / split
            y = (j) / split
            cosine = abs((1 - x**2 - y**2)**0.5)
            lum = limb_func(cosine)
            total += lum
            star[split + i][split + j] = lum

    return star, total


def lum_wrt_coord(img, tot):
    split = int((len(img) - 1) / 2)

    def shadow(coord_x, coord_y, R_p):
        nonlocal img, tot
        x, y, Rp = int(coord_x * split), int(coord_y * split), int(R_p * split)
        for i in range(-Rp, Rp + 1):
            if y - i >= -split and y - i <= split:
                rg_j = abs(int((Rp**2 - i**2)**0.5))
                for j in range(-rg_j, rg_j + 1):
                    if x + j >= -split and x + j <= split:
                        m = split - y + i
                        n = split + x + j
                        lum = img[m][n]
                        tot = tot - lum
                        img[m][n] = 0

    def lum():
        nonlocal tot
        return tot

    def star():
        nonlocal img
        return img

    return shadow, lum, star


if __name__ == '__main__':
    start = time.time()
    print('Time : {} seconds; {}'.format(round(time.time() - start, 2), 'Start'))
    split = 1000

    fig = plt.figure(figsize=(10, 10))


    star, total = initialize_star(lambda x : 1, split)
    print(total)
    ax = fig.add_subplot(111)
    ax.imshow(star, 'gray')
    ax.set_title('Star without Limb Darkening')
    ax.set_xticks(np.linspace(0, 2*split, 21))
    ax.set_xticklabels(['-1.0', '-0.9', '-0.8', '-0.7', '-0.6', '-0.5', '-0.4', '-0.3', '-0.2', '-0.1', '0.0', '+0.1', '+0.2', '+0.3', '+0.4', '+0.5', '+0.6', '+0.7', '+0.8', '+0.9', '+1.0'])
    ax.set_yticks(np.linspace(0, 2*split, 21))
    ax.set_yticklabels(['+1.0', '+0.9', '+0.8', '+0.7', '+0.6', '+0.5', '+0.4', '+0.3', '+0.2', '+0.1', '0.0', '-0.1', '-0.2', '-0.3', '-0.4', '-0.5', '-0.6', '-0.7', '-0.8', '-0.9', '-1.0'])
    ax.tick_params(labelbottom=True, labeltop=True, labelleft=True, labelright=True, bottom=True, top=True, left=True, right=True)
    plt.savefig(fname='plots/lum-coord/Initial star - no limb darkening.jpeg', dpi=500, pad_inches=0.0, quality=100)
    fig.clf()
    print('Time : {} seconds; {}'.format(round(time.time() - start, 2), 'Initial star - no limb darkening'))


    star, total = initialize_star(limb_dark_two_params, split)
    print(total)
    ax = fig.add_subplot(111)
    ax.imshow(star, 'gray')
    ax.set_title('Star without Limb Darkening')
    ax.set_xticks(np.linspace(0, 2*split, 21))
    ax.set_xticklabels(['-1.0', '-0.9', '-0.8', '-0.7', '-0.6', '-0.5', '-0.4', '-0.3', '-0.2', '-0.1', '0.0', '+0.1', '+0.2', '+0.3', '+0.4', '+0.5', '+0.6', '+0.7', '+0.8', '+0.9', '+1.0'])
    ax.set_yticks(np.linspace(0, 2*split, 21))
    ax.set_yticklabels(['+1.0', '+0.9', '+0.8', '+0.7', '+0.6', '+0.5', '+0.4', '+0.3', '+0.2', '+0.1', '0.0', '-0.1', '-0.2', '-0.3', '-0.4', '-0.5', '-0.6', '-0.7', '-0.8', '-0.9', '-1.0'])
    ax.tick_params(labelbottom=True, labeltop=True, labelleft=True, labelright=True, bottom=True, top=True, left=True, right=True)
    ax.set_title('Star with Quadratic Limb Darkening')
    plt.savefig(fname='plots/lum-coord/Initial star - limb darkening.jpeg', dpi=500, pad_inches=0.0, quality=100)
    fig.clf()
    print('Time : {} seconds; {}'.format(round(time.time() - start, 2), 'Initial star - limb darkening'))


    update, get_total, get_star = lum_wrt_coord(copy.deepcopy(star), copy.deepcopy(total))
    x, y, Rp = 0.2, -0.7, 0.04
    update(x, y, Rp)
    print(get_total())
    ax = fig.add_subplot(111)
    ax.imshow(get_star(), 'gray')
    ax.set_title('Star without Limb Darkening')
    ax.set_xticks(np.linspace(0, 2*split, 21))
    ax.set_xticklabels(['-1.0', '-0.9', '-0.8', '-0.7', '-0.6', '-0.5', '-0.4', '-0.3', '-0.2', '-0.1', '0.0', '+0.1', '+0.2', '+0.3', '+0.4', '+0.5', '+0.6', '+0.7', '+0.8', '+0.9', '+1.0'])
    ax.set_yticks(np.linspace(0, 2*split, 21))
    ax.set_yticklabels(['+1.0', '+0.9', '+0.8', '+0.7', '+0.6', '+0.5', '+0.4', '+0.3', '+0.2', '+0.1', '0.0', '-0.1', '-0.2', '-0.3', '-0.4', '-0.5', '-0.6', '-0.7', '-0.8', '-0.9', '-1.0'])
    ax.tick_params(labelbottom=True, labeltop=True, labelleft=True, labelright=True, bottom=True, top=True, left=True, right=True)
    ax.set_title('Shadow of a Planet with radius {2} at ({0}, {1})'.format(x, y, Rp))
    plt.savefig(fname='plots/lum-coord/1 Planet.jpeg', dpi=500, pad_inches=0.0, quality=100)
    fig.clf()
    print('Time : {} seconds; {}'.format(round(time.time() - start, 2), '1 Planet'))


    update, get_total, get_star = lum_wrt_coord(copy.deepcopy(star), copy.deepcopy(total))
    x1, y1, Rp1 = 0.05, 0.2, 0.04
    x2, y2, Rp2 = 0.1, 0.3, 0.1
    x3, y3, Rp3 = 0.15, 0.2, 0.05
    x4, y4, Rp4 = 0.9, 0.2, 0.15
    update(x1, y1, Rp1)
    update(x2, y2, Rp2)
    update(x3, y3, Rp3)
    update(x4, y4, Rp4)
    print(get_total())
    ax = fig.add_subplot(111)
    ax.imshow(get_star(), 'gray')
    ax.set_title('Star without Limb Darkening')
    ax.set_xticks(np.linspace(0, 2*split, 21))
    ax.set_xticklabels(['-1.0', '-0.9', '-0.8', '-0.7', '-0.6', '-0.5', '-0.4', '-0.3', '-0.2', '-0.1', '0.0', '+0.1', '+0.2', '+0.3', '+0.4', '+0.5', '+0.6', '+0.7', '+0.8', '+0.9', '+1.0'])
    ax.set_yticks(np.linspace(0, 2*split, 21))
    ax.set_yticklabels(['+1.0', '+0.9', '+0.8', '+0.7', '+0.6', '+0.5', '+0.4', '+0.3', '+0.2', '+0.1', '0.0', '-0.1', '-0.2', '-0.3', '-0.4', '-0.5', '-0.6', '-0.7', '-0.8', '-0.9', '-1.0'])
    ax.tick_params(labelbottom=True, labeltop=True, labelleft=True, labelright=True, bottom=True, top=True, left=True, right=True)
    ax.set_title('Shadow of 4 Planets')
    plt.savefig(fname='plots/lum-coord/4 Planets.jpeg', dpi=500, pad_inches=0.0, quality=100)
    fig.clf()
    print('Time : {} seconds; {}'.format(round(time.time() - start, 2), '4 Planets'))
