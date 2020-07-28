import os
import sys
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt

dir = os.path.dirname(__file__)

exoplanets = __import__('exoplanets').system


def update_graph(num, total, scat):
    # size_array = [1 for i in range(total)]
    # for i in range(total):
    #     if num % total == i:
    #         size_array[i] = 10
    size_array = [10 if num % total == i else 1 for i in range(total)]
    return scat,
    color_array = ['r' if num % total > i else 'b' for i in range(total)]
    scat[0].set_sizes(size_array)
    scat[1].set_color(color_array)


params_file = '1.yaml'
if len(sys.argv) > 1:
    params_file = sys.argv[1]

system = exoplanets(params_file, time_split=100, img_split=100, n=1.0)
time_coord = system.coords()
timespan = system.timespan
lum = system.output()

scat = plt.scatter(timespan, lum, s=1, c='b')
fig = plt.figure(figsize=(10, 10))

anim = animation.FuncAnimation(fig, update_graph, frames=len(timespan), interval=2,
                               repeat=True, fargs=(len(timespan), scat), blit=True)

ffmpeg_writer = animation.FFMpegWriter(fps=50)
now = time.strftime('%Y_%m_%d_%H_%M', time.localtime(time.time()))
anim.save('{}.mp4'.format(now), writer=ffmpeg_writer)
