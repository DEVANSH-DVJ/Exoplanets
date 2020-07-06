import os
import sys
import time

import copy
import random
import yaml

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


alpha_wrt_time = __import__("alpha(time)").alpha_wrt_time
coord_wrt_alpha = __import__("coord(alpha)").coord_wrt_alpha
initialize_star = __import__("lum(coord)").initialize_star
lum_wrt_coord = __import__("lum(coord)").lum_wrt_coord

params_file = os.path.join(os.path.dirname(__file__), "1.yaml")

with open(params_file, 'r') as stream:
    param = yaml.safe_load(stream)


class system(object):
    def __init__(self, file_name, time_split=100, img_split=100):
        try:
            params_file = os.path.join(os.path.dirname(__file__), file_name)
            with open(params_file, 'r') as stream:
                data = yaml.safe_load(stream)
            self.time_split = time_split
            self.img_split = img_split
            self.planets = data['planets']
            self.star_radius = data['star_radius']
            self.star_mass = data['star_mass']
            self.u = data['u']
            for planet in self.planets:
                # period_constant = (2 * np.pi) / ((scipy.constants.G * star_mass)**0.5)
                planet['period'] = (200.0 / (self.star_mass)**0.5) * (planet['semi-major']**1.5)
            self.total_time = max([planet['period'] for planet in self.planets])
        except:
            raise NameError('Check the params!')

        for planet in self.planets:
            split = self.time_split * planet['period'] / self.total_time
            planet['alphas'] = alpha_wrt_time(e=planet['eccentricity'], split=int(split))
            planet['coord_2d'], planet['coord_3d'] = coord_wrt_alpha(a=planet['semi-major'], e=planet['eccentricity'],
                                              i=planet['inclination'], w=planet['periastron_angle'])

        self.star, self.total = initialize_star(limb_func=self.limb_dark, split=img_split)

    def output(self, n=1.0):
        timespan = np.linspace(0, int(n)*self.total_time, int(n)*self.time_split+1)
        lum = []
        for time in timespan:
            update, get_lum, get_star = lum_wrt_coord(copy.deepcopy(self.star), copy.deepcopy(self.total))
            for planet in self.planets:
                x, y = planet['coord_2d'](planet['alphas'](time / planet['period']))
                if y*(planet['inclination'] - (np.pi/2)) > 0: # Only the part of orbit which is away from us
                    continue
                if x**2 + y**2 > 2 * ((1 + planet['planet_radius'])**2):
                    continue

                update(x, y, planet['planet_radius'])
            lum.append(get_lum())
        plt.scatter(timespan, lum, s=1, c='b')
        plt.show()


    def limb_dark(self, cosine):
        if len(self.u) == 2:
            return 1 - self.u[0] * (1 - cosine) - self.u[1] * ((1 - cosine)**2)
        else:
            raise NameError('Check the u values')



if __name__ == '__main__':
    params_file = "1.yaml"
    if len(sys.argv) > 1:
        params_file = sys.argv[1]

    exoplanets = system(params_file, time_split=10000, img_split=100)
    exoplanets.output()
