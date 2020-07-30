import os
import sys
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3

dir = os.path.dirname(__file__)

exoplanets = __import__('exoplanets').system

start = time.time()
print('Time : {} seconds; {}'.format(round(time.time() - start, 2), 'Start'))


def update_graph(iteration, total, scat, ax, time_coord, n_planets, planets):
    # locs = []
    x, y, z, s = [], [], [], []
    for planet_number in range(n_planets):
        # loc = time_coord[iteration][planet_number]
        # print(type(planets[planet_number]))
        # planets[planet_number]._offsets3d = (loc[0:1], loc[1:2], loc[2:3])
        x.append(time_coord[iteration][planet_number][0])
        y.append(time_coord[iteration][planet_number][1])
        z.append(time_coord[iteration][planet_number][2])
        s.append(float(planets[planet_number]['planet_radius'])*50)
    # print(s)
    # print(x, y, z)
    ax[1].cla()
    scat1 = ax[1].scatter3D(x, y, z, s=s, c='b')
    ax[1].set_xlim(-10.0, 10.0)
    ax[1].set_ylim(-10.0, 10.0)
    ax[1].set_zlim(-10.0, 10.0)

    # size_array = [1 for i in range(total)]
    # for i in range(total):
    #     if iteration % total == i:
    #         size_array[i] = 10
    size_array = [10 if iteration == i else 1 for i in range(total)]
    color_array = ['r' if iteration > i else 'b' for i in range(total)]
    scat[0].set_sizes(size_array)

    ax[0].set(title='Axes 1 : {}'.format(iteration))
    ax[1].set(title='Axes 2 : {}'.format(iteration))


params_file = '1.yaml'
if len(sys.argv) > 1:
    params_file = sys.argv[1]

system = exoplanets(params_file, time_split=100, img_split=100, n=1.0)
time_coord = system.coords()
timespan = system.timespan
lum = system.output()
n_planets = len(system.planets)

axes, scatters = [], []
fig = plt.figure(figsize=(10, 10))

axes.append(fig.add_axes([0.6, 0.1, 0.3, 0.3]))  # ax[0]
axes.append(fig.add_axes([0.1, 0.4, 0.5, 0.5], projection='3d'))  # ax[1]

scatters.append(axes[0].scatter(timespan, lum, s=1, c='b'))  # scat[0]

anim = animation.FuncAnimation(fig, update_graph, frames=len(timespan), interval=2,
                               repeat=True, fargs=(len(timespan), scatters, axes, time_coord, n_planets, system.planets), blit=False)

ffmpeg_writer = animation.FFMpegWriter(fps=25)
now = time.strftime('%Y_%m_%d_%H_%M', time.localtime(time.time()))
anim.save('animations/{}.mp4'.format(now), writer=ffmpeg_writer)

print('Time : {} seconds; {}'.format(round(time.time() - start, 2), 'Made the animation'))
