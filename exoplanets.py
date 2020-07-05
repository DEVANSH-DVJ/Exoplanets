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
            print(data)
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
        # print(self.star, self.total)

    def output(self):
        timespan = np.linspace(0, self.total_time, self.time_split+1)
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
    exoplanets = system("1.yaml", time_split=10000, img_split=100)
    exoplanets.output()


# class system(object):
#     def __init__(self, )
#
#
# class planet(object):
#     def __init__(self, semi_major, eccentricity, periastron_angle, inclination, planet_radius):
#         self.a = semi_major
#         self.e = eccentricity
#         self.w = periastron_angle
#         self.i = inclination
#         self.Rp = planet_radius
#
#     def reduce_distances(self, Rs):
#         self.a /= Rs
#         self.Rp /= Rs
#
# class system(object):
#     def __init__(self, star_radius, star_mass, planets, time_split=100, img_split=100):
#         try:
#             self.n = len(planets)
# #             period_constant = (2 * np.pi) / ((scipy.constants.G * star_mass)**0.5)
#             period_constant = 200.0 / (star_mass)**0.5
#             self.a, self.e, self.w, self.i, self.Rp, self.P  = ([] for i in range(6))
#             for planet in planets:
#                 planet.reduce_distances(star_radius)
#                 self.a.append(planet.a)
#                 self.e.append(planet.e)
#                 self.w.append(planet.w)
#                 self.i.append(planet.i)
#                 self.Rp.append(planet.Rp)
#                 self.P.append(planet.a**1.5 * period_constant)
#
#             self.time_split = int(time_split)
#             self.split = int(img_split)
#             self.u = [0.1, 0.2]
#
#             self.init_alpha_wrt_time()
#             self.init_stellar_limb_darkening()
#         except:
#             raise NameError('Check the input again! or try to debug')
#
#
#     def init_alpha_wrt_time(self):
#         self.total_time = max(self.P)
#         t_span = (0, self.total_time)
#         t = np.linspace(0, self.total_time, self.time_split+1)
#         y0 = np.array([0])
#
#         self.alpha_array = []
#         for i in range(self.n):
#             sol = solve_ivp(der_alpha, t_span, y0, t_eval = t, args = (self.e[i], self.P[i]))
#             self.alpha_array.append(sol.y[0])
#             print(len(sol.y[0]))
#
#         self.time_array = sol.t
#         print(len(sol.t))
#
#     def init_stellar_limb_darkening(self):
#         self.star = np.zeros((2*self.split+1, 2*self.split+1))
#         self.lum_total = 0
#         for i in range(-self.split, self.split+1):
#             rg_j = abs(int((self.split**2 - i**2)**0.5))
#             for j in range(-rg_j, rg_j+1):
#                 x = (i)/self.split
#                 y = (j)/self.split
#                 cosine = abs((1 - x**2 - y**2)**0.5)
#                 lum = 1 - self.u[0]*(1 - cosine) - self.u[1]*((1 - cosine)**2)
#                 self.lum_total += lum
#                 self.star[self.split+i][self.split+j] = lum
#
#
#     def output(self, time):
#         cur_star = copy.deepcopy(self.star)
#         cur_total = copy.deepcopy(self.lum_total)
#         t = time - int(time/self.total_time)
#         l = time * self.time_split / self.total_time
#
#         for k in range(self.n):
#             alpha = self.alpha_array[k][int(l)]
#
#             angle = alpha + self.w[k]
#             r = self.a[k] * (1 - self.e[k]**2) / (1 + self.e[k]*np.cos(alpha))
#             orig_x = r * np.cos(angle)
#             orig_y = r * np.sin(angle) * np.cos(self.i[k])
#
#             if orig_y*(self.i[k] - (np.pi/2)) > 0: # Only the part of orbit which is away from us
#                 continue
#             if orig_x**2 + orig_y**2 > 2 * ((1 + self.Rp[k])**2):
#                 continue
#             x, y, Rp = int(orig_x*self.split), int(orig_y*self.split), int(self.Rp[k]*self.split)
#             for i in range(-Rp, Rp+1):
#                 if y-i >= -self.split and y-i <= self.split:
#                     rg_j = abs(int((Rp**2 - i**2)**0.5))
#                     for j in range(-rg_j, rg_j+1):
#                         if x+j >= -self.split and x+j <= self.split:
#                             m = self.split - y + i
#                             n = self.split + x + j
#                             lum = cur_star[m][n]
#                             cur_total -= lum
#                             cur_star[m][n] = 0
#         return cur_total
#
# planet1 = planet(semi_major = 5, \
#                  eccentricity = 0.04, \
#                  periastron_angle = 270.0*(np.pi/180), \
#                  inclination = 89.9*(np.pi/180), \
#                  planet_radius = 0.1)
#
# planet2 = planet(semi_major = 5*(3**(2/3)), \
#                  eccentricity = 0.04, \
#                  periastron_angle = 270.0*(np.pi/180), \
#                  inclination = 89.9*(np.pi/180), \
#                  planet_radius = 0.05)
#
# print(time.localtime())
# exo = system(star_radius = 1.0, \
#              star_mass = 40, \
#              planets = [planet1, planet2], \
#              time_split = 10000, \
#              img_split = 100)
# times = exo.time_array
# print(time.localtime())
#
# print(time.localtime())
# total_lum = exo.lum_total
# lum = []
# for t in times:
#     lum.append(exo.output(t))
# lum = np.array(lum)/total_lum
# print(time.localtime())
#
# print(time.localtime())
# plt.scatter(times, lum, s=1)
# print(time.localtime())
#
# print(time.localtime())
# plt.scatter(times, lum, s=1)
# plt.xlim(400,600)
# print(time.localtime())
