import numpy as np

##############
### Pygame ###
##############

# Window height/width
w = 1500
h = w/2

# Where to display fitness
fitness_loc = (0.9*w, 0.05*h)


##############
### Colors ###
##############

cb = (0, 0, 0)
cdg = (252, 252, 252)
clg = (70, 70, 70)


##########################
### Physical Constants ###
##########################

# arm length
ra = int(w/10)
# ball radii
rb = int(w/100)
# current angle
o0 = -np.pi/2
# angular velocity, delta theta
do = 0
# rail length and endpoints
rdx = int(w/3)
r1 = (int(w/2 - rdx), int(h/2 - ra))
r2 = (int(w/2 + rdx), int(h/2 - ra))
# ball end coordinates (0: x, 1: y)
# use this value for centered start location
a0 = int(w/2)
# use this value for random start ocation
# a0 = np.random.choice(range(r1[0], r2[0])) 
a1 = int(h/2 - ra)
b0 = a0 - int(ra * np.cos(o0))
b1 = a1 - int(ra * np.sin(o0))


##########################
### Movement Constants ###
##########################

# velocities
vd = 5
vax = 0
dv = 0
adv = 0.0035
# friction due to wall (inelastic collision)
fw = 0.45
# friction due to rail (horizonatal deceleration constant)
fr = 2
# friction at the pendulum joint (fractional angular velocity retention)
fj = 0.991
# gravitational deceleration
g = -3


###################
### Menu Params ###
###################

# See menu.py
menu_params =   {'g': (g,-10, 0),
                'fr': (fr,0,10),
                'fj': (fj, 0.8,1.1),
                'fw': (fw, 0, 1)}

defaults = (w, h, fitness_loc, cb, cdg, clg, ra, rb, o0, do, rdx, r1, r2, a0, a1, b0, b1, vd, vax, dv, adv, fw, fr, fj, g, menu_params)