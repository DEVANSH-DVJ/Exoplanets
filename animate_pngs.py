import os
import sys
import time

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

now = time.strftime('%Y_%m_%d_%H_%M_', time.localtime(time.time()))
file_name = os.path.join(dir, 'pngs', now)

total = len(timespan)

fig = plt.figure(figsize=(10, 10))

ax1 = fig.add_axes([0.6, 0.1, 0.3, 0.3])  # ax[0]
ax2 = fig.add_axes([0.1, 0.6, 0.3, 0.3])  # ax[1]
scat2 = ax2.plot(timespan, lum)
x_lim = ax2.get_xlim()
y_lim = ax2.get_ylim()
for num in range(total):
    ax1.cla()
    ax2.cla()
    size_array = [10 if num == i else 1 for i in range(total)]
    color_array = ['r-' if num > i else 'b-' for i in range(total)]
    scat1 = ax1.scatter(timespan, lum, s=size_array, c='b')
    scat2 = ax2.plot(timespan[:num], lum[:num], 'b-')
    ax2.set_xlim(x_lim)
    ax2.set_ylim(y_lim)

    ax1.set(title='Axes 1 : {}'.format(num))
    ax2.set(title='Axes 2 : {}'.format(num))
    plt.savefig('{}{}.png'.format(file_name, num), dpi=96)

print('Time : {} seconds; {}'.format(round(time.time() - start, 2), 'Made the plots'))
