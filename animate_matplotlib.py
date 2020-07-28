import os
import sys
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt

dir = os.path.dirname(__file__)

exoplanets = __import__('exoplanets').system

start = time.time()
print('Time : {} seconds; {}'.format(round(time.time() - start, 2), 'Start'))


def update_graph(num, total, scat, ax):
    # size_array = [1 for i in range(total)]
    # for i in range(total):
    #     if num % total == i:
    #         size_array[i] = 10
    size_array = [10 if num % total == i else 1 for i in range(total)]
    color_array = ['r' if num % total > i else 'b' for i in range(total)]
    scat[0].set_sizes(size_array)
    scat[1].set_color(color_array)

    ax[0].set(title='Axes 1 : {}'.format(num))
    ax[1].set(title='Axes 2 : {}'.format(num))
    return scat, ax


params_file = '1.yaml'
if len(sys.argv) > 1:
    params_file = sys.argv[1]

system = exoplanets(params_file, time_split=100, img_split=100, n=1.0)
time_coord = system.coords()
timespan = system.timespan
lum = system.output()

axes, scatters = [], []
fig = plt.figure(figsize=(10, 10))

axes.append(fig.add_axes([0.6, 0.1, 0.3, 0.3]))  # ax[0]
axes.append(fig.add_axes([0.1, 0.6, 0.3, 0.3]))  # ax[1]

scatters.append(axes[0].scatter(timespan, lum, s=1, c='b'))  # scat[0]
scatters.append(axes[1].scatter(timespan, lum, s=1, c='b'))  # scat[1]

anim = animation.FuncAnimation(fig, update_graph, frames=len(timespan), interval=2,
                               repeat=True, fargs=(len(timespan), scatters, axes), blit=False)

ffmpeg_writer = animation.FFMpegWriter(fps=50)
now = time.strftime('%Y_%m_%d_%H_%M', time.localtime(time.time()))
anim.save('{}.mp4'.format(now), writer=ffmpeg_writer)

print('Time : {} seconds; {}'.format(round(time.time() - start, 2), 'Made the animation'))
