import os
import sys
import time

from celluloid import Camera
import matplotlib.animation as animation
import matplotlib.pyplot as plt

dir = os.path.dirname(__file__)

exoplanets = __import__('exoplanets').system

start = time.time()
print('Time : {} seconds; {}'.format(round(time.time() - start, 2), 'Start'))

params_file = '1.yaml'
if len(sys.argv) > 1:
    params_file = sys.argv[1]

system = exoplanets(params_file, time_split=100, img_split=100, n=1.0)
time_coord = system.coords()
timespan = system.timespan
lum = system.output()

axes, scatters = [], []
fig = plt.figure(figsize=(10, 10))
camera = Camera(fig)

ax1 = fig.add_axes([0.6, 0.1, 0.3, 0.3])  # ax[0]
ax2 = fig.add_axes([0.1, 0.6, 0.3, 0.3])  # ax[1]

total = len(timespan)
for num in range(total):
    # print(num)
    size_array = [10 if num == i else 1 for i in range(total)]
    color_array = ['r-' if num > i else 'b-' for i in range(total)]
    scat1 = ax1.scatter(timespan, lum, s=size_array, c='b')
    scat2 = ax2.plot(timespan[:num], lum[:num], 'b-')
    ax2.set_xlim(max(timespan) * -0.1, max(timespan) * 1.1)

    ax1.set(title='Axes 1 : {}'.format(num))
    ax2.set(title='Axes 2 : {}'.format(num))
    plt.draw()
    camera.snap()

anim = camera.animate()
ffmpeg_writer = animation.FFMpegWriter(fps=10)
now = time.strftime('%Y_%m_%d_%H_%M', time.localtime(time.time()))
anim.save('{}.mp4'.format(now), writer=ffmpeg_writer)

print('Time : {} seconds; {}'.format(round(time.time() - start, 2), 'Made the animation'))
