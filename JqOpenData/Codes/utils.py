#!/usr/bin/env python

import math

def distance(deg1, deg2):
    radius = 6378.137                               # km
    rad1 = [math.radians(rad) for rad in deg1]
    rad2 = [math.radians(rad) for rad in deg2]
    delta = rad2[0] - rad1[0]
    cos_rad = math.sin(rad1[1]) * math.sin(rad2[1]) + math.cos(rad1[1]) * math.cos(rad2[1]) * math.cos(delta)
    d = radius * math.acos(cos_rad)
    return d


if __name__ == '__main__':
    mitaka = [139.710121, 35.693105]
    shinjuku = [139.5607125, 35.7027021]
    print(distance(mitaka, shinjuku))
